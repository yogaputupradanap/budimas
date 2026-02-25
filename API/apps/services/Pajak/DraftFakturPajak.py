from apps.lib.paginate import Paginate
from flask import request, jsonify
from .BasePajak import BasePajak
import xml.etree.ElementTree as ET
from flask import Response
from apps.services.Perusahaan import Perusahaan
from apps.services.Faktur import BaseFaktur
from apps.lib.helper import   GetWhereBindParams, datetime_now
from apps.services.Pajak.UtilPajak import UtilPajak
class DraftFakturPajak(BasePajak):
  def __init__(self):
    super().__init__()

  def _mk_where(self, params: dict, conditions: dict):
        where, bind = GetWhereBindParams(params, conditions)
        return (f"WHERE {where}" if where else ""), bind

  def GetDraftListFaktur(self):
    try:
      where, bindParams = self.poolRequest(self.basefilterfaktur_condition)
      cleaned_where = [cond.strip() for cond in where.split(" and") if cond.strip()]
      base_conditions = ["COALESCE(faktur.status_faktur_pajak, 0) != 2", "COALESCE(faktur.status_faktur, 0) != 4"]
      # base_conditions = ["1=1"]
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
  
  def GetDraftDetailFaktur(self, id_faktur):
      try:
        conditions = {
            "id_faktur": "faktur.id = :id_faktur",
        }

        dict_param = {"id_faktur": id_faktur}
        where_clauses_base, bind_params_base = self._mk_where(dict_param, conditions)
        filterdata = UtilPajak().GetDataFilterDetailFaktur(where_clauses_base, bind_params_base)
        
        where_clauses_detail, bind_params_detail = self._mk_where(dict_param, conditions)
        tabledata = UtilPajak().GetDataDetailFakturTable(where_clauses_detail, bind_params_detail)

        return jsonify({
           'success': True,
            'message': 'Berhasil mendapatkan data detail faktur',
            'data': {
              'tabledata': tabledata,
              'filterdata': filterdata
            }
          })
      except Exception as e:
         return jsonify({
           'success': False,
           'message': str(e)
         }), 500

  def ExportPajakXml(self):
      try:
        conditions = {
            "id_faktur" : "faktur.id in :id_faktur",
         }

        where, bindParams = self.poolRequest(conditions)
        id_faktur_arr = [int(i) for i in bindParams.get('id_faktur').split(",")]
        bindParams['id_faktur'] = id_faktur_arr
        cleaned_filter = [cond.strip() for cond in where.split(" and") if cond.strip()]
        where_clauses = "WHERE " + " AND ".join([c for c in cleaned_filter if c])
        
        rows = UtilPajak().GetDataForExportFaktur(where_clauses, bindParams)

        perusahaan = Perusahaan().GetPerusahaanBy("PT Budimas Makmur Mulia")
        if(len(perusahaan) < 1):
           raise Exception("Data perusahaan tidak ditemukan")
        perusahaan = perusahaan[0]
        
        chunk_size = 300
        details = []
        for i in range(0, len(id_faktur_arr), chunk_size):
            chunk = id_faktur_arr[i:i + chunk_size]
            where_clauses_detail = "WHERE faktur.id IN :id_faktur_arr"
            bindParams_detail = {"id_faktur_arr": tuple(chunk)}
            items = UtilPajak().GetDataDetailXmlFakturTable(where_clauses_detail, bindParams_detail)
            if not items:
               continue
            details.extend(items)

        print("Show detail items for export:", details)
        print("Show rows for export:", rows)
        print("Show perusahaan data for export:", perusahaan)
        xml = UtilPajak().ConvertToXMLFaktur(rows, details, perusahaan)

        if not xml or len(xml) < 1:
           raise Exception("Gagal membuat data XML faktur pajak")
        
        # BaseFaktur().UpdateFakturBy(clauses=conditions, clauses_data=bindParams, data={"status_faktur_pajak": 1, "tanggal_export_pajak": datetime_now()})
        # print("Update status faktur terkini berhasil!")
        clauses_pajak = {
          "id_faktur": "id_faktur in :id_faktur"
        }
        data_from_pajak_ids = []
        id_faktur_pajak = {
          "id_faktur": id_faktur_arr
        }
        data_from_pajak = BasePajak().GetDataPajakBy(clauses=clauses_pajak, clauses_data=id_faktur_pajak)
        if len(data_from_pajak) > 0:
           data_from_pajak_ids = [d.get("id_faktur") for d in data_from_pajak if d.get("id_faktur")]
        not_listed_faktur_ids, same_id = UtilPajak()._GetNotListedIdfaktur(id_faktur_arr, data_from_pajak_ids)
        id_faktur_dict = {
           "id_faktur": not_listed_faktur_ids
        }
        rows_pajak = UtilPajak().GetDataPajakNotFromPajak(where_clauses, id_faktur_dict)

        if len(not_listed_faktur_ids) > 0:
           rows_pajak = [
              {**row, "tanggal_export_pajak": datetime_now(), "status_faktur_pajak": 1} for row in rows_pajak
           ]
           BasePajak().InsertPajak(rows_pajak)
        if len(same_id) > 0:
           update_id_faktur = {"id_faktur": tuple(same_id)}
           BasePajak().UpdatePajakBy(update_id_faktur, clauses_pajak, {"tanggal_export_pajak": datetime_now()})
        BaseFaktur().UpdateFakturBy(clauses_data=id_faktur_pajak, clauses=conditions, data={"status_faktur_pajak": 1})
        return Response(xml, mimetype='application/xml')
      except Exception as e:
         print("error export pajak xml:", str(e))
         return jsonify({
           'success': False,
           'message': str(e)
         }), 500
      