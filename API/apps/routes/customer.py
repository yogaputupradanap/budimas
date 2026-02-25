from flask import Blueprint, request
from apps.services.BaseServices import token_auth
from apps.services.Customer import Customer
from apps.lib.paginate import Paginate

customer = Blueprint('customer', __name__, url_prefix='/api/customer/')
customer.before_request(lambda: token_auth.login_required(lambda: None)())

@customer.route('get-customer-order/<int:plafon_id>')
def _1(plafon_id): return Customer().getCustomerOrder(plafon_id, 1)

@customer.route('get-customer-order-history/<int:plafon_id>')
def _2(plafon_id): return Customer().getCustomerOrder(plafon_id, 2)

@customer.route('sisa-plafon')
def _3(): return Customer().customerSisaPlafon()

@customer.route('history-customer')
def _4(): return Customer().getHistoryCustomer()

@customer.route('list-sales-customer/<int:id_user>')
def _5(id_user): return Customer().getSalesCustomer(id_user=id_user)

@customer.route('all')
def _55():
    customer = Paginate(request).setTable('customer').paginate()
    return customer