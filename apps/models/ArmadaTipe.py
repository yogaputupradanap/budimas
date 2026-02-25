from apps.conn2 import db
from apps.datatables import DataTables, DictMapper
from  apps.query   import  DB
from  apps.helper  import  *
from  flask        import  request
from  .  import  BaseModel
from apps.widget import btn_actions

class ArmadaTipe(BaseModel) :
    nama = BaseModel.string(50)

    base_query = """
                                    
        SELECT      armada_tipe.id,
        FROM        armada_tipe                      
        """

    @classmethod
    def all(cls):
        return DB(request).setRawQuery(cls.base_query).execute().fetchall().get()