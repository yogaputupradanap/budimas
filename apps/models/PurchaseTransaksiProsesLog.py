from  apps.models.BaseModel  import  BaseModel


class PurchaseTransaksiProsesLog(BaseModel) :

    __tablename__          = 'purchase_transaksi_proses_log'
    transaksi_id           = BaseModel.foreign('purchase_transaksi.id')
    user_id                = BaseModel.foreign('users.id')
    user_jabatan_id        = BaseModel.foreign('jabatan.id')
    proses_id_diselesaikan = BaseModel.integer()
    tanggal                = BaseModel.date()
    waktu                  = BaseModel.time()
    user                   = BaseModel.one_to_many('User', __tablename__, [user_id])
    user_jabatan           = BaseModel.one_to_many('UserJabatan', __tablename__, [user_jabatan_id])
    transaksi              = BaseModel.one_to_many_bi_ref('PurchaseTransaksi', 'proses_log', [transaksi_id])

    def __repr__(self)              :
        return f"data('{self.id}')"
    
    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id                     = data.get('id')
                self.transaksi_id           = data.get('transaksi_id')
                self.user_id                = data.get('user_id')
                self.user_jabatan_id        = data.get('user_jabatan_id')
                self.proses_id_diselesaikan = data.get('proses_id_diselesaikan')
                self.tanggal                = data.get('tanggal')
                self.waktu                  = data.get('waktu')
        return  self