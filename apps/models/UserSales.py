from apps.datatables import DataTables, DictMapper
from apps.models.BaseModel import BaseModel
from  apps.query   import  DB
from  apps.helper  import  *
from apps.conn2 import db
from  flask        import  request

from apps.widget import btn_actions


class UserSales(BaseModel) :
    
    __tablename__ = 'sales'
    
    # Kolom tabel
    id_user = BaseModel.foreign('users.id')
    id_principal = BaseModel.foreign('principal.id')
    id_wilayah1 = BaseModel.foreign('wilayah1.id')
    id_wilayah2 = BaseModel.foreign('wilayah2.id')
    id_tipe = BaseModel.foreign('sales_tipe.id')
    
    user = BaseModel.one_to_many('User',__tablename__, [id_user])
    principal = BaseModel.one_to_many('Principal', __tablename__, [id_principal])
    wilayah1 = BaseModel.one_to_many('Wilayah1',__tablename__, [id_wilayah1])
    wilayah2 = BaseModel.one_to_many('Wilayah2',__tablename__, [id_wilayah2])
    tipe = BaseModel.one_to_many('SalesTipe',__tablename__, [id_tipe])
    
    def __repr__(self) :
        return f"UserSales('{self.id}')"
    
    # def __init__(self, data=None) :
    #     self.set(data)
    
    def set(self, data=None) :
        if data :
            self.id = data.get('id')
            self.id_user = data.get('id_user')
            self.id_principal = data.get('id_principal')
            self.id_wilayah1 = data.get('id_wilayah1')
            self.id_wilayah2 = data.get('id_wilayah2')
            self.id_tipe = data.get('id_tipe')
        return self

    base_query = """
       SELECT 
    sales.id AS id_sales,
    sales.id_principal,
    sales.id_wilayah1,
    sales.id_wilayah2,
    sales.id_tipe,
    users.id,
    sales.id_user,
    users.nama,
    users.nik,
    cabang.id AS id_cabang,
    users.tanggal_lahir,
    users.alamat,
    users.telepon,
    users.email,
    users.username,
    sales_tipe.nama AS tipe,
    cabang.nama AS nama_cabang,
    COALESCE(principal.nama, '-') AS nama_principal,
    wilayah1.nama AS nama_wilayah1,
    wilayah2.nama AS nama_wilayah2,
    sales_detail.kode_sales,
    ARRAY_AGG(spa.id_principal) AS id_principals
FROM sales
LEFT JOIN users 
    ON users.id = sales.id_user
LEFT JOIN cabang 
    ON cabang.id = users.id_cabang
LEFT JOIN principal 
    ON principal.id = sales.id_principal
LEFT JOIN sales_tipe 
    ON sales_tipe.id = sales.id_tipe
LEFT JOIN wilayah1 
    ON wilayah1.id = sales.id_wilayah1
LEFT JOIN wilayah2 
    ON wilayah2.id = sales.id_wilayah2
LEFT JOIN sales_detail
    ON sales_detail.id_sales = sales.id
LEFT JOIN sales_principal_assignment spa
    ON spa.id_sales = sales.id
GROUP BY 
    sales.id, sales.id_principal, sales.id_wilayah1, sales.id_wilayah2, 
    sales.id_tipe, users.id, sales.id_user, users.nama, users.nik, 
    cabang.id, users.tanggal_lahir, users.alamat, users.telepon, 
    users.email, users.username, sales_tipe.nama, cabang.nama, 
    principal.nama, wilayah1.nama, wilayah2.nama, sales_detail.kode_sales

            
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
                .add_col(lambda i: btn_actions(i['id_sales']), "actions")
                .get()
            )
        )
    
    @classmethod
    def all_csv(cls):
        query = """
              select 
                users.nama,
                users.nik,
                users.id_cabang,
                users.tanggal_lahir,
                users.username,
                users.password,
                users.email,
                users.alamat,
                users.telepon,
                sales.id_tipe,
                sales.id_wilayah1,
                sales.id_wilayah2,
                sales_principal_assignment.id_principal 
              from sales
              join users on sales.id_user = users.id 
              join sales_principal_assignment on sales.id = sales_principal_assignment.id_sales             
              """
        result = DB(request).setRawQuery(query).execute().fetchall().get()
        return result