from apps.conn2 import db
from apps.datatables import DataTables, DictMapper
from  apps.query   import  DB
from  apps.helper  import  *
from  flask        import  request

from apps.widget import btn_actions


class Rute(db.Model) :

    __tablename__ = 'rute'

    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(25))
    prioritas = db.Column(db.Integer)
    id_cabang = db.Column(db.Integer, db.ForeignKey('cabang.id'))
    nama_rute = db.Column(db.String(100))
    deskripsi = db.Column(db.String(255))


    base_query = """
                                    
            SELECT      rute    .id,
						rute	.kode,
						rute	.nama_rute,
						rute	.deskripsi,
						cabang.nama AS nama_cabang,
                    	rute.id_cabang

            FROM        rute
			
			LEFT JOIN   cabang 
			    ON      cabang.id = rute.id_cabang
                                    
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