from  .  import  BaseModel


class Stok(BaseModel) :

    __tablename__   = 'stok'
    cabang_id       = BaseModel.foreign('cabang.id')
    produk_id       = BaseModel.foreign('produk.id')
    jumlah_ready    = BaseModel.integer()
    jumlah_booked   = BaseModel.integer()
    jumlah_delivery = BaseModel.integer()
    jumlah_incoming = BaseModel.integer()
    jumlah_gudang   = BaseModel.integer()
    jumlah_canvas   = BaseModel.integer()
    jumlah_good     = BaseModel.integer()
    jumlah_bad      = BaseModel.integer()
    tanggal_update  = BaseModel.date()
    waktu_update    = BaseModel.time()
    jumlah_picked   = BaseModel.integer()
    transfer_out    = BaseModel.integer()
    transfer_in     = BaseModel.integer()

    def __repr__(self)              :
        return f"data('{self.id}')"
    
    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id              = data.get('stok_id')
                self.cabang_id       = data.get('cabang_id')
                self.produk_id       = data.get('produk_id')
                self.jumlah_ready    = data.get('jumlah_ready')
                self.jumlah_booked   = data.get('jumlah_booked')
                self.jumlah_delivery = data.get('jumlah_delivery')
                self.jumlah_incoming = data.get('jumlah_incoming')
                self.jumlah_gudang   = data.get('jumlah_gudang')
                self.jumlah_canvas   = data.get('jumlah_canvas')
                self.jumlah_good     = data.get('jumlah_good')
                self.jumlah_bad      = data.get('jumlah_bad')
                self.tanggal_update  = data.get('tanggal_update')
                self.waktu_update    = data.get('waktu_update')
                self.jumlah_picked   = data.get('jumlah_picked')
                self.transfer_out    = data.get('transfer_out')
                self.transfer_in     = data.get('transfer_in')
        return  self