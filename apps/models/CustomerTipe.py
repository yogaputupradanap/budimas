from apps.models.BaseModel import BaseModel

class CustomerTipe(BaseModel):

    __tablename__ = 'customer_tipe'
    nama = BaseModel.string(50)
    kode = BaseModel.string(10)

    def __repr__(self):
        return f"data('{self.id}')"

    # def __init__(self, data=None):
    #     self.set(data)

    def set(self, data=None):
        if (data):
            self.id = data.get('customer_tipe_id')
            self.nama = data.get('nama')
            self.kode = data.get('kode')
        return self
