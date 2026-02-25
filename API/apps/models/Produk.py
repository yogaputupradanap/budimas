from  flask                  import  request

from apps.datatables import DataTables, DictMapper
from  apps.query             import  DB
from apps.models.BaseModel import BaseModel
from apps.conn2 import db
from apps.widget import btn_details, btn_actions


class Produk(BaseModel) :
    
    __tablename__ = 'produk'
    id_principal = BaseModel.foreign('principal.id')
    id_brand     = BaseModel.foreign('produk_brand.id')
    id_kategori  = BaseModel.foreign('produk_kategori.id')
    id_status    = BaseModel.integer()
    kode_sku     = BaseModel.string(25)
    kode_ean     = BaseModel.string(25)
    nama         = BaseModel.string(50)
    harga_beli   = BaseModel.float()
    keterangan   = BaseModel.string(50)
    harga_jual   = BaseModel.float()
    kubikasiperbox = BaseModel.integer()
    kubikasiperkarton = BaseModel.integer()
    isiperbox = BaseModel.integer()
    isiperkarton = BaseModel.integer()
    satuan = BaseModel.string(30)
    kubikasiperpieces = BaseModel.integer()
    
    def __repr__(self)              :
        return f"data('{self.id}')"

    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id           = data.get('produk_id')
                self.id_principal = data.get('id_principal')
                self.id_brand     = data.get('id_brand')
                self.id_kategori  = data.get('id_kategori')
                self.id_status    = data.get('id_status')
                self.kode_sku     = data.get('kode_sku')
                self.kode_ean     = data.get('kode_ean')
                self.nama         = data.get('nama')
                self.harga_beli   = data.get('harga_beli')
                self.keterangan   = data.get('keterangan')
        return  self

    base_query = """

            SELECT      produk           .*,
                        produk_brand     .nama  AS  brand,
                        produk_kategori  .nama  AS  kategori,
                        principal        .nama  AS  nama_principal

            FROM        produk

            LEFT JOIN   produk_brand 
                ON      produk_brand     .id            = 
                        produk           .id_brand 

            LEFT JOIN   produk_kategori 
                ON      produk_kategori  .id            = 
                        produk           .id_kategori

            LEFT JOIN   principal 
                ON      principal        .id            = 
                        produk           .id_principal

        """

    @classmethod
    def all(cls):
        return DB(request).setRawQuery(cls.base_query).execute().fetchall().get()

    @classmethod
    def all_table(cls):
        return DataTables(db).handle(
            base_query=cls.base_query,
            transformer=lambda data: (
                DictMapper(data)
                .to_dict()
                .add_col(lambda i: "", "")
                .add_col(lambda i: btn_details(i['id'], "harga"), "harga")
                .add_col(lambda i: btn_details(i['id'], "satuan"), "satuan")
                .add_col(lambda i: btn_actions(i['id']), "actions")
                .get()
            )
        )