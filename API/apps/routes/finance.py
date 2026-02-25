from flask import Blueprint, request
from apps.services.BaseServices import token_auth
from apps.services import Pembayaran

finance = Blueprint("finance", __name__, url_prefix="/api/finance/")
finance.before_request(lambda: token_auth.login_required(lambda: None)())

@finance.route("list-tagihan-jatuh-tempo/<id_plafon>")
def _1(id_plafon):
    return Pembayaran().listTagihanJatuhTempo(id_plafon)

@finance.route("list-faktur/<int:id_plafon>")
def _2(id_plafon):
    return Pembayaran().listFakturBetweenDates(id_plafon)

@finance.route("update-status-fakturs", methods=["POST"])
def _3():
    return Pembayaran().updateStatusFaktur()

@finance.route("create-payment", methods=["POST"])
def _4(): return Pembayaran().createPayment()

@finance.route("riwayat-setoran-customer")
def _5(): return Pembayaran().getRiwayatSetoranCustomer()

@finance.route("rekap-pembayaran-sales")
def _6(): return Pembayaran().getRekapPembayaranSales()

@finance.route("submit-rekap-pembayaran-sales", methods=["POST"])
def _7(): return Pembayaran().submitRekapPembayaranSales()