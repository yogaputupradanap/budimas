from  apps.models.BaseModel  import  BaseModel


class PurchaseOrderDetailTotal(BaseModel) :

    __tablename__          = 'purchase_order_detail_total'
    total_order            = BaseModel.float()
    total_terpenuhi        = BaseModel.float()
    total_tersisa          = BaseModel.float()
    order_id               = BaseModel.foreign('purchase_order.id')
    order_detail_id        = BaseModel.foreign('purchase_order_detail.id')
    order_detail_jumlah_id = BaseModel.foreign('purchase_order_detail_jumlah.id')
    subtotal               = BaseModel.float()
    
    def __repr__(self)              :
        return f"data('{self.id}')"

    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id                     = data.get('order_detail_total_id')
                self.total_order            = data.get('total_order')
                self.total_terpenuhi        = data.get('total_terpenuhi')
                self.total_tersisa          = data.get('total_tersisa')
                self.order_id               = data.get('order_id')
                self.order_detail_id        = data.get('order_detail_id')
                self.order_detail_jumlah_id = data.get('order_detail_jumlah_id')
        return  self