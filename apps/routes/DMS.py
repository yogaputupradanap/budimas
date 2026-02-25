from flask import Blueprint
from apps.services.BaseServices import token_auth
from apps.services import DMS

dms = Blueprint('dms', __name__, url_prefix='/api/dms/')
dms.before_request(lambda: token_auth.login_required(lambda: None)())

@dms.route('insert-dms' , methods=['POST'])
def _1(): return DMS().insertDms()

# @dms.route("process-dms", methods=['POST'])
# def _2(): return DMS().processDms()