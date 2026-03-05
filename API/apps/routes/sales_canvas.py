from flask import Blueprint

from apps.services.SalesCanvas import SalesCanvas
from apps.services.CanvasPayment import CanvasPayment
from apps.services.BaseServices import token_auth

sales_canvas = Blueprint("sales-canvas", __name__, url_prefix="/api/sales-canvas")
sales_canvas.before_request(lambda: token_auth.login_required(lambda: None)())

@sales_canvas.route('/all-canvas-request', methods=["GET"])
def getAllCanvasRequest(): return SalesCanvas().getAllCanvasRequest()

@sales_canvas.route('/all-canvas-order', methods=["GET"])
def getAllCanvasOrder(): return SalesCanvas().getAllCanvasOrder()

@sales_canvas.route('/list-product-canvas', methods=["GET"])
def getListProductCanvas(): return SalesCanvas().getListProductCanvas()

@sales_canvas.route('/list-order-canvas', methods=["GET"])
def getListOrderCanvas(): return SalesCanvas().getListOrderCanvas()

@sales_canvas.route('/create-canvas-request', methods=["POST"])
def createCanvasRequest(): return SalesCanvas().createCanvasRequest()

@sales_canvas.route('/create-canvas-order', methods=["POST"])
def createCanvasOrder(): return SalesCanvas().createCanvasOrder()

@sales_canvas.route('/update-canvas-request-temp', methods=["POST"])
def updateCanvasRequestTemp(): return SalesCanvas().updateCanvasRequestTemp()

@sales_canvas.route('/detail-canvas-request', methods=["GET"])
def getDetailCanvasRequest(): return SalesCanvas().getDetailCanvasRequest()

@sales_canvas.route('/confirm-edit-canvas-request', methods=["POST"])
def confirmEditCanvasRequest(): return SalesCanvas().updateCanvasData()

@sales_canvas.route('/detail-canvas-order', methods=["GET"])
def getDetailCanvasOrder(): return SalesCanvas().getDetailCanvasOrder()

@sales_canvas.route('/tagihan-pembayaran', methods=["GET"])
def paymentHistoryList(): return CanvasPayment().paymentHistoryList()

@sales_canvas.route('/submit-tagihan-pembayaran', methods=["POST"])
def submitTagihanPembayaran(): return CanvasPayment().submitTagihanPembayaran()