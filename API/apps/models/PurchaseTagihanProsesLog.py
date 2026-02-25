from  apps.models.BaseModel  import  BaseModel


class PurchaseTagihanProsesLog(BaseModel) :

    __tablename__          = 'purchase_tagihan_proses_log'
    tagihan_id             = BaseModel.foreign('purchase_tagihan.id')
    user_id                = BaseModel.foreign('users.id')
    user_jabatan_id        = BaseModel.foreign('jabatan.id')
    proses_id_diselesaikan = BaseModel.integer()
    tanggal                = BaseModel.date()
    waktu                  = BaseModel.time()
    user                   = BaseModel.one_to_many('User', __tablename__, [user_id])
    user_jabatan           = BaseModel.one_to_many('UserJabatan', __tablename__, [user_jabatan_id])
    tagihan                = BaseModel.one_to_many_bi_ref('PurchaseTagihan', 'proses_log', [tagihan_id])

    def __repr__(self)              :
        return f"data('{self.id}')"
    
    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id                     = data.get('id')
                self.tagihan_id             = data.get('tagihan_id')
                self.user_id                = data.get('user_id')
                self.user_jabatan_id        = data.get('user_jabatan_id')
                self.proses_id_diselesaikan = data.get('proses_id_diselesaikan')
                self.tanggal                = data.get('tanggal')
                self.waktu                  = data.get('waktu')
        return  self