from  apps.handler import  *
from  apps.helper  import  *
from  apps.widget  import  *
from  sqlalchemy   import  desc
from  .            import  Base
from  apps.models  import  User, UserJabatan as Jabatan, Cabang
from datetime import datetime
from apps.query import DB
from flask import request


class UserService(Base) :

    def __init__(self) :
        super().__init__()

    def userRequest(self, param):
        return parseJson(self.request if self.request else request).jsonType(param)

    # basic users CRUD
    def getUser(self, id_user, role, roleData):
        # 1. Ambil response lengkap
        response = (
            DB()
            .setRawQuery(
                """
                SELECT users.*, cabang.nama as nama_cabang, jabatan.nama as nama_jabatan
                FROM users 
                LEFT JOIN cabang ON cabang.id = users.id_cabang 
                LEFT JOIN jabatan ON jabatan.id = users.id_jabatan
                WHERE users.id = :id                                     
                """
            )
            .bindparams({"id": id_user})
            .execute()
            .fetchall()
            .get()
        )
        
        # 2. Ambil list dari 'result'
        data_list = response.get('result', [])
        
        # 3. Cek apakah data ditemukan
        if not data_list:
            return {"status": "error", "message": "User tidak ditemukan"}, 404
            
        user = data_list[0]
        
        # 4. Logika role mapping
        if not role and roleData: 
            return user
        
        user[role] = roleData
        return user


    @handle_error
    def token(self) :
        def fetch() :
            with self.db.session.begin() :
                return (
                    User.query.with_entities(User.tokens)
                        .filter_by(username=self.data['username'])
                        .filter_by(password=self.data['password'])
                        .first()
                )
        return  Mapper([fetch()]).to_dict().get()[0]


    @handle_error
    def detail_login(self) :
        def fetch() :
            with self.db.session.begin() :
                return (
                    User.query.with_entities(
                        User.id, User.nama, User.email,
                        User.telepon, User.no_rekening,
                        User.npwp, User.nama_wp, User.nik,
                        User.alamat, User.tanggal_lahir,
                        Cabang.id.label('cabang_id'),
                        Cabang.nama.label('cabang_nama'),
                        Jabatan.id.label('user_jabatan_id'),
                        Jabatan.nama.label('user_jabatan_nama')
                    )    
                    .outerjoin(User.cabang)
                    .outerjoin(User.jabatan)
                    .filter(User.tokens==self.data['tokens'])
                    .first()
                )
        return  Mapper([fetch()]).to_dict().get()[0]


    @handle_error
    def daftar_option(self) :
        def fetch() :
            with self.db.session.begin() :
                return (
                    User.query.with_entities(
                        User.id, User.nama, User.nik,
                        Jabatan.id.label('user_jabatan_id'),
                        Jabatan.kode.label('user_jabatan_kode')
                    )
                    .outerjoin(User.jabatan)
                    .all()
                )
        def text(i) :
            ket_1 = f"[{i['nik']}]" or ""
            ket_2 = f"[{i['user_jabatan_kode']}]" or ""
            return  f"{ket_1}{ket_2}{i['nama']}"
        return (
            Mapper(fetch()).to_dict()
                .add_col(lambda i : text(i), "text")
                .get()
        )
        

    

    
    