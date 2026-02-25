from  .  import  BaseModel


class Inventori(BaseModel) :

    __tablename__  = 'inventori'
    transaksi_kode = BaseModel.string(100)
    transaksi_tipe = BaseModel.integer()
    cabang_id      = BaseModel.foreign('cabang.id')
    user_id        = BaseModel.foreign('user.id')
    produk_id      = BaseModel.foreign('produk.id')
    produk_uom_id  = BaseModel.foreign('produk_uom.id')
    stok_tipe      = BaseModel.integer()
    stok_awal      = BaseModel.integer()
    stok_peralihan = BaseModel.integer()
    stok_akhir     = BaseModel.integer()
    harga          = BaseModel.float()
    valuasi        = BaseModel.float()
    tanggal        = BaseModel.date()
    waktu          = BaseModel.time()


    def __repr__(self)              :
        return f"data('{self.id}')"
    
    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id             = data.get('inventori_id')
                self.transaksi_kode = data.get('transaksi_kode')
                self.transaksi_tipe = data.get('transaksi_tipe')
                self.cabang_id      = data.get('cabang_id')
                self.user_id        = data.get('user_id')
                self.produk_id      = data.get('produk_id')
                self.produk_uom_id  = data.get('produk_uom_id')
                self.stok_tipe      = data.get('stok_tipe')
                self.stok_awal      = data.get('stok_awal')
                self.stok_peralihan = data.get('stok_peralihan')
                self.stok_akhir     = data.get('stok_akhir')
                self.harga          = data.get('harga')
                self.valuasi        = data.get('valuasi')
                self.tanggal        = data.get('tanggal')
                self.waktu          = data.get('waktu')
        return  self