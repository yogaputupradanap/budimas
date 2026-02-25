from  flask                  import  request
from  apps.query             import  DB
from  apps.models.BaseModel  import  BaseModel


class ProdukKategori(BaseModel) :
    
    __tablename__ = 'produk_kategori'
    nama          = BaseModel.string(50)
    
    def __repr__(self)              :
        return f"data('{self.id}')"

    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id   = data.get('produk_kategori_id')
                self.nama = data.get('nama')
        return  self