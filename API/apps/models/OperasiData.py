from  apps.query           import  DB
from  apps.helper          import  set as setResult
from  flask                import  request, abort, jsonify
from  werkzeug.exceptions  import  HTTPException
from  io                   import  StringIO
import  csv
from  apps.conn2  import  db
from apps.models import (
    Cabang,
    Customer,
    Produk,
    ProdukKategori,
    CustomerTipe,
    Principal,
    ProdukUOM,
    ProdukHargaJual,
    # Perusahaan,
    # ProdukBrand,
)

from apps.models.Perusahaan import Perusahaan
from apps.models.Wilayah import Wilayah1, Wilayah2, Wilayah3, Wilayah4
from apps.models.ProdukBrand import ProdukBrand
from apps.exceptions import ValidationException
from apps.handler import handle_error_rollback, handle_error

class OperasiData() :
    @staticmethod
    def _GetDataBy(tablename, column="*", clause="", params=None) :
        """
            Mendapatkan Data dari Tabel Berdasarkan Clause tertentu.

            @param  `tablename`    (str)   Nama Tabel yang ingin dioperasikan.
            @param  `column`       (str)   Kolom yang ingin diambil datanya.
            @param  `clause`       (str)   Clause untuk memfilter data.
            @result `list`         List of Dict berisi Data yang diambil.
        """
        
        query = f"SELECT {column} FROM {tablename} {clause}"
        try:
          result = DB(request).setRawQuery(query).bindparams(params).execute().fetchall().get()
        except Exception as e:
          print("====================== Show Error _GetDataBy =======================\n", str(e))
          return None
        return result
    
    @staticmethod
    def _GetWhereBindParams(data = None, clauses = None):
      """
      data: dict parameter input, mis. {"id_faktur": [1,2], "tanggal_awal": "2024-01-01"}
      clauses: dict peta key->kondisi, mis.
          {
            "id_faktur": "faktur.id IN :id_faktur",
            "tanggal_awal": "sales_order.tanggal_faktur >= :tanggal_awal",
            "tanggal_akhir": "sales_order.tanggal_faktur <= :tanggal_akhir",
          }
      return: (where_sql, bind_params)
        where_sql: string tanpa prefix 'WHERE'
        bind_params: dict untuk bindparams()
      """
      if not isinstance(data, dict) or not isinstance(clauses, dict) or not clauses:
          return "", {}

      parts = []
      bind = {}
      for key, condition in clauses.items():
          if key in data and data[key] not in (None, "", []):
              parts.append(condition)
              bind[key] = data[key]

      where_sql = " AND ".join(parts)
      return where_sql, bind

    def _GetNotListedId(source_ids=None, target_ids=None, keep_order=True):
      source_ids = list(source_ids or [])
      pajak_set = list(target_ids or [])

      if keep_order:
          # preservasi urutan source_ids
          not_in_pajak = [x for x in source_ids if x not in pajak_set]
          same_ids = [x for x in source_ids if x in pajak_set]
      else:
          faktur_set = set(source_ids)
          not_in_pajak = list(faktur_set - pajak_set)
          same_ids = list(faktur_set & pajak_set)

      return not_in_pajak, same_ids
    
    @staticmethod
    def _norm(v):
        try:
          return int(v)
        except Exception:
          return v
    
    @staticmethod
    @handle_error_rollback
    def _upsert_product(data_list, existing_data, column, model):
        data_list = list(data_list or [])
        if not data_list:
          return
            
        existing_map = {getattr(d, column): d for d in existing_data}
            # print("=============== Show existing_map ===============\n", existing_map)

        for data in data_list:
          key = data.get(column)
          if key in (None, "", []):
                    # Lewati baris tanpa key
            continue
                # print("=============== Show key ===============\n", key)
          if key in existing_map:

                    # Update existing record
            existing_record = existing_map[key]
            for attr, value in data.items():
              print("=============== Show attr value ===============\n", attr, value)
              print("=============== Show type Attr ===============\n", type(attr))
              if attr == column:
                continue
              if hasattr(model, str(attr)):
                setattr(existing_record, attr, (None if value == "" else value))
              # print("=============== Show data update ===============\n", data)
                    # print("=============== Updated existing record ===============", existing_record)
          else:
                    # Insert new record
            payload = {
              k: (None if v == "" else v)
              for k, v in data.items()
              if hasattr(model, k)
            }
                    # print("=============== Show data insert ===============\n", payload)
                    # print("=============== Inserting new record with payload ===============", payload)

            if column in payload:
              payload[column] = key
            pass
            db.session.add(model(**payload))
          print("=============== The new existing map ===============", existing_map)
          db.session.commit()
          return True
        # try:
        # except Exception as e:
        #     db.session.rollback()
        #     raise Exception("Kesalahan format data saat upsert", e)
        
    @staticmethod
    def _check_wilayah(data):
        ids1, ids2, ids3, ids4 = set(), set(), set(), set()
        for row in data:
            v1 = OperasiData._norm(row.get('id_wilayah1'))
            v2 = OperasiData._norm(row.get('id_wilayah2'))
            v3 = OperasiData._norm(row.get('id_wilayah3'))
            v4 = OperasiData._norm(row.get('id_wilayah4'))
            if v1 not in (None, "", []):
                ids1.add(v1)
            if v2 not in (None, "", []):
                ids2.add(v2)
            if v3 not in (None, "", []):
                ids3.add(v3)
            if v4 not in (None, "", []):
                ids4.add(v4)

        existing1 = Wilayah1.find_by(id=list(ids1)) if ids1 else []
        existing2 = Wilayah2.find_by(id=list(ids2)) if ids2 else []
        existing3 = Wilayah3.find_by(id=list(ids3)) if ids3 else []
        existing4 = Wilayah4.find_by(id=list(ids4)) if ids4 else []

        existing_map1 = {getattr(d, 'id') for d in existing1}
        existing_map2 = {getattr(d, 'id') for d in existing2}
        existing_map3 = {getattr(d, 'id') for d in existing3}
        existing_map4 = {getattr(d, 'id') for d in existing4}
  
        missing = {
            'id_wilayah1': sorted(list(ids1 - existing_map1)),
            'id_wilayah2': sorted(list(ids2 - existing_map2)),
            'id_wilayah3': sorted(list(ids3 - existing_map3)),
            'id_wilayah4': sorted(list(ids4 - existing_map4)),
        }

        if any(missing[k] for k in missing):
            list_missing = ", ".join(
                [f"{k}={v}" for k, v in missing.items() if v])
            raise Exception(f"Terdapat id wilayah yang tidak diketahui")
        
        return True
    
    def _check_unique_value(data_list, column):
        # existing_values = {getattr(d, column) for d in existing_data}
        actual_values = []
        for data in data_list:
            value = data.get(column)

            actual_values.append(value)
        
        duplicate = set([x for x in actual_values if actual_values.count(x) > 1])
        
        print("=============== Show data_list ===============\n", sorted(actual_values))
        if len(duplicate) > 0 :
          # duplicate
          printed_duplicate = ", ".join(map(str, duplicate))
          raise ValidationException(f"Ditemukan nilai kembar pada kolom: '{column}' dengan nilai: {printed_duplicate}")
        return True
    
    @handle_error
    def bulk_insert(table) :
        """
            Bulk Insert dengan Menggunakan File CSV.

            @param  `table`  (str)    Nama Tabel yang ingin dioperasikan "Insert".
            @param  `file`   (blob)   File dengan ekstensi CSV yang berisi Data.
            @result `dict`   Success Message atau Error Message.
        """
        
        # Menyimpan File yang Diupload.
        file = request.files['file'] 

        # Mengekstraksi Raw Content dari File.                  
        fileContent = file.stream.read().decode('utf-8') 

        # Merubah Raw Content Menjadi OrderedDict.
        data = csv.DictReader(StringIO(fileContent), delimiter=',')

        # Menyisipkan Data dari Data csvDictReader
        # dan Menyimpan Baris-baris `Values`.
        fields = None
        data = list(data)
        list_unique = []

        print("====================== Show data sample =======================\n", data[0] if len(data) > 0 else "No Data")
            
        dict_model = {
            'cabang'          : Cabang,
            'customer_tipe'   : CustomerTipe,
            'perusahaan'      : Perusahaan,
            'principal'       : Principal,
            'produk'          : Produk,
            'customer'        : Customer,
            'produk_brand'    : ProdukBrand,
            'produk_kategori' : ProdukKategori,
        }

        dict_unique_column = {
            'cabang'          : 'nama',
            'customer_tipe'   : 'kode',
            'perusahaan'      : 'kode',
            'principal'       : 'kode',
            'customer'        : 'kode',
            'produk'          : 'nama',
            'produk_brand'    : 'nama',
            'produk_kategori' : 'nama',
        }
        
        model = dict_model.get(table.lower())
        unique_key = dict_unique_column.get(table.lower())
        print('====================== Show model =======================\n', model)
        print('====================== Show unique_key =======================\n', unique_key)
        for row in data:
            # print("====================== Show row data =======================\n", row)
            # list_unique.append(OperasiData._norm(row.get(unique_key)))
            list_unique.append(row.get(unique_key))
        print('====================== Show list_unique =======================\n', list_unique)
        if model is None :
            raise ValidationException("Model tidak ditemukan untuk tabel: " + table)

        if table.lower() == 'cabang' or table.lower() == 'perusahaan' or table.lower() == 'principal' :
            OperasiData._check_wilayah(data)

        # print type model
        existing_data = model.find_by(**{unique_key: list_unique})
        column = model.get_column_map()
        try:
           pass
        except Exception as e:
           print("====================== Show Error Model =======================\n", str(e))
          #  return jsonify(str(e)), 500
        print('====================== Show existing_data =======================\n', existing_data)
        OperasiData._check_unique_value(data, unique_key)
        print("====================== Show old data =======================\n", data)
        new_data = [
                {k: v for k, v in item.items() if k != "id"}
                for item in data
            ]
        print("====================== Show new data =======================\n", new_data)

        result = OperasiData._upsert_product(new_data, existing_data, model=model, column=unique_key)

        print("====================== Show result upsert =======================\n", result)
        
        return setResult({"message" : "Data Successfully Added"}) 
        # try:
        # except Exception as e:
        #     print("====================== Show Error Model =======================\n", str(e))
        #     return jsonify(str(e)), 500