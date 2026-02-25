from  flask       import  request
from  apps.conn2  import  db
from apps.datatables import DataTables, DictMapper
from  apps.helper  import  *
from  apps.query  import  DB
from apps.widget import btn_actions
from  .  import  BaseModel

class Principal(BaseModel) :

    __tablename__ = 'principal'

    # id            = db.Column(db.Integer, primary_key=True)
    # nama          = db.Column(db.String(50))
    # alamat        = db.Column(db.String(100))
    # telepon       = db.Column(db.String(15))
    # npwp          = db.Column(db.String(25))
    # no_rekening   = db.Column(db.String(20))
    # pic           = db.Column(db.String(50))
    # id_perusahaan = db.Column(db.Integer)
    # id_wilayah1   = db.Column(db.Integer)
    # id_wilayah2   = db.Column(db.Integer)
    # id_wilayah3   = db.Column(db.Integer)
    # id_wilayah4   = db.Column(db.Integer)
    # kode          = db.Column(db.String(100))

    nama        = BaseModel.string(50)
    alamat      = BaseModel.string(100)
    telepon     = BaseModel.string(15)
    npwp        = BaseModel.string(25)
    no_rekening = BaseModel.string(20)
    pic         = BaseModel.string(50)
    id_perusahaan = BaseModel.foreign('perusahaan.id')
    id_wilayah1 = BaseModel.integer()
    id_wilayah2 = BaseModel.integer()
    id_wilayah3 = BaseModel.bigInteger()
    id_wilayah4 = BaseModel.bigInteger()
    kode        = BaseModel.string(100)

    def __repr__(self) :
        return f"data('{self.id}')"

    base_query = """
                                        
            SELECT      principal   .*,
                        perusahaan  .nama  AS  nama_perusahaan
                                    
            FROM        principal
            
            LEFT JOIN   perusahaan 
                ON      perusahaan  .id             = 
                        principal   .id_perusahaan
                                    
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