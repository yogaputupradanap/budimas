from flask import Blueprint
from apps.services.BaseServices import token_auth
from apps.services.StockTransfer import StockTransfer

stock_transfer = Blueprint('stock-transfer', __name__, url_prefix='/api/stock-transfer/')
stock_transfer.before_request(lambda: token_auth.login_required(lambda: None)())

@stock_transfer.route('pengiriman-stock-transfer', methods=['GET'])
def _1(): return StockTransfer().getPengirimanStockTransfer()

@stock_transfer.route('add-stock-transfer', methods=['POST'])
def _2(): return StockTransfer().addStockTransfer()

@stock_transfer.route('detail-stock-transfer', methods=['GET'])
def _3(): return StockTransfer().getStockOrderDetail()

@stock_transfer.route('konfirmasi-stock-transfer', methods=["POST"])
def _4(): return StockTransfer().konfirmasiRequest()

@stock_transfer.route('konfirmasi-admin-stock-transfer', methods=["POST"])
def _konfirmasi_admin(): return StockTransfer().konfirmasiAdmin()

@stock_transfer.route('penerimaan-stock-transfer', methods=["POST"])
def _5(): return StockTransfer().penerimaanBarang()

@stock_transfer.route('close-eskalasi-penerimaan-stock-transfer', methods=["POST"])
def _5_5(): return StockTransfer().closeEskalasiPenerimaanBarang()

@stock_transfer.route('tolak-stock-transfer', methods=["POST"])
def _6(): return StockTransfer().tolakPenerimaan()