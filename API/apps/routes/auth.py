from flask import Blueprint

from apps.models.User import User
from apps.services.User import UserService as UserS
from apps.services.Vouchers import Voucher
from apps.services.Akuntansi import Auth as loginakuntansi
from apps.services.Distribusi import Distribusi
from apps.services.StockTransfer import StockTransfer
from apps.services.DMS import DMS
from apps.services.Pajak import Auth as loginpajak
from apps.services.Sales import Sales
# from apps.services.Akuntansi import BaseAkuntasi



auth = Blueprint('auth', __name__)


@auth.route('/api/extra/getUserToken', methods=['GET'])
def _1(): return User.get_token_by_credential()


@auth.route('/api/auth/token', methods=['POST'])
def _1031(): return UserS().token()

@auth.route('/api/auth/sales/login', methods=["POST"])
def _11(): 
    print("LOGIN ROUTE HIT")
    return Sales().get_token_by_credential()

@auth.route('/api/auth/distribusi/login', methods=["POST"])
def _21(): 
    # print("LOGIN ROUTE HIT")
    return Distribusi().get_distribusi_info()

@auth.route('/api/auth/stock-transfer/login', methods=["POST"])
def _31(): return StockTransfer().get_stock_transfer_info()

@auth.route('/api/auth/master-voucher/login', methods=["POST"])
def _41(): return Voucher().getMasterVoucherUser()

@auth.route('/klaim-promo/login', methods=["POST"])
def _51(): return Promo().getPromoUser()

@auth.route('/api/auth/dms/login', methods=["POST"])
def _701(): return Auth().login()

@auth.route('/api/auth/login', methods=["POST"])
def _700(): return loginakuntansi().login()

@auth.route('/api/auth/pajak-login', methods=["POST"])
def _702():   
    return loginpajak().login()