from apps.datatables import DataTables, DictMapper
from apps.handler import handle_error
from apps.helper import *
from apps.models import BaseModel
from apps.query import DB
from apps.widget import btn_actions, btn_details
from apps.conn2 import db
from  .  import  BaseModel

class User(BaseModel):
    __tablename__ = 'users'
    nama = BaseModel.string(40)
    email = BaseModel.string(100)
    tokens = BaseModel.string(60)
    telepon = BaseModel.string(13)
    no_rekening = BaseModel.string(25)
    npwp = BaseModel.string(25)
    nama_wp = BaseModel.string(50)
    alamat_wp = BaseModel.string(50)
    id_jabatan = BaseModel.foreign('jabatan.id')
    id_cabang = BaseModel.foreign('cabang.id')
    username = BaseModel.string(25)
    password = BaseModel.string(200)
    nik = BaseModel.string(25)
    alamat = BaseModel.string(100)
    tanggal_lahir = BaseModel.date()
    cabang = BaseModel.one_to_many('Cabang', __tablename__, [id_cabang])
    jabatan = BaseModel.one_to_many('UserJabatan', __tablename__, [id_jabatan])

    def __repr__(self):
        return f"data('{self.id}')"

    @handle_error
    def get_token_by_credential():
        """
        Get user token by checking credentials with bcrypt hashed password
        """
        import bcrypt

        id = request.args.get('id')
        uname = request.args.get('username')
        paswd = request.args.get('password')

        query = ""
        params = {}

        if id:
            params["id"] = string_sanitized(id)
            query += "id=:id" if query == "" else " AND id=:id"

        if uname:
            params["username"] = string_sanitized(uname)
            query += "username=:username" if query == "" else " AND username=:username"

        if not paswd:
            return (
                DB().setRawQuery(f"SELECT tokens FROM users WHERE {query}")
                .bindparams(params).execute()
                .fetchall().get()
            )


        db = DB()
        db.setRawQuery(f"SELECT password, tokens FROM users WHERE {query}")
        db.bindparams(params)
        db.execute()

        result = db.result.fetchone()

        if not result:
            return {'result': [], 'status': 200}

        stored_hash = result[0].encode('utf-8')
        stored_hash = stored_hash.replace(b'$2y$', b'$2b$')
        password = paswd.encode('utf-8')


        if bcrypt.checkpw(password, stored_hash):
            return (
                DB().setRawQuery(f"SELECT tokens FROM users WHERE {query}")
                .bindparams(params).execute()
                .fetchall().get()
            )
        return {'result': [], 'status': 401}



    @classmethod
    def all(cls):
        return DB(request).setRawQuery("""
                                    
                SELECT      users    .*,
                            cabang   .nama  AS  nama_cabang, 
                            jabatan  .nama  AS  nama_jabatan
                                        
                FROM        users 
                                        
                LEFT JOIN   cabang 
                    ON      cabang   .id          =  
                            users    .id_cabang
                                        
                LEFT JOIN   jabatan 
                    ON      jabatan  .id          = 
                            users    .id_jabatan

        """).execute().fetchall().get()

    @classmethod
    def all_table(cls):
        return DataTables(db).handle(
            base_query="""
                                    
                SELECT      users    .id,
                            users    .nama,
                            users    .email,
                            users    .telepon,
                            users    .no_rekening,
                            users    .npwp,
                            users    .nama_wp,
                            users    .alamat_wp,
                            users    .id_jabatan,
                            users    .id_cabang,
                            users    .username,
                            users    .nik,
                            users    .alamat,
                            users    .tanggal_lahir,
                            users    .id_perusahaan,
                            cabang   .nama  AS  nama_cabang, 
                            jabatan  .nama  AS  nama_jabatan
                                        
                FROM        users 
                                        
                LEFT JOIN   cabang 
                    ON      cabang   .id          =  
                            users    .id_cabang
                                        
                LEFT JOIN   jabatan 
                    ON      jabatan  .id          = 
                            users    .id_jabatan
                            
                WHERE NOT   jabatan  .id          in (4,6)

        """,
            transformer=lambda data: (
                DictMapper(data)
                .to_dict()
                .add_col(lambda i: "", "")
                .add_col(lambda i: btn_actions(i['id']), "actions")
                .add_col(lambda i: btn_details(i['id']), "details")
                .get()
            )
        )

    def allByIdJabatanSales():
        """
        """
        return DB(request).setRawQuery("""
                                    
       SELECT      users.*, 
                   cabang.nama  AS  nama_cabang, 
                   jabatan.nama  AS  nama_jabatan
                               
       FROM        users
                               
       LEFT JOIN   cabang
           ON      cabang.id = users.id_cabang
                               
       LEFT JOIN   jabatan
           ON      jabatan.id = users.id_jabatan
           
       LEFT JOIN   sales
           ON      sales.id_user = users.id
           
       WHERE       users.id_jabatan = 4
           AND     sales.id_user IS NULL 
           
           
        """).execute().fetchall().get()

    @classmethod
    def all_csv(cls):
        query = """
            select 
              users.nama,
              users.email,
              users.telepon,
              users.no_rekening,
              users.npwp,
              users.nama_wp,
              users.alamat_wp,
              users.id_jabatan,
              users.id_cabang,
              users.username,
              users.password,
              users.nik,
              users.alamat,
              users.tanggal_lahir
            from
            users
          """
        
        return DB().setRawQuery(query).execute().fetchall().get()