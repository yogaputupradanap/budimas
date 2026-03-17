from flask import Blueprint
from apps.services.BaseServices import token_auth
from apps.services.StockOpname import StockOpname

stock_opname = Blueprint('stock-opname', __name__, url_prefix='/api/stock-opname/')
stock_opname.before_request(lambda: token_auth.login_required(lambda: None)())

@stock_opname.route('get-produks-stock-opname' , methods=['GET'])
def _1(): return StockOpname().getProduksStockOpname()

@stock_opname.route('create-stock-opname', methods=['POST'])
def _2(): return StockOpname().createStockOpname()

@stock_opname.route('stock-opname-diterima', methods=['PUT'])
def _3(): return StockOpname().stockOpnameDiterima()

@stock_opname.route('stock-opname-ditolak', methods=['PUT'])
def _4(): return StockOpname().stockOpnameDitolak()

@stock_opname.route('stock-opname', methods=['GET'])
def _5(): return StockOpname().getAllStockOpname()

@stock_opname.route('stock-opname-eskalasi', methods=['PUT'])
def _6(): return StockOpname().stockOpnameEskalasi()

@stock_opname.route('stock-opname-eskalasi-closed', methods=['PUT'])
def _7(): return StockOpname().stockOpnameEskalasiClose()