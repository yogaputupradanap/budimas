from flask import Blueprint
from apps.services.BaseServices import token_auth
from apps.services import *

principal = Blueprint("principal", __name__, url_prefix="/api/principal/")
principal.before_request(lambda: token_auth.login_required(lambda: None)())

@principal.route("get-principals")
def _1():
    return PrincipalService().getPrincipals()

@principal.route("get-principal")
def _2():
    return PrincipalService().getPrincipal()