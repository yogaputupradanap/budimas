from typing import Dict, List, Tuple, Any, Callable
from io import StringIO
import csv
import re 
from flask import request, jsonify
from werkzeug.exceptions import HTTPException

from apps.conn2 import db
from apps.query import DB
from apps.helper import set as setResult

from apps.models import (
    Cabang,
    Customer,
    CustomerTipe,
    Principal,
    ProdukKategori,
    Armada,
    Plafon,
    UserSales,
    SalesTipe,
    User
)
from apps.models.Produk import Produk
from apps.models.Perusahaan import Perusahaan
from apps.models.Wilayah import Wilayah1, Wilayah2, Wilayah3, Wilayah4
from apps.models.ProdukBrand import ProdukBrand

from apps.services.product.ProdukUOMServices import ProdukUOMServices
from apps.services.product.ProdukHargaJualServices import ProdukHargaJualServices
from apps.services.plafon.PlafonJadwalServices import PlafonJadwalServices
from apps.services.sales.SalesPrincipalAssignmentServices import SalesPrincipalAssignmentServices
from werkzeug.security import generate_password_hash

from apps.exceptions import ValidationException
from apps.handler import handle_error

import time  # Pastikan di-impor di atas file
import random # Pastikan di-impor di atas file


# ======================================================================
# Helper Functions
# ======================================================================
DEBUG = True
def _debug(*args):
    if DEBUG:
        print(*args)

def _norm(v):
    try:
        return int(v)
    except Exception:
        return v
    
def _noneify(value):
    # '' | '   ' | 'NULL' -> None
    if value is None:
        return None
    if isinstance(value, str):
        s = value.strip()
        if s == "" or s.upper() == "NULL":
            return None
        return value
    return value

def _noneify_dict(d: dict) -> dict:
    return {k: _noneify(v) for k, v in (d or {}).items()}

def is_required(value: Any, col_name: str) -> str | None:
    """Validator: Memastikan nilai tidak None atau string kosong."""
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return f"Kolom '{col_name}' wajib diisi."
    return None

def matches_regex(pattern: str, custom_msg: str = None):
    """
    Factory: Membuat validator untuk mencocokkan pola Regex tertentu.
    Contoh pattern email: r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    """
    # Compile pattern sekali saja agar performa lebih cepat
    compiled_pattern = re.compile(pattern)

    def validator(value: Any, col_name: str) -> str | None:
        # Jika kosong, kita anggap lolos (biarkan is_required yang handle wajib/tidaknya)
        if value in (None, ""):
            return None
        
        # Cek apakah value string cocok dengan pattern
        if not compiled_pattern.match(str(value)):
            return custom_msg or f"Format kolom '{col_name}' tidak valid."
            
    return validator

# --- Helper Instan untuk Email ---
is_email = matches_regex(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", 
    "Format email tidak valid (contoh: nama@domain.com)"
)

# ======================================================================
# Konfigurasi
# ======================================================================

# Jika menambahkan model baru, tambahkan juga pada UNIQUE_KEY_MAP di bawah
MODEL_MAP: Dict[str, Any] = {
    'cabang': Cabang,
    'customer_tipe': CustomerTipe,
    'perusahaan': Perusahaan,
    'principal': Principal,
    'produk': Produk,
    'customer': Customer,
    'produk_brand': ProdukBrand,
    'produk_kategori': ProdukKategori,
    'armada': Armada,
    'plafon': Plafon,
    'sales' : User, # Karena yang diinput pertama adalah user
    'user' : User,
}

UNIQUE_KEY_MAP: Dict[str, List[str]] = {
    'cabang': ['nama'],
    'customer_tipe': ['kode'],
    'perusahaan': ['kode'],
    'principal': ['kode'],
    'customer': ['kode'],
    'produk': ['kode_sku'],
    'produk_brand': ['nama'],
    'produk_kategori': ['nama'],
    'armada': ['no_pelat'],
    'plafon': ['id_principal', 'id_customer', 'id_sales'],
    'sales' : ['nama'],
    'user' : ['username']
}

