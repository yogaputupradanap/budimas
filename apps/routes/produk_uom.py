from flask import Blueprint
from apps.services.BaseServices import token_auth
from apps.services import ProdukUOM

produk_uom = Blueprint('produk-uom', __name__, url_prefix='/api/produk-uom/')
produk_uom.before_request(lambda: token_auth.login_required(lambda: None)())

@produk_uom.route('get-uoms', methods=['POST'])
def _1(): return ProdukUOM().getUoms()