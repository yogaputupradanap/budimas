from flask import jsonify, request
from apps.handler import handle_error_rollback
from apps.services.BaseServices import BaseServices
from apps.models.prefix import Prefix
import requests

import concurrent.futures

class ListFaktur(BaseServices):
    def __init__(self):
        super().__init__()
        self.listFaktur = "https://api-pajak-189463082311.asia-southeast2.run.app/api/pajak/get-list-faktur"
        self.perusahaan_api = "https://api-pajak-189463082311.asia-southeast2.run.app/api/base/perusahaan"
        
    @handle_error_rollback
    def getListGeneratedFaktur(self):
        no_faktur = request.args.get('no_faktur')

        response_faktur = requests.get(self.listFaktur)
        response_faktur.raise_for_status()
        faktur_data = response_faktur.json()

        # Mendapatkan prefix yang telah digunakan dari database
        used_prefixes = Prefix.query.filter(Prefix.sudah_digunakan == True)\
            .order_by(Prefix.id.asc())\
            .all()

        # Mengubah data faktur menjadi dictionary untuk akses cepat
        faktur_dict = {str(f['id']): f for f in faktur_data['pages']}
        data = []

        # Mengolah data faktur dan prefix
        for prefix in used_prefixes:
            faktur = faktur_dict.get(str(prefix.faktur_id))
            if not faktur:
                continue

            # Menyusun item data faktur
            item = {
                'id': faktur['id'],
                'no_faktur': faktur['no_faktur'],
                'customer': faktur['customer'],
                'tanggal_order': faktur['tanggal_order'],
                'nilai_faktur': faktur['nilai_faktur'],
                'principal': faktur['principal'],
                'npwp': faktur['npwp'],
                'no_faktur_pajak': prefix.no_faktur_pajak,
                'sudah_gunakan': prefix.sudah_digunakan,
                'tanggal_digunakan': prefix.tanggal_digunakan
            }

            if no_faktur and item['no_faktur'] != no_faktur:
                continue

            data.append(item)

        return jsonify({
            'success': True,
            'data': data
        })
        
    @handle_error_rollback  
    def getDetailListGeneratedFaktur(self):
        no_faktur = request.args.get('no_faktur')

        # Menggunakan ThreadPoolExecutor untuk menjalankan panggilan API secara paralel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            faktur = executor.submit(requests.get, self.listFaktur)
            perusahaan = executor.submit(requests.get, self.perusahaan_api)
            response_faktur, response_perusahaan = faktur.result(), perusahaan.result()

        response_faktur.raise_for_status()
        faktur_data = response_faktur.json()

        response_perusahaan.raise_for_status()
        perusahaan_data = response_perusahaan.json()

        used_prefixes = Prefix.query.filter(Prefix.sudah_digunakan == True)\
            .order_by(Prefix.id.asc())\
            .all()

        perusahaan_dict = {str(p['id']): p for p in perusahaan_data}
        faktur_dict = {str(f['id']): f for f in faktur_data['pages']}
        data = []

        for prefix in used_prefixes:
            faktur = faktur_dict.get(str(prefix.faktur_id))
            if not faktur:
                continue

            perusahaan = perusahaan_dict.get(str(prefix.id_perusahaan), {})
            item = {
                'id': faktur['id'],
                'no_faktur': faktur['no_faktur'],
                'customer': faktur['customer'],
                'tanggal_order': faktur['tanggal_order'],
                'nilai_faktur': faktur['nilai_faktur'],
                'principal': faktur['principal'],
                'npwp': faktur['npwp'],
                'no_faktur_pajak': prefix.no_faktur_pajak,
                'sudah_gunakan': prefix.sudah_digunakan,
                'tanggal_digunakan': prefix.tanggal_digunakan,
                'perusahaan': perusahaan.get('nama', '')
            }

            if no_faktur and item['no_faktur'] != no_faktur:
                continue

            data.append(item)

        return jsonify({
            'success': True,
            'data': data
        })