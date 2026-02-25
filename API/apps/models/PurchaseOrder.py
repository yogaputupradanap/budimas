from . import  BaseModel


class PurchaseOrder(BaseModel) :

    __tablename__      = 'purchase_order'
    cabang_id          = BaseModel.foreign('cabang.id')
    principal_id       = BaseModel.foreign('principal.id')
    proses_id_berjalan = BaseModel.integer()
    kode               = BaseModel.string(100)
    keterangan         = BaseModel.string(100)
    batch_pengiriman   = BaseModel.integer()
    total              = BaseModel.float()
    cabang             = BaseModel.one_to_many('Cabang', __tablename__, [cabang_id])
    principal          = BaseModel.one_to_many('Principal', __tablename__, [principal_id])
    proses_log         = BaseModel.one_to_many_bi_main('PurchaseOrderProsesLog', 'order')

    def __repr__(self)              :
        return f"data('{self.id}')"

    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id                 = data.get('order_id')
                self.cabang_id          = data.get('cabang_id')
                self.principal_id       = data.get('principal_id')
                self.proses_id_berjalan = data.get('proses_id_berjalan')
                self.kode               = data.get('kode')
                self.keterangan         = data.get('keterangan')
                self.total              = data.get('total')
        return  self