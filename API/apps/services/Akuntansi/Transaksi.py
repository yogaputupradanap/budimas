import datetime

from flask import request
import json

from apps.handler import handle_error, handle_error_rollback, nonServerErrorException
from apps.lib.helper import date_now, datetime_now, date_for_code, date_now_stamp
from apps.lib.paginate import Paginate
from apps.models.pengeluaran_kasir import pengeluaran_kasir
from .BaseAkuntansi import BaseAkuntansi
from typing import List

from ...lib.paginateV2 import PaginateV2
from ...models import Customer, MutasiBank, AccountingEntryModel, RekeningPerusahaan, Perusahaan
from ...models.sales_detail import SalesDetail


class Transaksi(BaseAkuntansi):
    def __init__(self):
        super().__init__()

    @handle_error_rollback
    def insertTransaksi(self):
            """
            Insert a new mutasi record into the database.
            """
            token = request.headers.get('Authorization')
            if not token:
                raise nonServerErrorException(401, "Token tidak ditemukan")
            token = token.split(" ")[1] if " " in token else token

            user = (
                self.query().setRawQuery(
                    "SELECT id FROM users WHERE tokens = :token",
                )
                .bindparams({'token': token})
                .execute()
                .fetchone()
                .result
            )

            user_id = user.get('id') if user else None
            if not user_id:
                raise nonServerErrorException(401, "Token tidak valid")

            tanggal_transaksi = self.req('tanggal_transaksi')
            id_rekening_perusahaan = self.req('id_rekening_perusahaan')
            tipe_transaksi = self.req('tipe')
            keterangan = self.req('keterangan')
            nominal = self.req('nominal')

            if not tanggal_transaksi or not id_rekening_perusahaan or not tipe_transaksi or not nominal:
                raise nonServerErrorException(400, "Data transaksi tidak lengkap")

            # Query mencari rekening
            rekening_perusahaan = (
                RekeningPerusahaan.query
                .join(Perusahaan, RekeningPerusahaan.id_perusahaan == Perusahaan.id)
                .filter(
                    RekeningPerusahaan.id == id_rekening_perusahaan, 
                    RekeningPerusahaan.is_aktif == True
                )
                .first()
            )

            if not rekening_perusahaan:
                raise nonServerErrorException(404, "Rekening Perusahaan tidak ditemukan")

            # Mengambil kode perusahaan dari relationship
            kode_perusahaan = rekening_perusahaan.perusahaan.kode
            prefix_kode_transaksi = f'ACC/{kode_perusahaan}-{date_now_stamp()}'

            # PERBAIKAN INDENTASI DI SINI
            last_prefix = (
                AccountingEntryModel.query
                .filter(AccountingEntryModel.kode_transaksi.startswith(prefix_kode_transaksi))
                .with_for_update()
                .order_by(AccountingEntryModel.kode_transaksi.desc())
                .first()
            )
                
            if last_prefix:
                # Mengambil nomor urut terakhir
                parts = last_prefix.kode_transaksi.split('/')
                last_number = int(parts[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            kode_transaksi = f"{prefix_kode_transaksi}/{str(new_number).zfill(4)}"

            insert_acounting_entry = AccountingEntryModel(
                id_rekening_perusahaan = id_rekening_perusahaan,
                tanggal_transaksi = tanggal_transaksi,
                nominal = nominal,
                tipe = tipe_transaksi,
                kode_transaksi = kode_transaksi,
                keterangan = keterangan,
                id_user = user_id,
                status = 0,
                created_at = datetime_now(),
            )
            
            self.add(insert_acounting_entry).flush()
            self.commit()

            return {
                "status": "success",
                "message": "Transaksi berhasil disimpan",
                "data": {
                    "id_mutasi_acc": insert_acounting_entry.id_mutasi_acc,
                    "kode_transaksi": insert_acounting_entry.kode_transaksi,
                }
            }

    @handle_error_rollback
    def updateTransaksi(self):
        """
        Insert a new mutasi record into the database.
        """

        token = request.headers.get('Authorization')
        if not token:
            raise nonServerErrorException(401, "Token tidak ditemukan")
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

        if not user_id:
            raise nonServerErrorException(401, "Token tidak valid", )

        id_accounting_entry = self.req('id_mutasi_acc')
        # print(f"DEBUG: Mencoba update transaksi dengan ID: {id_accounting_entry}")
        tanggal_transaksi = self.req('tanggal_transaksi')
        id_rekening_perusahaan = self.req('id_rekening_perusahaan')
        tipe_transaksi = self.req('tipe')
        keterangan = self.req('keterangan')
        nominal = self.req('nominal')

        if not tanggal_transaksi or not id_rekening_perusahaan or not tipe_transaksi or not nominal:
            raise nonServerErrorException(400, "Data transaksi tidak lengkap")

        # Query mencari rekening
            rekening_perusahaan = (
                RekeningPerusahaan.query
                .join(Perusahaan, RekeningPerusahaan.id_perusahaan == Perusahaan.id)
                .filter(
                    RekeningPerusahaan.id == id_rekening_perusahaan, 
                    RekeningPerusahaan.is_aktif == True
                )
                .first()
            )

            if not rekening_perusahaan:
                raise nonServerErrorException(404, "Rekening Perusahaan tidak ditemukan")

        try:
            id_accounting_entry = int(id_accounting_entry)
        except (TypeError, ValueError):
            raise nonServerErrorException(400, "ID Transaksi tidak valid")

        # Baru kemudian jalankan query
        update_acounting_entry = (AccountingEntryModel.query
                                .with_for_update()
                                .filter(AccountingEntryModel.id == id_accounting_entry)
                                .first())

        if not update_acounting_entry:
            raise nonServerErrorException(404, "Data transaksi tidak ditemukan")

        if update_acounting_entry.status == 1:
            raise nonServerErrorException(400, "Transaksi sudah dikonfirmasi, tidak bisa diubah")

        update_acounting_entry.id_rekening_perusahaan = id_rekening_perusahaan
        update_acounting_entry.tanggal_transaksi = tanggal_transaksi
        update_acounting_entry.nominal = nominal
        update_acounting_entry.tipe = tipe_transaksi
        update_acounting_entry.keterangan = keterangan


        self.add(update_acounting_entry).flush()
        self.commit()

        return {
            "status": "success",
            "message": "Transaksi berhasil disimpan",
            "data": {
                "id_mutasi_acc": update_acounting_entry.id_mutasi_acc,
                "kode_transaksi": update_acounting_entry.kode_transaksi,
            }
        }

    @handle_error
    def getListTransaksi(self):
            adv_filter_str = self.req('advancedFilters')
            
            # Ambil filter dasar
            tanggal_transaksi = self.req('tanggal_transaksi')
            id_rekening_perusahaan = self.req('id_rekening_perusahaan')
            tipe = self.req('tipe')

            # Parsing jika dikirim dalam bentuk JSON string
            if adv_filter_str:
                try:
                    filters = json.loads(adv_filter_str)
                    tanggal_transaksi = filters.get('tanggal_transaksi', tanggal_transaksi)
                    id_rekening_perusahaan = filters.get('id_rekening_perusahaan', id_rekening_perusahaan)
                    tipe = filters.get('tipe', tipe)
                except:
                    pass

            # QUERY HARUS DI LUAR BLOK IF (Indentasi ke kiri)
            query = """
                select
                ae.tanggal_transaksi,
                ae.kode_transaksi,
                rp.nomor_rekening,
                ae.tipe tipe_transaksi,
                ae.nominal,
                ae.keterangan,
                ae.id_rekening_perusahaan,
                ae.status,
                rp.id_perusahaan,
                ae.id_mutasi_acc
                from accounting_entry ae
                JOIN rekening_perusahaan rp
                     ON ae.id_rekening_perusahaan = rp.id_rekening_perusahaan    
            """

            bindParams = {}
            
            if tanggal_transaksi:
                # Ubah string '2026-02-11' menjadi object date
                date_val = datetime.datetime.strptime(tanggal_transaksi, '%Y-%m-%d').date()
                query += " AND CAST(ae.tanggal_transaksi AS DATE) = :tanggal_transaksi"
                bindParams['tanggal_transaksi'] = date_val

            if id_rekening_perusahaan:
                query += " AND ae.id_rekening_perusahaan = :id_rekening_perusahaan"
                bindParams['id_rekening_perusahaan'] = id_rekening_perusahaan

            if tipe:
                query += " AND ae.tipe = :tipe"
                bindParams['tipe'] = tipe

            query += " ORDER BY ae.created_at DESC"

            # Kembalikan hasil paginate di luar blok if
            return PaginateV2(request=request, query=query, bindParams=bindParams).paginate()
            return {
                "result": res.get('pages', {}).get('result', []),
                "total_data": res.get('total_data', 0),
                "status": "success"
            }