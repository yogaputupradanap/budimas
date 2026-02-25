from  .  import  BaseModel
from ..conn2 import db


class LogInventory(BaseModel) :

    __tablename__   = 'log_inventory'
    __table_args__ = {'extend_existing': True}
    id_log_inventory = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_transaksi    = BaseModel.integer()
    id_cabang       = BaseModel.integer()
    id_perusahaan  = BaseModel.integer()
    id_transaksi_tipe = BaseModel.integer()
    id_produk      = BaseModel.integer()
    id_user        = BaseModel.integer()
    stok_awal      = BaseModel.integer()
    stok_peralihan= BaseModel.integer()
    stok_akhir     = BaseModel.integer()
    harga         = BaseModel.float()
    tanggal        = BaseModel.date()
    valuasi        = BaseModel.integer()
    waktu          = BaseModel.time()
    keterangan     = BaseModel.string(100)
    produk_uom_id  = BaseModel.integer()


    def __repr__(self)              :
        return f"data('{self.id_log_inventory}')"
    
    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id_transaksi     = data.get('id_transaksi')
                self.id_cabang        = data.get('id_cabang')
                self.id_perusahaan   = data.get('id_perusahaan')
                self.id_transaksi_tipe= data.get('id_transaksi_tipe')
                self.id_produk       = data.get('id_produk')
                self.id_user         = data.get('id_user')
                self.stok_awal       = data.get('stok_awal')
                self.stok_peralihan = data.get('stok_peralihan')
                self.stok_akhir      = data.get('stok_akhir')
                self.harga           = data.get('harga')
                self.tanggal         = data.get('tanggal')
                self.valuasi         = data.get('valuasi')
                self.waktu           = data.get('waktu')
                self.keterangan      = data.get('keterangan')
                self.produk_uom_id   = data.get('produk_uom_id')
        return  self