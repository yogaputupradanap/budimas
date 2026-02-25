from  apps.handler import  *
from  apps.helper  import  *
from  apps.widget  import  *
from  sqlalchemy   import  desc
from  .            import  Base
from  apps.models  import  User, UserJabatan as Jabatan, Cabang


class UserService(Base) :

    def __init__(self) :
        super().__init__()


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
        
    

    
    