from .BaseAkuntasi import BaseAkuntasi
from apps.lib.paginate import Paginate
from flask import request
from apps.handler import handle_error_rollback, nonServerErrorException, handle_error
from apps.lib.helper import datetime_now_stamp
from apps.models import purchase_tagihan, purchase_tagihan_detail
from apps.lib.helper import extraUploadImage

class Hutang(BaseAkuntasi):
    def __init__(self):
        super().__init__()

    @handle_error
    def getHutang(self):
        conditions = {
            "principal": "principal.id = :principal",
            "jatuh_tempo": "purchase_tagihan.jatuh_tempo = :jatuh_tempo"
        }

        # Menggunakan poolRequest yang akan mengambil params dari request
        _, bindParams,where = self.poolRequest(conditions)
        where_clause = f"WHERE {where}" if where else ""

        query = f"""
                SELECT 
                    purchase_tagihan.id AS id_tagihan,
                    principal.nama AS nama_principal,
                    purchase_tagihan.no_tagihan as surat_tagihan,
                    purchase_tagihan.total as total_tagihan,
                    CASE 
                        WHEN purchase_tagihan.status_pembayaran = 1 THEN 'belum lunas'
                        WHEN purchase_tagihan.status_pembayaran = 2 THEN 'lunas'
                        ELSE 'tidak diketahui'
                    END AS status_bayar,
                    COUNT(purchase_tagihan_detail.id) AS jumlah_faktur,
                    purchase_tagihan.tanggal_bayar,
                    purchase_tagihan.jatuh_tempo
                FROM 
                    purchase_tagihan
                LEFT JOIN 
                    purchase_tagihan_detail ON purchase_tagihan.id = purchase_tagihan_detail.tagihan_id
                LEFT JOIN 
                    purchase_transaksi ON purchase_tagihan_detail.transaksi_id = purchase_transaksi.id
                LEFT JOIN 
                    purchase_order ON purchase_transaksi.order_id = purchase_order.id
                LEFT JOIN 
                    principal ON purchase_order.principal_id = principal.id
                {where_clause}
                GROUP BY 
                    purchase_tagihan.id, 
                    principal.nama, 
                    purchase_tagihan.no_tagihan, 
                    purchase_tagihan.total, 
                    purchase_tagihan.status_pembayaran,
                    purchase_tagihan.tanggal_bayar,
                    purchase_tagihan.jatuh_tempo
            """

        return Paginate(request, query, bindParams).paginate()

    @handle_error
    def getAddTagihan(self):
        conditions = {
            "no_tagihan": "purchase_tagihan.keterangan = :no_tagihan",
            "principal": "principal.id = :principal",
            "mulai_jatuh_tempo": "purchase_transaksi.jatuh_tempo >= :mulai_jatuh_tempo",
            "selesai_jatuh_tempo": "purchase_transaksi.jatuh_tempo <= :selesai_jatuh_tempo"
        }

        where, bindParams,_ = self.poolRequest(conditions)
        where = where.rstrip(' and')
        where_clause = f"where {where}" if where else 'where'

        query = f"""
            select
                purchase_transaksi.id as id_purchase_transaksi,
                purchase_transaksi.no_transaksi,
                purchase_transaksi.total as subtotal,
                purchase_transaksi.jatuh_tempo,
                purchase_order.kode as kode_order
            from purchase_transaksi
            left join purchase_order on purchase_transaksi.order_id = purchase_order.id
            left join principal on purchase_order.principal_id = principal.id
            {where_clause} 
            {' and ' if where else ''} purchase_transaksi.proses_id_berjalan = 3
        """

        return Paginate(request, query, bindParams).paginate()


    
    @handle_error_rollback
    def createTagihanPurchase(self):
        purchase_transaksis = self.req('purchase_transaksis')
        no_tagihan = f"TP-{datetime_now_stamp()}"
        
        if isinstance(purchase_transaksis, list):
            if not len(purchase_transaksis):
                raise nonServerErrorException('tidak ada faktur yang dipilih')
            
            # Hitung total dari semua subtotal
            total_tagihan = sum(float(pt['subtotal']) for pt in purchase_transaksis)
            
            # Buat record purchase_tagihan terlebih dahulu
            add_purchase_tagihan = purchase_tagihan(
                no_tagihan=no_tagihan,
                total=total_tagihan,
                status_pembayaran=1,

            )
            self.add(add_purchase_tagihan)
            self.flush()  # Untuk mendapatkan ID dari purchase_tagihan yang baru dibuat
            
             # Update proses_id_berjalan untuk semua transaksi terkait
            transaksi_ids = [pt['id_purchase_transaksi'] for pt in purchase_transaksis]
            update_query = f"""
                UPDATE purchase_transaksi 
                SET proses_id_berjalan = 4 
                WHERE id IN ({','.join(map(str, transaksi_ids))})
            """
            self.query().setRawQuery(update_query).execute()
            
            # Sekarang buat record purchase_tagihan_detail
            for purchase_transaksi in purchase_transaksis:
                add_purchase_tagihan_detail = purchase_tagihan_detail(
                    transaksi_id=purchase_transaksi['id_purchase_transaksi'],
                    tagihan_id=add_purchase_tagihan.id,  # Gunakan ID dari purchase_tagihan yang baru dibuat
                    subtotal=purchase_transaksi['subtotal']
                )
                self.add(add_purchase_tagihan_detail)
                
            self.commit()
            return {'status': 'success'}, 200
            
        raise nonServerErrorException('variable harus berupa list/array of object/dictionary')

    @handle_error
    def detailTagihanPurchasing(self):
        no_tagihan = self.req('no_tagihan')

        query = f"""
            select
                purchase_tagihan_detail.id as id_tagihan_detail,
                purchase_transaksi.no_transaksi,
                purchase_tagihan_detail.tagihan_id,
                purchase_transaksi.jatuh_tempo,
                purchase_tagihan_detail.subtotal,
                purchase_order.kode as kode_order,
                case
                    WHEN purchase_tagihan.status_pembayaran = 1 THEN 'belum lunas'
                    WHEN purchase_tagihan.status_pembayaran = 2 THEN 'lunas'
                    else 'tidak diketahui'
                end as status_bayar
            from purchase_tagihan_detail
            left join purchase_transaksi 
                on purchase_tagihan_detail.transaksi_id = purchase_transaksi.id
            left join purchase_tagihan 
                on purchase_tagihan_detail.tagihan_id = purchase_tagihan.id
            left join purchase_order
                on purchase_transaksi.order_id = purchase_order.id
            where purchase_tagihan.no_tagihan = '{no_tagihan}'
        """

        return self.query().setRawQuery(query).execute().fetchall().get()
    
    @handle_error_rollback
    def updatePembayaranTagihan(self):
        try:
            # Get request data
            no_tagihan = self.req('no_tagihan')
            tanggal_bayar = self.req('tanggal_bayar')
            keterangan = self.req('keterangan')
            bukti_bayar = request.files.get('bukti_bayar')
            
            # Upload bukti bayar jika ada
            bukti_bayar_filename = None
            if bukti_bayar:
                try:
                    upload_result = extraUploadImage(bukti_bayar)
                    bukti_bayar_filename = upload_result.get('filename')
                except Exception as e:
                    raise nonServerErrorException(f"Error uploading file: {str(e)}")
            
            # Check tagihan
            check_query = f"""
                SELECT id, status_pembayaran, total
                FROM purchase_tagihan 
                WHERE no_tagihan = '{no_tagihan}'
            """
            tagihan = self.db.session.execute(check_query).fetchone()
            
            if not tagihan:
                raise nonServerErrorException('Tagihan tidak ditemukan')
                
            if tagihan[1] == 2:
                raise nonServerErrorException('Tagihan sudah dibayar')

            # Update purchase_tagihan
            update_query = f"""
                UPDATE purchase_tagihan 
                SET 
                    status_pembayaran = 2,
                    tanggal_bayar = '{tanggal_bayar}',
                    keterangan = '{keterangan}',
                    bukti_bayar = {f"'{bukti_bayar_filename}'" if bukti_bayar_filename else 'NULL'},
                    nominal_pembayaran = total
                WHERE no_tagihan = '{no_tagihan}'
            """
            self.db.session.execute(update_query)

            # Get transaksi ids
            transaksi_query = f"""
                SELECT transaksi_id 
                FROM purchase_tagihan_detail 
                WHERE tagihan_id = {tagihan[0]}
            """
            transaksi_data = self.db.session.execute(transaksi_query).fetchall()

            if transaksi_data:
                transaksi_ids = [str(row[0]) for row in transaksi_data]
                
                # Update purchase_transaksi
                update_transaksi = f"""
                    UPDATE purchase_transaksi 
                    SET 
                        status_pembayaran = 2,
                        proses_id_berjalan = 5
                    WHERE id IN ({','.join(transaksi_ids)})
                """
                self.db.session.execute(update_transaksi)

            self.commit()
            return {'message': 'Pembayaran berhasil diproses'}, 200

        
        except Exception as e:
            raise nonServerErrorException(str(e))