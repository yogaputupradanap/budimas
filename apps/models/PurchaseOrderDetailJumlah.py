from  apps.models.BaseModel  import  BaseModel


class PurchaseOrderDetailJumlah(BaseModel) :

    __tablename__       = 'purchase_order_detail_jumlah'
    uom_id              = BaseModel.integer()
    uom_kode            = BaseModel.string(100)
    uom_nama            = BaseModel.string(100)
    uom_level           = BaseModel.integer()
    uom_faktor_konversi = BaseModel.float()
    uom_harga_beli      = BaseModel.float()
    uom_harga_beli_ppn  = BaseModel.float()
    jumlah              = BaseModel.integer()
    subtotal            = BaseModel.float()
    order_id            = BaseModel.foreign('purchase_order.id')
    order_detail_id     = BaseModel.foreign('purchase_order_detail.id')
    jumlah_per_uom      = BaseModel.integer()
    
    def __repr__(self)              :
        return f"data('{self.id}')"

    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id                  = data.get('order_detail_jumlah_id')
                self.uom_id              = data.get('uom_id')
                self.uom_kode            = data.get('uom_kode')
                self.uom_nama            = data.get('uom_nama')
                self.uom_level           = data.get('uom_level')
                self.uom_faktor_konversi = data.get('uom_faktor_konversi')
                self.uom_harga_beli      = data.get('uom_harga_beli')
                self.uom_harga_beli_ppn  = data.get('uom_harga_beli_ppn')
                self.jumlah              = data.get('jumlah')
                self.subtotal            = data.get('subtotal')
                self.order_id            = data.get('order_id')
                self.order_detail_id     = data.get('order_detail_id')
        return  self