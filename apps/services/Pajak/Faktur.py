from flask import jsonify, request
from apps.handler import handle_error_rollback
from apps.services.BaseServices import BaseServices
from apps.models.prefix import Prefix
from datetime import datetime
import requests

class Faktur(BaseServices):
    def __init__(self):
        super().__init__()
        self.listFaktur = "https://api-pajak-189463082311.asia-southeast2.run.app/api/pajak/get-list-faktur"

    @handle_error_rollback
    def getGeneratedFaktur(self):
        try:
            ids = request.args.get('ids', '').split(',')
            ids = [int(id) for id in ids]

            response_faktur = requests.get(self.listFaktur)
            response_faktur.raise_for_status()  
            faktur_data = response_faktur.json()

            available_prefixes = self.db.session.query(Prefix)\
                .filter(Prefix.sudah_digunakan == True)\
                .order_by(Prefix.id.asc())\
                .all()

            # Gabungkan data faktur dengan data prefix berdasarkan urutan
            data = []
            faktur_dict = {faktur['id']: faktur for faktur in faktur_data['pages']}  # Index faktur berdasarkan ID

            # Memproses hanya faktur yang sesuai dengan ids yang diterima
            for faktur_id in ids:
                faktur = faktur_dict.get(faktur_id)
                if faktur:
                    # Jika masih ada data prefix yang tersedia, kita ambil berdasarkan urutan
                    if len(available_prefixes) > 0:
                        matching_prefix = available_prefixes.pop(0)  

                        # Gabungkan data faktur dengan data prefix
                        data.append({
                            'id': faktur['id'],
                            'no_faktur': faktur['no_faktur'],
                            'customer': faktur['customer'],
                            'tanggal_order': faktur['tanggal_order'],
                            'nilai_faktur': faktur['nilai_faktur'],
                            'principal': faktur['principal'],
                            'npwp': faktur['npwp'],
                            'no_faktur_pajak': matching_prefix.no_faktur_pajak, 
                            'sudah_gunakan': matching_prefix.sudah_digunakan
                           
                        })

            return jsonify({
                'success': True,
                'data': data
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500

    @handle_error_rollback
    def addFakturPajak(self):
        try:
            selected_data = request.json.get('data', [])

            available_prefixes = self.db.session.query(Prefix)\
                .filter(Prefix.sudah_digunakan == False)\
                .order_by(Prefix.id.asc())\
                .limit(len(selected_data))\
                .all()

            if len(available_prefixes) < len(selected_data):
                return jsonify({
                    'success': False,
                    'message': f'Nomor faktur pajak tidak cukup. Tersedia: {len(available_prefixes)}, Dibutuhkan: {len(selected_data)}'
                }), 400

            current_time = datetime.utcnow()

            for idx, data in enumerate(selected_data):
                if idx < len(available_prefixes):
                    prefix = available_prefixes[idx]
                    prefix.sudah_digunakan = True
                    prefix.tanggal_digunakan = current_time
                    prefix.faktur_id = data['id']

            self.db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Faktur pajak berhasil di-generate'
            })

        except Exception as e:
            self.db.session.rollback()
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
  