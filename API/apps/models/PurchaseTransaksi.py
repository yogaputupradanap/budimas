from  apps.models.BaseModel  import  BaseModel


class PurchaseTransaksi(BaseModel) :

    __tablename__      = 'purchase_transaksi'
    order_id           = BaseModel.foreign('purchase_order.id')
    no_transaksi       = BaseModel.string(100)
    subtotal           = BaseModel.float()
    potongan           = BaseModel.float()
    biaya_lainnya      = BaseModel.float()
    total              = BaseModel.float()
    status_pembayaran  = BaseModel.integer()
    proses_id_berjalan = BaseModel.integer()
    batch              = BaseModel.integer()
    keterangan         = BaseModel.string(100)
    jatuh_tempo        = BaseModel.date()
    order              = BaseModel.one_to_many('PurchaseOrder', __tablename__, [order_id])
    proses_log         = BaseModel.one_to_many_bi_main('PurchaseTransaksiProsesLog', 'transaksi')

    def __repr__(self)              :
        return f"data('{self.id}')"

    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id                 = data.get('transaksi_id')
                self.order_id           = data.get('order_id')
                self.no_transaksi       = data.get('no_transaksi')
                self.subtotal           = data.get('subtotal')
                self.potongan           = data.get('potongan')
                self.biaya_lainnya      = data.get('biaya_lainnya')
                self.total              = data.get('total')
                self.status_pembayaran  = data.get('status_pembayaran')
                self.proses_id_berjalan = data.get('proses_id_berjalan')
                self.batch              = data.get('batch')
                self.keterangan         = data.get('keterangan')
                self.jatuh_tempo        = data.get('jatuh_tempo')
        return  self