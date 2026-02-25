from apps.services.BaseServices import BaseServices
from apps.models.pajak import pajak
from sqlalchemy.exc import SQLAlchemyError
from apps import native_db
from sqlalchemy import text as sa_text
from apps.lib.helper import GetWhereBindParams
from apps.lib.helper import datetime_now
class BasePajak(BaseServices):
    def __init__(self):
        super().__init__()
        self.allowed_columns = [
            "id_faktur", "id_perusahaan", "id_cabang", 
                              "no_faktur", "nsfp", "nama_fakturist", 
                              "tanggal_faktur", "subtotal_penjualan", "total_penjualan",
                              "subtotal_diskon", "dpp", "pajak", "keterangan_pajak",
                              "tanggal_import_pajak", "tanggal_export_pajak",
                              "export_pajak", "tanggal_lapor", "status_faktur_pajak",
        ]

      # Hanya dipake untuk menampilkan 2 view untuk draft faktur pajak dan final faktur pajak.
      # Pastikan kalau make harus menggunakan kondisi query yang sama
        self.basefilterfaktur_condition = {
          "id_principal"  : "principal.id = :id_principal",
          "id_perusahaan" : "perusahaan.id = :id_perusahaan",
          "id_cabang"     : "cabang.id = :id_cabang",
          "id_customer"   : "customer.id = :id_customer",
          "tanggal_faktur_start": "sales_order.tanggal_faktur >= :tanggal_faktur_start",
          "tanggal_faktur_end": "sales_order.tanggal_faktur <= :tanggal_faktur_end",
        }

    def poolRequest(self, conditions):
        where_clauses = []
        bindParams = {}

        for key, condition in conditions.items():
            value = self.req(key)
            if value:
                where_clauses.append(condition)
                bindParams[key] = value

        where = " and ".join(where_clauses)
        final_where_clause = f"{where} and" if len(where) else where

        return final_where_clause, bindParams
    
    def _normalize_bulk_rows(self, payload):
        rows = payload if isinstance(payload, (list, tuple, set)) else [payload]
        if not rows:
            return [], []
        
        cols = set()
        for r in rows:
            cols |= (set(r.keys()) & set(self.allowed_columns))
        cols = list(cols)
        if not cols:
            return [], []
        
        normalized_rows = []
        for r in rows:
            normalized_rows.append({col: r.get(col, None) for col in cols})
        return cols, normalized_rows

    def GetPajak(self):
        try:
            # pass
            query = f"""
                select * from pajak
            """
            rows = (
                self.query()
                .setRawQuery(query)
                .execute()
                .fetchall()
                .get()
            )
            return rows
        except Exception as e:
            print(e)
            return False

    def GetPajakById(self, pajak_id):
        try:
            conditions = {
                "pajak_id": "id = :pajak_id"
            }
            query = f"""
                select * from pajak
                where {conditions}
                """
            rows = (
                self.query()
                .setRawQuery(query)
                .bindparams({"pajak_id": int(pajak_id)})
                .execute()
                .fetchone()
                .get()
            )
            return rows or {}
        except Exception as e:
            print(e)
            return False
    
    def InsertPajak(self, data, chunk_size=500):
        try:
            cols, rows = self._normalize_bulk_rows(data)
            if not cols or not rows:
                return False
            
            columns = ', '.join(cols)
            values = ', '.join([f':{col}' for col in cols])

            query = f"""
                INSERT INTO pajak 
                  ({columns})
                VALUES
                  ({values})
                """
            
            total = 0
            if len(rows) < chunk_size:
                for i in rows:
                    (self.query()
                     .setRawQuery(query)
                     .bindparams(i)
                     .execute())
                return len(rows)
            
            with native_db.engine.begin() as conn:
                for i in range(0, len(rows), chunk_size):
                    chunk = rows[i:i + chunk_size]
                    result = conn.execute(
                        sa_text(query),
                        chunk
                    )
                    total += len(chunk)

            return total
        except Exception as e:
            print(e)
            return False
        
    def UpdatePajakBy(self, clauses_data={}, clauses={}, data={}):
        try:
            where_clauses, bindParams = GetWhereBindParams(clauses_data, clauses)
            if not bindParams or not where_clauses:
                return None
            set_parts = []
            valueBindParams = {}
            for key, value in data.items():
                placeholder = f"{key}"
                set_parts.append(f"{key} = :{placeholder}")
                valueBindParams[placeholder] = value

            set_value = ', '.join(set_parts)
            where_clause = f"""WHERE {where_clauses}"""
            query = f"""
              UPDATE pajak
              SET {set_value}  
              {where_clause}
             """
            print("query update pajak:", query)
            params = {**bindParams, **valueBindParams}
            print("get params:", params)
            self.query().setRawQuery(query).bindparams(params).execute()
            return True
        except Exception as e:
            print(e)
            return False
        
    def DeletePajak(self, pajak_id):
        try:
            conditions = "WHERE id = :id"
            query = f"""
                DELETE FROM pajak
                {conditions}
            """
            self.query().setRawQuery(query).bindparams({"id": int(pajak_id)}).execute()
            return True
        except Exception as e:
            print(e)
            return False
        
    def UpsertPajak(
        self,
        data,
        conflict_on="no_faktur",         # kolom unik; bisa string atau list[str]
        update_cols="all",                # "all" atau list[str] kolom yang di-update saat conflict
        chunk_size=500,                   # ukuran batch untuk payload besar
        do_nothing=False,                 # True => ON CONFLICT DO NOTHING
        touch_timestamp=True,             # True => set tanggal_import_pajak = now() untuk setiap baris
        return_summary=False              # True => kembalikan ringkasan inserted/updated
    ):
        """
        Upsert (insert/update) data ke tabel pajak.
        Prasyarat: kolom 'conflict_on' punya constraint UNIQUE/PRIMARY KEY (contoh: no_faktur).

        Param:
        - data: dict atau list[dict]
          Baris yang akan di-upsert. Kolom di luar allowed_columns akan diabaikan.
        - conflict_on: str | list[str]
          Target konflik ON CONFLICT. Default 'no_faktur'. Bisa komposit, mis. ['id_perusahaan','no_faktur'].
        - update_cols: "all" | list[str]
          Kolom yang di-update saat terjadi konflik:
          - "all": semua kolom insert (kecuali kolom konflik) akan di-set ke EXCLUDED.kolom.
          - list: hanya kolom yang disebut yang di-update (harus subset dari kolom insert).
        - chunk_size: int
          Ukuran batch executemany untuk payload sedang-besar.
        - do_nothing: bool
          Jika True, konflik diabaikan (DO NOTHING).
        - touch_timestamp: bool
          Jika True, isi/override tanggal_import_pajak dengan datetime_now() pada setiap baris (insert maupun update).
        - return_summary: bool
          Jika True, method menghitung jumlah inserted vs updated (khusus PostgreSQL) dengan RETURNING (xmax=0).

        Return:
        - Jika return_summary=True => dict: { 'processed': int, 'inserted': int, 'updated': int }
        - Jika return_summary=False => int: total baris yang diproses.
        - False jika gagal.
        """
        try:
            # Normalisasi input
            cols, rows = self._normalize_bulk_rows(data)
            if not cols or not rows:
                return False

            # Tambahkan timestamp jika diminta
            if touch_timestamp:
                if "tanggal_import_pajak" not in cols and "tanggal_import_pajak" in self.allowed_columns:
                    cols.append("tanggal_import_pajak")
                now = datetime_now()
                for r in rows:
                    r["tanggal_import_pajak"] = now

            # Susun bagian INSERT
            columns_sql = ", ".join(cols)
            values_sql = ", ".join([f":{c}" for c in cols])

            # Susun ON CONFLICT target
            conflict_cols = [conflict_on] if isinstance(conflict_on, str) else list(conflict_on or [])
            conflict_sql = ", ".join(conflict_cols)

            # Susun bagian DO UPDATE SET (kecuali jika DO NOTHING)
            set_sql = ""
            if not do_nothing:
                if update_cols == "all":
                    update_list = [c for c in cols if c not in conflict_cols]
                else:
                    update_list = [c for c in (update_cols or []) if c in cols and c not in conflict_cols]

                if update_list:
                    set_assign = [f"{c} = EXCLUDED.{c}" for c in update_list]
                    set_sql = "DO UPDATE SET " + ", ".join(set_assign)
                else:
                    # Tidak ada kolom untuk di-update, fallback DO NOTHING
                    do_nothing = True

            on_conflict_sql = f"ON CONFLICT ({conflict_sql}) DO NOTHING" if do_nothing else f"ON CONFLICT ({conflict_sql}) {set_sql}"

            # (Opsional) RETURNING untuk ringkasan insert/update
            returning_sql = " RETURNING (xmax = 0) AS inserted" if return_summary else ""

            sql = f"""
                INSERT INTO pajak ({columns_sql})
                VALUES ({values_sql})
                {on_conflict_sql}
                {returning_sql}
            """

            # Eksekusi
            total = 0
            inserted = 0
            updated = 0

            # Payload kecil
            if len(rows) <= chunk_size:
                if return_summary:
                    with native_db.engine.begin() as conn:
                        res = conn.execute(sa_text(sql), rows)
                        # PostgreSQL: (xmax = 0) TRUE -> inserted, FALSE -> updated
                        flags = [bool(m["inserted"]) for m in res.mappings().all()]
                        total = len(flags)
                        inserted = sum(1 for f in flags if f)
                        updated = total - inserted
                else:
                    for r in rows:
                        (self.query().setRawQuery(sql).bindparams(r).execute())
                    total = len(rows)

                return {"processed": total, "inserted": inserted, "updated": updated} if return_summary else total

            # Payload sedang-besar: batching executemany
            with native_db.engine.begin() as conn:
                for i in range(0, len(rows), chunk_size):
                    batch = rows[i:i + chunk_size]
                    res = conn.execute(sa_text(sql), batch)
                    if return_summary:
                        flags = [bool(m["inserted"]) for m in res.mappings().all()]
                        total += len(flags)
                        inserted += sum(1 for f in flags if f)
                        updated += len(flags) - sum(1 for f in flags if f)
                    else:
                        total += len(batch)

            return {"processed": total, "inserted": inserted, "updated": updated} if return_summary else total

        except Exception as e:
            print("UpsertPajak error:", e)
            return False

    def GetDataPajakBy(self, clauses_data, clauses):
        try:
            where_clauses, bindParams = GetWhereBindParams(clauses_data, clauses)
            if not bindParams:
                return None
            query = f"""
                select * from pajak
                where {where_clauses}
                """
            row = (
                self.query()
                .setRawQuery(query)
                .bindparams(bindParams)
                .execute()
                .fetchall()
                .get()
            )
            return row
        except Exception as e:
            print("error get data pajak by:", str(e))
            return None