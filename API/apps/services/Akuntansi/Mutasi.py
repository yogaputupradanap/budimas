import datetime

from flask import request

from apps.handler import handle_error, handle_error_rollback, nonServerErrorException
from apps.lib.helper import date_now, datetime_now, date_for_code
from apps.lib.paginate import Paginate
from apps.models.pengeluaran_kasir import pengeluaran_kasir
from .BaseAkuntansi import BaseAkuntansi
from typing import List

from ...lib.paginateV2 import PaginateV2
from ...models import Customer, MutasiBank, RekeningPerusahaan
from ...models.sales_detail import SalesDetail


class Mutasi(BaseAkuntansi):
    def __init__(self):
        super().__init__()

    @handle_error_rollback
    def insertMutasi(self):
        """
        Insert a new mutasi record into the database.
        """

        token = request.headers.get('Authorization')
        if not token:
            raise nonServerErrorException(401,"Token tidak ditemukan")
        token = token.split(" ")[1] if " " in token else token

        user = (
            self.query().setRawQuery(
                "SELECT id FROM users WHERE tokens = :token",
            )
            .bindparams({
                'token': token
            })
            .execute()
            .fetchone()
            .result
        )

        user_id = user.get('id') if user else None

        if not  user_id:
            raise nonServerErrorException(401,"Token tidak valid",)

        # 1. Ambil data dari request (Casting segera setelah ambil)
        raw_id_pers = self.req('id_perusahaan')
        raw_id_rek = self.req('id_rekening_perusahaan')
        data_mutasi = self.req('data_mutasi')

        if not all([raw_id_pers, raw_id_rek, data_mutasi]):
            raise nonServerErrorException(400, "Data tidak lengkap")

        id_perusahaan = int(raw_id_pers)
        id_rekening_perusahaan = int(raw_id_rek)

        # 2. Query Rekening (Gunakan .id karena sudah dimapping di model sebelumnya)
        rekening_perusahaan = RekeningPerusahaan.query.filter(
            RekeningPerusahaan.id == id_rekening_perusahaan,
            RekeningPerusahaan.id_perusahaan == id_perusahaan,
            RekeningPerusahaan.is_aktif == True
        ).first()

        if not rekening_perusahaan:
            raise nonServerErrorException(404, "Rekening aktif tidak ditemukan")

        # 3. Looping Mutasi
        for item in data_mutasi:
            tipe_str = str(item.get('tipe', '')).lower()
            if tipe_str not in ['cr', 'db']: continue

            # Generate nomor urut otomatis
            kode_prefix = f"{tipe_str.upper()}/{date_for_code()}"
            
            # Query ini sekarang AMAN karena MutasiBank.id sudah terhubung ke id_mutasi
            last_mutasi = MutasiBank.query.filter(MutasiBank.kode_mutasi.startswith(kode_prefix))\
                            .order_by(MutasiBank.kode_mutasi.desc())\
                            .with_for_update().first()
            
            next_num = (int(last_mutasi.kode_mutasi.split('/')[-1]) + 1) if last_mutasi else 1
            kode_mutasi = f"{kode_prefix}/{next_num:04d}"

            # Simpan Record Baru
            new_record = MutasiBank(
                id_rekening_perusahaan=rekening_perusahaan.id, # Gunakan .id hasil mapping
                tanggal_mutasi=datetime.datetime.strptime(item.get('tanggal'), '%d/%m/%Y').date(),
                nominal_mutasi=item.get('jumlah', 0),
                tipe=(1 if tipe_str == 'cr' else 2),
                keterangan=item.get('keterangan', ''),
                tanggal_upload=datetime_now(),
                saldo_akhir=item.get('saldo', 0),
                id_user=user_id,
                kode_mutasi=kode_mutasi,
                sisa=item.get('jumlah', 0),
                status_mutasi=1
            )
            self.db.session.add(new_record)

        self.db.session.commit()
        print(f"DEBUG: Berhasil insert {len(data_mutasi)} data ke mutasi_bank.")
        
        return {"status": "success", "message": "Mutasi berhasil disimpan"}

    @handle_error
    def getListKonfirmasiSetoranNonTunai(self):
        """
        Get a list of confirmed non-cash deposits.
        """

        periode_awal = self.req('periode_awal')
        periode_akhir = self.req('periode_akhir')
        status_mutasi = self.req('status_mutasi')
        if not status_mutasi:
            status_mutasi = 1
        bindParams = {}

        query = """
            select
                mb.tanggal_mutasi, mb.nominal_mutasi, mb.kode_mutasi, mb.id_mutasi, mb.sisa, mb.keterangan
            from mutasi_bank mb
                
            """

        if periode_awal and periode_akhir:
            # 2025-08-01
            start_date = datetime.datetime.strptime(periode_awal, '%Y-%m-%d').date()
            end_date =  datetime.datetime.strptime(periode_akhir, '%Y-%m-%d').date()

            query += f"where mb.tanggal_mutasi between :start_date and :end_date "

            bindParams['start_date'] = start_date
            bindParams['end_date'] = end_date

        if not periode_awal or not periode_akhir:
            if int(status_mutasi) == 2:
                query += "where mb.tipe = :tipe "
                bindParams['tipe'] = 2  # Debit
                pass
            else:
                query += "where mb.status_mutasi = :status_mutasi "
                bindParams['status_mutasi'] = status_mutasi
                query += "and mb.tipe = :tipe "
                bindParams['tipe'] = 2  # Debit
        else:
            if int(status_mutasi) == 2:
                query += "and mb.tipe = :tipe "
                bindParams['tipe'] = 2  # Debit
                pass
            else:
                query += "and mb.status_mutasi = :status_mutasi "
                bindParams['status_mutasi'] = status_mutasi
                query += "and mb.tipe = :tipe "
                bindParams['tipe'] = 2  # Debit


        return PaginateV2(request=request,query=query, bindParams=bindParams).paginate()


    @handle_error
    def getDetailKonfirmasiSetoranNonTunai(self, id_mutasi):
        """
        Get details of a confirmed non-cash deposit.
        """


        if not id_mutasi:
            raise nonServerErrorException(400, "ID mutasi tidak ditemukan")

        mutasi = (
            self.query().setRawQuery(
                """
                SELECT mb.id_mutasi, mb.kode_mutasi, mb.tanggal_mutasi, mb.nominal_mutasi,
                    mb.sisa,
                       mb.id_user, u.nama
                FROM mutasi_bank mb
                         JOIN users u ON mb.id_user = u.id
                WHERE mb.id_mutasi = :id_mutasi
                """,
            )
            .bindparams(
                {
                    'id_mutasi': id_mutasi
                }
            )
            .execute()
            .fetchone()
            .result
        )

        if not mutasi:
            raise nonServerErrorException(404, "Mutasi tidak ditemukan")

        return {
            "status": "success",
            "data": mutasi
        }

