from flask import request
from sqlalchemy import text
from collections import defaultdict
from datetime import datetime


from .BaseAkuntansi import BaseAkuntansi
from ...lib.paginateV2 import PaginateV2
from apps import native_db as db
import re

def extract_id(self, text):
    # Mencari angka terakhir dalam string
    match = re.findall(r'\d+', str(text))
    return match[-1] if match else None


class Jurnal(BaseAkuntansi):
    def __init__(self):
        super().__init__()
    
    def getBukuBesar(self):

        # ===============================
        # 1. Ambil Parameter
        # ===============================
        all_undefined = request.args.getlist('undefined')

        p_awal = self.req("periode_awal")
        p_akhir = self.req("periode_akhir")
        id_coa = self.req("id_coa")
        id_cabang = self.req("id_cabang")

        if not p_awal and len(all_undefined) > 0:
            p_awal = all_undefined[0]
        if not p_akhir and len(all_undefined) > 1:
            p_akhir = all_undefined[1]

        periode_awal = p_awal or '1900-01-01'
        periode_akhir = p_akhir or '2100-12-31'

        # ===============================
        # 2. Saldo Awal
        # ===============================
        sql_sa = """
            SELECT SUM(COALESCE(jd.debit, 0) - COALESCE(jd.kredit, 0)) as saldo_awal
            FROM public.jurnal_detail jd
            JOIN public.jurnal j ON jd.id_jurnal = j.id_jurnal
            LEFT JOIN public.jurnal_mal_detail jmd ON jd.id_mal_detail = jmd.id_mal_detail
            WHERE j.tanggal < :periode_awal
        """

        params_sa = {"periode_awal": periode_awal}

        if id_coa:
            sql_sa += " AND jmd.id_coa = :id_coa"
            params_sa["id_coa"] = id_coa

        res_sa = db.session.execute(text(sql_sa), params_sa).fetchone()
        saldo_awal_value = float(res_sa[0] or 0) if res_sa else 0.0

        # ===============================
        # 3. Query Detail
        # ===============================
        query_detail = """
            SELECT 
                j.id_jurnal, j.tanggal,
                p.nama AS nama_perusahaan,
                c.nama AS nama_cabang,
                u.nama AS created_by,
                coa.nama_akun,
                coa.nomor_akun,
                j.keterangan AS keterangan_umum,
                jd.keterangan AS keterangan_item,
                COALESCE(jd.debit, 0) AS debit,
                COALESCE(jd.kredit, 0) AS kredit,
                sm.nama_kolom_view,
                coa.id_coa,
                coa.parent_id
            FROM public.jurnal j
            INNER JOIN public.jurnal_detail jd ON j.id_jurnal = jd.id_jurnal
            LEFT JOIN public.jurnal_mal_detail jmd ON jd.id_mal_detail = jmd.id_mal_detail
            LEFT JOIN public.coa coa ON jmd.id_coa = coa.id_coa
            LEFT JOIN public.perusahaan p ON j.id_perusahaan = p.id
            LEFT JOIN public.cabang c ON j.id_cabang = c.id
            LEFT JOIN public.users u ON jd.created_by = u.id
            LEFT JOIN public.source_modul sm ON jmd.id_source_data = sm.id_source_data
            WHERE j.tanggal BETWEEN :periode_awal AND :periode_akhir
        """

        params_detail = {
            "periode_awal": periode_awal,
            "periode_akhir": periode_akhir
        }

        if id_coa:
            query_detail += " AND jmd.id_coa = :id_coa"
            params_detail["id_coa"] = id_coa

        if id_cabang:
            query_detail += " AND j.id_cabang = :id_cabang"
            params_detail["id_cabang"] = id_cabang

        query_detail += """
            ORDER BY 
                COALESCE(coa.parent_id, coa.id_coa),
                coa.id_coa,
                j.tanggal ASC,
                j.id_jurnal ASC
        """

        res_detail = db.session.execute(text(query_detail), params_detail).fetchall()

        if not res_detail:
            return {
                "result": [],
                "count": 0,
                "summary": {
                    "saldo_awal": saldo_awal_value,
                    "total_debet": 0,
                    "total_kredit": 0,
                    "saldo_akhir": saldo_awal_value
                }
            }

        # ===============================
        # 4. Ambil Semua Parent Sekaligus (NO N+1 QUERY)
        # ===============================
        parent_ids = set()

        for row in res_detail:
            if row.parent_id:
                parent_ids.add(int(row.parent_id))
            else:
                parent_ids.add(int(row.id_coa))

        parent_rows = db.session.execute(
            text("""
                SELECT id_coa, nama_akun, nomor_akun
                FROM public.coa
                WHERE id_coa = ANY(:ids)
            """),
            {"ids": list(parent_ids)}
        ).fetchall()

        parent_map = {
            row.id_coa: {
                "nama_akun": row.nama_akun,
                "nomor_akun": row.nomor_akun
            }
            for row in parent_rows
        }

        # ===============================
        # 5. Build Final Data
        # ===============================
        running_balance = saldo_awal_value
        total_debit = 0
        total_kredit = 0

        final_data = []
        current_parent = None
        row_number = 1

        for row in res_detail:

            dr = float(row.debit or 0)
            cr = float(row.kredit or 0)

            running_balance += (dr - cr)
            total_debit += dr
            total_kredit += cr

            tgl_str = row.tanggal.strftime('%Y-%m-%d') if row.tanggal else ""

            parent_id = int(row.parent_id) if row.parent_id else int(row.id_coa)

            # ===============================
            # Insert Parent Jika Berubah
            # ===============================
            if current_parent != parent_id:

                parent_info = parent_map.get(parent_id)

                if parent_info:
                    final_data.append({
                        "row_num": "",
                        "id_jurnal": None,
                        "tanggal": "",
                        "nama_perusahaan": "",
                        "nama_cabang": "",
                        "nama_akun": parent_info["nama_akun"],  # <-- KAS muncul di sini
                        "nomor_akun": parent_info["nomor_akun"],
                        "keterangan": "",
                        "debit": "",
                        "kredit": "",
                        "saldo_kumulatif": "",
                        "modul": "",
                        "coa_id": parent_id,
                        "parent_id": None,
                        "isParent": True
                    })

                current_parent = parent_id

            # ===============================
            # Insert Child
            # ===============================
            final_data.append({
                "row_num": row_number,
                "id_jurnal": row.id_jurnal,
                "tanggal": tgl_str,
                "nama_perusahaan": row.nama_perusahaan,
                "nama_cabang": row.nama_cabang,
                "nama_akun": row.nama_akun,  # <-- Kas Besar
                "nomor_akun": row.nomor_akun,
                "keterangan": row.keterangan_item or row.keterangan_umum,
                "debit": dr,
                "kredit": cr,
                "saldo_kumulatif": running_balance,
                "modul": row.nama_kolom_view,
                "coa_id": row.id_coa,
                "parent_id": row.parent_id,
                "isParent": False
            })

            row_number += 1

        # ===============================
        # 6. Return
        # ===============================
        return {
            "result": final_data,
            "count": len(final_data),
            "summary": {
                "saldo_awal": saldo_awal_value,
                "total_debet": total_debit,
                "total_kredit": total_kredit,
                "saldo_akhir": running_balance
            }
        }

    def getJurnal(self):
        id_cabang = self.req("id_cabang")
        id_perusahaan = self.req("id_perusahaan")
        periode_awal = self.req("periode_awal")
        periode_akhir = self.req("periode_akhir")

        bindParams = {}
        query_clauses = []
        
        if id_cabang:
            query_clauses.append("j.id_cabang = :id_cabang")
            bindParams["id_cabang"] = id_cabang
        if id_perusahaan:
            query_clauses.append("j.id_perusahaan = :id_perusahaan")
            bindParams["id_perusahaan"] = id_perusahaan
        if periode_awal:
            query_clauses.append("j.tanggal >= :periode_awal")
            bindParams["periode_awal"] = periode_awal
        if periode_akhir:
            query_clauses.append("j.tanggal <= :periode_akhir")
            bindParams["periode_akhir"] = periode_akhir

        where_statement = " WHERE " + " AND ".join(query_clauses) if query_clauses else ""

        query = f"""
            SELECT 
                j.id_jurnal AS id,
                j.id_jurnal,
                j.tanggal,
                j.keterangan,
                p.nama AS nama_perusahaan,
                c.nama AS nama_cabang,
                cm.nama_akun AS jenis_transaksi,
                JSON_AGG(
                    jsonb_build_object(
                        'nama_akun', jd.nama_akun,
                        'debit', COALESCE(jd.debit, 0),
                        'kredit', COALESCE(jd.kredit, 0),
                        'keterangan', jd.keterangan
                    ) ORDER BY jd.id_jurnal_detail ASC
                ) AS info_jurnal
            FROM jurnal j
            INNER JOIN jurnal_detail jd ON j.id_jurnal = jd.id_jurnal
            INNER JOIN jurnal_mal jm ON j.id_jurnal_mal = jm.id_jurnal_mal
            INNER JOIN coa cm ON jm.main_coa_id = cm.id_coa
            INNER JOIN perusahaan p ON j.id_perusahaan = p.id
            LEFT JOIN cabang c ON j.id_cabang = c.id
            {where_statement}
            GROUP BY 
                j.id_jurnal, 
                j.tanggal, 
                j.keterangan, 
                p.nama, 
                c.nama, 
                cm.nama_akun
        """

        # Kembalikan langsung object paginasinya
        return PaginateV2(request=request, query=query, bindParams=bindParams).paginate()

    def detailJurnal(self, id_jurnal):
        query = f"""
            SELECT j.id_jurnal,
                j.tanggal,
                p.nama AS nama_perusahaan,
                c.nama AS nama_cabang,
                jm.id_fitur_mal,
                u.nama AS created_by,
                cm.nama_akun AS jenis_transaksi,
                j.keterangan,
                json_agg(
                    jsonb_build_object(
                        'nama_akun', coa.nomor_akun || ' - ' || coa.nama_akun,
                        'keterangan', j.keterangan,
                        'debit', COALESCE(jd.debit, 0),
                        'kredit', COALESCE(jd.kredit, 0),
                        'jenis_transaksi', sm.nama_kolom_view,
                        'created_by', u.nama
                    ) ORDER BY jd.id_jurnal_detail ASC
                ) AS info_jurnal
            FROM jurnal j
            JOIN jurnal_detail jd ON j.id_jurnal = jd.id_jurnal
            JOIN jurnal_mal jm ON j.id_jurnal_mal = jm.id_jurnal_mal
            JOIN coa cm ON jm.main_coa_id = cm.id_coa
            JOIN perusahaan p ON jm.id_perusahaan = p.id
            LEFT JOIN cabang c ON j.id_cabang = c.id
            JOIN users u ON jd.created_by = u.id
            JOIN jurnal_mal_detail jmd ON jd.id_mal_detail = jmd.id_mal_detail
            JOIN coa ON jmd.id_coa = coa.id_coa
            JOIN source_modul sm ON jmd.id_source_data = sm.id_source_data
            WHERE j.id_jurnal = :id_jurnal
            GROUP BY j.id_jurnal, j.tanggal, jm.id_fitur_mal, cm.nama_akun, p.nama, c.nama, u.id 
            ORDER BY j.id_jurnal DESC
        """
        
        result_query = self.query().setRawQuery(query).bindparams({"id_jurnal": id_jurnal}).execute().fetchone()
        if not result_query:
            return None
            
        row = result_query.result
        id_fitur_mal = row["id_fitur_mal"]
        raw_keterangan = row["keterangan"] or ""
        keterangan_detail = None

        # Helper untuk ambil ID terakhir (misal dari "ID: 144" ambil 144)
        def get_last_id(text):
            nums = re.findall(r'\d+', str(text))
            return nums[-1] if nums else "0"

        match id_fitur_mal:
            case 1:
                keterangan_detail = self.__get_keterangan_for_id_fitur_mal_1(raw_keterangan)
            case 2:
                keterangan_detail = self.__get_keterangan_for_id_fitur_mal_2(raw_keterangan)
            case 3 | 4 | 5:
                is_order_batch = "id_order_batch" in raw_keterangan
                target_id = get_last_id(raw_keterangan)
                # Panggil fungsi sesuai fitur
                if id_fitur_mal == 3: keterangan_detail = self.__get_keterangan_for_id_fitur_mal_3(target_id, is_order_batch)
                if id_fitur_mal == 4: keterangan_detail = self.__get_keterangan_for_id_fitur_mal_4(target_id, is_order_batch)
                if id_fitur_mal == 5: keterangan_detail = self.__get_keterangan_for_id_fitur_mal_5(target_id, is_order_batch)
            case 6 | 12 | 13 | 14:
                # Format: "id_setoran:1;id_faktur:10"
                parts = raw_keterangan.split(";")
                id_setoran = get_last_id(parts[0]) if len(parts) > 0 else "0"
                id_faktur = get_last_id(parts[1]) if len(parts) > 1 else "0"
                
                if id_fitur_mal == 6: keterangan_detail = self.__get_keterangan_for_id_fitur_mal_6(id_faktur, id_setoran)
                # ... dst untuk 12, 13, 14
            # ... (lanjutkan untuk case lainnya dengan get_last_id)
            case _:
                keterangan_detail = None

        row["keterangan_detail"] = keterangan_detail
        return row

    def __get_keterangan_for_id_fitur_mal_1(self, id_keterangan):
        """
        Get keterangan untuk Fitur Pembelian (1).
        Memastikan ID bersih dari string deskriptif.
        """
        # Proteksi: Ambil angka terakhir jika input berupa string deskriptif
        try:
            if isinstance(id_keterangan, str):
                clean_id = int(id_keterangan.split()[-1])
            else:
                clean_id = int(id_keterangan)
        except (ValueError, IndexError, TypeError):
            print(f"ERROR: ID Keterangan tidak valid: {id_keterangan}")
            return []

        result = (
            self.query()
            .setRawQuery(
                """
                SELECT p.nama,
                    pt.id AS transaksi_id,
                    JSONB_BUILD_OBJECT(
                            'uom_1', MAX(CASE WHEN podj.uom_level = 1 THEN ptdj.jumlah END),
                            'uom_2', MAX(CASE WHEN podj.uom_level = 2 THEN ptdj.jumlah END),
                            'uom_3', MAX(CASE WHEN podj.uom_level = 3 THEN ptdj.jumlah END)
                    )     AS qtys
                FROM purchase_transaksi pt
                        JOIN purchase_transaksi_detail ptd ON ptd.transaksi_id = pt.id
                        JOIN purchase_transaksi_detail_jumlah ptdj ON ptdj.transaksi_id = pt.id
                        JOIN purchase_order_detail_jumlah podj ON podj.id = ptdj.order_detail_jumlah_id
                        JOIN purchase_order_detail pod ON pod.id = podj.order_detail_id
                        JOIN produk p ON p.id = pod.produk_id
                WHERE pt.id = :id_keterangan
                GROUP BY p.nama, pt.id
                ORDER BY MAX(ptdj.id) DESC;
                """
            )
            .bindparams({"id_keterangan": clean_id})
            .execute()
            .fetchall()
            .get()
        )
        return result

    def __get_keterangan_for_id_fitur_mal_2(self, id_keterangan):
        """
        Get keterangan for id_fitur_mal = 2 (Penjualan)
        """
        result = (
            self.query()
            .setRawQuery(
                """
                select purchase_transaksi.no_transaksi,
                       purchase_tagihan_detail.subtotal
                from purchase_tagihan_detail
                         left join purchase_transaksi
                                   on purchase_tagihan_detail.transaksi_id = purchase_transaksi.id
                         left join purchase_tagihan
                                   on purchase_tagihan_detail.tagihan_id = purchase_tagihan.id
                         left join purchase_order
                                   on purchase_transaksi.order_id = purchase_order.id
                where purchase_tagihan.id = :id_keterangan
                """
            ).bindparams({"id_keterangan": id_keterangan})
            .execute()
            .fetchall()
            .get()
        )

        return result

    def __get_keterangan_for_id_fitur_mal_3(self, id_keterangan, is_order_batch=False):
        """
        Get keterangan for id_fitur_mal = 3 (Retur Pembelian)
        """

        query = """
                SELECT p.nama, pp.jumlah_picked
                FROM sales_order so
                         JOIN sales_order_detail sod ON so.id = sod.id_sales_order
                         JOIN produk p ON sod.id_produk = p.id
                         JOIN proses_picking pp ON pp.id_order_detail = sod.id
                """
        if is_order_batch:
            query += " WHERE so.id_order_batch = :id_keterangan"
        else:
            query += " WHERE so.id = :id_keterangan"

        result = (
            self.query()
            .setRawQuery(query)
            .bindparams({"id_keterangan": id_keterangan})
            .execute()
            .fetchall()
            .get()
        )
        return result

    def __get_keterangan_for_id_fitur_mal_4(self, id_keterangan, is_order_batch=False):
        """
        Get keterangan for id_fitur_mal = 3 (Retur Pembelian)
        """

        query = """
                SELECT p.nama, pp.jumlah_picked
                FROM sales_order so
                         JOIN sales_order_detail sod ON so.id = sod.id_sales_order
                         JOIN produk p ON sod.id_produk = p.id
                         JOIN proses_picking pp ON pp.id_order_detail = sod.id
                """
        if is_order_batch:
            query += " WHERE so.id_order_batch = :id_keterangan"
        else:
            query += " WHERE so.id = :id_keterangan"

        result = (
            self.query()
            .setRawQuery(query)
            .bindparams({"id_keterangan": id_keterangan})
            .execute()
            .fetchall()
            .get()
        )
        return result

    def __get_keterangan_for_id_fitur_mal_5(self, id_keterangan, is_order_batch=False):
        """
        Get keterangan for id_fitur_mal = 3 (Retur Pembelian)
        """

        query = """
                SELECT p.nama, sod.pieces_delivered, sod.box_delivered, sod.karton_delivered
                FROM sales_order so
                         JOIN sales_order_detail sod ON so.id = sod.id_sales_order
                         JOIN produk p ON sod.id_produk = p.id \
                """
        if is_order_batch:
            query += " WHERE so.id_order_batch = :id_keterangan"
        else:
            query += " WHERE so.id = :id_keterangan"

        result = (
            self.query()
            .setRawQuery(query)
            .bindparams({"id_keterangan": id_keterangan})
            .execute()
            .fetchall()
            .get()
        )
        return result

    def __get_keterangan_for_id_fitur_mal_6(self, id_faktur, id_setoran):
        """
        Get keterangan for id_fitur_mal = 6 (Setoran Faktur)
        """
        # Query faktur
        query_faktur = """
                       SELECT f.no_faktur

                       FROM faktur f
                       WHERE f.id = :id_faktur \
                       """

        row_faktur = (
            self.query()
            .setRawQuery(query_faktur)
            .bindparams({"id_faktur": id_faktur.strip()})
            .execute()
            .fetchall()
            .get()
        )

        return row_faktur

    def __get_keterangan_for_id_fitur_mal_7(self, id_keterangan):
        """
        Get keterangan for id_fitur_mal = 7 (Contoh Fitur Lain)
        """
        result = (
            self.query()
            .setRawQuery(
                """
                SELECT sod.uom_3,
                       sod.uom_2,
                       sod.uom_1,
                       p.nama,
                       sod.stok,
                       sod.stok_sistem,
                       SUM(sod.stok - sod.stok_sistem) AS selisih
                from stock_opname so
                         JOIN stock_opname_detail sod ON so.id_stock_opname = sod.id_stock_opname
                         JOIN produk p ON sod.id_produk = p.id
                WHERE so.id_stock_opname = :id_keterangan
                GROUP BY sod.uom_3, sod.uom_2, sod.uom_1, p.nama, sod.stok, sod.stok_sistem
                """
            )
            .bindparams({"id_keterangan": id_keterangan})
            .execute()
            .fetchall()
            .get()
        )
        return result

    def __get_keterangan_for_id_fitur_mal_8(self, id_keterangan):
        """
        Get keterangan for id_fitur_mal = 7 (Contoh Fitur Lain)
        """
        result = (
            self.query()
            .setRawQuery(
                """
                SELECT sod.uom_3,
                       sod.uom_2,
                       sod.uom_1,
                       p.nama,
                       sod.stok,
                       sod.stok_sistem,
                       SUM(sod.stok - sod.stok_sistem) AS selisih
                from stock_opname so
                         JOIN stock_opname_detail sod ON so.id_stock_opname = sod.id_stock_opname
                         JOIN produk p ON sod.id_produk = p.id
                WHERE so.id_stock_opname = :id_keterangan
                GROUP BY sod.uom_3, sod.uom_2, sod.uom_1, p.nama, sod.stok, sod.stok_sistem
                """
            )
            .bindparams({"id_keterangan": id_keterangan})
            .execute()
            .fetchall()
            .get()
        )
        return result

    def __get_keterangan_for_id_fitur_mal_9(self, id_keterangan):
        """
        Get keterangan for id_fitur_mal = 9 (Contoh Fitur Lain)
        """
        result = (
            self.query()
            .setRawQuery(
                """
                SELECT std.jumlah_diterima,
                       p.nama
                FROM stock_transfer st
                         JOIN stock_transfer_detail std ON st.id = std.id_stock_transfer
                         JOIN produk p ON std.id_produk = p.id
                WHERE st.id = :id_keterangan
                """
            )
            .bindparams({"id_keterangan": id_keterangan})
            .execute()
            .fetchall()
            .get()
        )
        return result

    def __get_keterangan_for_id_fitur_mal_10(self, id_keterangan):
        """
        Get keterangan for id_fitur_mal = 9 (Contoh Fitur Lain)
        """
        result = (
            self.query()
            .setRawQuery(
                """
                SELECT std.jumlah_diterima,
                       p.nama
                FROM stock_transfer st
                         JOIN stock_transfer_detail std ON st.id = std.id_stock_transfer
                         JOIN produk p ON std.id_produk = p.id
                WHERE st.id = :id_keterangan
                """
            )
            .bindparams({"id_keterangan": id_keterangan})
            .execute()
            .fetchall()
            .get()
        )
        return result

    def __get_keterangan_for_id_fitur_mal_11(self, id_keterangan):
        """
        Get keterangan for id_fitur_mal = 6 (Setoran Faktur)
        """
        # Query faktur
        query_faktur = """
                       SELECT pk.keterangan_pengeluaran
                       FROM pengeluaran_kasir pk
                       WHERE pk.id = :id_keterangan \
                       """

        row_faktur = (
            self.query()
            .setRawQuery(query_faktur)
            .bindparams({"id_keterangan": id_keterangan.strip()})
            .execute()
            .fetchone()
            .result
        )

        return row_faktur.get("keterangan_pengeluaran")

    def __get_keterangan_for_id_fitur_mal_12(self, id_faktur, id_setoran):
        """
        Get keterangan for id_fitur_mal = 6 (Setoran Faktur)
        """
        # Query faktur
        query_faktur = """
                       SELECT f.no_faktur

                       FROM faktur f
                       WHERE f.id = :id_faktur \
                       """

        row_faktur = (
            self.query()
            .setRawQuery(query_faktur)
            .bindparams({"id_faktur": id_faktur.strip()})
            .execute()
            .fetchall()
            .get()
        )

        return row_faktur

    def __get_keterangan_for_id_fitur_mal_13(self, id_faktur, id_setoran):
        """
        Get keterangan for id_fitur_mal = 6 (Setoran Faktur)
        """
        # Query faktur
        query_faktur = """
                       SELECT f.no_faktur

                       FROM faktur f
                       WHERE f.id = :id_faktur \
                       """

        row_faktur = (
            self.query()
            .setRawQuery(query_faktur)
            .bindparams({"id_faktur": id_faktur.strip()})
            .execute()
            .fetchall()
            .get()
        )

        return row_faktur

    def __get_keterangan_for_id_fitur_mal_14(self, id_faktur, id_setoran):
        """
        Get keterangan for id_fitur_mal = 6 (Setoran Faktur)
        """
        # Query faktur
        query_faktur = """
                       SELECT f.no_faktur

                       FROM faktur f
                       WHERE f.id = :id_faktur \
                       """

        row_faktur = (
            self.query()
            .setRawQuery(query_faktur)
            .bindparams({"id_faktur": id_faktur.strip()})
            .execute()
            .fetchall()
            .get()
        )

        return row_faktur

    def __get_keterangan_for_id_fitur_mal_15(self, id_keterangan):
        """
        Get keterangan for id_fitur_mal = 6 (Setoran Faktur)
        """
        # Query faktur
        query_faktur = """
                       SELECT pk.keterangan_pengeluaran
                       FROM pengeluaran_kasir pk
                       WHERE pk.id = :id_keterangan \
                       """

        row_faktur = (
            self.query()
            .setRawQuery(query_faktur)
            .bindparams({"id_keterangan": id_keterangan.strip()})
            .execute()
            .fetchone()
            .result
        )

        return row_faktur.get("keterangan_pengeluaran")

    def __get_keterangan_for_id_fitur_mal_16(self, id_keterangan, is_order_batch=False):
        """
        Get keterangan for id_fitur_mal = 3 (Retur Pembelian)
        """

        query = """
                SELECT p.nama, sod.pieces_delivered, sod.box_delivered, sod.karton_delivered
                FROM sales_order so
                         JOIN sales_order_detail sod ON so.id = sod.id_sales_order
                         JOIN produk p ON sod.id_produk = p.id \
                """
        if is_order_batch:
            query += " WHERE so.id_order_batch = :id_keterangan"
        else:
            query += " WHERE so.id = :id_keterangan"

        result = (
            self.query()
            .setRawQuery(query)
            .bindparams({"id_keterangan": id_keterangan})
            .execute()
            .fetchall()
            .get()
        )
        return result

    def __get_keterangan_for_id_fitur_mal_17(self, id_keterangan):
        """
        Get keterangan for id_fitur_mal = 1 (Pembelian)
        """
        result = (
            self.query()
            .setRawQuery(
                """
                SELECT p.nama,
                       po.id AS transaksi_id,
                       JSONB_BUILD_OBJECT(
                               'uom_1', MAX(CASE WHEN podj.uom_level = 1 THEN podj.jumlah END),
                               'uom_2', MAX(CASE WHEN podj.uom_level = 2 THEN podj.jumlah END),
                               'uom_3', MAX(CASE WHEN podj.uom_level = 3 THEN podj.jumlah END)
                       )     AS qtys
                FROM purchase_order po
                         JOIN purchase_order_detail pod
                              ON pod.order_id = po.id
                         JOIN purchase_order_detail_jumlah podj
                              ON podj.order_id = po.id
                         JOIN produk p
                              ON p.id = pod.produk_id
                WHERE po.id = :id_keterangan
                GROUP BY p.nama, po.id
                ORDER BY MAX(podj.id) DESC;

                """
            )
            .bindparams({"id_keterangan": id_keterangan})
            .execute()
            .fetchall()
            .get()
        )
        return result

    def __get_keterangan_for_id_fitur_mal_18(self, id_keterangan):
        """
        Get keterangan for id_fitur_mal = 1 (Pembelian)
        """
        result = (
            self.query()
            .setRawQuery(
                """
                SELECT p.nama,
                       po.id AS transaksi_id,
                       JSONB_BUILD_OBJECT(
                               'uom_1', MAX(CASE WHEN podj.uom_level = 1 THEN podj.jumlah END),
                               'uom_2', MAX(CASE WHEN podj.uom_level = 2 THEN podj.jumlah END),
                               'uom_3', MAX(CASE WHEN podj.uom_level = 3 THEN podj.jumlah END)
                       )     AS qtys
                FROM purchase_order po
                         JOIN purchase_order_detail pod
                              ON pod.order_id = po.id
                         JOIN purchase_order_detail_jumlah podj
                              ON podj.order_id = po.id
                         JOIN produk p
                              ON p.id = pod.produk_id
                WHERE po.id = :id_keterangan
                GROUP BY p.nama, po.id
                ORDER BY MAX(podj.id) DESC;

                """
            )
            .bindparams({"id_keterangan": id_keterangan})
            .execute()
            .fetchall()
            .get()
        )
        return result

    def __get_keterangan_for_id_fitur_mal_19(self, id_keterangan):
        """
        Get keterangan for id_fitur_mal = 1 (Pembelian)
        """
        result = (
            self.query()
            .setRawQuery(
                """
                SELECT p.nama,
                       pt.id AS transaksi_id,
                       JSONB_BUILD_OBJECT(
                               'uom_1', MAX(CASE WHEN podj.uom_level = 1 THEN ptdj.jumlah END),
                               'uom_2', MAX(CASE WHEN podj.uom_level = 2 THEN ptdj.jumlah END),
                               'uom_3', MAX(CASE WHEN podj.uom_level = 3 THEN ptdj.jumlah END)
                       )     AS qtys
                FROM purchase_transaksi pt
                         JOIN purchase_transaksi_detail ptd
                              ON ptd.transaksi_id = pt.id
                         JOIN purchase_transaksi_detail_jumlah ptdj
                              ON ptdj.transaksi_id = pt.id
                         JOIN purchase_order_detail_jumlah podj
                              ON podj.id = ptdj.order_detail_jumlah_id
                         JOIN purchase_order_detail pod
                              ON pod.id = podj.order_detail_id
                         JOIN produk p
                              ON p.id = pod.produk_id
                WHERE pt.id = :id_keterangan
                GROUP BY p.nama, pt.id
                ORDER BY MAX(ptdj.id) DESC;

                """
            )
            .bindparams({"id_keterangan": id_keterangan})
            .execute()
            .fetchall()
            .get()
        )
        return result

    def __get_keterangan_for_id_fitur_mal_20(self, id_keterangan):
        """
        Get keterangan for id_fitur_mal =  1 (Pembelian)
        """
        result = (
            self.query()
            .setRawQuery(
                """
                SELECT p.nama,
                       pt.id AS transaksi_id,
                       JSONB_BUILD_OBJECT(
                               'uom_1', MAX(CASE WHEN podj.uom_level = 1 THEN ptdj.jumlah END),
                               'uom_2', MAX(CASE WHEN podj.uom_level = 2 THEN ptdj.jumlah END),
                               'uom_3', MAX(CASE WHEN podj.uom_level = 3 THEN ptdj.jumlah END)
                       )     AS qtys
                FROM purchase_transaksi pt
                         JOIN purchase_transaksi_detail ptd
                              ON ptd.transaksi_id = pt.id
                         JOIN purchase_transaksi_detail_jumlah ptdj
                              ON ptdj.transaksi_id = pt.id
                         JOIN purchase_order_detail_jumlah podj
                              ON podj.id = ptdj.order_detail_jumlah_id
                         JOIN purchase_order_detail pod
                              ON pod.id = podj.order_detail_id
                         JOIN produk p
                              ON p.id = pod.produk_id
                WHERE pt.id = :id_keterangan
                GROUP BY p.nama, pt.id
                ORDER BY MAX(ptdj.id) DESC;

                """
            )
            .bindparams({"id_keterangan": id_keterangan})
            .execute()
            .fetchall()
            .get()
        )
        return result

    def __get_keterangan_for_id_fitur_mal_21(self, id_keterangan):
        """
        Get keterangan for id_fitur_mal = 2 (Penjualan)
        """
        result = (
            self.query()
            .setRawQuery(
                """
                select purchase_transaksi.no_transaksi,
                       purchase_tagihan_detail.subtotal
                from purchase_tagihan_detail
                         left join purchase_transaksi
                                   on purchase_tagihan_detail.transaksi_id = purchase_transaksi.id
                         left join purchase_tagihan
                                   on purchase_tagihan_detail.tagihan_id = purchase_tagihan.id
                         left join purchase_order
                                   on purchase_transaksi.order_id = purchase_order.id
                where purchase_tagihan.id = :id_keterangan
                """
            ).bindparams({"id_keterangan": id_keterangan})
            .execute()
            .fetchall()
            .get()
        )

        return result

    def __get_keterangan_for_id_fitur_mal_22(self, id_keterangan):
        """
        Get keterangan for id_fitur_mal = 2 (Penjualan)
        """
        result = (
            self.query()
            .setRawQuery(
                """
                select purchase_transaksi.no_transaksi,
                       purchase_tagihan_detail.subtotal,
                       purchase_transaksi.potongan
                from purchase_tagihan_detail
                         left join purchase_transaksi
                                   on purchase_tagihan_detail.transaksi_id = purchase_transaksi.id
                         left join purchase_tagihan
                                   on purchase_tagihan_detail.tagihan_id = purchase_tagihan.id
                         left join purchase_order
                                   on purchase_transaksi.order_id = purchase_order.id
                where purchase_tagihan.id = :id_keterangan
                  AND purchase_transaksi.potongan IS NOT NULL
                """
            ).bindparams({"id_keterangan": id_keterangan})
            .execute()
            .fetchall()
            .get()
        )

        return result

    def __get_keterangan_for_id_fitur_mal_23(self, id_keterangan):
        """
        Get keterangan for id_fitur_mal = 2 (Penjualan)
        """
        result = (
            self.query()
            .setRawQuery(
                """
                select purchase_transaksi.no_transaksi,
                       purchase_tagihan_detail.subtotal,
                       purchase_transaksi.potongan
                from purchase_tagihan_detail
                         left join purchase_transaksi
                                   on purchase_tagihan_detail.transaksi_id = purchase_transaksi.id
                         left join purchase_tagihan
                                   on purchase_tagihan_detail.tagihan_id = purchase_tagihan.id
                         left join purchase_order
                                   on purchase_transaksi.order_id = purchase_order.id
                where purchase_tagihan.id = :id_keterangan
                  AND purchase_transaksi.potongan IS NOT NULL
                """
            ).bindparams({"id_keterangan": id_keterangan})
            .execute()
            .fetchall()
            .get()
        )

        return result

    def __get_keterangan_for_id_fitur_mal_24(self, id_keterangan):
        """
        Get keterangan for id_fitur_mal = 6 (Setoran Faktur)
        """
        # Query faktur
        query_faktur = """
                       SELECT kb.keterangan
                       FROM kasbon_klaim kb
                       WHERE kb.id_kasbon_klaim = :id_keterangan \
                       """

        row_faktur = (
            self.query()
            .setRawQuery(query_faktur)
            .bindparams({"id_keterangan": id_keterangan.strip()})
            .execute()
            .fetchone()
            .result
        )

        return row_faktur.get("keterangan")

    def __get_keterangan_for_id_fitur_mal_25(self, id_keterangan):
        """
        Get keterangan for id_fitur_mal = 6 (Setoran Faktur)
        """
        # Query faktur
        query_faktur = """
                       SELECT kb.keterangan
                       FROM kasbon_klaim kb
                       WHERE kb.id_kasbon_klaim = :id_keterangan \
                       """

        row_faktur = (
            self.query()
            .setRawQuery(query_faktur)
            .bindparams({"id_keterangan": id_keterangan.strip()})
            .execute()
            .fetchone()
            .result
        )

        return row_faktur.get("keterangan")
