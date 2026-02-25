from  apps.query   import  DB
from  apps.helper  import  *
from  flask        import  request
from . import  BaseModel

class ProdukHargaJual(BaseModel) :
    __tablename__       = 'produk_harga_jual'
    id_produk           = BaseModel.foreign('produk.id')
    id_tipe_harga      = BaseModel.foreign('produk_tipe_harga.id')
    harga               = BaseModel.float()

    def __repr__(self)              :
        return f"data('{self.id}')"

    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id                  = data.get('produk_harga_jual_id')
                self.id_produk           = data.get('id_produk')
                self.id_tipe_harga      = data.get('id_tipe_harga')
                self.harga               = data.get('harga')
        return  self
    
    def all() :
        """
        """
        return DB(request).setRawQuery("""
                                                           
            SELECT      produk_harga_jual   .*,
                        produk_tipe_harga   .nama  AS  tipe_harga
                                        
            FROM        produk_harga_jual
                                        
            LEFT JOIN   produk
                ON      produk              .id             = 
                        produk_harga_jual   .id_produk
                                                                
            LEFT JOIN   produk_tipe_harga
                ON      produk_tipe_harga   .id             =
                        produk_harga_jual   .id_tipe_harga
                                                                    
        """).execute().fetchall().get()