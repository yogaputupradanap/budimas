from apps.services.BaseServices import token_auth
from apps.lib.query import DB
from flask import  Blueprint, request
from apps.lib.paginate import Paginate

base = Blueprint('base_routes', __name__, url_prefix='/api/base/<tablename>')
base.before_request(lambda: token_auth.login_required(lambda: None)())

@base.route('', methods=['GET'])
def _1(tablename) : return DB(request).setTable(tablename).select().execute().fetchall().get()

@base.route('', methods=['POST'])
def _2(tablename) : return DB(request).setTable(tablename).insert().execute().get()

@base.route('', methods=['PUT'])
def _3(tablename) : return DB(request).setTable(tablename).update().execute().get()

@base.route('', methods=['DELETE'])
def _4(tablename) : return DB(request).setTable(tablename).delete().execute().get()

@base.route('paginate', methods=['GET'])
def _5(tablename): return Paginate(request).setTable(tablename).paginate()

@base.route('all', methods=['GET'])
def _6(tablename): return Paginate(request).setTable(tablename).getAll()