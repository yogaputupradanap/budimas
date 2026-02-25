from apps.handler import handle_error
import requests
from flask import request
from apps.lib.paginate import Paginate
from apps.services.BaseServices import BaseServices

class ListNoPajak(BaseServices):
    def __init__(self):
        super().__init__()
        self.listFaktur = "https://api-pajak-189463082311.asia-southeast2.run.app/api/pajak/get-list-faktur"

    @handle_error
    def getListNoPajak(self):

        valid_columns = ['id', 'faktur_id', 'no_faktur_pajak', 'sudah_digunakan', 'tanggal_digunakan']

        query = "SELECT id, faktur_id, no_faktur_pajak, sudah_digunakan, tanggal_digunakan FROM prefix"
        result = Paginate(request, query, allowed_columns=valid_columns).paginate()

        response = requests.get(self.listFaktur)
        response.raise_for_status()
        faktur_map = {item['id']: item['no_faktur'] for item in response.json().get('pages', []) if item.get('id')}

        for item in result.get('pages', []):
            item['no_faktur'] = faktur_map.get(item.get('faktur_id'), '-')

        return result