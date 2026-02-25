from apps.conn2 import db
from apps.datatables import DataTables, DictMapper
from  apps.query   import  DB
from  apps.helper  import  *
from  flask        import  request

from apps.widget import btn_actions


class PeriodeClosed() :


    base_query = """
                                    
        SELECT     
                    periode_closed.id_periode,
                    periode_closed.tanggal_close,
            periode_closed.keterangan,
                    cabang.id AS id_cabang,            
                    cabang.nama AS nama_cabang                                        
        FROM        periode_closed
                    
        LEFT JOIN   cabang 
            ON      cabang.id = periode_closed.id_cabang                                                                
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
                .add_col(lambda i: btn_actions(i['id_periode']), "actions")
                .get()
            )
        )