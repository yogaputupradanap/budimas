from  .  import  BaseModel
from ..conn2 import db


class TipeTransaksi(BaseModel) :

    __tablename__   = 'tipe_transaksi'
    nama            = BaseModel.string(100)
    deskripsi        = BaseModel.string(100)


    def __repr__(self)              :
        return f"data('{self.id_log_inventory}')"
    
    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id = data.get('id')
                self.nama = data.get('nama')
                self.deskripsi = data.get('deskripsi')
        return  self