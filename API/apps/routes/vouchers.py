from flask import Blueprint
from apps.services.Vouchers import Voucher
from apps.services.BaseServices import token_auth

voucher = Blueprint("voucher", __name__, url_prefix="/api/voucher")
voucher.before_request(lambda: token_auth.login_required(lambda: None)())

@voucher.route("", methods=["GET"])
def _gettVoucher(): return Voucher().getVouchers()

@voucher.route("/<int:tipe>", methods=["POST"])
def _insertVoucher(tipe): return Voucher().insertVoucher(tipe)

@voucher.route("/<int:tipe>", methods=["PUT"])
def _updateVoucher(tipe): return Voucher().updateVoucher(tipe)

@voucher.route("/<int:tipe>", methods=["DELETE"])
def _deleteVoucher(tipe): return Voucher().deleteVoucher(tipe)

@voucher.route("/tolak-voucher", methods=["POST"])
def _decline_voucher(): return Voucher().declineProductVoucher()

@voucher.route("/tolak-voucher-regular", methods=["POST"])
def _decline_voucher_regular(): return Voucher().declineRegularVoucher()

@voucher.route("/use-voucher", methods=["POST"])
def _use_voucher(): return Voucher().useVoucher()

@voucher.route("/get-v1-regular")
def _1(): return Voucher().getVoucher_1_reguler()

@voucher.route("/get-v2-product/<int:id_produk>")
def _2(id_produk): return Voucher().getVoucher_2_produk(id_produk)

@voucher.route("/get-v2-regular")
def _2r(): return Voucher().getVoucher_2_reguler()

@voucher.route("/get-v3-product/<int:id_produk>")
def _3(id_produk): return Voucher().getVoucher_3_produk(id_produk)

@voucher.route("/get-v3-regular")
def _3r(): return Voucher().getVoucher_3_reguler()

@voucher.route("/get-voucher-by-id/<int:tipe>")
def _getVoucherById(tipe): return Voucher().getVoucherById(tipe)

@voucher.route("/get-v2-product-all")
def _get_v2_product_all(): return Voucher().getVoucher_2_produk_all()

@voucher.route("/get-v3-product-all")
def _get_v3_product_all(): return Voucher().getVoucher_3_produk_all()