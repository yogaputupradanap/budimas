from apps.handler import *
from apps.helper import *
from apps.widget import *
from sqlalchemy import desc
from . import Base
from apps.models import (
    Cabang,
    CustomerTipe,
    Customer
)
from ..models.Rute import Rute


class CustomerService(Base):
    def __init__(self):
        super().__init__()

    @handle_error
    def query(self):
        return (
            self.db.session.query(
                Customer.id,
                Customer.kode,
                Customer.nama,
                Customer.alamat,
                Customer.id_cabang,
                Customer.id_rute,
                Customer.id_tipe,
                Customer.id_wilayah1,
                Customer.id_wilayah2,
                Customer.id_wilayah3,
                Customer.id_wilayah4,
                Customer.latitude,
                Customer.longitude,
                Customer.no_rekening,
                Customer.npwp,
                Customer.pic,
                Customer.telepon,
                Customer.telepon2,
                Customer.id_tipe_harga,
                CustomerTipe.nama.label('tipe'),
                Cabang.nama.label('nama_cabang'),
                Rute.nama_rute
            )
            .outerjoin(CustomerTipe, Customer.id_tipe == CustomerTipe.id)
            .outerjoin(Cabang, Customer.id_cabang == Cabang.id)
            .outerjoin(Rute, Customer.id_rute == Rute.id)
        )

    # def transform_data(self, data):
    #     """Transform data untuk response"""
    #     return (
    #         Mapper(data)
    #         .to_dict()
    #         .add_col(lambda i: "", "")
    #         .add_col(lambda i: btn_actions(i['id']), "actions")
    #         .get()
    #     )
    #
    # @handle_error
    # def get_all(self):
    #     """Method untuk datatables"""
    #     return self.get_datatables(self.query(), self.transform_data)

    @handle_error
    def get_all(self):
        """Method untuk datatables dengan transform data"""
        return self.get_datatables(
            self.query(),
            lambda data: (
                Mapper(data)
                .to_dict()
                .add_col(lambda i: "", "")
                .add_col(lambda i: btn_actions(i['id']), "actions")
                .get()
            )
        )
