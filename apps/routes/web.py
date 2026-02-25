from flask import Blueprint

from apps.handler import *
from apps.helper import *
from apps.models.BaseModel import BaseModel
from apps.models import Cabang
from apps.models.Armada import Armada
from apps.models.Budget import Budget
from apps.models.Customer import Customer
from apps.models.Fitur import Fitur
from apps.models.FiturJabatan import FiturJabatan
from apps.models.FiturUser import FiturUser
from apps.models.PeriodeClosed import PeriodeClosed
from apps.models.Plafon import Plafon
from apps.models.PlafonJadwal import PlafonJadwal
from apps.models.PlafonWeek import PlafonWeek
from apps.models.Principal import Principal
from apps.models.Produk import Produk
from apps.models.ProdukHargaJual import ProdukHargaJual
from apps.models.Rute import Rute
from apps.models.User import User
from apps.models.UserDriver import UserDriver
from apps.models.UserSales import UserSales
from apps.models.Perusahaan import Perusahaan
from apps.services.Cabang import CabangService
from apps.services.CustomerService import CustomerService
from apps.services.PlafonService import PlafonService
from apps.services.Principal import PrincipalService as PrincipalS
from apps.services.Produk import ProdukService as ProdukS
from apps.services.PurchaseOrder import PurchaseOrder
from apps.services.PurchaseTransaksi import PurchaseTransaksi
from apps.services.User import UserService as UserS
from apps.services.OperasiDataServices import OperasiDataServices

web = Blueprint('web_routes', __name__, url_prefix='/api/extra/')
web.before_request(lambda: token_auth.login_required(lambda: None)())


@web.route('getUser', methods=['GET'])
def _getUser(): return User.all()

@web.route('getUserCsv', methods=['GET'])
def _getUserCsv(): return User.all_csv()

@web.route('getUserTable', methods=['GET'])
def _getUserTable(): return User.all_table()


@web.route('getUserByIdJabatanSales', methods=['GET'])
def _allByIdJabatanSales(): return User.allByIdJabatanSales()


@web.route('getUserAksesDistinct', methods=['GET'])
def _2(): return FiturUser.get_list_by_distinct_user()


@web.route('getFiturUser', methods=['GET'])
def _3(): return FiturUser.all()


@web.route('getFiturUserTersedia', methods=['GET'])
def _4(): return Fitur.get_list_tersedia_by_user()


@web.route('getFiturJabatan', methods=['GET'])
def _5(): return FiturJabatan.all()


@web.route('getFiturJabatanTersedia', methods=['GET'])
def _6(): return Fitur.get_list_tersedia_by_jabatan()


@web.route('getArmada', methods=['GET'])
def _getArmada(): return Armada.all()

@web.route('getPeriodeClosed', methods=['GET'])
def _getPeriodeClosed(): return PeriodeClosed.all()

@web.route('getArmadaTable', methods=['GET'])
def _getArmadaTable(): return Armada.all_table()

@web.route('getPeriodeClosedTable', methods=['GET'])
def _getPeriodeClosedTable(): return PeriodeClosed.all_table()

@web.route('getCabangTable', methods=['GET'])
def _getCabangTable(): return Cabang.all_table()


@web.route('getRute', methods=['GET'])
def _getRute(): return Rute.all()

@web.route('getRuteTable', methods=['GET'])
def _getRuteTable(): return Rute.all_table()


@web.route('getProduk', methods=['GET'])
def _getProduk(): return Produk.all()

@web.route('getProdukTable', methods=['GET'])
def _getProdukTable(): return Produk.all_table()


@web.route('getProdukHarga', methods=['GET'])
def _10(): return ProdukHargaJual.all()


@web.route('getCustomerOpt', methods=['GET'])
def _111(): return Customer.allOpt()


@web.route('getCustomer', methods=['GET'])
def _11(): return Customer().all_table()


@web.route('getBudget', methods=['GET'])
def _getBudget(): return Budget.all()

@web.route('getBudgetTable', methods=['GET'])
def _getBudgetTable(): return Budget.all_table()


@web.route('getDriver', methods=['GET'])
def _getDriver(): return UserDriver.all()

@web.route('getDriverTable', methods=['GET'])
def _getDriverTable(): return UserDriver.all_table()


@web.route('getSales', methods=['GET'])
def _getSales(): return UserSales.all()

@web.route('getSalesCsv', methods=['GET'])
def _getSalesCsv(): return UserSales.all_csv()

@web.route('getSalesTable', methods=['GET'])
def _getSalesTable(): return UserSales.all_table()


@web.route('getPlafonOpt', methods=['GET'])
def _151(): return Plafon.allOpt()


@web.route('getPlafon', methods=['GET'])
def _15(): return Plafon().all_table()

@web.route('getPlafonCsv', methods=['GET'])
def _15_csv(): return Plafon().all_csv()


@web.route('getPlafonJadwal', methods=['GET'])
def _16(): return PlafonJadwal.all()


@web.route('getPrincipal', methods=['GET'])
def _getPrincipal(): return Principal.all()

@web.route('getPrincipalCsv', methods=['GET'])
def _getPrincipalCsv(): return Principal.all_csv()

@web.route('getPrincipalTable', methods=['GET'])
def _getPrincipalTable(): return Principal.all_table()


