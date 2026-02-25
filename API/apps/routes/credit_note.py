from flask import Blueprint

from apps.services import CreditNoteService
from apps.services.BaseServices import token_auth



credit_note = Blueprint('credit-note', __name__, url_prefix='/api/credit-note/')
credit_note.before_request(lambda: token_auth.login_required(lambda: None)())

@credit_note.route('get-list-credit-note', methods=['GET'])
def _getListCreditNote():
    return CreditNoteService().getCreditNoteList()

@credit_note.route('use-credit-note', methods=['POST'])
def _useCreditNote():
    return CreditNoteService().useCreditNote()