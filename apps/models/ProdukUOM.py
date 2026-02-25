from . import  BaseModel


class ProdukUOM(BaseModel):
    
    __tablename__       = 'produk_uom'
    kode                = BaseModel.string(25)
    nama                = BaseModel.string(50)
    level               = BaseModel.integer()
    packing_satuan      = BaseModel.string(15)
    packing_tinggi      = BaseModel.float()
    packing_panjang     = BaseModel.float()
    packing_lebar       = BaseModel.float()
    berat_satuan        = BaseModel.string(15)
    berat_bersih        = BaseModel.float()
    berat_kotor         = BaseModel.float()
    set_default_sales   = BaseModel.integer()
    set_default_storage = BaseModel.integer()
    id_produk           = BaseModel.foreign('produk.id')
    faktor_konversi     = BaseModel.integer()

    def __repr__(self)              :
        return f"data('{self.id}')"

    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id                  = data.get('produk_uom_id')
                self.kode                = data.get('kode')
                self.nama                = data.get('nama')
                self.level               = data.get('level')
                self.packing_satuan      = data.get('packing_satuan')
                self.packing_tinggi      = data.get('packing_tinggi')
                self.packing_panjang     = data.get('packing_panjang')
                self.packing_lebar       = data.get('packing_lebar')
                self.berat_satuan        = data.get('berat_satuan')
                self.berat_bersih        = data.get('berat_bersih')
                self.berat_kotor         = data.get('berat_kotor')
                self.set_default_sales   = data.get('set_default_sales')
                self.set_default_storage = data.get('set_default_storage')
                self.id_produk           = data.get('id_produk')
                self.faktor_konversi     = data.get('faktor_konversi')
        return  self