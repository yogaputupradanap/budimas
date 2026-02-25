from . import BaseServices
from apps.handler import handle_error, handle_error_rollback, nonServerErrorException
from apps.models import info_pengeluaran_driver, pengeluaran_driver, faktur as Faktur
from flask import escape

class Driver(BaseServices):
        
    @handle_error
    def searchDriver(self):
        """
         @brief Search for driver.
         @return dict
        """
        nama_driver = escape(self.req('nama_driver'))
        tanggal = escape(self.req('tanggal'))
        
        return (
            self
            .query()
            .setRawQuery(
                f"""
                    select 
                    info_pengeluaran_driver.id_driver,
                    info_pengeluaran_driver.id as id_info_driver,
                    users.nama as nama_driver,
                    info_pengeluaran_driver.helper,
                    info_pengeluaran_driver.uang_saku,
                    sum(pengeluaran_driver.nominal) 
                    + info_pengeluaran_driver.isi_bbm_rupiah as total_pengeluran,
                    info_pengeluaran_driver.uang_saku - 
                    ( sum(pengeluaran_driver.nominal) + 
                    info_pengeluaran_driver.isi_bbm_rupiah ) as sisa_uang,
                    info_pengeluaran_driver.tanggal as tanggal_berangkat
                    from driver
                    join users 
                    on driver.id_user = users.id
                    join info_pengeluaran_driver
                    on info_pengeluaran_driver.id_driver = driver.id
                    join pengeluaran_driver
                    on pengeluaran_driver.id_info = info_pengeluaran_driver.id
                    where 
                    users.nama ILIKE '%{nama_driver}%'
                    and
                    info_pengeluaran_driver.tanggal = '{tanggal}'
                    group by
                    info_pengeluaran_driver.id_driver,
                    info_pengeluaran_driver.id,
                    users.nama,
                    info_pengeluaran_driver.uang_saku,
                    info_pengeluaran_driver.uang_saku,
                    info_pengeluaran_driver.tanggal 
                """
            )
            .execute()
            .fetchall()
            .get()
        )
        
    @handle_error
    def getAllDriver(self):
        """
         @brief Get all drivers and nama.
         @return A list of driver names and other informations
        """
        id_cabang = self.req('id_cabang')
        return (
            self
            .query()
            .setRawQuery(
                """
                    SELECT 
                    driver.*,
                    users.nama
                    FROM driver
                    INNER JOIN users ON driver.id_user = users.id
                    where users.id_cabang = :id_cabang
                """
            )
            .bindparams({
                "id_cabang": id_cabang
            })
            .execute()
            .fetchall()
            .get()
        )
    
    @handle_error
    def getPengeluaranDriverList(self, id = None):
        """
         @brief Get a list of Pengeluaran drivers. If id is specified only the list of drivers with that id will be returned
         @param id of the driver to get
         @return dict
        """
        addWhere = f'where info_pengeluaran_driver.id = { escape(id) }' if id else ''
        
        return (
            self
            .query()
            .setRawQuery(
                f"""
                    select 
                    info_pengeluaran_driver.id_driver,
                    info_pengeluaran_driver.id as id_info_driver,
                    users.nama as nama_driver,
                    info_pengeluaran_driver.helper,
                    info_pengeluaran_driver.uang_saku,
                    sum(pengeluaran_driver.nominal) 
                    + info_pengeluaran_driver.isi_bbm_rupiah as total_pengeluran,
                    info_pengeluaran_driver.uang_saku - 
                    ( sum(pengeluaran_driver.nominal) + 
                    info_pengeluaran_driver.isi_bbm_rupiah ) as sisa_uang,
                    info_pengeluaran_driver.tanggal as tanggal_berangkat
                    from driver
                    join users 
                    on driver.id_user = users.id
                    join info_pengeluaran_driver
                    on info_pengeluaran_driver.id_driver = driver.id
                    join pengeluaran_driver
                    on pengeluaran_driver.id_info = info_pengeluaran_driver.id
                    {addWhere}
                    group by
                    info_pengeluaran_driver.id_driver,
                    info_pengeluaran_driver.id,
                    users.nama,
                    info_pengeluaran_driver.uang_saku,
                    info_pengeluaran_driver.uang_saku,
                    info_pengeluaran_driver.tanggal
                """
            )
            .execute()
            .fetchall()
            .get()
        )
    
    @handle_error
    def getPengeluaranDriverInfoUpdate(self, id_info_pengeluaran_driver):
        """
         @brief Update information about Pengeluaran driver. This is a query that returns a dictionary of all values that need to be updated in order to get the latest information.
         @param id_info_pengeluaran_driver id of Pengeluaran driver to update
         @return dict of all values that need to be updated in order to get the latest informations
        """
        return (
            self
            .query()
            .setRawQuery(
                """
                    select
                    distinct info_pengeluaran_driver.id as id_info_pengeluaran_driver,
                    info_pengeluaran_driver.id_driver,
                    info_pengeluaran_driver.tujuan,
                    info_pengeluaran_driver.km_berangkat,
                    info_pengeluaran_driver.helper,
                    info_pengeluaran_driver.km_pulang,
                    info_pengeluaran_driver.km_isi_bbm,
                    info_pengeluaran_driver.isi_bbm_liter,
                    info_pengeluaran_driver.isi_bbm_rupiah,
                    info_pengeluaran_driver.uang_saku,
                    info_pengeluaran_driver.tanggal
                    from customer
                    join rute on customer.id_rute = rute.id 
                    join cabang on customer.id_cabang = cabang.id
                    join plafon on plafon.id_customer = customer.id
                    join sales_order on sales_order.id_plafon = plafon.id
                    join faktur on faktur.id_sales_order = sales_order.id
                    join sales_order_detail on sales_order_detail.id_sales_order = sales_order.id
                    join proses_picking on proses_picking.id_order_detail = sales_order_detail.id
                    join driver on driver.id = proses_picking.id_driver
                    join info_pengeluaran_driver on info_pengeluaran_driver.id_driver = driver.id
                    where faktur.jenis_faktur = 'penjualan'
                    and info_pengeluaran_driver.id = :id
                """
            )
            .bindparams({
                "id": id_info_pengeluaran_driver
            })
            .execute()
            .fetchone()
            .result
        )
    
    @handle_error
    def getPengeluaranDriverInfoFaktursUpdate(self, id_info_pengeluaran_driver):
        fakturs = (
            self
            .query()
            .setRawQuery(
                  """
                    select
                    faktur.id as id_faktur,
                    tipe_pengeluaran.id as id_tipe,
                    faktur.no_faktur as nomor_faktur,
                    customer.nama as nama_customer,
                    pengeluaran_driver.nominal as nominal_pengeluran,
                    tipe_pengeluaran.tipe as tipe_pengeluaran,
                    pengeluaran_driver.keterangan,
                    rute.kode as kode_rute
                    from customer
                    join rute on customer.id_rute = rute.id 
                    join cabang on customer.id_cabang = cabang.id
                    join plafon on plafon.id_customer = customer.id
                    join sales_order on sales_order.id_plafon = plafon.id
                    join faktur on faktur.id_sales_order = sales_order.id
                    join pengeluaran_driver on pengeluaran_driver.id_faktur = faktur.id
                    join tipe_pengeluaran on tipe_pengeluaran.id = pengeluaran_driver.id_tipe
                    where faktur.jenis_faktur = 'penjualan'
                    and pengeluaran_driver.id_info = :id 
                    group by
                    faktur.id,
                    tipe_pengeluaran.id,
                    customer.nama,
                    pengeluaran_driver.nominal,
                    tipe_pengeluaran.tipe,
                    pengeluaran_driver.keterangan,
                    rute.kode
                    order by tipe_pengeluaran.id asc
                  """      
            )
            .bindparams({
                "id": id_info_pengeluaran_driver
            })
            .execute()
            .fetchall()
            .get()
        )
        
        fakturObj = {}
        
        for faktur in fakturs:
            id_faktur = faktur['id_faktur']
            id_tipe = faktur['id_tipe']
            nominal = faktur['nominal_pengeluran']
            addedBase = { **faktur, "nominal_parkir": nominal }
            
            if id_faktur in fakturObj:
                if id_tipe == 7:
                    fakturObj[id_faktur]['nominal_bongkar'] = nominal
                elif id_tipe == 8:
                    fakturObj[id_faktur]['nominal_lainnya'] = nominal
            else:
                fakturObj[id_faktur] = addedBase
        
        list_faktur = [value for value in fakturObj.values()]
        
        return list_faktur
    
    @handle_error
    def getPengeluaranDriverInfoFaktursAdd(self, id_driver):
        return (
            self
            .query()
            .setRawQuery(
                """
                    select
                    faktur.id as id_faktur,
                    faktur.no_faktur as nomor_faktur,
                    customer.nama as nama_customer,
                    rute.kode as kode_rute
                    from customer
                    join rute on customer.id_rute = rute.id 
                    join cabang on customer.id_cabang = cabang.id
                    join plafon on plafon.id_customer = customer.id
                    join sales_order on sales_order.id_plafon = plafon.id
                    join faktur on faktur.id_sales_order = sales_order.id
                    join sales_order_detail on sales_order_detail.id_sales_order = sales_order.id
                    join proses_picking on proses_picking.id_order_detail = sales_order_detail.id
                    where faktur.jenis_faktur = 'penjualan'
                    and proses_picking.id_driver = :id
                    and faktur.status_faktur = 5
                    group by
                    faktur.id,
                    customer.nama,
                    rute.kode
                    order by faktur.id asc
                """
            )
            .bindparams({
                'id': id_driver
            })
            .execute()
            .fetchall()
            .get()
        )
    
    @handle_error_rollback
    def addPengeluaranDriver(self):
        fakturs = self.req('fakturs')
        
        add_info_pengeluaran_driver = info_pengeluaran_driver(
            id_driver = self.req('id_driver'),
            tujuan = self.req('tujuan'),
            km_berangkat = self.req('km_berangkat'),
            helper = self.req('helper'),
            km_pulang = self.req('km_pulang'),
            km_isi_bbm = self.req('km_isi_bbm'),
            isi_bbm_liter = self.req('isi_bbm_liter'),
            isi_bbm_rupiah = self.req('isi_bbm_rupiah'),
            uang_saku = self.req('uang_saku'),
            tanggal = self.req('tanggal')
        )
        
        self.add(add_info_pengeluaran_driver).flush()
        
        if len(fakturs) :
            for faktur in fakturs:
                id_faktur = faktur['id_faktur']
                
                add_pengeluaran_driver = pengeluaran_driver(
                    id_tipe = faktur['id_tipe'],
                    nominal = faktur['nominal'],
                    keterangan = faktur['keterangan'],
                    id_faktur = id_faktur,
                    id_info = add_info_pengeluaran_driver.id,
                )
                
                if(self.is_production):
                    update_faktur = Faktur.query.filter(Faktur.id == id_faktur).first()
                    update_faktur.status_faktur = 8
                
                self.add(add_pengeluaran_driver).flush()
        
        else:
            raise nonServerErrorException("Driver tidak mempunyai faktur")

        self.commit()
        
        result = self.getPengeluaranDriverList(add_info_pengeluaran_driver.id)[0]
        
        return result, 200
    
    @handle_error_rollback
    def updatePengeluaranDriver(self):
        id_info_pengeluaran_driver = self.req('id')
        fakturs = self.req('fakturs')
        
        update_info_pengeluaran_driver = (
            info_pengeluaran_driver.query
            .filter(info_pengeluaran_driver.id == id_info_pengeluaran_driver)
            .first()
        )
        
        update_info_pengeluaran_driver.tujuan = self.req('tujuan')
        update_info_pengeluaran_driver.km_berangkat = self.req('km_berangkat')
        update_info_pengeluaran_driver.helper = self.req('helper')
        update_info_pengeluaran_driver.km_pulang = self.req('km_pulang')
        update_info_pengeluaran_driver.km_isi_bbm = self.req('km_isi_bbm')
        update_info_pengeluaran_driver.isi_bbm_liter = self.req('isi_bbm_liter')
        update_info_pengeluaran_driver.isi_bbm_rupiah = self.req('isi_bbm_rupiah')
        update_info_pengeluaran_driver.uang_saku = self.req('uang_saku')
        update_info_pengeluaran_driver.tanggal = self.req('tanggal')
        
        self.flush()
        
        if len(fakturs) :
            for faktur in fakturs:
                id_tipe = faktur['id_tipe']
                id_faktur = faktur['id_faktur']
                nominal = faktur['nominal']
                
                update_pengeluaran_driver = (
                    pengeluaran_driver
                    .query
                    .filter(
                        pengeluaran_driver.id_info == id_info_pengeluaran_driver, 
                        pengeluaran_driver.id_tipe == id_tipe,
                        pengeluaran_driver.id_faktur == id_faktur
                    )
                    .first()
                )
                
                if nominal: update_pengeluaran_driver.nominal = nominal
                update_pengeluaran_driver.keterangan = faktur['keterangan']
                
                self.flush()
        
        self.commit()
        
        result = self.getPengeluaranDriverList(id_info_pengeluaran_driver)[0]
        return result, 200