from sqlalchemy import func, literal, cast, Date, case
from flask import g, request, current_app
from datetime import datetime
import bcrypt

from apps.handler import handle_error, nonServerErrorException
from apps.lib.convert_uom import convert_uom
from apps.lib.paginate import Paginate
from apps.services import BaseServices
from apps.models import (
    voucher_2 as V2,
    voucher_3 as V3,
    voucher_2_cabang as V2Cabang,
    voucher_3_cabang as V3Cabang,
    draft_voucher as DraftVoucher,
    klaim as Klaim,
    klaim_detail as KlaimDetail,
    klaim_kategori as KlaimKategori,
    kasbon_klaim as KasbonKlaim,
    kasbon_klaim_detail as KasbonKlaimDetail,
    principal as Principal,
    perusahaan as Perusahaan,
    sales_order as SalesOrder,
    sales_order_detail as SalesOrderDetail,
    faktur as Faktur,
    plafon as Plafon,
    customer as Customer,
    cabang as Cabang,
    produk as Produk
)

class Promo(BaseServices):
    def __init__(self):
        super().__init__()

    """
    ========================
    Utility - Helper
    ========================
    """
    def apply_pagination(self, data, filters=None):
        if filters and filters.get('no-paginate') == 'true':
            return {
                'pages': data,
                'total_data': len(data),
                'status': 'success'
            }
        
        page = int(request.args.get('page', 0))
        limit = int(request.args.get('limit', 5))
        offset = page * limit
        
        if hasattr(data, "all"):
            total_data = data.count()
            pages = data.offset(offset).limit(limit).all()
        else:
            total_data = len(data)
            pages = data[offset:offset + limit]
            
        return {
            'pages': pages,
            'total_data': total_data,
            'page': page,
            'limit': limit,
            'status': 'success'
        }

    def _format_date(self, date):
        return date.strftime('%Y-%m-%d') if date else None
    
    """
    ========================
    Utility - Status Mapping
    ========================
    """
    def _get_status_count(self, voucher_id, tipe_voucher, status_promo):
        return self.db.session.query(
            func.count(DraftVoucher.id)
        ).filter(
            DraftVoucher.id_voucher == voucher_id,
            DraftVoucher.tipe_voucher == tipe_voucher,
            DraftVoucher.status_promo == status_promo
        ).scalar() or 0

    def _get_status_voucher(self, status_voucher):
        status_map = {
            1: 'Aktif',
            2: 'Belum Aktif',
            3: 'Kadaluarsa',
            4: 'Dibatalkan',
            5: 'Ditangguhkan',
        }
        return status_map.get(status_voucher, 'Unknown')
                
    def _get_status_promo(self, status, asDropdown=False):
        status_map = {
            0: 'Draft',
            1: 'Terkonfirmasi',
            2: 'Terpakai',
            3: 'Tertolak',
        }
        
        if asDropdown:
            return [
                {'id': status_id, 'nama': status_nama}
                for status_id, status_nama in status_map.items()
            ]

        return status_map.get(status, 'Unknown')

    def _get_status_klaim(self, status, asDropdown=False):
        status_map = {
            0: 'Draft',
            1: 'Pengajuan klaim',
            2: 'Klaim disetujui',
            3: 'Klaim ditolak',
            4: 'Klaim sudah digunakan',
        }
        
        if asDropdown:
            return [
                {'id': status_id, 'nama': status_nama}
                for status_id, status_nama in status_map.items()
            ]

        return status_map.get(status, 'Unknown')

    def _get_status_kasbon(self, status):
        status_map = {
            0: 'Draft',
            1: 'Disetujui',
            2: 'Ditolak', 
            3: 'Diberikan'
        }
        return status_map.get(status, 'Unknown')

    def _get_tipe_kasbon(self, tipe):
        tipe_map = {
            1: 'Tunai',
            2: 'Non Tunai'
        }
        return tipe_map.get(tipe, 'Unknown')

    """
    ==========================
    Utility - Dropdown Builder
    ==========================
    """
    @handle_error
    def getDropdownData(self):
        def principal_query(model):
            return self.db.session.query(
                Principal.id,
                Principal.nama
            ).join(model, model.id_principal == Principal.id).filter(
                model.status_voucher == 1  # Status voucher aktif
            )
            
        def kode_promo_query(model):
            return self.db.session.query(
                model.id,
                model.kode_voucher.label('kode_promo'),
                model.nama_voucher.label('nama_promo'),
                model.id_principal
            ).filter(model.status_voucher == 1).all()

        principals = principal_query(V2).union(principal_query(V3)).distinct().all()
        principal_list = [{ 'id': principal.id, 'nama': principal.nama } for principal in principals]
        principal_list.sort(key=lambda x: x['nama'])
        
        kode_promo_data = [
            *[
                {
                    'id': int(row.id),
                    'kode_promo': row.kode_promo,
                    'nama_promo': row.nama_promo,
                    'id_principal': row .id_principal
                } for row in kode_promo_query(V2)
            ],
            *[
                {
                    'id': int(row.id),
                    'kode_promo': row.kode_promo,
                    'nama_promo': row.nama_promo,
                    'id_principal': row.id_principal
                } for row in kode_promo_query(V3)
            ]
        ]
        
        kode_promo_data.sort(key=lambda x: x['kode_promo'])
        return {
            'principal': principal_list,
            'kode_promo': kode_promo_data,
            'status': 'success'
        }
        
    @handle_error
    def getDropdownDataLog(self):
        principal_base_query = self._build_draft_voucher_base_query(include_principal=True)
        principal_query = principal_base_query.with_entities(
            Principal.nama.label('principal_nama'),
            func.coalesce(V2.id_principal, V3.id_principal).label('id_principal')
        ).distinct()

        principal_list = []
        seen_principals = set()
        for row in principal_query.all():
            if row.id_principal and row.id_principal not in seen_principals:
                seen_principals.add(row.id_principal)
                principal_list.append({
                    'id': row.id_principal,
                    'nama': row.principal_nama
                })
                
        principal_list.sort(key=lambda x: x['nama'])
        
        kode_promo_base_query = self._build_draft_voucher_base_query(include_principal=False)
        kode_promo_query = kode_promo_base_query.with_entities(
            func.coalesce(V2.kode_voucher, V3.kode_voucher).label('kode_promo'),
            func.coalesce(V2.nama_voucher, V3.nama_voucher).label('nama_promo'),
            func.coalesce(V2.id_principal, V3.id_principal).label('id_principal'),
            DraftVoucher.id_voucher,
            DraftVoucher.tipe_voucher
        ).filter(
            func.coalesce(V2.kode_voucher, V3.kode_voucher).isnot(None)
        ).distinct()
        
        kode_promo_list = []
        seen_combinations = set()
        
        for row in kode_promo_query.all():
            unique_key = (row.kode_promo, row.nama_promo, row.id_principal)
            if unique_key not in seen_combinations:
                seen_combinations.add(unique_key)
                kode_promo_list.append({
                    'kode_promo': row.kode_promo,
                    'nama_promo': row.nama_promo,
                    'id_principal': row.id_principal,
                    'id_voucher': row.id_voucher,
                    'tipe_voucher': row.tipe_voucher
                })
                
        kode_promo_list.sort(key=lambda x: x['kode_promo'])
        status_penggunaan_list = self._get_status_promo(None, asDropdown=True)

        return {
            'principal': principal_list,
            'kode_promo': kode_promo_list,
            'status_penggunaan': status_penggunaan_list,
            'status': 'success'
        }

    @handle_error
    def getDropdownDataKlaim(self):
        status_filter = request.args.get('status_klaim', type=int)

        principal_query = self.db.session.query(
            Principal.id.label('id_principal'),
            Principal.nama.label('principal_nama')
        ).select_from(Klaim) \
        .outerjoin(V2, V2.kode_voucher == Klaim.kode_voucher) \
        .outerjoin(V3, V3.kode_voucher == Klaim.kode_voucher) \
        .join(Principal, Principal.id == func.coalesce(V2.id_principal, V3.id_principal)) \
        .distinct()

        if status_filter:
            principal_query = principal_query.filter(Klaim.status == status_filter)

        principal_list = []
        seen_principals = set()
        for row in principal_query.all():
            if row.id_principal and row.id_principal not in seen_principals:
                seen_principals.add(row.id_principal)
                principal_list.append({
                    'id': row.id_principal,
                    'nama': row.principal_nama
                })
                
        principal_list.sort(key=lambda x: x['nama'])
        
        # Query kode promo dari tabel klaim
        kode_promo_query = self.db.session.query(
            Klaim.kode_voucher.label('kode_promo'),
            func.coalesce(V2.nama_voucher, V3.nama_voucher).label('nama_promo'),
            func.coalesce(V2.id_principal, V3.id_principal).label('id_principal'),
            Klaim.id_voucher
        ).select_from(Klaim) \
        .outerjoin(V2, V2.kode_voucher == Klaim.kode_voucher) \
        .outerjoin(V3, V3.kode_voucher == Klaim.kode_voucher) \
        .filter(Klaim.kode_voucher.isnot(None)) \
        .distinct()

        if status_filter:
            kode_promo_query = kode_promo_query.filter(Klaim.status == status_filter)
        
        kode_promo_list = []
        seen_combinations = set()
        
        for row in kode_promo_query.all():
            unique_key = (row.kode_promo, row.nama_promo, row.id_principal)
            if unique_key not in seen_combinations:
                seen_combinations.add(unique_key)
                kode_promo_list.append({
                    'kode_promo': row.kode_promo,
                    'nama_promo': row.nama_promo,
                    'id_principal': row.id_principal,
                    'id_voucher': row.id_voucher
                })
                
        kode_promo_list.sort(key=lambda x: x['kode_promo'])
        status_klaim_list = self._get_status_klaim(None, asDropdown=True)

        return {
            'principal': principal_list,
            'kode_promo': kode_promo_list,
            'status_klaim': status_klaim_list,
            'status': 'success'
        }

    """
    ========================
    Utility - Query Builder
    ========================
    """
    def _build_voucher_query(self, voucher_model, tipe_promo):
        persentase_diskon_column = (
            voucher_model.persentase_diskon_2 
            if voucher_model == V2 
            else voucher_model.persentase_diskon_3
        )

        nominal_promo_case = func.coalesce(
            case(
                (voucher_model.kategori_voucher == 1, persentase_diskon_column),
                else_=voucher_model.nominal_diskon
            ), 0
        )
        
        return self.db.session.query(
            voucher_model.id,
            voucher_model.kode_voucher.label('kode_promo'),
            voucher_model.nama_voucher.label('nama_promo'),
            voucher_model.status_voucher.label('status_promo'),
            nominal_promo_case.label('nominal_promo'),
            voucher_model.budget_diskon.label('limit'),
            voucher_model.tanggal_mulai,
            voucher_model.tanggal_kadaluarsa.label('tanggal_selesai'),
            voucher_model.keterangan,
            voucher_model.syarat_ketentuan,
            voucher_model.syarat_wajib,
            voucher_model.id_principal,
            voucher_model.kategori_voucher.label('kategori_promo'),
            Principal.nama.label('principal'),
            literal(tipe_promo).label('tipe_promo') 
        ).join(Principal, voucher_model.id_principal == Principal.id
        ).filter(voucher_model.status_voucher == 1)     # Status Voucher Aktif
      
    def _build_draft_voucher_base_query(self, include_principal):
        query = self.db.session.query(
            DraftVoucher.id.label('id'),
            Faktur.no_faktur.label('no_faktur'),
            DraftVoucher.jumlah_diskon.label('nominal_promo'),
            DraftVoucher.status_promo.label('status_penggunaan'),
            func.coalesce(V2.kode_voucher, V3.kode_voucher).label('kode_promo'),
            func.coalesce(V2.nama_voucher, V3.nama_voucher).label('nama_promo'),
            func.coalesce(V2.id_principal, V3.id_principal).label('id_principal')
        ).select_from(DraftVoucher) \
        .join(SalesOrder, DraftVoucher.id_sales_order == SalesOrder.id) \
        .join(Faktur, SalesOrder.id == Faktur.id_sales_order) \
        .outerjoin(V2, (DraftVoucher.id_voucher == V2.id) & (DraftVoucher.tipe_voucher == 2)) \
        .outerjoin(V3, (DraftVoucher.id_voucher == V3.id) & (DraftVoucher.tipe_voucher == 3))
        
        if include_principal:
            query = query.add_columns(Principal.nama.label('principal_nama')) \
                    .outerjoin(Principal, Principal.id == func.coalesce(
                         V2.id_principal, V3.id_principal
                    ))
                    
        return query
        
    def _format_voucher_data(self, row, tipe_promo):        
        terpakai_count = self._get_status_count(row.id, tipe_promo, 2)
        terklaim_count = self._get_status_count(row.id, tipe_promo, 2)
        terkonfirmasi_count = self._get_status_count(row.id, tipe_promo, 1)
        cabang_nama = self._get_cabang_nama(row.id, tipe_promo)
        kategori_promo = getattr(row, 'kategori_promo', None)
        nominal_promo = getattr(row, 'nominal_promo', None)
            
        return {
            'id': row.id or 0,
            'kode_promo': row.kode_promo or '',
            'nama_promo': row.nama_promo or '',
            'nominal_promo': float(nominal_promo or 0),
            'status_promo': self._get_status_voucher(row.status_promo),
            'limit': float(row.limit or 0),
            'terpakai': terpakai_count,
            'terkonfirmasi': terkonfirmasi_count,
            'tanggal_mulai': self._format_date(row.tanggal_mulai),
            'tanggal_selesai': self._format_date(row.tanggal_selesai),
            'keterangan': row.keterangan or '',
            'syarat_ketentuan': row.syarat_ketentuan or '',
            'syarat_wajib': row.syarat_wajib or '',
            'id_principal': row.id_principal or 0,
            'principal': row.principal or '',
            'tipe_promo': row.tipe_promo or '',
            'kategori_promo': kategori_promo,
            'terklaim': terklaim_count,
            'cabang': cabang_nama
        }

    """
    =================
    Utility - Filters
    =================
    """ 
    def _apply_filter_by_key(self, query, key, value, filter_type='default'):
        if value is None or value == "":
            return query
        
        filter_configs = {
            'default': {
                'id_principal': lambda query, value: query \
                    .filter(func.coalesce(V2.id_principal, V3.id_principal) == int(value)),
                'kode_promo': lambda query, value: query \
                    .filter((V2.kode_voucher == value) | (V3.kode_voucher == value)),
                'nama_promo': lambda query, value: query.filter(
                    (V2.nama_voucher.ilike(f"%{value}%")) | (V3.nama_voucher.ilike(f"%{value}%"))
                ),
                'status_penggunaan': lambda query, value: query.filter(DraftVoucher.status_promo == int(value)),
                'filters': lambda query, value: query.filter(
                    (Klaim.nomor_klaim.ilike(f"%{value}%")) |
                    (Faktur.no_faktur.ilike(f"%{value}%")) |
                    (V2.kode_voucher.ilike(f"%{value}%")) |
                    (V3.kode_voucher.ilike(f"%{value}%")) |
                    (V2.nama_voucher.ilike(f"%{value}%")) |
                    (V3.nama_voucher.ilike(f"%{value}%")) |
                    (Principal.nama.ilike(f"%{value}%"))
                )
            },
            'klaim': {
                'id_principal': lambda query, value: query.filter(func.coalesce(V2.id_principal, V3.id_principal) == int(value)),
                'kode_promo': lambda query, value: query.filter(Klaim.kode_voucher.ilike(f"%{value}%")),
                'nama_promo': lambda query, value: query.filter(
                    (V2.nama_voucher.ilike(f"%{value}%")) | (V3.nama_voucher.ilike(f"%{value}%"))
                ),
                'status_klaim': lambda query, value: query.filter(Klaim.status == int(value)),
                'filters': lambda query, value: query.filter(
                    (Klaim.nomor_klaim.ilike(f"%{value}%")) |
                    (Klaim.kode_voucher.ilike(f"%{value}%")) |
                    (V2.nama_voucher.ilike(f"%{value}%")) |
                    (V3.nama_voucher.ilike(f"%{value}%")) |
                    (Principal.nama.ilike(f"%{value}%"))
                )
            },
            'kasbon': {
                'id_principal': lambda query, value: query.filter(KasbonKlaim.id_principal == int(value)),
                'tanggal_pengajuan': lambda query, value: self._handle_tanggal_filter(query, value),
                'status_kasbon': lambda query, value: query.filter(KasbonKlaim.status_kasbon == int(value)),
                'filters': lambda query, value: query.filter(
                    (KasbonKlaim.kode_kasbon_klaim.ilike(f"%{value}%")) |
                    (Principal.nama.ilike(f"%{value}%")) |
                    (KasbonKlaim.keterangan.ilike(f"%{value}%"))
                )
            }
        }
        
        config = filter_configs.get(filter_type, filter_configs['default'])
        filter_func = config.get(key)
        
        return filter_func(query, value) if filter_func else query

    def apply_filters(self, query, filters, filter_type='default'):
        skip_keys = ['page', 'limit', 'no-paginate', 'order', 'field']
        for key, value in filters.items():
            if key in skip_keys:
                continue
            
            key_clean = key.rstrip("=")
            query = self._apply_filter_by_key(query, key_clean, value, filter_type)
        return query

    def apply_filters_klaim(self, query, filters):
        return self.apply_filters(query, filters, filter_type='klaim')

    def apply_filters_kasbon(self, query, filters):
        return self.apply_filters(query, filters, filter_type='kasbon')

    def _handle_tanggal_filter(self, query, value):
        if isinstance(value, str) and value != "":
            if "GMT" in value:
                try:
                    date_obj = datetime.strptime(value.split(' GMT')[0], '%a %b %d %Y %H:%M:%S')
                    date_value = date_obj.date()
                except:
                    return query
            else:
                try:
                    date_obj = datetime.strptime(value, '%Y-%m-%d')
                    date_value = date_obj.date()
                except:
                    return query
                
            return query.filter(cast(KasbonKlaim.tanggal_pengajuan, Date) == date_value)
        return query

    """
    ====================
    Promo Service Layer
    ====================
    """
    @handle_error
    def getPromoUser(self):
        email = self.req('email')
        password = self.req('password')
        
        user_info = """
            SELECT 
                users.tokens AS token, 
                users.id AS id_user,
                users.nama AS nama_user, 
                users.email AS user_email, 
                users.id_jabatan,
                users.password
            FROM users
            WHERE users.email = :email
            AND users.id_jabatan IN (20)
        """
        
        loginBindParam = {"email": email}
        user = self.query().setRawQuery(user_info).bindparams(loginBindParam).execute().fetchone().result
        
        if not user:
            raise nonServerErrorException(401, "Email salah atau tidak terdaftar")
        
        password_bytes = password.encode('utf-8')
        stored_hash = user['password'].encode('utf-8') if isinstance(user['password'], str) else user['password']
        
        if not bcrypt.checkpw(password_bytes, stored_hash):
            raise nonServerErrorException(401, "Password salah")
        
        return user

    @handle_error
    def getPromo(self):
        voucher_2_data = self._build_voucher_query(V2, '2').with_entities(
            V2.kode_voucher.label('kode_promo'),
            V2.id,
            V2.nama_voucher,
            V2.id_principal,
            literal('2').label('tipe'),
        )
        voucher_3_data = self._build_voucher_query(V3, '3').with_entities(
            V3.kode_voucher.label('kode_promo'),  
            V3.id,
            V3.nama_voucher,
            V3.id_principal,
            literal('3').label('tipe'),
        )
        
        union_query = voucher_2_data.union_all(voucher_3_data).order_by("kode_promo")
        pagination_result = self.apply_pagination(union_query)

        pages = [self._format_voucher_data(row, row.tipe) for row in pagination_result['pages']]
        pagination_result['pages'] = pages
    
        return pagination_result

    @handle_error
    def getPromoByKode(self, kode_promo):
        voucher_data, tipe_voucher = self.get_voucher_data(kode_promo)
        
        if not voucher_data:
            raise nonServerErrorException(404, "Kode promo tidak ditemukan")
        
        # Format and return data
        formatted_data = self._format_voucher_data(voucher_data, tipe_voucher)
        formatted_data.pop('terklaim', None)
        
        return formatted_data
    
    @handle_error
    def getPromoFiltered(self, filters):
        def filter_query(query, model):
            for key, value in filters.items():
                if value is None or value == "":
                    continue
                key_clean = key.rstrip("=")
                if key_clean == "id_principal":
                    query = query.filter(model.id_principal == int(value))
                elif key_clean == "kode_promo":
                    query = query.filter(model.kode_voucher == value)
                elif key_clean == "filters":
                    query = query.filter(
                        (model.kode_voucher.ilike(f"%{value}%")) |
                        (model.nama_voucher.ilike(f"%{value}%"))
                    )
            return query.all()
        
        v2_data = filter_query(self._build_voucher_query(V2, '2'), V2)
        v3_data = filter_query(self._build_voucher_query(V3, '3'), V3)
        
        combined_data = [self._format_voucher_data(row, 2) for row in v2_data] + \
                        [self._format_voucher_data(row, 3) for row in v3_data] 
        
        combined_data.sort(key=lambda x: x['kode_promo'])
        if filters.get('no-paginate') == 'true':
            result = {
                'pages': combined_data,
                'total_data': len(combined_data),
                'status': 'success'
            }
        else:
            pagination_result = self.apply_pagination(combined_data)
            result = {
                'pages': pagination_result['pages'],
                'total_data': pagination_result['total_data'],
                'status': 'success'
            }
            
        return result

    @handle_error
    def getLogPenggunaanPromo(self):
        filters = request.args.to_dict()
        base_query = self._build_draft_voucher_base_query(include_principal=True)
        filtered_query = self.apply_filters(base_query, filters, filter_type='default')
        result = filtered_query.distinct().all()

        log_data = []
        for row in result:
            log_entry = {
                'id': row.id,
                'no_faktur': row.no_faktur,
                'kode_promo': row.kode_promo,
                'nama_promo': row.nama_promo,
                'nominal_promo': float(row.nominal_promo),
                'status_penggunaan': self._get_status_promo(row.status_penggunaan),
                'principal': row.principal_nama
            }
            log_data.append(log_entry)
            
        pagination_result = self.apply_pagination(log_data, filters)
        return {
            'pages': pagination_result['pages'],
            'total_data': pagination_result['total_data'],
            'status': 'success'
        }

    """
    =====================
    Klaim Service Layer
    =====================
    """
    def _calculate_klaim_counter(self, id_principal):
        existing_count = self.db.session.query(func.count(Klaim.id)) \
            .select_from(Klaim) \
            .outerjoin(V2, V2.kode_voucher == Klaim.kode_voucher) \
            .outerjoin(V3, V3.kode_voucher == Klaim.kode_voucher) \
            .filter(func.coalesce(V2.id_principal, V3.id_principal) == id_principal) \
            .scalar() or 0
    
        return existing_count + 1
        
    @handle_error
    def generateKlaimCode(self):
        data = request.get_json() or {}
        id_principal = data.get('id_principal')

        if not id_principal:
            raise nonServerErrorException(400, "Id principal tidak boleh kosong")
        
        principal, perusahaan = self._get_principal_and_perusahaan(id_principal)
        counter = self._calculate_klaim_counter(id_principal)
        formatted_code = f"CL/{perusahaan.kode}-{principal.kode}/{counter:04d}"

        result = {
            "kode_klaim": formatted_code,
            "counter": counter,
            "kode_perusahaan": perusahaan.kode,
            "kode_principal": principal.kode
        }

        return result
    
    @handle_error
    def getListFaktur(self):
        kode_promo = request.args.get('kode_promo')
        klaim_id = request.args.get('id')

        if klaim_id:
            klaim = self.db.session.query(Klaim.kode_voucher).filter(Klaim.id == int(klaim_id)).first()
            if not klaim:
                raise nonServerErrorException(404, "Klaim tidak ditemukan")
            kode_promo = klaim.kode_voucher
        
        if not kode_promo:
            raise nonServerErrorException(400, "Parameter kode_promo atau id harus diisi")
        
        voucher_data, tipe_voucher = self.get_voucher_data(kode_promo)
        if not voucher_data:
            raise nonServerErrorException(404, "Kode promo tidak ditemukan")
        
        base_query = self.db.session.query(
            DraftVoucher.id.label('id'),
            DraftVoucher.jumlah_diskon.label('estimasi_klaim'),
            DraftVoucher.status_promo.label('status_promo'),
            DraftVoucher.id_sales_order_detail.label('id_sales_order_detail'),
            Faktur.no_faktur.label('no_faktur'),
            Customer.nama.label('customer'),
            SalesOrderDetail.hargaorder.label('harga_order'),
            SalesOrderDetail.pieces_order.label('pieces_order'),
            SalesOrderDetail.box_order.label('box_order'),
            SalesOrderDetail.karton_order.label('karton_order'),
            Produk.isiperbox.label('pieces_per_box'),
            Produk.isiperkarton.label('pieces_per_karton'),
            Produk.ppn.label('ppn')
        ).select_from(DraftVoucher) \
        .join(SalesOrder, DraftVoucher.id_sales_order == SalesOrder.id) \
        .join(Faktur, SalesOrder.id == Faktur.id_sales_order) \
        .join(Plafon, SalesOrder.id_plafon == Plafon.id) \
        .join(Customer, Plafon.id_customer == Customer.id) \
        .join(SalesOrderDetail, DraftVoucher.id_sales_order_detail == SalesOrderDetail.id) \
        .join(Produk, SalesOrderDetail.id_produk == Produk.id) \
        .filter(
            DraftVoucher.id_voucher == voucher_data.id,
            DraftVoucher.tipe_voucher == tipe_voucher,
            DraftVoucher.status_promo == 2  # Status promo terpakai
        ).order_by(DraftVoucher.id.desc())  
        
        result = base_query.all()

        faktur_list = []
        for row in result:
            pieces_order = float(row.pieces_order or 0)
            box_order = float(row.box_order or 0)
            karton_order = float(row.karton_order or 0)
            pieces_per_box = float(row.pieces_per_box or 1)
            pieces_per_karton = float(row.pieces_per_karton or 1)
            harga_order = float(row.harga_order or 0)
            ppn = float(row.ppn or 0)

            if pieces_per_box <= 0: pieces_per_box = 1.0
            if pieces_per_karton <= 0: pieces_per_karton = 1.0

            uom_data = { 'pieces': pieces_order, 'box': box_order, 'karton': karton_order }
            factor_data = { 'box': pieces_per_box, 'karton': pieces_per_karton }
            
            converter = convert_uom(uom_data, factor_data)
            total_pieces = converter.convert_to('pieces').get()['pieces']
            
            calculated_dpp = harga_order * total_pieces
            calculated_ppn_value = calculated_dpp * (ppn / 100)
            calculated_total_with_ppn = calculated_dpp + calculated_ppn_value

            faktur_list.append({
                'id': row.id or 0,
                'no_faktur': row.no_faktur or '',
                'customer': row.customer or '',
                'estimasi_klaim': float(row.estimasi_klaim or 0),
                'status_promo': self._get_status_voucher(row.status_promo),
                'ppn': ppn,
                'calculated_dpp': calculated_dpp,
                'calculated_ppn_value': calculated_ppn_value,
                'calculated_total_with_ppn': calculated_total_with_ppn,  
                'box_order': int(box_order),
                'pieces_order': int(pieces_order),
                'karton_order': int(karton_order),
                'harga_order': float(harga_order),
                'total_pieces': int(total_pieces)
            })

        pagination_result = self.apply_pagination(faktur_list)
        return {
            'pages': pagination_result['pages'],
            'total_data': pagination_result['total_data'],
            'status': 'success'
        }
        
    @handle_error
    def getKlaimKategori(self):
        query = self.db.session.query(
            KlaimKategori.id,
            KlaimKategori.nama,
            KlaimKategori.deskripsi
        ).select_from(KlaimKategori
        ).order_by(KlaimKategori.id.asc())
        
        result = [{
            "id": row.id,
            "nama": row.nama,
            "deskripsi": row.deskripsi
        } for row in query.all()]

        return result

    @handle_error
    def ajukanDataKlaim(self):
        data = request.get_json() or {}
        
        kode_voucher = data.get('kode_voucher')
        voucher_row = self.db.session.query(V2).filter(
            V2.kode_voucher == kode_voucher
        ).first()
        tipe_voucher = 2
        
        if not voucher_row:
            voucher_row = self.db.session.query(V3).filter(
                V3.kode_voucher == kode_voucher
            ).first()
            tipe_voucher = 3
            
        id_voucher = voucher_row.id if voucher_row else None
        id_user_adm_klaim = getattr(g, "user_id", None) or data.get("id_user_adm_klaim")
        
        klaim_obj = Klaim(
            id_voucher = id_voucher,
            kode_voucher = kode_voucher,
            total_dpp = data.get('total_dpp'),
            total_ppn = data.get('total_ppn'),
            total_pph = data.get('total_pph'),
            nomor_klaim = data.get('nomor_klaim'),
            id_user_adm_klaim = id_user_adm_klaim,
            id_kategori_klaim = data.get('id_kategori_klaim'),
            total_klaim_diajukan = data.get('total_klaim_diajukan'),
            tanggal_pengajuan_klaim = data.get('tanggal_pengajuan_klaim'),
            status = 1 if data.get('status_klaim') else 0
        )
        self.db.session.add(klaim_obj)
        self.db.session.flush()
        
        draft_voucher_ids = data.get('id_draft_voucher', [])
        if isinstance(draft_voucher_ids, int):
            draft_voucher_ids = [draft_voucher_ids] 
        elif not isinstance(draft_voucher_ids, list):
            draft_voucher_ids = []
        
        for draft_voucher_id in draft_voucher_ids:
           klaim_detail_obj = KlaimDetail(
                id_klaim = klaim_obj.id,
                id_draft_voucher = draft_voucher_id,
                dpp = data.get('dpp', 0),
                ppn = data.get('ppn', 0),
                pph = data.get('pph', 0),
           )
           
        self.db.session.add(klaim_detail_obj)
        self.db.session.commit()
        
        return {'status': 'success', 'message': 'Klaim berhasil diajukan'}

    @handle_error
    def getKlaimPromo(self, filters=None):
        if filters is None:
            filters = request.args.to_dict()
            
        base_query = self.db.session.query(
            Klaim.id.label('id'),
            Klaim.nomor_klaim.label('nomor_klaim'),
            Klaim.id_voucher.label('id_voucher'),
            Klaim.kode_voucher.label('kode_promo'),
            Klaim.total_klaim_diajukan.label('nominal_klaim'),
            Klaim.status.label('status_klaim'),
            func.coalesce(V2.nama_voucher, V3.nama_voucher).label('nama_promo'),
            func.coalesce(V2.id_principal, V3.id_principal).label('id_principal'),
            Principal.nama.label('principal')
        ).select_from(Klaim) \
        .outerjoin(V2, V2.kode_voucher == Klaim.kode_voucher) \
        .outerjoin(V3, V3.kode_voucher == Klaim.kode_voucher) \
        .outerjoin(Principal, Principal.id == func.coalesce(V2.id_principal, V3.id_principal))
        
        filtered_query = self.apply_filters_klaim(base_query, filters)
        result = filtered_query.order_by(Klaim.id.desc()).all()

        klaim_data = []
        for row in result:
            klaim_entry = {
                'id': row.id or 0,
                'nomor_klaim': row.nomor_klaim or '',
                'kode_promo': row.kode_promo or '',
                'nama_promo': row.nama_promo or '',
                'nominal_klaim': float(row.nominal_klaim or 0),
                'status_klaim': self._get_status_klaim(row.status_klaim),
                'principal': row.principal or ''
            }
            klaim_data.append(klaim_entry)
            
        pagination_result = self.apply_pagination(klaim_data, filters)
        return {
            'pages': pagination_result['pages'],
            'total_data': pagination_result['total_data'],
            'status': 'success'
        }
 
    @handle_error
    def getKlaimDetail(self, id, status_filter=None):
        klaim_query = self.db.session.query(
            Klaim.id,
            Klaim.nomor_klaim,
            Klaim.kode_voucher.label('kode_promo'),
            Klaim.total_klaim_diajukan,
            Klaim.tanggal_pengajuan_klaim,
            Klaim.id_kategori_klaim,
            Klaim.tanggal_pengajuan_klaim,
            Klaim.total_dpp,
            Klaim.total_ppn,
            Klaim.total_pph,
            Principal.nama.label('principal'),
            KlaimKategori.nama.label('nama_kategori_klaim'),
            func.coalesce(V2.nama_voucher, V3.nama_voucher).label('nama_promo'),
            Klaim.status.label('status_klaim_id')
        ).outerjoin(V2, V2.kode_voucher == Klaim.kode_voucher) \
         .outerjoin(V3, V3.kode_voucher == Klaim.kode_voucher) \
         .outerjoin(Principal, Principal.id == func.coalesce(V2.id_principal, V3.id_principal)) \
         .outerjoin(KlaimKategori, KlaimKategori.id == Klaim.id_kategori_klaim) \
         .filter(Klaim.id == id)

        if status_filter:
            klaim_query = klaim_query.filter(Klaim.status == status_filter)

        klaim_query = klaim_query.first()

        if not klaim_query:
            raise nonServerErrorException(404, "Klaim tidak ditemukan")

        return {
            'id': klaim_query.id,
            'nomor_klaim': klaim_query.nomor_klaim,
            'kode_promo': klaim_query.kode_promo,
            'nama_promo': klaim_query.nama_promo,
            'principal': klaim_query.principal,
            'total_dpp': klaim_query.total_dpp,
            'total_ppn': klaim_query.total_ppn,
            'total_pph': klaim_query.total_pph,
            'id_kategori_klaim': klaim_query.id_kategori_klaim,
            'nama_kategori_klaim': klaim_query.nama_kategori_klaim,
            'total_klaim_diajukan': klaim_query.total_klaim_diajukan,
            'tanggal_pengajuan_klaim': klaim_query.tanggal_pengajuan_klaim,
            'status_klaim': self._get_status_klaim(klaim_query.status_klaim_id),
        }

    @handle_error
    def updateKlaimStatus(self, klaim_id, status):
        klaim_obj = self.db.session.query(Klaim).filter(Klaim.id == klaim_id, Klaim.status != 4).first()
        if not klaim_obj:
            raise nonServerErrorException(404, "Klaim tidak ditemukan")

        klaim_obj.status = status
        self.db.session.commit()

        return {
            'status': 'success',
            'message': 'Status klaim berhasil diperbarui',
        }

    @handle_error
    def ajukanUlangKlaim(self):
        data = request.get_json() or {}
        klaim_id = data.get('klaim_id')
        
        if not klaim_id:
            raise nonServerErrorException(400, "ID klaim harus diisi")
        
        existing_klaim = self.db.session.query(Klaim).filter(Klaim.id == klaim_id).first()
        if not existing_klaim:
            raise nonServerErrorException(404, "Klaim yang akan diajukan ulang tidak ditemukan")
        
        if existing_klaim.status != 3:
            raise nonServerErrorException(400, "Hanya klaim yang ditolak yang dapat diajukan ulang")
        
        existing_klaim.status = 1
        existing_klaim.total_dpp = data.get('total_dpp')
        existing_klaim.total_ppn = data.get('total_ppn')
        existing_klaim.total_pph = data.get('total_pph')
        existing_klaim.id_kategori_klaim = data.get('id_kategori_klaim')
        existing_klaim.total_klaim_diajukan = data.get('total_klaim_diajukan')
        existing_klaim.tanggal_pengajuan_klaim = data.get('tanggal_pengajuan_klaim')
        
        draft_voucher_ids = data.get('id_draft_voucher', [])
        if isinstance(draft_voucher_ids, int):
            draft_voucher_ids = [draft_voucher_ids]
        elif not isinstance(draft_voucher_ids, list):
            draft_voucher_ids = []
        
        if draft_voucher_ids:
            self.db.session.query(KlaimDetail).filter(
                KlaimDetail.id_klaim == klaim_id
            ).delete()
            for draft_voucher_id in draft_voucher_ids:
                klaim_detail_obj = KlaimDetail(
                    id_klaim = klaim_id,
                    id_draft_voucher = draft_voucher_id,
                    dpp = data.get('dpp', 0),
                    ppn = data.get('ppn', 0),
                    pph = data.get('pph', 0),
                )
                self.db.session.add(klaim_detail_obj)
        
        self.db.session.commit()
        return {'status': 'success', 'message': 'Klaim berhasil diajukan ulang'}

    """
    =====================
    Kasbon Service Layer
    =====================
    """
    def _calculate_kasbon_counter(self, id_principal, tanggal_pengajuan):
        tanggal_str = tanggal_pengajuan.strftime('%Y%m%d') \
            if isinstance(tanggal_pengajuan, datetime) \
            else tanggal_pengajuan.replace('-', '')
            
        existing_count = self.db.session.query(
            func.count(KasbonKlaim.id_kasbon_klaim)
            ).filter(
                KasbonKlaim.id_principal == id_principal
            ).scalar() or 0
    
        return existing_count + 1
    
    def _generate_kasbon_code(self, id_principal, tanggal_pengajuan):
        principal = self.db.session.query(Principal) \
            .filter(Principal.id == id_principal).first()
            
        if not principal:
            raise nonServerErrorException(404, "Principal tidak ditemukan")
        
        if isinstance(tanggal_pengajuan, str):
            tanggal_obj = datetime.strptime(tanggal_pengajuan, '%Y-%m-%d')
        else:
            tanggal_obj = tanggal_pengajuan
        
        tanggal_str = tanggal_obj.strftime('%Y%m%d')
        counter = self._calculate_kasbon_counter(id_principal, tanggal_obj)
        kode_kasbon = f"OUT/KSB/{tanggal_str}/{principal.kode}/{counter:04d}"
        
        return kode_kasbon, counter
    
    @handle_error
    def getKasbonKlaim(self, filters=None):
        if filters is None:
            filters = request.args.to_dict()
        
        base_query = self.db.session.query(
            KasbonKlaim.id_kasbon_klaim.label('id'),
            KasbonKlaim.kode_kasbon_klaim.label('kode_kasbon_klaim'),
            KasbonKlaim.tanggal_pengajuan.label('tanggal_pengajuan'),
            KasbonKlaim.nominal_kasbon_diajukan.label('nominal_kasbon_diajukan'),
            KasbonKlaim.nominal_kasbon_disetujui.label('nominal_kasbon_disetujui'),
            KasbonKlaim.total_kasbon_terpakai.label('total_kasbon_terpakai'),
            KasbonKlaim.keterangan.label('keterangan'),
            KasbonKlaim.status_kasbon.label('status_kasbon'),
            KasbonKlaim.tipe_kasbon.label('tipe_kasbon'),
            Principal.nama.label('principal')
        ).select_from(KasbonKlaim) \
        .join(Principal, KasbonKlaim.id_principal == Principal.id)
        
        filtered_query = self.apply_filters_kasbon(base_query, filters)
        result = filtered_query.order_by(KasbonKlaim.id_kasbon_klaim.desc()).all()

        kasbon_data = []
        for row in result:
            kasbon_entry = {
                'id': row.id or 0,
                'kode_kasbon_klaim': row.kode_kasbon_klaim or '',
                'tanggal_pengajuan': row.tanggal_pengajuan.strftime('%Y-%m-%d') if row.tanggal_pengajuan else '',
                'nominal_kasbon_diajukan': float(row.nominal_kasbon_diajukan or 0),
                'nominal_kasbon_disetujui': float(row.nominal_kasbon_disetujui or 0),
                'total_kasbon_terpakai': float(row.total_kasbon_terpakai or 0),
                'keterangan': row.keterangan or '',
                'status_kasbon': self._get_status_kasbon(row.status_kasbon),
                'tipe_kasbon': self._get_tipe_kasbon(row.tipe_kasbon),
                'principal': row.principal or ''
            }
            kasbon_data.append(kasbon_entry)
            
        pagination_result = self.apply_pagination(kasbon_data, filters)
        return {
            'pages': pagination_result['pages'],
            'total_data': pagination_result['total_data'],
            'status': 'success'
        }

    @handle_error
    def ajukanKasbonKlaim(self):
        data = request.get_json() or {}
        
        id_principal = data.get('id_principal')
        tanggal_pengajuan = data.get('tanggal_pengajuan')
        nominal_kasbon_diajukan = data.get('nominal_kasbon_diajukan')
        id_user_pengaju = getattr(g, "user_id", None) or data.get("id_user_pengaju")
        kode_kasbon, counter = self._generate_kasbon_code(id_principal, tanggal_pengajuan)
    
        kasbon_obj = KasbonKlaim(
            kode_kasbon_klaim = kode_kasbon,
            tanggal_pengajuan = tanggal_pengajuan,
            nominal_kasbon_diajukan = float(nominal_kasbon_diajukan),
            nominal_kasbon_disetujui = int(nominal_kasbon_diajukan),
            total_kasbon_terpakai = 0.0,
            keterangan = data.get('keterangan', ''),
            status_kasbon = 0,
            id_user_pengaju = id_user_pengaju,
            id_user_approval = None,
            id_principal = id_principal,
            tipe_kasbon = data.get('tipe_kasbon', 1)
        )
        self.db.session.add(kasbon_obj)
        self.db.session.flush()
        
        kasbon_detail_obj = KasbonKlaimDetail(
            id_kasbon_klaim=kasbon_obj.id_kasbon_klaim,
            id_klaim = None,
            nominal_dijamin = data.get('nominal_kasbon_disetujui', 0.0),
        )
        self.db.session.add(kasbon_detail_obj)

        data_principal = self.db.session.query(Principal).filter(
            Principal.id == id_principal
        ).first()

        payload_pubsub = {
            "id_fitur_mal":24,
            "id_kasbon_klaim":kasbon_obj.id_kasbon_klaim,
            "created_by":id_user_pengaju,
            "id_principal":id_principal,
            "id_cabang": None,
            "id_perusahaan": data_principal.id_perusahaan,
        }

        pubsub = getattr(current_app, 'pubsub', None)
        if pubsub:
            success = pubsub.publish(data=payload_pubsub, topic='create_jurnal')
            if success:
                current_app.logger.info('Published Jurnal')
            else:
                current_app.logger.error('Failed to publish Jurnal')
                raise nonServerErrorException(status_code=500, message='Gagal mengirim pesan ke sistem jurnal')
        else:
            current_app.logger.error('PubSub not configured in the app')
            raise nonServerErrorException(status_code=500, message='Gagal mengirim pesan ke sistem jurnal')

        self.db.session.commit()
        
        return {
            'status': 'success',
            'message': 'Kasbon berhasil diajukan',
            'kode_kasbon': kode_kasbon,
            'id_kasbon': kasbon_obj.id_kasbon_klaim,
            'id_kasbon_detail': kasbon_detail_obj.id_kasbon_klaim_detail
        }

    @handle_error
    def getKasbonKlaimDetail(self, id_kasbon_klaim):
        kasbon_query = self.db.session.query(
            KasbonKlaim.id_kasbon_klaim.label('id'),
            KasbonKlaim.kode_kasbon_klaim.label('kode_kasbon_klaim'),
            KasbonKlaim.tanggal_pengajuan.label('tanggal_pengajuan'),
            KasbonKlaim.nominal_kasbon_diajukan.label('nominal_kasbon_diajukan'),
            KasbonKlaim.nominal_kasbon_disetujui.label('nominal_kasbon_disetujui'),
            KasbonKlaim.total_kasbon_terpakai.label('total_kasbon_terpakai'),
            KasbonKlaim.keterangan.label('keterangan'),
            KasbonKlaim.status_kasbon.label('status_kasbon'),
            KasbonKlaim.tipe_kasbon.label('tipe_kasbon'),
            Principal.nama.label('principal')
        ).select_from(KasbonKlaim) \
        .join(Principal, KasbonKlaim.id_principal == Principal.id) \
        .filter(KasbonKlaim.id_kasbon_klaim == id_kasbon_klaim).first()

        if not kasbon_query:
            raise nonServerErrorException(404, "Data kasbon klaim tidak ditemukan")

        kasbon_detail = {
            'id': kasbon_query.id or 0,
            'kode_kasbon_klaim': kasbon_query.kode_kasbon_klaim or '',
            'tanggal_pengajuan': self._format_date(kasbon_query.tanggal_pengajuan),
            'nominal_kasbon_diajukan': float(kasbon_query.nominal_kasbon_diajukan or 0),
            'nominal_kasbon_disetujui': float(kasbon_query.nominal_kasbon_disetujui or 0),
            'total_kasbon_terpakai': float(kasbon_query.total_kasbon_terpakai or 0),
            'keterangan': kasbon_query.keterangan or '',
            'status_kasbon': self._get_status_kasbon(kasbon_query.status_kasbon),
            'tipe_kasbon': self._get_tipe_kasbon(kasbon_query.tipe_kasbon),
            'principal': kasbon_query.principal or ''
        }

        return kasbon_detail

    @handle_error
    def getListDetailKasbonKlaim(self, id_kasbon_klaim, filters=None):
        if filters is None:
            filters = request.args.to_dict()
            
        kasbon_klaim = self.db.session.query(KasbonKlaim).filter(
            KasbonKlaim.id_kasbon_klaim == id_kasbon_klaim
        ).first()
        
        if not kasbon_klaim:
            raise nonServerErrorException(404, "Kasbon klaim tidak ditemukan")
            
        base_query = self.db.session.query(
            Klaim.id.label('id'),
            Klaim.nomor_klaim.label('nomor_klaim'),
            Klaim.kode_voucher.label('kode_promo'),
            Klaim.total_klaim_diajukan.label('nominal_klaim'),
            Klaim.status.label('status_klaim'),
            func.coalesce(V2.nama_voucher, V3.nama_voucher).label('nama_promo'),
            Principal.nama.label('principal')
        ).select_from(Klaim) \
        .outerjoin(V2, V2.kode_voucher == Klaim.kode_voucher) \
        .outerjoin(V3, V3.kode_voucher == Klaim.kode_voucher) \
        .outerjoin(Principal, Principal.id == func.coalesce(V2.id_principal, V3.id_principal)) \
        .filter(KasbonKlaimDetail.id_kasbon_klaim == id_kasbon_klaim) \
        .distinct()
        
        filtered_query = self.apply_filters_klaim(base_query, filters)
        result = filtered_query.order_by(Klaim.id.desc()).all()
        
        klaim_data = []
        for row in result:
            klaim_entry = {
                'id': row.id or 0,
                'nomor_klaim': row.nomor_klaim or '',
                'kode_promo': row.kode_promo or '',
                'nama_promo': row.nama_promo or '',
                'nominal_klaim': float(row.nominal_klaim or 0),
                'status_klaim': self._get_status_klaim(row.status_klaim),
                'principal': row.principal or ''
            }
            klaim_data.append(klaim_entry)
            
        pagination_result = self.apply_pagination(klaim_data, filters)
        return {
            'pages': pagination_result['pages'],
            'total_data': pagination_result['total_data'],
            'status': 'success'
        }

    @handle_error
    def konfirmasiKasbonKlaim(self, id_kasbon_klaim):
        data = request.get_json() or {}
        selectedKlaim_ids = data.get("selectedKlaimIds", [])

        if not selectedKlaim_ids:
            raise nonServerErrorException(400, "No claims selected")
        
        kasbon_obj = self.db.session.query(KasbonKlaim).filter(
            KasbonKlaim.id_kasbon_klaim == id_kasbon_klaim
        ).first()
        
        if not kasbon_obj:
            raise nonServerErrorException(404, "Kasbon klaim tidak ditemukan")  

        klaim_objs = self.db.session.query(Klaim) \
            .filter(Klaim.id.in_(selectedKlaim_ids)).all()
            
        for klaim in klaim_objs:
            klaim.status = 2    # Klaim Disetujui
            klaim.tanggal_penerimaan_klaim = datetime.now()
            klaim.total_klaim_diterima = klaim.total_klaim_diajukan
            
        total_kasbon_terpakai = sum([
            float(klaim.total_klaim_diajukan or 0) for klaim in klaim_objs
        ])
        
        kasbon_obj.total_kasbon_terpakai = total_kasbon_terpakai
        kasbon_obj.id_user_approval = data.get("id_user_approval")
        kasbon_obj.status_kasbon = 3  # Kasbon Klaim Diberikan

        for klaim in klaim_objs:
            existing_detail = self.db.session.query(KasbonKlaimDetail).filter(
                KasbonKlaimDetail.id_kasbon_klaim == id_kasbon_klaim,
                KasbonKlaimDetail.id_klaim == klaim.id
            ).first()
            
            if not existing_detail:
                kasbon_detail_obj = KasbonKlaimDetail(
                    id_kasbon_klaim = id_kasbon_klaim,
                    id_klaim = klaim.id,
                    nominal_dijamin = float(klaim.total_klaim_diajukan or 0)
                )
                self.db.session.add(kasbon_detail_obj)

        data_principal = self.db.session.query(Principal).filter(
            Principal.id == kasbon_obj.id_principal
        ).first()

        payload_pubsub = {
            "id_fitur_mal": 25,
            "id_kasbon_klaim": id_kasbon_klaim,
            "created_by": data.get("id_user_approval"),
            "id_principal": kasbon_obj.id_principal,
            "id_cabang": None,
            "id_perusahaan": data_principal.id_perusahaan,
        }

        pubsub = getattr(current_app, 'pubsub', None)
        if pubsub:
            success = pubsub.publish(data=payload_pubsub, topic='create_jurnal')
            if success:
                current_app.logger.info('Published Jurnal')
            else:
                current_app.logger.error('Failed to publish Jurnal')
                raise nonServerErrorException(status_code=500, message='Gagal mengirim pesan ke sistem jurnal')
        else:
            current_app.logger.error('PubSub not configured in the app')
            raise nonServerErrorException(status_code=500, message='Gagal mengirim pesan ke sistem jurnal')

        self.db.session.commit()

        return {
            "status": "success",
            "message": "Kasbon klaim berhasil dikonfirmasi",
            "total_kasbon_terpakai": total_kasbon_terpakai,
            "updated_klaim_ids": selectedKlaim_ids,
            "id_kasbon_klaim": id_kasbon_klaim
        }

    """
    =========
    Others
    =========
    """
    def _get_cabang_nama(self, voucher_id, tipe_voucher):
        if tipe_voucher == 2:
            cabang_row = (
                self.db.session.query(Cabang.nama)
                .join(V2Cabang, V2Cabang.id_cabang == Cabang.id)
                .filter(V2Cabang.id_voucher == voucher_id)
                .all()
            )
        elif tipe_voucher == 3:
            cabang_row = (
                self.db.session.query(Cabang.nama)
                .join(V3Cabang, V3Cabang.id_cabang == Cabang.id)
                .filter(V3Cabang.id_voucher == voucher_id)
                .all()
            )
        else:
            cabang_row = []
        return ", ".join([row[0] for row in cabang_row]) if cabang_row else ""
     
    def get_voucher_data(self, kode_promo):
        voucher_data = self._build_voucher_query(V2, '2').filter(
            V2.kode_voucher == kode_promo
        ).first()
        
        if voucher_data:
            return voucher_data, 2
            
        voucher_data = self._build_voucher_query(V3, '3').filter(
            V3.kode_voucher == kode_promo
        ).first()
        
        if voucher_data:
            return voucher_data, 3
        
        return None, None
            
    def _get_principal_and_perusahaan(self, id_principal):
        principal = self.db.session.query(Principal).filter(Principal.id == id_principal).first()
        if not principal:
            raise nonServerErrorException(404, "Principal tidak ditemukan")
        
        perusahaan = self.db.session.query(Perusahaan).filter(Perusahaan.id == principal.id_perusahaan).first()
        if not perusahaan:
            raise nonServerErrorException(404, "Perusahaan tidak ditemukan")
        
        return principal, perusahaan
