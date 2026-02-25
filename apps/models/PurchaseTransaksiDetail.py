from  apps.models.BaseModel  import  BaseModel


class PurchaseTransaksiDetail(BaseModel) :

    __tablename__   = 'purchase_transaksi_detail'
    transaksi_id    = BaseModel.foreign('purchase_transaksi.id')
    tanggal_expired = BaseModel.date()
    batch_number    = BaseModel.string(50)
    subtotal        = BaseModel.float()
    order_detail_id = BaseModel.foreign('purchase_order_detail.id')
    transaksi       = BaseModel.one_to_many('PurchaseTransaksi', __tablename__, [transaksi_id])
    order_detail    = BaseModel.one_to_many('PurchaseOrderDetail', __tablename__, [order_detail_id])

    def __repr__(self)              :
        return f"data('{self.id}')"

    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id              = data.get('transaksi_detail_id')
                self.transaksi_id    = data.get('transaksi_id')
                self.tanggal_expired = data.get('tanggal_expired')
                self.batch_number    = data.get('batch_number')
                self.order_detail_id = data.get('order_detail_id')
                self.subtotal        = data.get('subtotal')
        return  self