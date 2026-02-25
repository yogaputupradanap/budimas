from flask import Blueprint, request
from apps.services.BaseServices import token_auth
from apps.services.Produk import ProdukService

produk = Blueprint('produk', __name__, url_prefix='/api/produk/')
produk.before_request(lambda: token_auth.login_required(lambda: None)())

@produk.route('get-plafon-produks')
def _1(): return Produk().getPlafonProduks()

@produk.route("get-produk", methods=['GET'])
def _2():
    id_produk = int(request.args.get("id_produk"))
    return ProdukService().fetch_detail_transaksi(id_produk)

@produk.route("stok-ready")
def _3(): return Produk().getStokReady()