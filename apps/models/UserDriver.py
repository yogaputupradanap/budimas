from apps.datatables import DataTables, DictMapper
from  apps.query   import  DB
from  apps.helper  import  *
from  flask        import  request
from apps.conn2 import db

from apps.widget import btn_actions


class UserDriver() :

    base_query = """
                                   
        SELECT      driver.id as id,
                    driver.id_user as id_user,
                    driver.id_armada,
                    driver.id_wilayah1,
                    driver.id_wilayah2,
                    users.nama,
                    users.nik,
                    cabang.nama AS nama_cabang,
                    users.id_cabang,
                    users.email,
                    users.telepon,
                    users.alamat,
                    users.tanggal_lahir,
                    wilayah1.nama AS nama_wilayah1,
                    wilayah2.nama AS nama_wilayah2
  
                                   
        FROM        driver
                                   
        LEFT JOIN   users 
            ON      users     .id           = 
                    driver    .id_user
		
		LEFT JOIN   cabang 
		    ON      cabang.id = users.id_cabang
		    
		left join wilayah1 on driver.id_wilayah1 = wilayah1.id
		left join wilayah2 on driver.id_wilayah2 = wilayah2.id
                                   

                                   
        """
    
    @classmethod
    def all(cls):
        return DB(request).setRawQuery(cls.base_query).execute().fetchall().get()

    @classmethod
    def all_table(cls):
        result = DataTables(db).handle(
            base_query=cls.base_query,
            transformer=lambda data: (
                DictMapper(data)
                .to_dict()
                .add_col(lambda i: "", "")
                .add_col(lambda i: btn_actions(i['id']), "actions")
                .get()
            )
        )

        return result 