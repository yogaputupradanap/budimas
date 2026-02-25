from  apps.models.BaseModel  import  BaseModel


class PurchaseTagihanDetail(BaseModel) :

    __tablename__ = 'purchase_tagihan_detail'
    tagihan_id    = BaseModel.foreign('purchase_order.id')
    transaksi_id  = BaseModel.foreign('purchase_transaksi.id')
    subtotal      = BaseModel.float()

    def __repr__(self)              :
        return f"data('{self.id}')"

    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id            = data.get('tagihan_detail_id')
                self.tagihan_id    = data.get('tagihan_id')
                self.transaksi_id  = data.get('transaksi_id')
                self.subtotal      = data.get('subtotal')
        return  self