from  apps.models.BaseModel  import  BaseModel


class PurchaseOrderDetail(BaseModel) :

    __tablename__     = 'purchase_order_detail'
    produk_id         = BaseModel.foreign('produk.id')
    produk_kode       = BaseModel.string(100)
    produk_nama       = BaseModel.string(100)
    produk_harga_beli = BaseModel.float()
    order_id          = BaseModel.foreign('purchase_order.id')
    ppn               = BaseModel.float()
    total_order       = BaseModel.float()
    total_terpenuhi   = BaseModel.float()
    total_tersisa     = BaseModel.float()
    subtotal          = BaseModel.float()

    def __repr__(self)              :
        return f"data('{self.id}')"

    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id                = data.get('order_detail_id')
                self.produk_id         = data.get('produk_id')
                self.produk_kode       = data.get('produk_kode')
                self.produk_nama       = data.get('produk_nama')
                self.produk_harga_beli = data.get('produk_harga_beli')
                self.order_id          = data.get('order_id')
                self.total_order       = data.get('total_order')
                self.total_terpenuhi   = data.get('total_terpenuhi')
                self.total_tersisa     = data.get('total_tersisa')
                self.subtotal          = data.get('subtotal')
                self.ppn               = data.get('ppn')
        return  self