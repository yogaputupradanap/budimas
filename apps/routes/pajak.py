from flask import Blueprint
from apps.services.BaseServices import token_auth
from apps.services.Pajak import *
# from apps.services.Pajak.DraftFakturPajak import *
from apps.services.BaseServices import token_auth

pajak = Blueprint('pajak', __name__, url_prefix='/api/pajak/')
pajak.before_request(lambda: token_auth.login_required(lambda: None)())
# pajak.before_request(lambda: token_auth.login_required(lambda: None)())

@pajak.route('get-draf-list-faktur', methods=['GET'])
def _get_pajak(): return DraftFakturPajak().GetDraftListFaktur()

@pajak.route('get-final-list-faktur', methods=['GET'])
def _get_final_pajak(): return FinalFakturPajak().GetFinalListFaktur()

@pajak.route('get-detail-draf-faktur/<id>', methods=['GET'])
def _get_detail_draf_faktur(id): return DraftFakturPajak().GetDraftDetailFaktur(id)

@pajak.route('export-xml-draf-pajak', methods=['GET'])
def _export_xml_draft_pajak(): return DraftFakturPajak().ExportPajakXml()

@pajak.route('get-faktur-by-file', methods=['GET'])
def _get_faktur_by_file(): return FinalFakturPajak().GetFakturByFile()

@pajak.route('add-data-to-pajak', methods=['POST'])
def _add_data_to_pajak(): return FinalFakturPajak().AddDataToPajak()