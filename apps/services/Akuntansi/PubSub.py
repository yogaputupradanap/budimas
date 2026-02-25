from apps.models import JurnalModel, JurnalDetailModel
from .BaseAkuntansi import BaseAkuntansi
from ...handler import handle_error_rollback
from ...lib.helper import date_for_code, date_now
from sqlalchemy import text
import time
import traceback
import json


class PubSubService(BaseAkuntansi):
    def __init__(self):
        super().__init__()

    def __get_journal_map(self, id_fitur_mal, id_perusahaan, id_principal=None):
        # Pastikan id_principal benar-benar integer atau None
        try:
            param_principal = int(id_principal) if id_principal else None
        except (ValueError, TypeError):
            param_principal = None
        
        query = """
                SELECT jm.id_jurnal_mal,
                       jmd.type,
                       jmd.id_mal_detail,
                       jmd.urutan,
                       c.nama_akun,
                       sm.nama_tabel,
                       sm.nama_kolom_db,
                       sm.id_source_data,
                       CASE
                           WHEN c.principal_id IS NULL THEN 'non_principal'
                           WHEN c.principal_id = CAST(:id_principal AS INTEGER) THEN 'principal_match'
                           ELSE 'other'
                           END AS coa_category
                FROM jurnal_mal jm
                         JOIN jurnal_mal_detail jmd
                              ON jm.id_jurnal_mal = jmd.id_jurnal_mal
                         JOIN coa c
                              ON jmd.id_coa = c.id_coa
                         JOIN source_modul sm
                              ON jmd.id_source_data = sm.id_source_data
                WHERE jm.id_fitur_mal = :id_fitur_mal
                  AND jm.id_perusahaan = :id_perusahaan
                  AND jm.is_deleted = false
                  AND jmd.is_deleted = false
                  AND (
                    c.principal_id IS NULL 
                    OR CAST(:id_principal AS INTEGER) IS NULL 
                    OR c.principal_id = CAST(:id_principal AS INTEGER)
                  )
                ORDER BY jmd.urutan ASC
                """

        result = self.query().setRawQuery(query).bindparams(
            {
                "id_fitur_mal": id_fitur_mal,
                "id_perusahaan": id_perusahaan,
                "id_principal": param_principal,
            }
        ).execute().fetchall().get()
        
        return result

    @handle_error_rollback
    def handle_konfirmasi_purchase(self, data):
        id_fitur_mal = 1
        print(f"DEBUG: Data masuk ke Handler: {data}")
        
        # Ambil ID yang benar dari payload (di log Anda kuncinya 'id_order')
        id_transaksi = data.get('id_transaksi') or data.get('id_order')
        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        created_by = data.get('created_by')
        id_principal = data.get('id_principal')

        if not id_transaksi:
            print("ERROR: ID Transaksi/Order tidak ditemukan dalam payload")
            return {"status": "failed", "message": "ID Missing"}

        mapping_response = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)
        
        # PERBAIKAN: Ambil isi ['result'] dari dictionary tersebut
        journal_mals = mapping_response.get('result', [])

        print(f"DEBUG: Journal Mals List: {journal_mals}") # Sekarang ini akan berisi List of Dicts
        
        data_for_journal = []

        # Sekarang loop ini akan berjalan dengan benar
        for journal_mal in journal_mals:
            # Karena journal_mals sekarang adalah List, journal_mal otomatis menjadi Dictionary
            if not isinstance(journal_mal, dict):
                 continue
                 
            target_amount = 0

            # LOGIKA IF HARUS DI DALAM FOR (INDENT KE DALAM)
            if journal_mal.get('id_source_data') == 2:
                target_amount = self.__get_amount_purchase_transaksi_ppn(id_transaksi)
            else:
                nama_kolom = (journal_mal.get('nama_kolom_db') or 'total').lower()
                nama_tabel = (journal_mal.get('nama_tabel') or 'purchase_transaksi').lower()
                
                # Eksekusi Query
                exec_query = self.query().setRawQuery(f"SELECT {nama_kolom} FROM {nama_tabel} WHERE id = :id") \
                                 .bindparams({"id": id_transaksi}).execute().fetchone()

                if exec_query and exec_query.result:
                    raw_res = exec_query.result
                    # Cek apakah hasil query berupa dictionary atau nilai langsung
                    if isinstance(raw_res, dict):
                        target_amount = raw_res.get(nama_kolom, 0)
                    else:
                        target_amount = raw_res
                else:
                    target_amount = 0

            # Konversi aman ke float
            try:
                final_amount = float(target_amount) if target_amount else 0.0
            except:
                final_amount = 0.0

            # Append ke list jurnal
            data_for_journal.append({
                "type": 'debit' if journal_mal.get('type') == 1 else 'kredit',
                "urutan": journal_mal.get('urutan'),
                "nama_akun": journal_mal.get('nama_akun'),
                "amount": final_amount,
                "id_jurnal_mal": journal_mal.get('id_jurnal_mal'),
                "id_jurnal_mal_detail": journal_mal.get('id_mal_detail'),
            })
        # AKHIR LOOPING

        # Proses Insert Jurnal (Di luar looping for)
        if data_for_journal:
            mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)
            self.__insert_to_jurnal(
                mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, 
                id_perusahaan=id_perusahaan,
                id_cabang=id_cabang, 
                keterangan=f"Konfirmasi Purchase ID: {id_transaksi}", 
                created_by=created_by
            )
            self.commit()
            return {"status": "success"}
        
        return {"status": "failed", "message": "No data for journal"}

    @handle_error_rollback
    def handle_konfirmasi_tagihan(self, data):
        id_fitur_mal = 2  # contoh id_fitur_mal untuk konfirmasi tagihan
        print("Received data for konfirmasi tagihan:", data)
        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_tagihan = data.get('id_tagihan')
        id_principal = data.get('id_principal')
        created_by = data.get('created_by')

        print(f"Processing tagihan_id: {id_tagihan}")
        journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)

        data_for_journal = []

        for journal_mal in journal_mals:
            id_jurnal_mal = journal_mal['id_jurnal_mal']
            type = journal_mal['type']
            urutan = journal_mal['urutan']
            nama_akun = journal_mal['nama_akun']
            id_source_data = journal_mal['id_source_data']
            nama_tabel = journal_mal['nama_tabel']
            nama_kolom_db = journal_mal['nama_kolom_db']

            data = self.query().setRawQuery(f"""    
                SELECT {nama_kolom_db.lower()} FROM {nama_tabel.lower()}
                    WHERE id = :id
                """).bindparams({
                "id": id_tagihan
            }).execute().fetchone().result
            amount = data.get(nama_kolom_db, 0)
            print(
                f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
            data_for_journal.append({
                "type": type == 1 and 'debit' or 'kredit',
                "urutan": urutan,
                "nama_akun": nama_akun,
                "amount": amount,
                "id_jurnal_mal": id_jurnal_mal,
                "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
            })

        mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

        self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                id_cabang=id_cabang, keterangan=id_tagihan, created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    @handle_error_rollback
    def handle_picking(self, data):
        id_fitur_mal = 3  # contoh id_fitur_mal untuk konfirmasi tagihan
        print("Received data for picking:", data)
        list_faktur = data.get('data', {})
        created_by = data.get('created_by')

        print(f"Processing faktur: {list_faktur}")
        for id_faktur, data_faktur in list_faktur.items():

            id_perusahaan = data_faktur.get('id_perusahaan')
            id_cabang = data_faktur.get('id_cabang')
            id_principal = data_faktur.get('id_principal')

            journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)

            id_order_batch = data_faktur.get('id_order_batch')
            id_sales_order = data_faktur.get('id_sales_order')

            by_order_batch = id_order_batch is not None

            data_for_journal = []

            for journal_mal in journal_mals:
                id_jurnal_mal = journal_mal['id_jurnal_mal']
                type = journal_mal['type']
                urutan = journal_mal['urutan']
                nama_akun = journal_mal['nama_akun']
                id_source_data = journal_mal['id_source_data']
                nama_tabel = journal_mal['nama_tabel']
                nama_kolom_db = journal_mal['nama_kolom_db']

                if by_order_batch:
                    amount = self.__get_amount_process_picking_by_order_batch(id_order_batch)
                else:
                    amount = self.__get_amount_process_picking_by_sales_order(id_sales_order)

                print(
                    f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
                data_for_journal.append({
                    "type": type == 1 and 'debit' or 'kredit',
                    "urutan": urutan,
                    "nama_akun": nama_akun,
                    "amount": amount,
                    "id_jurnal_mal": id_jurnal_mal,
                    "keterangan": f"id_order_batch:{id_order_batch}" if by_order_batch else f"id_sales_order:{id_sales_order}",
                    "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
                })

            mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

            self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                    id_cabang=id_cabang,
                                    keterangan=None,
                                    created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    @handle_error_rollback
    def handle_shipping(self, data):
        id_fitur_mal = 4  # contoh id_fitur_mal untuk konfirmasi tagihan
        print("Received data for shipping:", data)
        list_faktur = data.get('data', {})
        created_by = data.get('created_by')

        print(f"Processing faktur: {list_faktur}")
        for id_faktur, data_faktur in list_faktur.items():

            id_perusahaan = data_faktur.get('id_perusahaan')
            id_cabang = data_faktur.get('id_cabang')
            id_principal = data_faktur.get('id_principal')

            journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)

            id_order_batch = data_faktur.get('id_order_batch')
            id_sales_order = data_faktur.get('id_sales_order')

            by_order_batch = id_order_batch is not None

            data_for_journal = []

            for journal_mal in journal_mals:
                id_jurnal_mal = journal_mal['id_jurnal_mal']
                type = journal_mal['type']
                urutan = journal_mal['urutan']
                nama_akun = journal_mal['nama_akun']
                id_source_data = journal_mal['id_source_data']
                nama_tabel = journal_mal['nama_tabel']
                nama_kolom_db = journal_mal['nama_kolom_db']

                if id_source_data in [7, 8]:
                    if by_order_batch:
                        amount = self.__get_amount_process_picking_by_order_batch(id_order_batch)
                    else:
                        amount = self.__get_amount_process_picking_by_sales_order(id_sales_order)
                else:
                    if by_order_batch:
                        data = self.query().setRawQuery(f"""
                        SELECT {nama_kolom_db} FROM {nama_tabel}
                            WHERE id_order_batch = :id_order_batch
                        """).bindparams({"id_order_batch": id_order_batch}).execute().fetchone().result
                    else:
                        data = self.query().setRawQuery(f"""
                        SELECT {nama_kolom_db} FROM {nama_tabel}
                            WHERE id_sales_order = :id_sales_order
                        """).bindparams({"id_sales_order": id_sales_order}).execute().fetchone().result
                    amount = data.get(nama_kolom_db, 0)

                print(
                    f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
                data_for_journal.append({
                    "type": type == 1 and 'debit' or 'kredit',
                    "urutan": urutan,
                    "nama_akun": nama_akun,
                    "amount": amount,
                    "id_jurnal_mal": id_jurnal_mal,
                    "keterangan": f"id_order_batch:{id_order_batch}" if by_order_batch else f"id_sales_order:{id_sales_order}",
                    "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
                })

            mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

            self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                    id_cabang=id_cabang,
                                    keterangan=None,
                                    created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    @handle_error_rollback
    def handle_realisasi(self, data):
        id_fitur_mal = 5  # contoh id_fitur_mal untuk konfirmasi tagihan
        print("Received data for realisasi:", data)
        created_by = data.get('created_by')

        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_principal = data.get('id_principal')
        id_order_batch = data.get('id_order_batch')
        id_sales_order = data.get('id_sales_order')

        journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)

        data_for_journal = []

        by_order_batch = id_order_batch is not None

        for journal_mal in journal_mals:
            id_jurnal_mal = journal_mal['id_jurnal_mal']
            type = journal_mal['type']
            urutan = journal_mal['urutan']
            nama_akun = journal_mal['nama_akun']
            id_source_data = journal_mal['id_source_data']
            nama_tabel = journal_mal['nama_tabel']
            nama_kolom_db = journal_mal['nama_kolom_db']

            if by_order_batch:
                data = self.query().setRawQuery(f"""    
                                SELECT {nama_kolom_db.lower()} FROM {nama_tabel.lower()}
                                    WHERE id_order_batch = :id_order_batch
                                """).bindparams({
                    "id_order_batch": id_order_batch
                }).execute().fetchone().result
            else:
                data = self.query().setRawQuery(f"""    
                                SELECT {nama_kolom_db.lower()} FROM {nama_tabel.lower()}
                                    WHERE id_sales_order = :id_sales_order
                                """).bindparams({
                    "id_sales_order": id_sales_order
                }).execute().fetchone().result

            amount = data.get(nama_kolom_db, 0)

            print(
                f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
            data_for_journal.append({
                "type": type == 1 and 'debit' or 'kredit',
                "urutan": urutan,
                "nama_akun": nama_akun,
                "amount": amount,
                "id_jurnal_mal": id_jurnal_mal,
                "keterangan": f"id_order_batch:{id_order_batch}" if by_order_batch else f"id_sales_order:{id_sales_order}",
                "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
            })

        mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

        self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                id_cabang=id_cabang, keterangan=None,
                                created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    def handle_piutang_non_tunai(self, data):
        id_fitur_mal = 6  # contoh id_fitur_mal untuk konfirmasi tagihan
        print("Received data for piutang non tunai:", data)
        created_by = data.get('created_by')

        data_setorans = data.get('data', {})

        for id_setoran, data_setoran in data_setorans.items():

            id_cabang = data_setoran.get('id_cabang')
            id_perusahaan = data_setoran.get('id_perusahaan')
            id_principal = data_setoran.get('id_principal')

            journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)
            id_faktur = data_setoran.get('id_faktur')

            data_for_journal = []

            for journal_mal in journal_mals:
                id_jurnal_mal = journal_mal['id_jurnal_mal']
                type = journal_mal['type']
                urutan = journal_mal['urutan']
                nama_akun = journal_mal['nama_akun']
                id_source_data = journal_mal['id_source_data']
                nama_tabel = journal_mal['nama_tabel']
                nama_kolom_db = journal_mal['nama_kolom_db']

                if id_source_data == 13:
                    data = self.query().setRawQuery(f"""
                        SELECT {nama_kolom_db} FROM  {nama_tabel.lower()}
                        WHERE id = :id 
                    """).bindparams({"id": id_faktur}).execute().fetchone().result
                else:
                    data = self.query().setRawQuery(f"""
                        SELECT {nama_kolom_db} FROM  {nama_tabel.lower()}
                        WHERE id = :id_setoran
                    """).bindparams({"id_setoran": id_setoran}).execute().fetchone().result

                amount = data.get(nama_kolom_db, 0)

                print(
                    f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
                data_for_journal.append({
                    "type": type == 1 and 'debit' or 'kredit',
                    "urutan": urutan,
                    "nama_akun": nama_akun,
                    "amount": amount,
                    "id_jurnal_mal": id_jurnal_mal,
                    "keterangan": f"id_setoran:{id_setoran};id_faktur:{data_setoran.get('id_faktur')}",
                    "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
                })

            mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

            self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                    id_cabang=id_cabang, keterangan=None,
                                    created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    @handle_error_rollback
    def handle_terima_stock_opname(self, data):
        id_fitur_mal = 7
        print("Received data for stock opname:", data)
        created_by = data.get('created_by')

        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_principal = data.get('id_principal')
        id_stock_opname = data.get('id_stock_opname')

        journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)

        data_for_journal = []

        for journal_mal in journal_mals:
            id_jurnal_mal = journal_mal['id_jurnal_mal']
            type = journal_mal['type']
            urutan = journal_mal['urutan']
            nama_akun = journal_mal['nama_akun']
            id_source_data = journal_mal['id_source_data']
            nama_tabel = journal_mal['nama_tabel']
            nama_kolom_db = journal_mal['nama_kolom_db']

            amount = self.__get_amount_stock_opname(id_stock_opname)

            print(
                f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
            data_for_journal.append({
                "type": type == 1 and 'debit' or 'kredit',
                "urutan": urutan,
                "nama_akun": nama_akun,
                "amount": amount,
                "id_jurnal_mal": id_jurnal_mal,
                "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
            })

        mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

        self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                id_cabang=id_cabang, keterangan=id_stock_opname,
                                created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    @handle_error_rollback
    def handle_close_eskalasi_stock_opname(self, data):
        id_fitur_mal = 8
        print("Received data for stock opname:", data)
        created_by = data.get('created_by')

        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_stock_opname = data.get('id_stock_opname')
        id_principal = data.get('id_principal')

        journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)

        data_for_journal = []

        for journal_mal in journal_mals:
            id_jurnal_mal = journal_mal['id_jurnal_mal']
            type = journal_mal['type']
            urutan = journal_mal['urutan']
            nama_akun = journal_mal['nama_akun']
            id_source_data = journal_mal['id_source_data']
            nama_tabel = journal_mal['nama_tabel']
            nama_kolom_db = journal_mal['nama_kolom_db']

            amount = self.__get_amount_stock_opname(id_stock_opname)

            print(
                f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
            data_for_journal.append({
                "type": type == 1 and 'debit' or 'kredit',
                "urutan": urutan,
                "nama_akun": nama_akun,
                "amount": amount,
                "id_jurnal_mal": id_jurnal_mal,
                "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
            })

        mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

        self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                id_cabang=id_cabang, keterangan=id_stock_opname,
                                created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    @handle_error_rollback
    def handle_konfirmasi_penerimaan_stock_transfer(self, data):
        id_fitur_mal = 9
        print("Received data for stock transfer:", data)
        created_by = data.get('created_by')

        id_stock_transfer = data.get('id_stock_transfer')

        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_principal = data.get('id_principal')

        data_for_journal = []
        journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)

        for journal_mal in journal_mals:
            id_jurnal_mal = journal_mal['id_jurnal_mal']
            type = journal_mal['type']
            urutan = journal_mal['urutan']
            nama_akun = journal_mal['nama_akun']
            id_source_data = journal_mal['id_source_data']
            nama_tabel = journal_mal['nama_tabel']
            nama_kolom_db = journal_mal['nama_kolom_db']

            amount = self.__get_amount_stock_transfer_from_jumlah_diterima(id_stock_transfer)

            print(
                f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
            data_for_journal.append({
                "type": type == 1 and 'debit' or 'kredit',
                "urutan": urutan,
                "nama_akun": nama_akun,
                "amount": amount,
                "id_jurnal_mal": id_jurnal_mal,
                "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
            })

        mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

        self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                id_cabang=id_cabang, keterangan=id_stock_transfer,
                                created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    @handle_error_rollback
    def handle_konfirmasi_close_eskalasi_penerimaan_stock_transfer(self, data):
        id_fitur_mal = 10
        print("Received data for stock transfer:", data)
        created_by = data.get('created_by')

        id_stock_transfer = data.get('id_stock_transfer')

        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_principal = data.get('id_principal')

        data_for_journal = []
        journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)

        for journal_mal in journal_mals:
            id_jurnal_mal = journal_mal['id_jurnal_mal']
            type = journal_mal['type']
            urutan = journal_mal['urutan']
            nama_akun = journal_mal['nama_akun']
            id_source_data = journal_mal['id_source_data']
            nama_tabel = journal_mal['nama_tabel']
            nama_kolom_db = journal_mal['nama_kolom_db']

            amount = self.__get_amount_stock_transfer_from_jumlah_diterima(id_stock_transfer)

            print(
                f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
            data_for_journal.append({
                "type": type == 1 and 'debit' or 'kredit',
                "urutan": urutan,
                "nama_akun": nama_akun,
                "amount": amount,
                "id_jurnal_mal": id_jurnal_mal,
                "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
            })

        mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

        self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                id_cabang=id_cabang, keterangan=id_stock_transfer,
                                created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    @handle_error_rollback
    def handle_konfirmasi_pengeluaran_kasir(self, data):
        id_fitur_mal = 11  # contoh id_fitur_mal untuk konfirmasi tagihan
        print("Received data for konfirmasi pengeluaran kasir:", data)
        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_pengeluaran = data.get('id_pengeluaran')
        created_by = data.get('created_by')

        print(f"Processing id_pengeluaran: {id_pengeluaran}")
        journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan)

        data_for_journal = []

        for journal_mal in journal_mals:
            id_jurnal_mal = journal_mal['id_jurnal_mal']
            type = journal_mal['type']
            urutan = journal_mal['urutan']
            nama_akun = journal_mal['nama_akun']
            id_source_data = journal_mal['id_source_data']
            nama_tabel = journal_mal['nama_tabel']
            nama_kolom_db = journal_mal['nama_kolom_db']

            data = self.query().setRawQuery(f"""    
                    SELECT {nama_kolom_db.lower()} FROM {nama_tabel.lower()}
                        WHERE id = :id
                    """).bindparams({
                "id": id_pengeluaran
            }).execute().fetchone().result
            amount = data.get(nama_kolom_db, 0)
            print(
                f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
            data_for_journal.append({
                "type": type == 1 and 'debit' or 'kredit',
                "urutan": urutan,
                "nama_akun": nama_akun,
                "amount": amount,
                "id_jurnal_mal": id_jurnal_mal,
                "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
            })

        mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

        self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                id_cabang=id_cabang, keterangan=id_pengeluaran, created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    def handle_piutang_tunai(self, data):
        id_fitur_mal = 12
        print("Received data for piutang tunai:", data)
        created_by = data.get('created_by')

        data_setorans = data.get('data', {})

        for id_setoran, data_setoran in data_setorans.items():

            id_cabang = data_setoran.get('id_cabang')
            id_perusahaan = data_setoran.get('id_perusahaan')
            id_principal = data_setoran.get('id_principal')

            journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)
            id_faktur = data_setoran.get('id_faktur')

            data_for_journal = []

            for journal_mal in journal_mals:
                id_jurnal_mal = journal_mal['id_jurnal_mal']
                type = journal_mal['type']
                urutan = journal_mal['urutan']
                nama_akun = journal_mal['nama_akun']
                id_source_data = journal_mal['id_source_data']
                nama_tabel = journal_mal['nama_tabel']
                nama_kolom_db = journal_mal['nama_kolom_db']

                if id_source_data == 25:
                    data = self.query().setRawQuery(f"""
                        SELECT {nama_kolom_db} FROM  {nama_tabel.lower()}
                        WHERE id = :id 
                    """).bindparams({"id": id_faktur}).execute().fetchone().result
                else:
                    data = self.query().setRawQuery(f"""
                        SELECT {nama_kolom_db} FROM  {nama_tabel.lower()}
                        WHERE id = :id_setoran
                    """).bindparams({"id_setoran": id_setoran}).execute().fetchone().result

                amount = data.get(nama_kolom_db, 0)

                print(
                    f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
                data_for_journal.append({
                    "type": type == 1 and 'debit' or 'kredit',
                    "urutan": urutan,
                    "nama_akun": nama_akun,
                    "amount": amount,
                    "id_jurnal_mal": id_jurnal_mal,
                    "keterangan": f"id_setoran:{id_setoran};id_faktur:{data_setoran.get('id_faktur')}",
                    "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
                })

            mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

            self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                    id_cabang=id_cabang, keterangan=None,
                                    created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    def handle_konfirmasi_kasir_tunai_sales(self, data):
        id_fitur_mal = 13
        print("Received data for konfirmasi tunai sales:", data)
        created_by = data.get('created_by')

        data_setorans = data.get('data', {})

        for id_setoran, data_setoran in data_setorans.items():

            id_cabang = data_setoran.get('id_cabang')
            id_perusahaan = data_setoran.get('id_perusahaan')
            id_principal = data_setoran.get('id_principal')

            journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)
            id_faktur = data_setoran.get('id_faktur')

            data_for_journal = []

            for journal_mal in journal_mals:
                id_jurnal_mal = journal_mal['id_jurnal_mal']
                type = journal_mal['type']
                urutan = journal_mal['urutan']
                nama_akun = journal_mal['nama_akun']
                id_source_data = journal_mal['id_source_data']
                nama_tabel = journal_mal['nama_tabel']
                nama_kolom_db = journal_mal['nama_kolom_db']

                data = self.query().setRawQuery(f"""
                    SELECT {nama_kolom_db} FROM  {nama_tabel.lower()}
                    WHERE id = :id_setoran
                """).bindparams({"id_setoran": id_setoran}).execute().fetchone().result

                amount = data.get(nama_kolom_db, 0)

                print(
                    f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
                data_for_journal.append({
                    "type": type == 1 and 'debit' or 'kredit',
                    "urutan": urutan,
                    "nama_akun": nama_akun,
                    "amount": amount,
                    "id_jurnal_mal": id_jurnal_mal,
                    "keterangan": f"id_setoran:{id_setoran};id_faktur:{data_setoran.get('id_faktur')}",
                    "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
                })

            mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

            self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                    id_cabang=id_cabang, keterangan=None,
                                    created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    def handle_konfirmas_kasir_tunai_kepala_gudang(self, data):
        id_fitur_mal = 14
        print("Received data for konfirmasi tunai kepala gudang:", data)
        created_by = data.get('created_by')

        data_setorans = data.get('data', {})

        for id_setoran, data_setoran in data_setorans.items():

            id_cabang = data_setoran.get('id_cabang')
            id_perusahaan = data_setoran.get('id_perusahaan')
            id_principal = data_setoran.get('id_principal')

            journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)
            id_faktur = data_setoran.get('id_faktur')

            data_for_journal = []

            for journal_mal in journal_mals:
                id_jurnal_mal = journal_mal['id_jurnal_mal']
                type = journal_mal['type']
                urutan = journal_mal['urutan']
                nama_akun = journal_mal['nama_akun']
                id_source_data = journal_mal['id_source_data']
                nama_tabel = journal_mal['nama_tabel']
                nama_kolom_db = journal_mal['nama_kolom_db']

                data = self.query().setRawQuery(f"""
                    SELECT {nama_kolom_db} FROM  {nama_tabel.lower()}
                    WHERE id = :id_setoran
                """).bindparams({"id_setoran": id_setoran}).execute().fetchone().result

                amount = data.get(nama_kolom_db, 0)

                print(
                    f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
                data_for_journal.append({
                    "type": type == 1 and 'debit' or 'kredit',
                    "urutan": urutan,
                    "nama_akun": nama_akun,
                    "amount": amount,
                    "id_jurnal_mal": id_jurnal_mal,
                    "keterangan": f"id_setoran:{id_setoran};id_faktur:{data_setoran.get('id_faktur')}",
                    "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
                })

            mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

            self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                    id_cabang=id_cabang, keterangan=None,
                                    created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    @handle_error_rollback
    def handle_ajukan_pengeluaran_kasir(self, data):
        id_fitur_mal = 15  # contoh id_fitur_mal untuk konfirmasi tagihan
        print("Received data for ajukan pengeluaran kasir:", data)
        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_pengeluaran = data.get('id_pengeluaran')
        created_by = data.get('created_by')

        print(f"Processing id_pengeluaran: {id_pengeluaran}")
        journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan)

        data_for_journal = []

        for journal_mal in journal_mals:
            id_jurnal_mal = journal_mal['id_jurnal_mal']
            type = journal_mal['type']
            urutan = journal_mal['urutan']
            nama_akun = journal_mal['nama_akun']
            id_source_data = journal_mal['id_source_data']
            nama_tabel = journal_mal['nama_tabel']
            nama_kolom_db = journal_mal['nama_kolom_db']

            data = self.query().setRawQuery(f"""    
                        SELECT {nama_kolom_db.lower()} FROM {nama_tabel.lower()}
                            WHERE id = :id
                        """).bindparams({
                "id": id_pengeluaran
            }).execute().fetchone().result
            amount = data.get(nama_kolom_db, 0)
            print(
                f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
            data_for_journal.append({
                "type": type == 1 and 'debit' or 'kredit',
                "urutan": urutan,
                "nama_akun": nama_akun,
                "amount": amount,
                "id_jurnal_mal": id_jurnal_mal,
                "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
            })

        mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

        self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                id_cabang=id_cabang, keterangan=id_pengeluaran, created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    @handle_error_rollback
    def handle_realisasi_cod(self, data):
        id_fitur_mal = 16  # contoh id_fitur_mal untuk konfirmasi tagihan
        print("Received data for realisasi cod:", data)
        created_by = data.get('created_by')

        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_principal = data.get('id_principal')
        id_order_batch = data.get('id_order_batch')
        id_sales_order = data.get('id_sales_order')
        id_setoran = data.get('id_setoran')

        journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)

        data_for_journal = []

        by_order_batch = id_order_batch is not None

        for journal_mal in journal_mals:
            id_jurnal_mal = journal_mal['id_jurnal_mal']
            type = journal_mal['type']
            urutan = journal_mal['urutan']
            nama_akun = journal_mal['nama_akun']
            id_source_data = journal_mal['id_source_data']
            nama_tabel = journal_mal['nama_tabel']
            nama_kolom_db = journal_mal['nama_kolom_db']

            if id_source_data == 33:
                data = self.query().setRawQuery(f"""    
                                    SELECT {nama_kolom_db.lower()} FROM {nama_tabel.lower()}
                                        WHERE id = :id_setoran
                                    """).bindparams({
                    "id_setoran": id_setoran
                }).execute().fetchone().result
            elif by_order_batch:
                data = self.query().setRawQuery(f"""    
                                    SELECT {nama_kolom_db.lower()} FROM {nama_tabel.lower()}
                                        WHERE id_order_batch = :id_order_batch
                                    """).bindparams({
                    "id_order_batch": id_order_batch
                }).execute().fetchone().result
            else:
                data = self.query().setRawQuery(f"""    
                                    SELECT {nama_kolom_db.lower()} FROM {nama_tabel.lower()}
                                        WHERE id_sales_order = :id_sales_order
                                    """).bindparams({
                    "id_sales_order": id_sales_order
                }).execute().fetchone().result

            amount = data.get(nama_kolom_db, 0)

            print(
                f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
            data_for_journal.append({
                "type": type == 1 and 'debit' or 'kredit',
                "urutan": urutan,
                "nama_akun": nama_akun,
                "amount": amount,
                "id_jurnal_mal": id_jurnal_mal,
                "keterangan": f"id_order_batch:{id_order_batch};id_setoran:{id_setoran}" if by_order_batch else f"id_sales_order:{id_sales_order};id_setoran:{id_setoran}",
                "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
            })

        mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

        self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                id_cabang=id_cabang, keterangan=None,
                                created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }


    @handle_error_rollback
    def handle_request_purchase(self, data):
        # 1. Identifikasi Payload
        id_fitur_mal = data.get('id_fitur_mal', 17) 
        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_order_raw = data.get('id_order')
        id_principal = data.get('id_principal')
        created_by = data.get('created_by')

        print(f"--- START PROCESSING REQUEST PURCHASE ID: {id_order_raw} ---")
        
        # 2. Ambil Mapping Jurnal
        res_journal_map = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)
        journal_mals = res_journal_map if isinstance(res_journal_map, list) else res_journal_map.get('result', [])
        
        if not journal_mals: 
            print(f"WARNING: Mapping tidak ditemukan untuk Fitur {id_fitur_mal}")
            return {"status": "success"}

        # 3. AMBIL DATA DENGAN ENGINE LANGSUNG (BYPASS SESSION CACHE)
        # Ini krusial untuk memastikan data yang baru saja di-commit terlihat
        transaksi_data = None
        query_check = text("SELECT * FROM purchase_order WHERE id = :id")
        
        for attempt in range(5): 
            try:
                # Menggunakan engine.connect() agar mendapatkan snapshot DB terbaru
                with self.db.engine.connect() as connection:
                    result = connection.execute(query_check, {"id": id_order_raw})
                    res_check = result.fetchone()
                
                if res_check:
                    # Konversi hasil row menjadi dictionary agar mudah diakses
                    transaksi_data = res_check._asdict() if hasattr(res_check, '_asdict') else res_check
                    break
            except Exception as e:
                print(f"DEBUG: Koneksi engine gagal: {str(e)}")
            
            print(f"DEBUG: PO {id_order_raw} belum terlihat, retry {attempt+1}/5...")
            time.sleep(2) 

        if not transaksi_data:
            print(f"ERROR: Data PO {id_order_raw} tetap tidak ditemukan di database.")
            return {"status": "failed"}

        data_for_journal = []

        # 4. LOOP MAPPING UNTUK CALCULATE AMOUNT
        for journal_mal in journal_mals:
            target_kolom = (journal_mal.get('nama_kolom_db') or 'total').lower()
            
            # Ambil nominal secara dinamis dari hasil query
            # Jika kolom di mapping tidak ada di tabel, fallback ke kolom 'total'
            amount = transaksi_data.get(target_kolom, transaksi_data.get('total', 0))

            data_for_journal.append({
                "type": 'debit' if journal_mal.get('type') == 1 else 'kredit',
                "urutan": journal_mal.get('urutan'),
                "nama_akun": journal_mal.get('nama_akun'),
                "amount": float(amount) if amount else 0.0,
                "id_jurnal_mal": journal_mal.get('id_jurnal_mal'),
                "id_jurnal_mal_detail": journal_mal.get('id_mal_detail'),
            })
            print(f"   > Acc: {journal_mal.get('nama_akun')} | Col: {target_kolom} | Val: {amount}")

        # 5. SIMPAN KE TABEL JURNAL
        if data_for_journal and any(d['amount'] > 0 for d in data_for_journal):
            # Validasi Balance (Opsional Log)
            debit_total = sum(d['amount'] for d in data_for_journal if d['type'] == 'debit')
            kredit_total = sum(d['amount'] for d in data_for_journal if d['type'] == 'kredit')
            
            mapping = self.__mapping_by_id_jurnal_mal(data_for_journal)
            self.__insert_to_jurnal(
                mapping_by_id_jurnal_mal=mapping,
                id_perusahaan=id_perusahaan,
                id_cabang=id_cabang,
                keterangan=f"Request Purchase Order ID: {id_order_raw}",
                created_by=created_by
            )
            self.db.session.commit()
            print(f"--- SUCCESS: Jurnal PO {id_order_raw} Berhasil Disimpan ---")
        else:
            print(f"--- SKIP: Jurnal PO {id_order_raw} tidak disimpan (Amount 0) ---")
        
        return {"status": "success"}

    # @handle_error_rollback
    # def handle_konfirmasi_purchase(self, data):
    #     print(f"--- START PROCESSING KONFIRMASI PURCHASE ---")
    #     id_order_raw = data.get('id_order') 

    #     # 1. Gunakan Tabel yang Benar (Order, bukan purchase_transaksi jika data diupdate di sana)
    #     # Kita coba cari di purchase_transaksi dulu, kalau gagal cari di orders
    #     transaksi_data = None
        
    #     # Retry logic tetap ada untuk mengantisipasi lag Commit
    #     for attempt in range(5):
    #         try:
    #             # Bypass Session Cache dengan Engine baru
    #             with self.db.engine.connect() as connection:
    #                 # Coba cari di purchase_transaksi
    #                 query = text("SELECT * FROM purchase_transaksi WHERE order_id = :id LIMIT 1")
    #                 res = connection.execute(query, {"id": id_order_raw}).fetchone()
                    
    #                 if not res:
    #                     # FALLBACK: Cari langsung di tabel Order (biasanya nama tabelnya 'orders' atau 'order')
    #                     # Sesuaikan dengan nama tabel model Order Anda
    #                     query_fallback = text("SELECT * FROM purchase_order WHERE id = :id")
    #                     res = connection.execute(query_fallback, {"id": id_order_raw}).fetchone()

    #                 if res:
    #                     transaksi_data = res._asdict()
    #                     break
    #         except Exception as e:
    #             print(f"DEBUG: Error query: {str(e)}")
            
    #         print(f"DEBUG: Data {id_order_raw} belum muncul, retry {attempt+1}...")
    #         time.sleep(2)

    #     if not transaksi_data:
    #         print(f"ERROR: Data transaksi ID {id_order_raw} TIDAK DITEMUKAN di tabel manapun.")
    #         return {"status": "failed"}

    #     data_for_journal = []

    #     # 4. Iterasi Detail Mapping
    #     for journal_mal in journal_mals:
    #         id_source_data = journal_mal.get('id_source_data')
    #         amount = 0.0

    #         # Logika pengambilan angka berdasarkan metadata mapping atau kolom DB
    #         # Menggunakan .get(key, default) agar tidak crash jika kolom missing di tabel
    #         if id_source_data == 38: # Pajak/PPN
    #             amount = transaksi_data.get('ppn', 0)
    #         elif id_source_data in [1, 3]: # Total Transaksi
    #             amount = transaksi_data.get('total', 0)
    #         elif id_source_data == 2: # Subtotal
    #             amount = transaksi_data.get('subtotal', 0)
    #         else:
    #             # Fallback ke nama_kolom_db jika ada di mapping
    #             nama_kolom = (journal_mal.get('nama_kolom_db') or 'total').lower()
    #             amount = transaksi_data.get(nama_kolom, transaksi_data.get('total', 0))

    #         amount = float(amount) if amount else 0.0
            
    #         data_for_journal.append({
    #             "type": 'debit' if journal_mal.get('type') == 1 else 'kredit',
    #             "urutan": journal_mal.get('urutan'),
    #             "nama_akun": journal_mal.get('nama_akun'),
    #             "amount": amount,
    #             "id_jurnal_mal": journal_mal.get('id_jurnal_mal'),
    #             "id_jurnal_mal_detail": journal_mal.get('id_mal_detail'),
    #         })
    #         print(f"LOG JURNAL: {journal_mal.get('nama_akun')} | {amount} ({'D' if journal_mal.get('type') == 1 else 'K'})")

    #     # 5. Simpan ke Database
    #     if data_for_journal and any(d['amount'] > 0 for d in data_for_journal):
    #         # Validasi Balance sederhana
    #         total_d = sum(d['amount'] for d in data_for_journal if d['type'] == 'debit')
    #         total_k = sum(d['amount'] for d in data_for_journal if d['type'] == 'kredit')
            
    #         if abs(total_d - total_k) > 0.01:
    #             print(f"!!! WARNING: Jurnal Unbalanced! D: {total_d} | K: {total_k}")

    #         mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)
    #         self.__insert_to_jurnal(
    #             mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, 
    #             id_perusahaan=id_perusahaan,
    #             id_cabang=id_cabang, 
    #             keterangan=f"Konfirmasi Purchase ID: {transaksi_data.get('id')}", 
    #             created_by=created_by
    #         )
    #         self.db.session.commit()
    #         print(f"--- SUCCESS: Jurnal Fitur {id_fitur_mal} Berhasil Disimpan ---")
    #     else:
    #         print(f"--- SKIP: Jurnal tidak disimpan (Amount 0) ---")

    #     return {"status": "success"}

    @handle_error_rollback
    def handle_penerimaan_barang(self, data):
        id_fitur_mal = 19  # contoh id_fitur_mal untuk konfirmasi purchase
        print("Received data for penerimaan barang:", data)
        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_transaksi = data.get('id_transaksi')
        created_by = data.get('created_by')
        id_principal = data.get('id_principal')

        print(f"Processing id_transaksi: {id_transaksi}")
        journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)

        data_for_journal = []

        for journal_mal in journal_mals:
            id_jurnal_mal = journal_mal['id_jurnal_mal']
            type = journal_mal['type']
            urutan = journal_mal['urutan']
            nama_akun = journal_mal['nama_akun']
            id_source_data = journal_mal['id_source_data']
            nama_tabel = journal_mal['nama_tabel']
            nama_kolom_db = journal_mal['nama_kolom_db']

            data = self.query().setRawQuery(f"""
                SELECT {nama_kolom_db.lower()} FROM {nama_tabel.lower()}
                    WHERE id = :id 
                """).bindparams({
                "id": id_transaksi
            }).execute().fetchone().result

            amount = data.get(nama_kolom_db, 0)

            print(
                f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
            data_for_journal.append({
                "type": type == 1 and 'debit' or 'kredit',
                "urutan": urutan,
                "nama_akun": nama_akun,
                "amount": amount,
                "id_jurnal_mal": id_jurnal_mal,
                "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
            })

        mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

        self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                id_cabang=id_cabang, keterangan=id_transaksi, created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    @handle_error_rollback
    def handle_konfirmasi_purchase_potongan_hutang(self, data):
        id_fitur_mal = 20
        print("Received data for konfirmasi purchase potongan hutang:", data)
        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_transaksi = data.get('id_transaksi')
        created_by = data.get('created_by')
        id_principal = data.get('id_principal')

        print(f"Processing id_transaksi: {id_transaksi}")
        journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)

        data_for_journal = []

        for journal_mal in journal_mals:
            id_jurnal_mal = journal_mal['id_jurnal_mal']
            type = journal_mal['type']
            urutan = journal_mal['urutan']
            nama_akun = journal_mal['nama_akun']
            id_source_data = journal_mal['id_source_data']
            nama_tabel = journal_mal['nama_tabel']
            nama_kolom_db = journal_mal['nama_kolom_db']

            data = self.query().setRawQuery(f"""
                    SELECT {nama_kolom_db.lower()} FROM {nama_tabel.lower()}
                        WHERE id = :id 
                    """).bindparams({
                "id": id_transaksi
            }).execute().fetchone().result

            amount = data.get(nama_kolom_db, 0)

            print(
                f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
            data_for_journal.append({
                "type": type == 1 and 'debit' or 'kredit',
                "urutan": urutan,
                "nama_akun": nama_akun,
                "amount": amount,
                "id_jurnal_mal": id_jurnal_mal,
                "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
            })

        mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

        self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                id_cabang=id_cabang, keterangan=id_transaksi, created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    @handle_error_rollback
    def handle_buat_tagihan(self, data):
        id_fitur_mal = 21  # contoh id_fitur_mal untuk konfirmasi tagihan
        print("Received data for buat tagihan:", data)
        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_tagihan = data.get('id_tagihan')
        id_principal = data.get('id_principal')
        created_by = data.get('created_by')

        print(f"Processing tagihan_id: {id_tagihan}")
        journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)

        data_for_journal = []

        for journal_mal in journal_mals:
            id_jurnal_mal = journal_mal['id_jurnal_mal']
            type = journal_mal['type']
            urutan = journal_mal['urutan']
            nama_akun = journal_mal['nama_akun']
            id_source_data = journal_mal['id_source_data']
            nama_tabel = journal_mal['nama_tabel']
            nama_kolom_db = journal_mal['nama_kolom_db']

            data = self.query().setRawQuery(f"""    
                    SELECT {nama_kolom_db.lower()} FROM {nama_tabel.lower()}
                        WHERE id = :id
                    """).bindparams({
                "id": id_tagihan
            }).execute().fetchone().result
            amount = data.get(nama_kolom_db, 0)
            print(
                f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
            data_for_journal.append({
                "type": type == 1 and 'debit' or 'kredit',
                "urutan": urutan,
                "nama_akun": nama_akun,
                "amount": amount,
                "id_jurnal_mal": id_jurnal_mal,
                "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
            })

        mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

        self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                id_cabang=id_cabang, keterangan=id_tagihan, created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    @handle_error_rollback
    def handle_buat_tagihan_potongan_hutang(self, data):
        id_fitur_mal = 22
        print("Received data for buat tagihan potongan hutang:", data)
        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_tagihan = data.get('id_tagihan')
        created_by = data.get('created_by')
        id_principal = data.get('id_principal')

        print(f"Processing tagihan_id: {id_tagihan}")
        journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)

        data_for_journal = []

        for journal_mal in journal_mals:
            id_jurnal_mal = journal_mal['id_jurnal_mal']
            type = journal_mal['type']
            urutan = journal_mal['urutan']
            nama_akun = journal_mal['nama_akun']
            id_source_data = journal_mal['id_source_data']
            nama_tabel = journal_mal['nama_tabel']
            nama_kolom_db = journal_mal['nama_kolom_db']

            data = self.query().setRawQuery(f"""
                        SELECT SUM(COALESCE(pts.potongan, 0)) AS total FROM purchase_tagihan pt
                                JOIN purchase_tagihan_detail ptd
                                 ON ptd.tagihan_id = pt.id
                                 JOIN purchase_transaksi pts
                                 ON pts.id = ptd.transaksi_id
                            WHERE pt.id = :id                              
                        """).bindparams({
                "id": id_tagihan
            }).execute().fetchone().result

            amount = data.get("total", 0)

            print(
                f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
            data_for_journal.append({
                "type": type == 1 and 'debit' or 'kredit',
                "urutan": urutan,
                "nama_akun": nama_akun,
                "amount": amount,
                "id_jurnal_mal": id_jurnal_mal,
                "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
            })

        mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

        self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                id_cabang=id_cabang, keterangan=id_tagihan, created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    @handle_error_rollback
    def handle_konfirmasi_tagihan_potongan_hutang(self, data):
        id_fitur_mal = 23
        print("Received data for konfirmasi tagihan potongan hutang:", data)
        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_tagihan = data.get('id_tagihan')
        created_by = data.get('created_by')
        id_principal = data.get('id_principal')

        print(f"Processing tagihan_id: {id_tagihan}")
        journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)

        data_for_journal = []

        for journal_mal in journal_mals:
            id_jurnal_mal = journal_mal['id_jurnal_mal']
            type = journal_mal['type']
            urutan = journal_mal['urutan']
            nama_akun = journal_mal['nama_akun']
            id_source_data = journal_mal['id_source_data']
            nama_tabel = journal_mal['nama_tabel']
            nama_kolom_db = journal_mal['nama_kolom_db']

            data = self.query().setRawQuery(f"""
                            SELECT SUM(COALESCE(pts.potongan, 0)) AS total FROM purchase_tagihan pt
                                    JOIN purchase_tagihan_detail ptd
                                     ON ptd.tagihan_id = pt.id
                                     JOIN purchase_transaksi pts
                                     ON pts.id = ptd.transaksi_id
                                WHERE pt.id = :id                              
                            """).bindparams({
                "id": id_tagihan
            }).execute().fetchone().result

            amount = data.get("total", 0)

            print(
                f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
            data_for_journal.append({
                "type": type == 1 and 'debit' or 'kredit',
                "urutan": urutan,
                "nama_akun": nama_akun,
                "amount": amount,
                "id_jurnal_mal": id_jurnal_mal,
                "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
            })

        mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

        self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                id_cabang=id_cabang, keterangan=id_tagihan, created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    @handle_error_rollback
    def handle_ajukan_kasbon_klaim(self, data):
        id_fitur_mal = 24  # contoh id_fitur_mal untuk ajukan kasbon
        print("Received data for ajukan kasbon:", data)
        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_kasbon_klaim = data.get('id_kasbon_klaim')
        id_principal = data.get('id_principal')
        created_by = data.get('created_by')

        print(f"Processing kasbon_klaim_id: {id_kasbon_klaim}")
        journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)

        data_for_journal = []

        for journal_mal in journal_mals:
            id_jurnal_mal = journal_mal['id_jurnal_mal']
            type = journal_mal['type']
            urutan = journal_mal['urutan']
            nama_akun = journal_mal['nama_akun']
            id_source_data = journal_mal['id_source_data']
            nama_tabel = journal_mal['nama_tabel']
            nama_kolom_db = journal_mal['nama_kolom_db']

            data = self.query().setRawQuery(f"""    
                    SELECT {nama_kolom_db.lower()} FROM {nama_tabel.lower()}
                        WHERE id_kasbon_klaim = :id
                    """).bindparams({
                "id": id_kasbon_klaim
            }).execute().fetchone().result
            amount = data.get(nama_kolom_db, 0)
            print(
                f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
            data_for_journal.append({
                "type": type == 1 and 'debit' or 'kredit',
                "urutan": urutan,
                "nama_akun": nama_akun,
                "amount": amount,
                "id_jurnal_mal": id_jurnal_mal,
                "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
            })

        mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

        self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                id_cabang=id_cabang, keterangan=id_kasbon_klaim, created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    @handle_error_rollback
    def handle_konfirmasi_kasbon_klaim(self, data):
        id_fitur_mal = 25  # contoh id_fitur_mal untuk ajukan kasbon
        print("Received data for konfirmasi kasbon:", data)
        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_kasbon_klaim = data.get('id_kasbon_klaim')
        id_principal = data.get('id_principal')
        created_by = data.get('created_by')

        print(f"Processing kasbon_klaim_id: {id_kasbon_klaim}")
        journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)

        data_for_journal = []

        for journal_mal in journal_mals:
            id_jurnal_mal = journal_mal['id_jurnal_mal']
            type = journal_mal['type']
            urutan = journal_mal['urutan']
            nama_akun = journal_mal['nama_akun']
            id_source_data = journal_mal['id_source_data']
            nama_tabel = journal_mal['nama_tabel']
            nama_kolom_db = journal_mal['nama_kolom_db']

            data = self.query().setRawQuery(f"""    
                        SELECT {nama_kolom_db.lower()} FROM {nama_tabel.lower()}
                            WHERE id_kasbon_klaim = :id
                        """).bindparams({
                "id": id_kasbon_klaim
            }).execute().fetchone().result
            amount = data.get(nama_kolom_db, 0)
            print(
                f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
            data_for_journal.append({
                "type": type == 1 and 'debit' or 'kredit',
                "urutan": urutan,
                "nama_akun": nama_akun,
                "amount": amount,
                "id_jurnal_mal": id_jurnal_mal,
                "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
            })

        mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

        self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                id_cabang=id_cabang, keterangan=id_kasbon_klaim, created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    @handle_error_rollback
    def handle_klaim_sudah_digunakan(self, data):
        id_fitur_mal = 26  # contoh id_fitur_mal  untuk klaim sudah gunakan kasbon
        print("Received data for klaim sudah digunakan:", data)
        id_perusahaan = data.get('id_perusahaan')
        id_cabang = data.get('id_cabang')
        id_klaim = data.get('id_klaim')
        id_principal = data.get('id_principal')
        created_by = data.get('created_by')

        print(f"Processing id_klaim: {id_klaim}")
        journal_mals = self.__get_journal_map(id_fitur_mal, id_perusahaan, id_principal)

        data_for_journal = []

        for journal_mal in journal_mals:
            id_jurnal_mal = journal_mal['id_jurnal_mal']
            type = journal_mal['type']
            urutan = journal_mal['urutan']
            nama_akun = journal_mal['nama_akun']
            id_source_data = journal_mal['id_source_data']
            nama_tabel = journal_mal['nama_tabel']
            nama_kolom_db = journal_mal['nama_kolom_db']

            data = self.query().setRawQuery(f"""    
                            SELECT {nama_kolom_db.lower()} FROM {nama_tabel.lower()}
                                WHERE id = :id
                            """).bindparams({
                "id": id_klaim
            }).execute().fetchone().result
            amount = data.get(nama_kolom_db, 0)
            print(
                f"Journal Mal ID: {id_jurnal_mal}, Type: {type}, Urutan: {urutan}, Akun: {nama_akun}, Amount: {amount}")
            data_for_journal.append({
                "type": type == 1 and 'debit' or 'kredit',
                "urutan": urutan,
                "nama_akun": nama_akun,
                "amount": amount,
                "id_jurnal_mal": id_jurnal_mal,
                "id_jurnal_mal_detail": journal_mal['id_mal_detail'],
            })

        mapping_by_id_jurnal_mal = self.__mapping_by_id_jurnal_mal(data_for_journal)

        self.__insert_to_jurnal(mapping_by_id_jurnal_mal=mapping_by_id_jurnal_mal, id_perusahaan=id_perusahaan,
                                id_cabang=id_cabang, keterangan=id_klaim, created_by=created_by)

        self.commit()

        return {
            "status": "success",
        }

    def __mapping_by_id_jurnal_mal(self, data_for_journal):
        mapping_by_id_jurnal_mal = {}
        for entry in data_for_journal:
            id_jurnal_mal = entry.get('id_jurnal_mal')
            if id_jurnal_mal not in mapping_by_id_jurnal_mal:
                mapping_by_id_jurnal_mal[id_jurnal_mal] = []
            mapping_by_id_jurnal_mal[id_jurnal_mal].append(entry)

        return mapping_by_id_jurnal_mal

    def __insert_to_jurnal(self, mapping_by_id_jurnal_mal: dict[str, list], id_perusahaan, id_cabang, keterangan, created_by):
        for id_jurnal_mal, data_for_journal in mapping_by_id_jurnal_mal.items():
            # 1. Validasi Balance (PENTING!)
            total_debit = sum(float(e['amount']) for e in data_for_journal if e['type'] == 'debit')
            total_kredit = sum(float(e['amount']) for e in data_for_journal if e['type'] == 'kredit')
            
            if abs(total_debit - total_kredit) > 0.001:
                print(f"!!! WARNING: Jurnal ID MAL {id_jurnal_mal} tidak balance! D: {total_debit} | K: {total_kredit}")
                # Kamu bisa raise exception di sini jika ingin membatalkan insert yang tidak balance

            # 2. Penomoran Otomatis
            kode_prefix = f"JRL/{date_for_code()}"
            last_prefix = (
                JurnalDetailModel.query.filter(JurnalDetailModel.kode_jurnal.startswith(kode_prefix))
                .with_for_update() # Mengunci row agar tidak ada nomor ganda
                .order_by(JurnalDetailModel.kode_jurnal.desc())
                .first()
            )

            new_number = (int(last_prefix.kode_jurnal.split('/')[-1]) + 1) if last_prefix else 1
            kode_jurnal = f"{kode_prefix}/{str(new_number).zfill(5)}"

            # 3. Insert Header
            insert_jurnal = JurnalModel(
                id_jurnal_mal=id_jurnal_mal,
                id_perusahaan=id_perusahaan,
                id_cabang=id_cabang,
                tanggal=date_now(),
                keterangan=f"PO ID: {keterangan}" if keterangan else "Tanpa Keterangan"
            )
            self.add(insert_jurnal).flush()

            # 4. Insert Details
            for entry in data_for_journal:
                insert_jurnal_detail = JurnalDetailModel(
                    kode_jurnal=kode_jurnal,
                    id_jurnal=insert_jurnal.id_jurnal,
                    id_mal_detail=entry['id_jurnal_mal_detail'],
                    nama_akun=entry['nama_akun'],
                    debit=entry['amount'] if entry['type'] == 'debit' else 0,
                    kredit=entry['amount'] if entry['type'] == 'kredit' else 0,
                    created_by=created_by,
                )
                self.add(insert_jurnal_detail)
            
            print(f"SUCCESS: Tersimpan Jurnal {kode_jurnal} untuk MAL ID {id_jurnal_mal}")

    def __get_amount_purchase_transaksi_ppn(self, transaksi_id):
        query = """
                SELECT SUM((podj.uom_harga_beli_ppn - podj.uom_harga_beli) * podj.jumlah) AS total_ppn
                FROM purchase_transaksi pt
                         JOIN purchase_order po
                              ON pt.order_id = po.id
                         JOIN purchase_order_detail_jumlah podj
                              ON po.id = podj.order_id
                WHERE pt.id = :transaksi_id
                  AND podj.jumlah IS NOT NULL
                GROUP BY pt.id, podj.order_detail_id
                """
        result = self.query().setRawQuery(query).bindparams({"transaksi_id": transaksi_id}).execute().fetchone().result

        return result['total_ppn'] if result else 0

    def __get_amount_purchase_order_ppn(self, order_id):
        query = """
                SELECT SUM((podj.uom_harga_beli_ppn - podj.uom_harga_beli) * podj.jumlah) AS total_ppn
                FROM purchase_order po
                         JOIN purchase_order_detail_jumlah podj
                              ON po.id = podj.order_id
                WHERE po.id = :order_id
                  AND podj.jumlah IS NOT NULL
                GROUP BY podj.order_detail_id
                """
        result = self.query().setRawQuery(query).bindparams({"order_id": order_id}).execute().fetchone().result

        return result['total_ppn'] if result else 0

    def __get_amount_process_picking_by_order_batch(self, id_order_batch):
        query = """
                SELECT SUM(sod.hargaorder * pp.jumlah_picked) AS total_amount
                FROM sales_order so
                         JOIN sales_order_detail sod
                              ON so.id = sod.id_sales_order
                         JOIN proses_picking pp
                              ON sod.id = pp.id_order_detail
                WHERE so.id_order_batch = :id_order_batch \
                """
        result = self.query().setRawQuery(query).bindparams({
            "id_order_batch": id_order_batch
        }).execute().fetchone().result

        return result['total_amount'] if result else 0

    def __get_amount_process_picking_by_sales_order(self, id_sales_order):
        query = """
                SELECT SUM(sod.hargaorder * pp.jumlah_picked) AS total_amount
                FROM sales_order so
                         JOIN sales_order_detail sod
                              ON so.id = sod.id_sales_order
                         JOIN proses_picking pp
                              ON sod.id = pp.id_order_detail
                WHERE so.id = :id_sales_order \
                """
        result = self.query().setRawQuery(query).bindparams({
            "id_sales_order": id_sales_order
        }).execute().fetchone().result

        return result['total_amount'] if result else 0

    def __get_amount_shipping_by_sales_order(self, id_sales_order):
        query = """
                SELECT SUM(sod.subtotaldelivered) AS total_amount
                FROM sales_order so
                         JOIN sales_order_detail sod
                              ON so.id = sod.id_sales_order
                WHERE so.id = :id_sales_order \
                """
        result = self.query().setRawQuery(query).bindparams({
            "id_sales_order": id_sales_order
        }).execute().fetchone().result

        return result['total_amount'] if result else 0

    def __get_amount_shipping_by_order_batch(self, id_order_batch):
        query = """
                SELECT SUM(sod.subtotaldelivered) AS total_amount
                FROM sales_order so
                         JOIN sales_order_detail sod
                              ON so.id = sod.id_sales_order
                WHERE so.id_order_batch = :id_order_batch \
                """
        result = self.query().setRawQuery(query).bindparams({
            "id_order_batch": id_order_batch
        }).execute().fetchone().result

        return result['total_amount'] if result else 0

    def __get_amount_stock_opname(self, id_stock_opname):
        query = """
                SELECT SUM(sod.subtotal_selisih) AS total_amount
                FROM stock_opname so
                         JOIN stock_opname_detail sod
                              ON so.id_stock_opname = sod.id_stock_opname
                WHERE so.id_stock_opname = :id_stock_opname \
                """
        result = self.query().setRawQuery(query).bindparams({
            "id_stock_opname": id_stock_opname
        }).execute().fetchone().result

        return result['total_amount'] if result else 0

    def __get_amount_stock_transfer_from_jumlah_diterima(self, id_stock_transfer):
        query = """
                SELECT SUM(std.jumlah_diterima * COALESCE(p.harga_beli, 0)) AS total_amount
                FROM stock_transfer st
                         JOIN public.stock_transfer_detail std
                              ON st.id = std.id_stock_transfer
                         JOIN produk p
                              ON p.id = std.id_produk
                WHERE st.id = :id_stock_transfer \
                """
        result = self.query().setRawQuery(query).bindparams({
            "id_stock_transfer": id_stock_transfer
        }).execute().fetchone().result

        return result['total_amount'] if result else 0

    def __get_amount_stock_transfer_from_jumlah_picked(self, id_stock_transfer):
        query = """
                SELECT SUM(std.jumlah_picked * COALESCE(p.harga_beli, 0)) AS total_amount
                FROM stock_transfer st
                         JOIN public.stock_transfer_detail std
                              ON st.id = std.id_stock_transfer
                         JOIN produk p
                              ON p.id = std.id_produk
                WHERE st.id = :id_stock_transfer \
                """
        result = self.query().setRawQuery(query).bindparams({
            "id_stock_transfer": id_stock_transfer
        }).execute().fetchone().result

        return result['total_amount'] if result else 0
