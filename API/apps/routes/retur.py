from flask import Blueprint, request
from apps.services.BaseServices import token_auth
from apps.services.Retur import  Retur

retur = Blueprint("retur", __name__, url_prefix="/api/retur/")
retur.before_request(lambda: token_auth.login_required(lambda: None)())

@retur.route("get-list-pengajuan", methods=["GET"])
def _1(): return Retur().get_list_pengajuan()

@retur.route("get-detail-retur/<string:id_request>", methods=["GET"])
def _2(id_request):
    return Retur().get_retur_detail(id_request)

@retur.route("cetak-kpr/<string:id_request>", methods=["PATCH"])
def _3(id_request):
    return Retur().cetak_kpr(id_request)

@retur.route("retur", methods=["GET"])
def _4():
    """
    Endpoint to get list of retur requests.
    """
    return Retur().get_retur_list()

@retur.route("insert-retur-stock/<string:id_request>", methods=["POST"])
def _5(id_request):
    """
    Endpoint to insert retur stock.
    """
    return Retur().insert_retur_stock(id_request)