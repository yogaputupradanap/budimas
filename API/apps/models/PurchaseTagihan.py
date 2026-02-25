from  apps.models.BaseModel  import  BaseModel


class PurchaseTagihan(BaseModel) :

    __tablename__      = 'purchase_tagihan'
    transaksi_id       = BaseModel.foreign('purchase_transaksi.id')
    jatuh_tempo        = BaseModel.date()
    total              = BaseModel.float()
    nominal_pembayaran = BaseModel.float()
    status_pembayaran  = BaseModel.integer()
    tipe_setoran       = BaseModel.string(50)
    keterangan         = BaseModel.string(100)
    proses_log         = BaseModel.one_to_many_bi_main('PurchaseTagihanProsesLog', 'tagihan')

    def __repr__(self)              :
        return f"data('{self.id}')"

    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id                 = data.get('tagihan_id')
                self.transaksi_id       = data.get('transaksi_id')
                self.jatuh_tempo        = data.get('jatuh_tempo')
                self.total              = data.get('total')
                self.nominal_pembayaran = data.get('nominal_pembayaran')
                self.status_pembayaran  = data.get('status_pembayaran')
                self.tipe_setoran       = data.get('tipe_setoran')
                self.keterangan         = data.get('keterangan')
        return  self