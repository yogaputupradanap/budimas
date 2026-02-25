from flask import Blueprint, request

from apps.services import Promo
from apps.services.BaseServices import token_auth

promo = Blueprint("promo", __name__, url_prefix="/api/promo")
promo.before_request(lambda: token_auth.login_required(lambda: None)())

@promo.route("", methods=["GET"])
def _getPromo():
    filters = request.args.to_dict()

    if filters:
        return Promo().getPromoFiltered(filters)
    else:
        return Promo().getPromo()

@promo.route("/<string:kode_promo>", methods=["GET"])
def _getPromoByKode(kode_promo): return Promo().getPromoByKode(kode_promo)

@promo.route("/dropdown-data", methods=["GET"])
def _getDropdownData(): return Promo().getDropdownData()

@promo.route("/dropdown-data-log", methods=["GET"])
def _getDropdownDataLog(): return Promo().getDropdownDataLog()

@promo.route("/dropdown-data-klaim", methods=["GET"])
def _getDropdownDataKlaim(): return Promo().getDropdownDataKlaim()

@promo.route("/generate-code", methods=["POST"])
def _generateCode(): return Promo().generateKlaimCode()

@promo.route("/list-faktur", methods=["GET"])
def _getListFaktur(): return Promo().getListFaktur()

@promo.route("/klaim-kategori", methods=["GET"])
def _getKlaimKategori(): return Promo().getKlaimKategori()

@promo.route("/ajukan-klaim", methods=["POST"])
def _ajukanDataKlaim(): return Promo().ajukanDataKlaim()

@promo.route("/ajukan-ulang-klaim", methods=["PUT"])
def _ajukanUlangKlaim(): return Promo().ajukanUlangKlaim()

@promo.route("/log-penggunaan", methods=["GET"])
def _getLogPenggunaan(): return Promo().getLogPenggunaanPromo()

@promo.route("/klaim-promo", methods=["GET"])
def _getKlaimPromo():
    filters = request.args.to_dict()
    return Promo().getKlaimPromo(filters)

@promo.route("/klaim-promo/ditolak", methods=["GET"])
def _getKlaimPromoDitolak():
    filters = request.args.to_dict()
    filters['status_klaim'] = '3'
    return Promo().getKlaimPromo(filters)

@promo.route("/klaim-promo/detail/<int:id>", methods=["GET"])
def _getKlaimPromoDetail(id):
    return Promo().getKlaimDetail(id)

@promo.route("/kasbon-klaim", methods=["GET"])
def _getKasbonKlaim():
    filters = request.args.to_dict()
    return Promo().getKasbonKlaim(filters)

@promo.route("/kasbon-klaim/ajukan", methods=["POST"])
def _ajukanKasbonKlaim():
    return Promo().ajukanKasbonKlaim()

@promo.route('/klaim-promo/update-status/<int:klaim_id>', methods=['PUT'])
def update_klaim_status(klaim_id):
    data = request.get_json() or {}
    status = data.get('status_klaim')
    return Promo().updateKlaimStatus(klaim_id, status)

@promo.route("/kasbon-klaim/<int:id_kasbon_klaim>", methods=["GET"])
def _getKasbonKlaimDetail(id_kasbon_klaim):
    return Promo().getKasbonKlaimDetail(id_kasbon_klaim)

@promo.route("/kasbon-klaim/<int:id_kasbon_klaim>/klaim", methods=["GET"])
def _getKlaimForKasbonKlaim(id_kasbon_klaim, filters=None):
    filters = request.args.to_dict()
    return Promo().getListDetailKasbonKlaim(id_kasbon_klaim, filters)

@promo.route("/kasbon-klaim/<int:id_kasbon_klaim>/konfirmasi", methods=["POST"])
def _konfirmasiKasbonKlaim(id_kasbon_klaim):
    return Promo().konfirmasiKasbonKlaim(id_kasbon_klaim)