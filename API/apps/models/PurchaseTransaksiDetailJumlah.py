from  apps.models.BaseModel  import  BaseModel


class PurchaseTransaksiDetailJumlah(BaseModel) :

    __tablename__          = 'purchase_transaksi_detail_jumlah'
    transaksi_id           = BaseModel.foreign('purchase_order.id')
    transaksi_detail_id    = BaseModel.foreign('purchase_transaksi_detail.id')
    jumlah                 = BaseModel.integer()
    subtotal               = BaseModel.float()
    order_detail_jumlah_id = BaseModel.foreign('purchase_order_detail_jumlah.id')
    order_detail_jumlah    = BaseModel.one_to_many('PurchaseOrderDetailJumlah', __tablename__, [order_detail_jumlah_id])

    def __repr__(self)              :
        return f"data('{self.id}')"

    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id                     = data.get('transaksi_detail_jumlah_id')
                self.transaksi_id           = data.get('transaksi_id')
                self.transaksi_detail_id    = data.get('transaksi_detail_id')
                self.jumlah                 = data.get('jumlah')
                self.subtotal               = data.get('subtotal')
                self.order_detail_jumlah_id = data.get('order_detail_jumlah_id')
        return  self