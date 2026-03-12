from apps.lib.paginate import Paginate
from flask import request
from apps.handler import handle_error, handle_error_rollback, nonServerErrorException
from apps.models import setoran
from .BaseAkuntasi import BaseAkuntasi
from apps.lib.helper import date_now

class Setoran(BaseAkuntasi):
    def __init__(self):
        super().__init__()
        
        self.baseFrom = """
            from setoran
            join sales_order on setoran.id_sales_order = sales_order.id
            join faktur on faktur.id_sales_order = sales_order.id
            join plafon on plafon.id = sales_order.id_plafon
            join customer on customer.id = plafon.id_customer
        """

    @handle_error
    def getListSetoran(self, tipe_setoran):
        tanggal = date_now()
        periode_awal = self.req('periode_awal')
        periode_akhir = self.req('periode_akhir')
        
        tanggal_query = f"setoran.draft_tanggal_input <= :tanggal"
        tanggal_params = { 'tanggal': tanggal }
        
        periode_query = f"setoran.draft_tanggal_input between :periode_awal and :periode_akhir"
        periode_params = {'periode_awal': periode_awal, 'periode_akhir': periode_akhir}
        
        conditions = {
            "sales": 'sales.id = :sales',
            'status': 'setoran.status_setoran = :status',
        }
        
        where, bindparams,_ = self.poolRequest(conditions)
        
        if periode_awal and periode_akhir :
            where = f"{where} {periode_query} and "
            bindparams = {**bindparams, **periode_params}
        else :
            where = f"{where} {tanggal_query} and "
            bindparams = {**bindparams, **tanggal_params}
        
        query = f"""
            with status_tagihan as not materialized (
                select 
                setoran.draft_tanggal_input,
                setoran.nama_sales,
                sum(setoran.draft_jumlah_setor) as setoran_piutang,
                array_agg(setoran.status_setoran) as status
                from setoran 
                join sales_order on setoran.id_sales_order = sales_order.id
                join plafon on sales_order.id_plafon = plafon.id
			    left join sales on sales.id_user = plafon.id_sales
                where {where} 
                setoran.tipe_setoran = {tipe_setoran}
                group by setoran.nama_sales, setoran.draft_tanggal_input	
            )
            select 
            status_tagihan.*,
            case 
                when status = array_fill(1::int, array[array_length(status, 1)]) then 'sales'
                when status = array_fill(2::int, array[array_length(status, 1)]) then 'kasir'
                when status = array_fill(3::int, array[array_length(status, 1)]) then 'audit'
            end as status_setoran
            from 
            status_tagihan
        """

        return Paginate(request, query, bindparams).paginate()
    
    @handle_error
    def getDetailListSetoran(self):
        nama_sales = self.req('nama_sales')
        tanggal = self.req('tanggal')
        
        conditions = {
            "tanggal": "setoran.draft_tanggal_input = :tanggal",
            "tipe_setoran": "setoran.tipe_setoran = :tipe_setoran"
        }
        
        where, bindparams,_ = self.poolRequest(conditions)
        
        queryInformasi = f"""
            select 
            count(distinct customer.id) as jumlah_customer,
            sum(setoran.draft_jumlah_setor) as total_setoran
            {self.baseFrom}
            where {where} setoran.nama_sales ILIKE '%{nama_sales}%'
        """
        
        queryData = f"""
            select 
            setoran.id as id_setoran,
            customer.id as id_customer,
            setoran.draft_tanggal_input as tanggal,
            customer.nama as nama_customer,
            faktur.no_faktur,
            (faktur.total_penjualan - (
                select COALESCE(sum(s2.jumlah_setoran), 0)
                from setoran s2
                where s2.id_sales_order = sales_order.id
            )) as tagihan,
            setoran.draft_jumlah_setor as setoran,
            case
                when (faktur.total_penjualan - (
                    select COALESCE(sum(s2.jumlah_setoran), 0)
                    from setoran s2
                    where s2.id_sales_order = sales_order.id
                )) = 0 then 'lunas'
                else 'belum lunas'
            end as status_pembayaran,
            setoran.status_setoran,
            setoran.bukti_transfer,
            setoran.biaya_lainnya,
            setoran.ket_biaya_lainnya,
            setoran.max_biaya_lainnya
            {self.baseFrom}
            where {where} setoran.nama_sales ILIKE '%{nama_sales}%'
        """
        
        informasiSetoran = self.query().setRawQuery(queryInformasi).bindparams(bindparams).execute().fetchone().result
        listSetoran = self.query().setRawQuery(queryData).bindparams(bindparams).execute().fetchall().get()
        
        return {
            "informasi": { **informasiSetoran, "nama_sales": nama_sales, "tanggal": tanggal },
            "data": listSetoran
        }
        
    @handle_error_rollback
    def konfirmasiSetoran(self):
        id_setoran = self.req('id_setoran')
        status_setoran = self.req('status_setoran')
        
        for id in id_setoran:
            update_setoran = setoran.query.filter(setoran.id == id).first()
            
            if not update_setoran: raise nonServerErrorException('tidak bisa menemukan id setoran yang dimaksud')
            
            update_setoran.status_setoran = int(status_setoran)
            
            if int(status_setoran) == 3:
                update_setoran.tanggal_setoran_diterima = date_now()
                
                # Pastikan kedua nilai ada sebelum membandingkan
                biaya_lainnya = update_setoran.biaya_lainnya or 0
                max_biaya = update_setoran.max_biaya_lainnya or 0
                
                if biaya_lainnya > max_biaya:
                    # Jika melebihi max, jumlah_setoran hanya dari draft_jumlah_setor
                    update_setoran.jumlah_setoran = round(float(update_setoran.draft_jumlah_setor))
                else:
                    # Jika tidak melebihi max atau tidak ada max, jumlah_setoran = draft_jumlah_setor - biaya_lainnya
                    update_setoran.jumlah_setoran = round(float(update_setoran.draft_jumlah_setor) + biaya_lainnya)
            
            self.flush()
            
        self.commit()
        
        return {'status': 'konfirmasi sukses'}, 200
    
    @handle_error_rollback
    def addBiayaLainnya(self):
        id_setoran = self.req('id_setoran')
        biaya_lainnya = self.req('biaya_lainnya')
        ket_biaya_lainnya = self.req('ket_biaya_lainnya')
        is_max_biaya = self.req('is_max_biaya')  # terima boolean
        
        update_setoran = setoran.query.filter(setoran.id == id_setoran).first()
        
        if not update_setoran: 
            raise nonServerErrorException('tidak bisa menemukan id setoran yang dimaksud')
        
        update_setoran.biaya_lainnya = biaya_lainnya
        update_setoran.ket_biaya_lainnya = ket_biaya_lainnya
        update_setoran.max_biaya_lainnya = 5000 if is_max_biaya else 2900
        
        self.flush()
        self.commit()
        
        return {'status': 'biaya lainnya berhasil ditambahkan'}, 200