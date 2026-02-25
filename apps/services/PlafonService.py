from apps.handler import *
from apps.helper import *
from . import Base
from apps.models import Plafon, Customer, Principal, User, ProdukTipeHarga, UserSales
from apps.widget import *
from ..datatables import DataTables, DictMapper


class PlafonService(Base):
    def __init__(self):
        super().__init__()

    @handle_error
    def query(self):
        return (
            self.db.session.query(
                Plafon.id,  # id
                Plafon.id_customer,  # id_customer
                Plafon.id_principal,  # id_principal
                Plafon.id_sales,  # id_sales
                Plafon.id_tipe_harga,  # id_tipe_harga
                UserSales.id_user,  # id_user dari tabel sales
                Plafon.kode.label('kode'),  # kode
                Customer.kode.label('kode_customer'),  # kode_customer
                Plafon.limit_bon.label('limit_bon'),  # limit_bon
                Plafon.lock_order.label('lock_order'),  # lock_order
                Customer.nama.label('nama_customer'),  # nama_customer
                Principal.nama.label('nama_principal'),  # nama_principal
                User.nama.label('nama_user'),  # nama_user
                Plafon.sisa_bon.label('sisa_bon'),  # sisa_bon
                Plafon.tempo.label('tempo'),  # tempo
                Plafon.tempo_label.label('tempo_label'),  # tempo_label
                ProdukTipeHarga.nama.label('tipe_harga'),  # tipe_harga
                Plafon.top.label('top')  # top
            )
            .outerjoin(Customer, Customer.id == Plafon.id_customer)
            .outerjoin(Principal, Principal.id == Plafon.id_principal)
            .outerjoin(UserSales, UserSales.id == Plafon.id_sales)  # Join dengan sales menggunakan id_sales
            .outerjoin(User, User.id == UserSales.id_user)  # Join dengan users melalui UserSales
            .outerjoin(ProdukTipeHarga, ProdukTipeHarga.id == Plafon.id_tipe_harga)
        )

    @handle_error
    def get_all(self):
        return self.get_datatables(
            self.query(),
            lambda data: (
                Mapper(data)
                .to_dict()
                .add_col(lambda i: "", "")
                .add_col(lambda i: btn_actions(i['id']), "actions")
                .add_col(lambda i: btn_details(i['id']), "detail_jadwal")
                .get()
            )
        )
    base_query = """
                    SELECT 
                    Plafon.id,
                    Plafon.id_customer,
                    Plafon.id_principal,
                    Plafon.id_sales,
                    Plafon.id_tipe_harga,
                    UserSales.id_user,
                    Plafon.kode as kode,
                    Customer.kode as kode_customer,
                    Plafon.limit_bon as limit_bon,
                    Plafon.lock_order as lock_order,
                    Customer.nama as nama_customer,
                    Principal.nama as nama_principal,
                    User.nama as nama_user,
                    Plafon.sisa_bon as sisa_bon,
                    Plafon.tempo as tempo,
                    Plafon.tempo_label as tempo_label,
                    ProdukTipeHarga.nama as tipe_harga,
                    Plafon.top as top
                FROM Plafon
                LEFT OUTER JOIN Customer ON Customer.id = Plafon.id_customer
                LEFT OUTER JOIN Principal ON Principal.id = Plafon.id_principal  
                LEFT OUTER JOIN UserSales ON UserSales.id = Plafon.id_sales
                LEFT OUTER JOIN User ON User.id = UserSales.id_user
                LEFT OUTER JOIN ProdukTipeHarga ON ProdukTipeHarga.id = Plafon.id_tipe_harga
    """
    @classmethod
    def all_table(cls):
        return DataTables(db).handle(
            base_query=cls.base_query,
            transformer=lambda data: (
                DictMapper(data)
                .to_dict()
                .add_col(lambda i: btn_actions(i['id']), "actions")
                .add_col(lambda i: btn_details(i['id']), "detail_jadwal")
                .get()
            )
        )