@web.route('getcurrentPlafonWeek', methods=['GET'])
def _18():
    result = PlafonWeek.get_current_week()
    return set(result) if result or empty(list(result)) else abort(HTTPException)


@web.route('create/bulk/<table>', methods=['POST'])
def _19(table): return OperasiDataServices.bulk_insert(table)


@web.route('purchase-order/gen-kode/<id>', methods=['GET'])
def _216(id): return handle_response_data(
    PurchaseOrder().kode(int(id), 0)
)

@web.route('purchase-order/gen-kode/<cabang_id>/<principal_id>', methods=['GET'])
def _216_with_principal(cabang_id, principal_id):
    return handle_response_data(
        PurchaseOrder().kode(int(cabang_id), int(principal_id))
    )
    

@web.route('purchase-order/daftar-produk/<id>', methods=['GET'])
def _211(id): return handle_response_data(
    PurchaseOrder().detail_produk(int(id))
)


@web.route('purchase-order/daftar-laporan', methods=['GET'])
def _200(): return handle_response_datatable(
    PurchaseOrder().daftar_laporan()
)


@web.route('purchase-order/daftar-konfirmasi', methods=['GET'])
def _201(): return handle_response_datatable(
    PurchaseOrder().daftar_konfirmasi()
)


@web.route('purchase-order/daftar-purchase', methods=['GET'])
def _202(): return handle_response_datatable(
    PurchaseOrder().daftar_purchase()
)


@web.route('purchase-order/detail-riwayat/<id>', methods=['GET'])
def _2066(id): return handle_response_data(
    PurchaseOrder().detail_riwayat(int(id))
)


@web.route('purchase-order/detail-purchase/<id>', methods=['GET'])
def _206(id): return handle_response_data(
    PurchaseOrder().detail_riwayat(int(id))
)


@web.route('purchase-order/detail-purchase-laporan/<id>', methods=['GET'])
def _213(id): return handle_response_data(
    PurchaseOrder().detail_riwayat_laporan(int(id))
)


@web.route('purchase-order/proses/request', methods=['POST'])
def _203(): return handle_response_data(
    PurchaseOrder().proses_request()
)

# @web.route('purchase-order/all', methods=['POST'])
# def _1032(): return handle_response_data(
#     PurchaseOrder().proses_request()
# )


@web.route('purchase-order/proses/konfirmasi', methods=['POST'])
def _204(): 
    return PurchaseOrder().proses_konfirmasi()


@web.route('purchase-order/proses/closed', methods=['POST'])
def _205(): 
    return PurchaseOrder().proses_closed()

@web.route('purchase-transaksi/daftar-laporan', methods=['GET'])
def _231(): return handle_response_datatable(
    PurchaseTransaksi().all()
)


@web.route('purchase-transaksi/proses/penerimaan-barang', methods=['POST'])
def _207(): 
    return PurchaseTransaksi().proses_penerimaan_barang()


@web.route('purchase-transaksi/daftar-konfirmasi', methods=['GET'])
def _208(): return handle_response_datatable(
    PurchaseTransaksi().daftar_konfirmasi()
)


@web.route('purchase-transaksi/detail-riwayat/<id>', methods=['GET'])
def _209(id): return handle_response_data(
    PurchaseTransaksi().detail_riwayat(int(id))
)


@web.route('purchase-transaksi/show/table/list-proses-tagihan', methods=['GET'])
def _210(): return handle_response_datatable(
    PurchaseTransaksi().daftar_tagihan()
)


@web.route('purchase-transaksi/proses/konfirmasi', methods=['POST'])
def _212(): return handle_response_data(
    PurchaseTransaksi().konfirmasi_purchase()
)


@web.route('cabang/option', methods=['GET'])
def _101(): return handle_response_data(
    CabangService().daftar_option()
)

@web.route('getCabang', methods=['GET'])
def _getCabang(): return Cabang.all()

@web.route('getPerusahaan', methods=['GET'])
def _getPerusahaan(): return Perusahaan.all()

@web.route('principal/option', methods=['GET'])
def _102(): return handle_response_data(
    PrincipalS().daftar_option()
)


@web.route('user/option', methods=['GET'])
def _103(): return handle_response_data(
    UserS().daftar_option()
)


@web.route('produk/option', methods=['GET'])
def _104(): return handle_response_data(
    ProdukS().daftar_option()
)


@web.route('produk/option/principal/<id>', methods=['GET'])
def _105(id): return handle_response_data(
    ProdukS().daftar_option_principal(int(id))
)


@web.route('user/detail-login', methods=['GET'])
def _1031(): return handle_response_data(
    UserS().detail_login()
)


@web.route('purchase-transaksi/last-batch/<order_id>', methods=['GET'])
def get_last_batch(order_id):
    return handle_response_data(
        PurchaseTransaksi().get_last_batch_number(int(order_id))
    )


@web.route('purchase-transaksi/daftar-laporan/<id>', methods=['GET'])
def _transaksi_by_order(id): return handle_response_datatable(
    PurchaseTransaksi().daftar_transaksi_by_order(int(id))
)

@web.route('meta/columns/<table>', methods=['GET'])
def list_columns_path(table):
    schema = request.args.get('schema', 'public')
    try:
        return BaseModel.get_columns_by_table(table, schema=schema)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
