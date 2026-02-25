from apps.datatables import DictMapper, DataTables
from  apps.query   import  DB
from  apps.helper  import  *
from apps.conn2 import db
from  flask        import  request

from apps.widget import btn_actions, btn_details


class Budget():

    base_query = """
            SELECT  budget.*,
                    departemen.nama AS nama_departemen,
                    principal.nama AS nama_principal
            FROM    budget
            LEFT JOIN departemen ON departemen.id = budget.id_departemen
            LEFT JOIN principal ON principal.id = budget.id_principal
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
                .add_col(lambda i: btn_actions(i['id']), "actions")
                .get()
            )
        )