FOREIGN_KEY_LOOKUP_MAP: Dict[str, List[Dict[str, Any]]] = {
    'plafon': [
        {
            'csv_column': 'id_sales',  # Nama kolom di file CSV
            'fk_column': 'id_user',    # Kolom target di tabel 'plafon'
            'lookup_model': UserSales,      # Model yang akan di-query
            'lookup_column': 'id'         # Kolom di model 'Sales' untuk dicocokkan
        },
    ],
}

VALIDATION_RULES_MAP: Dict[str, Dict[str, List[Callable]]] = {
    'user': {
        'email': [is_email],
    }
}


# ======================================================================
# Service
# ======================================================================

class OperasiDataServices:
    # POST_PROCESS_MAP: Dict[str, List[Callable]] = {
    #     'produk': [
    #         ProdukUOMServices.insertdelete_produk_uom,
    #         ProdukHargaJualServices.insertdelete_produk_hargajual,
    #     ],
    #     'plafon': [
    #         PlafonJadwalServices.insertdelete_plafon_jadwal,
    #     ],
    #     'sales': [
    #         _post_process_sales,
    #     ],
    # }
    
    # ------------------------- Post-processors ------------------------------
    @staticmethod
    def _post_process_sales(result_list: List[Dict[str, Any]]) -> dict:
        """
        Post-processor khusus untuk data 'sales'.
        Memanggil service SalesPrincipalAssignmentServices.
        """
        _debug("==== Memulai post-process Sales ====")
        
        if not result_list:
            _debug("Tidak ada data user untuk diproses.")
            return True
        

        result = SalesPrincipalAssignmentServices._insertdelete_sales_principal_assignment(result_list)
        return result


    # ------------------------- Generators ------------------------------
    @staticmethod
    def _add_generated_field(
        rows: List[dict], 
        column_name: str, 
        generator_func: Callable[[int, dict], Any]
    ) -> List[dict]:
        """
        Menambahkan field yang digenerasi ke setiap baris menggunakan
        fungsi 'generator_func' (callback).

        Args:
            rows: List of data dicts.
            column_name: Nama kolom baru (misal: 'kode_plafon').
            generator_func: Fungsi callback yang akan dipanggil untuk setiap baris.
                            Fungsi ini harus menerima 2 argumen:
                            - index (int): Indeks baris saat ini (mulai dari 0)
                            - row (dict): Data baris saat ini
        """
        if not rows:
            return []

        for index, row in enumerate(rows):
            # Panggil fungsi callback yang diberikan pengguna
            generated_value = generator_func(index, row)
            
            # Masukkan nilainya ke baris
            row[column_name] = generated_value
            
        return rows

    @staticmethod
    def _apply_generator_to_row(
        row: Dict[str, Any], 
        column_name: str, 
        generator_func: Callable[[int, Dict[str, Any]], Any],
        row_index: int
    ) -> Dict[str, Any]:
        """
        Menerapkan 'generator_func' (callback) ke 'row' tunggal.
        
        Fungsi ini memodifikasi 'row' dan mengembalikannya.
        """
        # 1. Panggil callback yang diberikan untuk mendapatkan nilai baru
        generated_value = generator_func(row_index, row)
        
        # 2. Tambahkan nilai itu ke 'row' (payload)
        row[column_name] = generated_value
        
        # 3. Kembalikan 'row' yang sudah dimodifikasi
        return row

    @staticmethod
    def _get_composite_key(
        row: dict, 
        key_columns: List[str]
    ) -> Tuple[Any, ...]:
        """
        Membuat 'tuple key' yang hashable dari baris data (dict) 
        berdasarkan list kolom.
        """
        # Gunakan _noneify agar konsisten dengan logika upsert
        return tuple(_norm(_noneify(row.get(col))) for col in key_columns)

    @staticmethod
    def _key_has_empty(
        key_tuple: tuple
        , empty_values={None, ''}
      ) -> bool:
        """
        Cek apakah tuple key mengandung nilai kosong (None atau '').
        """
        # Kita juga cek 'NULL' string untuk konsistensi _noneify
        empty_values_full = {None, '', 'NULL'}
        return any(v in empty_values_full for v in key_tuple)

    # ----------------------------- Validations -------------------------------
    @staticmethod
    def _validate_row_payload(
        payload: Dict[str, Any], 
        rules_map: Dict[str, List[Callable]], 
        row_index: int
    ):
        """
        Mesin validasi generik.
        Menerapkan semua aturan di 'rules_map' ke 'payload'.
        Akan raise ValidationException jika ada error.
        """
        errors = []
        
        # Iterasi setiap kolom yang punya aturan
        for col_name, validators in rules_map.items():
            value = payload.get(col_name) # Ambil nilai dari payload
            
            # Iterasi setiap fungsi validator untuk kolom tsb
            for validator_func in validators:
                try:
                    # Panggil validator-nya
                    error_message = validator_func(value, col_name)
                    
                    if error_message:
                        errors.append(error_message)
                        
                except Exception as e:
                    # Menangkap error di dalam fungsi validator itu sendiri
                    errors.append(f"Error internal pada validator '{col_name}': {e}")

        if errors:
            # Jika ada error, gabungkan semua dan raise
            error_details = "; ".join(errors)
            raise ValidationException(
                f"Validasi gagal untuk data baris ke-{row_index}: {error_details}"
            )
        
        # Jika lolos, return True
        return True

    @staticmethod
    def _get_model_and_key(table: str) -> Tuple[Any, List[str]]:
        """
        Selalu mengembalikan model dan list dari kolom unik.
        """
        table_lower = (table or "").lower()
        model = MODEL_MAP.get(table_lower)
        unique_key_config = UNIQUE_KEY_MAP.get(table_lower)
        
        if model is None:
            raise ValidationException(f"Model tidak ditemukan untuk tabel: {table}")
        if not unique_key_config:
            raise ValidationException(f"Kolom unik untuk tabel '{table}' tidak dikonfigurasi")
        
        # NORMALISASI: Selalu kembalikan list, walau isinya cuma 1
        if isinstance(unique_key_config, str):
            return model, [unique_key_config] 
        return model, unique_key_config

    @staticmethod
    def _collect_composite_keys(
        rows: List[dict], 
        key_columns: List[str]
      ) -> List[Tuple]:
        """
        Mengumpulkan composite keys unik (sebagai tuples) dari baris CSV.
        Nilai kosong akan diabaikan.
        """
        keys = set()
        for row in rows or []:
            key_tuple = OperasiDataServices._get_composite_key(row, key_columns)
            
            # Jangan kumpulkan key yang mengandung nilai kosong
            if OperasiDataServices._key_has_empty(key_tuple):
                continue
                
            keys.add(key_tuple)
        return list(keys)

    @staticmethod
    def _filter_out_id(rows: List[dict]) -> List[dict]:
        return [{k: v for k, v in r.items() if k != "id"} for r in rows or []]

    @staticmethod
    def _check_wilayah(rows: List[dict]) -> bool:
        ids1, ids2, ids3, ids4 = set(), set(), set(), set()
        for row in rows or []:
            v1 = _norm(row.get('id_wilayah1'))
            v2 = _norm(row.get('id_wilayah2'))
            v3 = _norm(row.get('id_wilayah3'))
            v4 = _norm(row.get('id_wilayah4'))
            if v1 not in (None, "", []): ids1.add(v1)
            if v2 not in (None, "", []): ids2.add(v2)
            if v3 not in (None, "", []): ids3.add(v3)
            if v4 not in (None, "", []): ids4.add(v4)

        ex1 = {getattr(d, 'id') for d in (Wilayah1.find_by(id=list(ids1)) if ids1 else [])}
        ex2 = {getattr(d, 'id') for d in (Wilayah2.find_by(id=list(ids2)) if ids2 else [])}
        ex3 = {getattr(d, 'id') for d in (Wilayah3.find_by(id=list(ids3)) if ids3 else [])}
        ex4 = {getattr(d, 'id') for d in (Wilayah4.find_by(id=list(ids4)) if ids4 else [])}

        missing = {
            'id_wilayah1': sorted(list(ids1 - ex1)),
            'id_wilayah2': sorted(list(ids2 - ex2)),
            'id_wilayah3': sorted(list(ids3 - ex3)),
            'id_wilayah4': sorted(list(ids4 - ex4)),
        }

        if any(missing[k] for k in missing):
            # sengaja tidak mengekspos detil angka id agar pesan tetap ringkas
            raise ValidationException("Terdapat id wilayah yang tidak diketahui")
        return True
    
    @staticmethod
    def _preprocess_foreign_keys(
        rows: List[dict], 
        lookup_config_list: List[Dict[str, Any]]
      ) -> List[dict]:
        """
        Versi GENERIC untuk 'enrichment' data.
        Secara dinamis mem-fetch foreign keys berdasarkan konfigurasi
        dan menginjeksi ID-nya ke dalam 'rows'.
        """
        _debug("==== Memulai Pre-processing Foreign Key Generic ====")
        errors = []
        
        # 1. Lakukan satu lookup batch PER ATURAN (per foreign key)
        for lookup_rule in lookup_config_list:
            csv_col = lookup_rule['csv_column']
            fk_col = lookup_rule['fk_column']
            model = lookup_rule['lookup_model']
            lookup_col = lookup_rule['lookup_column']
            
            _debug(f"--> Memproses FK: {csv_col} -> {fk_col} (via {model.__name__}.{lookup_col})")

            # 2. Kumpulkan semua nilai unik dari CSV untuk lookup ini
            values_to_fetch = set()
            for row in rows:
                val = _noneify(_norm(row.get(csv_col)))
                if val:
                    # Konversi ke tuple jika list (menangani unhashable)
                    if isinstance(val, list):
                        val = tuple(val)
                    values_to_fetch.add(val)
            
            if not values_to_fetch:
                _debug(f"--> Tidak ada nilai untuk di-lookup pada {csv_col}")
                # Pastikan kolom fk di-set None jika tidak ada nilai lookup
                for row in rows:
                    if fk_col not in row:
                        row[fk_col] = None
                continue

            # 3. Fetch data ID dari database dalam satu batch
            try:
                # Menggunakan find_by() yang sudah support 'IN' clause
                results = model.find_by(**{lookup_col: list(values_to_fetch)})
                _debug("====== Result data preprocess_foreign_keys ====== \n", results)
            except Exception as e:
                raise ValidationException(f"Error saat query ke model {model.__name__} (kolom {lookup_col}): {e}")

            # 4. Buat Peta (Map) untuk lookup O(1)
            id_map = {getattr(r, lookup_col): r.id for r in results}
            _debug(f"--> Ditemukan {len(id_map)} ID unik dari {len(values_to_fetch)} nilai")

            # 5. Iterasi ulang, 'enrich' baris, dan kumpulkan error
            for i, row in enumerate(rows, start=1):
                csv_value = _noneify(_norm(row.get(csv_col)))
                
                if not csv_value:
                    row[fk_col] = None # Pastikan kolom FK ada
                    continue
                
                # Konversi ke tuple jika list (untuk pencocokan key)
                if isinstance(csv_value, list):
                    csv_value = tuple(csv_value)

                _debug("====== Show id map ======\n", id_map)
                _debug("====== Show csv value ======\n", csv_value)
                found_id = id_map.get(csv_value)
                _debug("====== Show found_id ======\n", found_id)
                
                if not found_id:
                    # Error: CSV punya nilai, tapi tidak ditemukan di DB
                    errors.append(f"baris {i}: {csv_col} '{csv_value}' tidak ditemukan di {model.__name__}")
                
                # Injeksi ID ke dict 'row'.
                # Ini akan dipakai oleh _collect_composite_keys nanti.
                row[fk_col] = found_id

        if errors:
            # Batasi jumlah error yang ditampilkan agar tidak spam
            display_errors = errors[:13]
            summary = f"...dan {len(errors) - 15} error lainnya." if len(errors) > 15 else ""
            
            raise ValidationException(
                "Gagal memproses data. Referensi tidak valid:\n" + "\n".join(display_errors) + f"\n{summary}"
            )
        
        _debug("==== Pre-processing Foreign Key Selesai ====")
        return rows

    @staticmethod
    def _check_unique_value(
        rows: List[dict], 
        column: List[str], 
        empty_values={None, ''}
      ) -> bool:
        """
        Cek duplikasi pada kolom unik di dalam file (kosong diabaikan).
        Versi ini sudah menangani composite keys dan unhashable types (list).
        """
        all_duplicate = set()
        first_seen_at = {}

        for index, row in enumerate(rows or []):
            has_empty = False
            key_values = []
            
            for col in column:
                value = row.get(col)
                
                # FIX: unhashable type: 'list'
                if isinstance(value, list):
                    value = tuple(value)

                key_values.append(value)
                if value in empty_values:
                    has_empty = True
                    break  # Optimasi
            
            # FIX: Logika "kosong diabaikan"
            if has_empty:
                continue
                
            key = tuple(key_values)
            current_row_number = index + 1
            
            try:
                if key in first_seen_at:
                    all_duplicate.add(current_row_number)
                    all_duplicate.add(first_seen_at[key])  # baris pertama
                else:
                    first_seen_at[key] = current_row_number
            except TypeError as e:
                # Menangkap jika masih ada tipe unhashable lain (misal: dict)
                raise ValidationException(
                    f"Error tipe data unhashable di baris {current_row_number} (kolom: '{', '.join(column)}'). "
                    f"Pastikan data tidak mengandung dict. Error: {e}"
                )

        if all_duplicate:
            printed = ", ".join(map(str, sorted(all_duplicate)))
            raise ValidationException(f"Ditemukan nilai kembar pada kolom: '{', '.join(column)}' pada baris: {printed}")
        return True

    # ------------------------------- Upsert ----------------------------------

    @staticmethod
    # @handle_error_rollback
    def _upsert_data(
        data_list: List[dict], 
        existing_data: List[Any], 
        key_columns: List[str], 
        model: Any, 
        new_row_generators: Dict[str, Callable[[int, dict], Any]] = None, 
        validation_rules: Dict[str, List[Callable]] = None
        ) -> List[Any]:
        """
        Upsert record berdasarkan KUNCI KOMPOSIT (list kolom).
        """
        data_list = [_noneify_dict(r) for r in (data_list or [])]
        if not data_list:
            return []
        
        
        # Peta existing: (composite_tuple_key) -> instance Model
        existing_map = {}
        for d in (existing_data or []):
            # Ambil dict dari instance model untuk build key
            model_dict = d.__dict__ 
            existing_key = OperasiDataServices._get_composite_key(model_dict, key_columns)
            existing_map[existing_key] = d

        dataset = []
        key_columns_set = set(key_columns) # Untuk cek 'if attr in ...'

        _debug("==== incoming data_list ====\n", data_list)
        
        for i, data in enumerate(data_list, start=1):
            # Buat composite key dari baris CSV
            key_tuple = OperasiDataServices._get_composite_key(data, key_columns)
            
            # Validasi setiap baris jika ada aturan validasi
            if validation_rules:
              try:
                  OperasiDataServices._validate_row_payload(
                      data, validation_rules, i
                  )
              except ValidationException as e:
                  # Tangkap, rollback, dan berikan pesan error yang jelas
                  db.session.rollback()
                  _debug(f"==== Validasi Gagal (Baris {i}) ====\n", payload)
                  raise e

            # Jika key mengandung kosong, lewati baris ini
            if OperasiDataServices._key_has_empty(key_tuple):
                continue

            # =====================================================
            # UPDATE EXISTING RECORD
            # =====================================================
            if key_tuple in existing_map:
                existing_record = existing_map[key_tuple]
                try:
                    for attr, value in data.items():
                        # Jangan update 'id' atau kolom yg jadi bagian dari unique key
                        if attr == 'id' or attr in key_columns_set:
                            continue
                        if isinstance(attr, str) and hasattr(existing_record, attr):
                            setattr(existing_record, attr, None if value == "" else value)

                    db.session.flush()

                    if model is Produk:
                        data['id_produk'] = getattr(existing_record, 'id', None)
                    elif model is Plafon:
                        data['id_plafon'] = getattr(existing_record, 'id', None)
                    elif model is User:
                        data['id_user'] = getattr(existing_record, 'id', None)
                    elif model is UserSales:
                        data['id_sales'] = getattr(existing_record, 'id', None)
                    dataset.append(data)

                except Exception as inner_err:
                    db.session.rollback()
                    _debug("==== Update error for record ====\n", data)
                    _debug("==== Exception message ====\n", str(inner_err))
                    raise ValidationException(
                        f"Kesalahan format data saat update record baris ke-{i}"
                    )

            # =====================================================
            # INSERT NEW RECORD
            # =====================================================
            else:
                payload = {
                    k: (None if v == "" else v)
                    for k, v in data.items()
                    if isinstance(k, str) and hasattr(model, k) and k != 'id'
                }
                
                # Pastikan semua kolom key ada di payload
                for col_name, col_value in zip(key_columns, key_tuple):
                    payload[col_name] = col_value

                if new_row_generators:
                    for col_name, gen_func in new_row_generators.items():
                        # Panggil helper yang baru kita buat
                        payload = OperasiDataServices._apply_generator_to_row(
                            row=payload,
                            column_name=col_name,
                            generator_func=gen_func,
                            row_index=i  # Gunakan 'i' dari enumerate
                        )

                try:
                    new_record = model(**payload)
                    db.session.add(new_record)
                    db.session.flush()

                    if model is Produk:
                        data['id_produk'] = getattr(new_record, 'id', None)
                    elif model is Plafon:
                        data['id_plafon'] = getattr(new_record, 'id', None)
                    elif model is User:
                        data['id_user'] = getattr(new_record, 'id', None)
                    elif model is UserSales:
                        data['id_sales'] = getattr(new_record, 'id', None)
                    dataset.append(data)

                except Exception as inner_err:
                    db.session.rollback()
                    _debug("==== Insert error for record ====\n", payload)
                    _debug("==== Get type model ====\n", model.__tablename__)
                    _debug("==== Exception message ====\n", str(inner_err))
                    raise ValidationException(
                        f"Kesalahan format data saat insert record baris ke-{i}"
                    )

        _debug("==== final existing_map (keys) ====\n", existing_map.keys())
        db.session.commit()
        return dataset
    # ------------------------------- Entry -----------------------------------

    @staticmethod
    @handle_error
    def bulk_insert(table: str):
        """
        Bulk Insert dengan File CSV.
        - Hilangkan BOM (utf-8-sig).
        - Validasi wilayah untuk tabel tertentu.
        - Cek duplikasi kolom unik di dalam file.
        - Upsert data dan kembalikan hasil ringkas.
        """

        generator_map = {}

        # 1) Baca file
        file = request.files['file']
        file_content = file.stream.read().decode('utf-8-sig')  # hilangkan BOM
        reader = csv.DictReader(StringIO(file_content), delimiter=',')
        rows = list(reader)

        _debug("==== sample row ====\n", rows[0] if rows else "No Data")

        # 2) Tentukan model & kolom unik (INI BERUBAH)
        model, unique_key_cols = OperasiDataServices._get_model_and_key(table)
        _debug("==== model ====\n", model)
        _debug("==== unique_key_cols ====\n", unique_key_cols)

        # 3) Validasi referensi wilayah (sama)
        if table.lower() in ('cabang', 'perusahaan', 'principal'):
            OperasiDataServices._check_wilayah(rows)

        if table.lower() == 'plafon':
            generator_map['kode'] = lambda idx, row: f"PL{int(time.time())}{random.randint(100,1000)}"
        elif table.lower() == 'user':
            # Untuk user, generate password hash dari kolom 'password'
            def password_hash_generator(idx, row):
                raw_password = row.get('password', 'defaultpassword')
                return generate_password_hash(raw_password)
            generator_map['password'] = password_hash_generator

        lookup_config = FOREIGN_KEY_LOOKUP_MAP.get(table.lower())
        
        if lookup_config:
            _debug(f"Menjalankan pre-processing FK untuk '{table}'...")
            try:
                # Fungsi ini akan memodifikasi 'rows'
                # Menambahkan 'id_customer', 'id_principal', dll.
                rows = OperasiDataServices._preprocess_foreign_keys(rows, lookup_config)
                
            except Exception as e:
                raise ValidationException(f"Error saat pre-processing data referensi: {e}")
        else:
            _debug(f"Tidak ada konfigurasi pre-processing FK untuk '{table}'.")

        # 4) Ambil existing berdasarkan unique values dari file
        unique_key_tuples = OperasiDataServices._collect_composite_keys(rows, unique_key_cols)
        _debug("==== unique_key_tuples ====\n", unique_key_tuples)
        
        existing_data = model.find_by_composite_keys(
            unique_key_cols, unique_key_tuples
        ) if unique_key_tuples else []
        
        _debug("==== existing_data ====\n", [d.id for d in existing_data]) # Debug ID saja

        # 5) Cek duplikasi dalam file
        if table.lower() not in ('produk', 'plafon', 'sales'):
            # Panggil _check_unique_value
            validate = OperasiDataServices._check_unique_value(rows, unique_key_cols)
            _debug("======== validate ========\n", validate)

        # 6) Buang kolom id (sama)
        cleaned_rows = OperasiDataServices._filter_out_id(rows)

        # 6.6) Ambil aturan validasi untuk tabel ini
        validation_rules_for_table = VALIDATION_RULES_MAP.get(table.lower())

        # 7) Upsert
        result = OperasiDataServices._upsert_data(
            cleaned_rows, 
            existing_data, 
            model=model, 
            key_columns=unique_key_cols,
            new_row_generators=generator_map,
            validation_rules=validation_rules_for_table
        )

        _debug("==== upsert result ====\n", result)
        if table.lower() == 'sales':
            model = UserSales
            unique_key_tuples = OperasiDataServices._collect_composite_keys(
                result, 
                ['id_user', 'id_tipe']
            )
            _debug("==== sales unique_key_tuples ====\n", unique_key_tuples)
            existing_data = model.find_by_composite_keys(
                ['id_user', 'id_tipe'], unique_key_tuples
            )
            _debug("==== existing sales data ====\n", [d.id for d in existing_data]) # Debug ID saja
            result_sales = OperasiDataServices._upsert_data(
                result, 
                existing_data, 
                model=model, 
                key_columns=['id_user', 'id_tipe'],
                new_row_generators=None
            )
            _debug("==== upsert sales result ====\n", result_sales)
            sales_assignment = SalesPrincipalAssignmentServices()
            result_sales_assignment = sales_assignment.insertdelete_sales_principal_assignment(result_sales)
            if result_sales_assignment is False:
                raise ValidationException("Kesalahan format data penugasan principal sales")
            # pass

        # 8) Post-process khusus produk
        if table.lower() == 'produk':
            _debug("==== post-process UOM & Harga Jual ====\n")
            uom = ProdukUOMServices()
            harga = ProdukHargaJualServices()
            result_uom = uom.insertdelete_produk_uom(result)
            if result_uom is False:
                raise ValidationException("Kesalahan format data UOM")
            # _debug("==== post-process UOM result ====\n", result_uom)
            result_hargajual = harga.insertdelete_produk_hargajual(result)
            if result_hargajual is False:
                raise ValidationException("Kesalahan format data harga jual")
        
        if table.lower() == 'plafon':
            _debug("==== post-process Plafon Sisa Bon ====\n")
            plafon_jadwal = PlafonJadwalServices()
            result_plafon_jadwal = plafon_jadwal.insertdelete_plafon_jadwal(result)
            _debug("==== post-process Plafon Jadwal result ====\n", result_plafon_jadwal)
            if result_plafon_jadwal is False:
                raise ValidationException("Kesalahan format data jadwal plafon")
            

        return setResult({"message": "Data Successfully Added"})