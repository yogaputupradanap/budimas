from flask import Blueprint, request
from apps.services.BaseServices import token_auth
from apps.services.SalesOrder import SalesOrder
from apps.services.Sales import  Sales

sales = Blueprint("sales", __name__, url_prefix="/api/sales/")
sales.before_request(lambda: token_auth.login_required(lambda: None)())

@sales.route("get-user/<int:id_user>")
def _1(id_user):
    return Sales().getSales(id_user)

@sales.route("get-user-info/<int:user_id>")
def _2(user_id):
    tahun = request.args.get('tahun')
    bulan = request.args.get('bulan')
    return Sales().salesInfo(user_id, tahun, bulan)

@sales.route("get-user-info-month")
def _2_5():
    user_id = request.args.get('user_id')
    tahun = request.args.get('tahun')
    bulan = request.args.get('bulan')
    
    return Sales().salesInfo(user_id, tahun, bulan)
    
@sales.route("stock-opname", methods=["POST"])
def _3():
    return SalesOrder().SalesStockOpname()

@sales.route("get-saleses")
def _4():
    return Sales().getSaleses()

@sales.route("sales-request", methods=["POST"])
def _5(): 
    return SalesOrder().SalesRequestWithDBT()

@sales.route("sales-skip-request", methods=["POST"])
def _6():
    return SalesOrder().salesSkipRequest()

@sales.route("history-order/<int:id_plafon>")
def _7(id_plafon):
    return Sales().history(id_plafon, "penjualan")

@sales.route("history-retur/<int:id_plafon>")
def _8(id_plafon):
    return Sales().history(id_plafon, "retur")

@sales.route("search-invoice")
def _9(): return SalesOrder().searchFaktur() 

@sales.route("sales-retur", methods=["POST"])
def _10(): return SalesOrder().createReturRequest()

@sales.route("check-retur", methods=["GET"])
def _10_5(): return SalesOrder().checkReturRequest()

@sales.route("skip-sales-order", methods=["POST"])
def _11(): return SalesOrder().lewatiSalesOrder()

@sales.route('get-omset')
def _12(): return Sales().getOmset()
