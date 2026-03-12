from flask import Blueprint
from apps.services.BaseServices import token_auth
from apps.services.Akuntasi import *

akuntasi = Blueprint('akuntasi', __name__, url_prefix='/api/akuntasi/')
# akuntasi.before_request(lambda: token_auth.login_required(lambda: None)())``

# routes for jurnal 
@akuntasi.route('get-jurnal', methods=['GET'])
def _getJurnal(): 
    return Jurnal().getJurnal()

@akuntasi.route('detail-jurnal/<id_jurnal>', methods=['GET'])
def _detailJurnal(id_jurnal):
    return Jurnal().detailJurnal(id_jurnal)

# routes for hutang
@akuntasi.route('get-hutang', methods=['GET'])
def _getHutang(): return Hutang().getHutang()

@akuntasi.route('get-tagihan-purchase', methods=['GET'])
def _getAddTagihan(): return Hutang().getAddTagihan()

@akuntasi.route('create-tagihan-purchase', methods=['POST'])
def _createTagihanPurchase(): return Hutang().createTagihanPurchase()

@akuntasi.route('detail-tagihan-purchase', methods=['GET'])
def _detailtagihanPurchase(): return Hutang().detailTagihanPurchasing()

@akuntasi.route('create-pembayaran-tagihan', methods=['POST'])
def _createPembayaranTagihan(): return Hutang().updatePembayaranTagihan()

# get list setoran tunai tipe setoran : 1 (tunai), 2 (non tunai)
@akuntasi.route('list-setoran-tunai', methods=['GET'])
def _listSetoran(): return Setoran().getListSetoran(1)

@akuntasi.route('list-setoran-non-tunai', methods=['GET'])
def _listSetoranNonTunai(): return Setoran().getListSetoran(2)

@akuntasi.route('detail-setoran', methods=['GET'])
def _detailSetoran(): return Setoran().getDetailListSetoran()

@akuntasi.route('konfirmasi-setoran', methods=['POST'])
def _konfirmasiSetoran(): return Setoran().konfirmasiSetoran()

@akuntasi.route('add-biaya-lain', methods=['POST'])
def _addBiayaLain(): return Setoran().addBiayaLainnya()