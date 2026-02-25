from .BasePajak import BasePajak
from apps.services.Pajak.UtilPajak import UtilPajak
from flask import request, jsonify
from apps.services.Faktur import BaseFaktur
from apps.lib.helper import GetWhereBindParams, datetime_now, join_into
class FinalFakturPajak(BasePajak):
  def __init__(self):
    super().__init__()
    self.status_faktur_pajak = {
      "draft": 0,
      "sudah_export": 1,
      "approved": 2,
      "canceled": 3,
      "amanded": 4
    }

  def _mk_where(self, params: dict, conditions: dict):
        where, bind = GetWhereBindParams(params, conditions)
        return (f"WHERE {where}" if where else ""), bind
  
  def GetFinalListFaktur(self):
    try:
      where, bindParams = self.poolRequest(self.basefilterfaktur_condition)
      cleaned_where = [cond.strip() for cond in where.split(" and") if cond.strip()]
      base_conditions = ["faktur.status_faktur_pajak = 2"]
      if cleaned_where:
        base_conditions = cleaned_where + base_conditions

      where_clauses = "WHERE " + " AND ".join([c for c in base_conditions if c])
      
      rows = UtilPajak().GetDataFakturTable(where_clauses, bindParams)

      return jsonify({
        'success': True,
        'message': 'Berhasil mendapatkan data faktur',
        'data': rows
      })
    except Exception as e:
      return jsonify({
        'success': False,
        'message': str(e)
      }), 500
    
  def GetFakturByFile(self):
      try:
        body = self.req('no_faktur_arr')
        if not body or len(body) < 1:
          raise ValueError("No faktur is required!")
        conditions = {
          "no_faktur_arr": "faktur.no_faktur in :no_faktur_arr",
        }
        
        where, bindParams = self.poolRequest(conditions)
        no_faktur_arr = [i.strip() for i in bindParams.get('no_faktur_arr').split(",")]
        bindParams['no_faktur_arr'] = no_faktur_arr
        cleaned_where = [cond.strip() for cond in where.split(" and") if cond.strip()]
        where_clauses = "WHERE " + " AND ".join([c for c in cleaned_where if c])
      
        rows = UtilPajak().GetDataFakturTable(where_clauses, bindParams)

        if len(rows) < 1:
          raise ValueError("No faktur found in database")

        return jsonify({
                'success': True,
                'message': 'Berhasil mendapatkan data faktur',
                'data': rows
              })
      except Exception as e:
         return jsonify({
           'success': False,
           'message': str(e)
         }), 500
      
  def AddDataToPajak(self):
    """
    Upsert data pajak dari body (list dict) berdasarkan no_faktur.
    - Menentukan status_faktur_pajak (draft / approved dll).
    - Mengambil baris faktur yang belum ada di pajak (insert).
    - Mengambil baris yang sudah ada (update).
    - Update juga tabel faktur (status_faktur_pajak = 2).
    """
    try:
      body = request.get_json() or []
      if not body:
        raise ValueError("Data tidak boleh kosong!")

      # Kumpulkan no_faktur valid
      no_faktur_all = [r["no_faktur"] for r in body if r.get("no_faktur")]
      if not no_faktur_all:
        raise ValueError("Field no_faktur kosong!")

      # Ambil yang sudah ada di pajak
      clause_pajak = {"no_faktur": "pajak.no_faktur in :no_faktur"}
      existing_rows = BasePajak().GetDataPajakBy(
        clauses_data={"no_faktur": no_faktur_all},
        clauses=clause_pajak
      ) or []
      existing_set = {r["no_faktur"] for r in existing_rows}

      # Pisahkan untuk insert / update
      to_insert = [nf for nf in no_faktur_all if nf not in existing_set]
      to_update = list(existing_set)

      # Helper mapping status
      def map_status(raw, has_nsfp):
        key = (raw or "").lower().replace(" ", "_")
        return self.status_faktur_pajak.get(key, 2 if has_nsfp else 1)

      now = datetime_now()

      rows_for_upsert = []

      # INSERT: ambil data dasar faktur lalu merge body (join nsfp/dpp/pajak dll)
      if to_insert:
        clause_faktur = {"no_faktur": "faktur.no_faktur in :no_faktur"}
        where_faktur, bind_faktur = self._mk_where({"no_faktur": to_insert}, clause_faktur)
        base_rows = UtilPajak().GetDataPajakNotFromPajak(where_faktur, bind_faktur) or []
        merged_insert = join_into(base_rows, body, "no_faktur",
                                  ["nsfp", "dpp", "pajak", "subtotal_penjualan", "status_faktur",
                                   "dpp_csv", "ppn_csv", "hpp_csv"])
        for r in merged_insert:
          status_fp = map_status(r.get("status_faktur"), r.get("nsfp") is not None)
          # Override numeric bila approved
          dpp = int(r.get("dpp", 0))
          pajak_val = int(r.get("pajak", 0))
          subtotal_penjualan = int(r.get("subtotal_penjualan", 0))
          if status_fp == 2:  # approved
            dpp = int(r.get("dpp_csv", dpp))
            pajak_val = int(r.get("ppn_csv", pajak_val))
            subtotal_penjualan = int(r.get("hpp_csv", subtotal_penjualan))
          rows_for_upsert.append({
            "no_faktur": r["no_faktur"],
            "nsfp": r.get("nsfp"),
            "dpp": dpp,
            "pajak": pajak_val,
            "subtotal_penjualan": subtotal_penjualan,
            "status_faktur_pajak": status_fp,
            "tanggal_import_pajak": now
          })

      # UPDATE: siapkan baris dari body langsung
      if to_update:
        body_update = [r for r in body if r.get("no_faktur") in to_update]
        for r in body_update:
          status_fp = map_status(r.get("status_faktur"), r.get("nsfp") is not None)
          dpp = int(r.get("dpp", 0))
          pajak_val = int(r.get("pajak", 0))
            # Gunakan nilai CSV bila approved
          subtotal_penjualan = int(r.get("subtotal_penjualan", 0))
          if status_fp == 2:
            dpp = int(r.get("dpp_csv", dpp))
            pajak_val = int(r.get("ppn_csv", pajak_val))
            subtotal_penjualan = int(r.get("hpp_csv", subtotal_penjualan))
          rows_for_upsert.append({
            "no_faktur": r["no_faktur"],
            "nsfp": r.get("nsfp"),
            "dpp": dpp,
            "pajak": pajak_val,
            "subtotal_penjualan": subtotal_penjualan,
            "status_faktur_pajak": status_fp,
            "tanggal_import_pajak": now
          })

      if not rows_for_upsert:
        return jsonify({
          "success": True,
            "message": "Tidak ada baris untuk diproses",
            "data": None
        })

      # Upsert pajak (no_faktur unik)
      upsert_summary = BasePajak().UpsertPajak(
        data=rows_for_upsert,
        conflict_on="no_faktur",
        update_cols=["nsfp", "dpp", "pajak", "subtotal_penjualan",
                     "status_faktur_pajak", "tanggal_import_pajak"],
        return_summary=True
      )

      status_dict = {"amanded": 0, "canceled": 0}
      for nf in body:
        print("Updating faktur:", nf['no_faktur'], "to status: ", nf.get("status_faktur_pajak"))
        raw = (nf.get("status_faktur_pajak") or "").lower().replace(" ", "_")
        if raw in status_dict:
          status_dict[raw] += 1
        key_status = self.status_faktur_pajak.get(nf.get("status_faktur_pajak").lower().replace(" ", "_"))
        BaseFaktur().UpdateFakturBy(
          clauses_data={"no_faktur": nf['no_faktur']},
          clauses={"no_faktur": "faktur.no_faktur = :no_faktur"},
          data={"status_faktur_pajak": key_status}
        )

      return jsonify({
        "success": True,
        "message": "Berhasil memproses upsert pajak",
        "data": status_dict
      })
    except Exception as e:
      print("AddDataToPajak error:", e)
      return jsonify({
        "success": False,
        "message": str(e)
      }), 500