from flask import json, current_app, jsonify, request, copy_current_request_context
from sqlalchemy import func , desc, text
import re, json
import threading

from apps.handler import *
from apps.models import (
    Cabang, Principal,
    User, UserJabatan,
    PurchaseOrder as Order,
    PurchaseOrderDetail as OrderDetail,
    PurchaseOrderDetailJumlah as OrderDetailJumlah,
    PurchaseOrderProsesLog as OrderProsesLog,
    Stok
)
from apps.widget import *
from . import Base, ProdukService as Produk
from ..query import DB
from apps.lib.pubsub import PubSub




def parse_laravel_payload(flat_data):
    result = {}
    for key, value in flat_data.items():
        parts = re.findall(r'([^\[\]]+)', key)
        current = result
        for i, part in enumerate(parts):
            if part.isdigit():
                part = int(part)

            if i == len(parts) - 1:
                current[part] = value
            else:
                if part not in current:
                    next_part = parts[i+1]
                    current[part] = {} # Selalu gunakan dict dulu untuk menampung index
                current = current[part]

    # Fungsi pembantu untuk mengubah dict ber-index angka menjadi list
    def densify(data):
        if isinstance(data, dict):
            # Cek apakah semua key adalah integer
            if data and all(isinstance(k, int) for k in data.keys()):
                # Urutkan berdasarkan index dan ubah jadi list
                sorted_keys = sorted(data.keys())
                return [densify(data[k]) for k in sorted_keys]
            else:
                # Rekursif untuk dictionary biasa
                return {k: densify(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [densify(i) for i in data]
        return data

    return densify(result)


class PurchaseOrder(Base):

    def __init__(self):
        super().__init__()

    @handle_error
    def query(self, cabang_id=None):
        query = (
            self.db.session.query(
                Order.id,
                Order.kode,
                Order.keterangan,
                Order.proses_id_berjalan,
                OrderProsesLog.proses_id_diselesaikan,
                OrderProsesLog.tanggal,
                OrderProsesLog.waktu,
                Cabang.id.label('cabang_id'),
                Cabang.nama.label('cabang_nama'),
                Principal.id.label('principal_id'),
                Principal.nama.label('principal_nama'),
                User.id.label('user_id'),
                User.nama.label('user_nama'),
                UserJabatan.id.label('user_jabatan_id'),
                UserJabatan.nama.label('user_jabatan_nama')
            )
            .outerjoin(Order.cabang)
            .outerjoin(Order.principal)
            .outerjoin(Order.proses_log)
            .outerjoin(OrderProsesLog.user)
            .outerjoin(OrderProsesLog.user_jabatan)
        )
        
        if cabang_id:
            query = query.filter(Order.cabang_id == cabang_id)
            
        return query

    @handle_error
    def query_laporan(self):
        cabang_id = request.args.get('cabang_id', type=int)
        
        pic_order = self.db.session.query(
            OrderProsesLog.order_id,
            User.nama.label('pic_order_nama')
        ).join(User).filter(OrderProsesLog.proses_id_diselesaikan == 1).subquery()

        pic_konfirmasi = self.db.session.query(
            OrderProsesLog.order_id,
            User.nama.label('pic_konfirmasi_nama')
        ).join(User).filter(OrderProsesLog.proses_id_diselesaikan == 2).subquery()

        base_query = (
            self.db.session.query(
                Order.id,
                Order.kode,
                Order.keterangan,
                Order.proses_id_berjalan,
                func.max(OrderProsesLog.proses_id_diselesaikan).label('proses_id_diselesaikan'),
                func.max(OrderProsesLog.tanggal).label('tanggal'),
                func.max(OrderProsesLog.waktu).label('waktu'),
                Cabang.id.label('cabang_id'),
                Cabang.nama.label('cabang_nama'),
                Principal.id.label('principal_id'),
                Principal.nama.label('principal_nama'),
                pic_order.c.pic_order_nama,
                pic_konfirmasi.c.pic_konfirmasi_nama
            )
            .outerjoin(Order.cabang)
            .outerjoin(Order.principal)
            .outerjoin(Order.proses_log)
            .outerjoin(pic_order, Order.id == pic_order.c.order_id)
            .outerjoin(pic_konfirmasi, Order.id == pic_konfirmasi.c.order_id)
        )

        if cabang_id:
            base_query = base_query.filter(Order.cabang_id == cabang_id)

        filtered_query = self.apply_filters(base_query, [
            {
                'field': Principal.id,
                'param': 'principal_id',
                'converter': int
            },
            {
                'field': Order.proses_id_berjalan,
                'param': 'status',
                'converter': int
            },
            {
                'field': OrderProsesLog.tanggal,
                'param': 'date',
                'type': 'date_range'
            }
        ])

        return filtered_query.group_by(
            Order.id,
            Cabang.id,
            Principal.id,
            pic_order.c.pic_order_nama,
            pic_konfirmasi.c.pic_konfirmasi_nama
        )


    @handle_error
    def fetch_daftar_konfirmasi(self, cabang_id=None):
        with self.db.session.begin():
            return (
                self.query(cabang_id)
                .filter(Order.proses_id_berjalan == 2)
                .filter(OrderProsesLog.proses_id_diselesaikan == 1)
                .all()
            )

    @handle_error
    def fetch_daftar_purchase(self, cabang_id=None):
        with self.db.session.begin():
            return (
                self.query(cabang_id)
                .filter(Order.proses_id_berjalan == 3)
                .filter(OrderProsesLog.proses_id_diselesaikan == 1)
                .all()
            )

    @handle_error
    def fetch_detail_jumlah(self, id):
        return (
            OrderDetailJumlah.query
            .filter_by(order_detail_id=id)
            .order_by(desc(OrderDetailJumlah.uom_level))
            .all()
        )

    @handle_error
    def fetch_log(self, id):
        return (
            OrderProsesLog.query
            .filter_by(order_id=id)
            .order_by(desc(OrderProsesLog.id))
            .first()
        )

    @handle_error
    def fetch_laporan(self):
        with self.db.session.begin():
            results = self.query_laporan().all()
            print("Menampilkan data laporan:", results)  # Debugging line
            return results

    @handle_error
    def kode(self, cabang_id, principal_id):
        # Get cabang name from cabang ID
        cabang = self.db.session.query(Cabang.nama).filter(Cabang.id == cabang_id).first()
        cabang_nama = cabang.nama if cabang else "-"
        
        # Stripping spaces in cabang name
        format_cabang = cabang_nama.strip().replace(" ", "")
        
        # Get Principal data from principal ID
        principal_kode = '-'
        
        if principal_id and principal_id != 0:
            principal = self.db.session.query(
                Principal.kode
            ).filter(Principal.id == principal_id).first()
            
            if principal:
                principal_kode = principal.kode if principal.kode else (
                    principal.nama[:3].upper() if principal.nama else "-"
                )
        
        # Get current date prefix (YYYYMM)
        date_prefix = date_now_without_day_stamp()

        latest_order = self.db.session.query(Order).order_by(Order.id.desc()).first()
        
        # Default value for the latest_counter
        next_counter = 1
        
        if latest_order:
            try:
                parts = latest_order.kode.split('/')
                if len(parts) >= 4:
                    latest_counter = int(parts[-1])
                    next_counter = latest_counter + 1
            except ValueError:
                next_counter = 1

        # Format the counter as a 4-digit zero-padded number
        counter = f"{next_counter:04d}"
        prefix = f"{date_prefix}/{format_cabang}/{principal_kode}"    
        final_format_code = f"{prefix}/{counter}"
        
        return final_format_code

    @handle_error
    def daftar_laporan(self):
        cabang_id = request.args.get('cabang_id', type=int)

        def get_status_label(id):
            status_mapping = {
                1: ("Request", "info"),
                2: ("Need Confirm", "danger"),
                3: ("In Transit", "info"),
                4: ("Closed", "success"),
            }
            status_text, color = status_mapping.get(id, ("Unknown", "secondary"))
            return create_status_button(status_text, color)

        return (
            Mapper(self.fetch_laporan())
            .to_dict()
            .add_col(lambda i: "", "")
            .add_col(lambda i: btn_details(i['id']), "btn_detail")
            .add_col(lambda i: btn_cetak(i['id']), "btn_cetak")
            .add_col(lambda i: get_status_label(i['proses_id_berjalan']), "btn_status")
            .add_col(lambda i: i['pic_order_nama'], "pic_order_nama")
            .add_col(lambda i: i['pic_konfirmasi_nama'], "pic_konfirmasi_nama")
            .get()
        )

    @handle_error
    def daftar_konfirmasi(self):
        cabang_id = request.args.get('cabang_id', type=int)
    
        return (
            Mapper(self.fetch_daftar_konfirmasi(cabang_id))
            .to_dict()
            .add_col(lambda i: "", "")
            .add_col(lambda i: btn_details(i['id']), "btn_detail")
            .get()
        )

    @handle_error
    def daftar_purchase(self):
        cabang_id = request.args.get('cabang_id', type=int)

        return (
            Mapper(self.fetch_daftar_purchase(cabang_id))
            .to_dict()
            .add_col(lambda i: "", "")
            .add_col(lambda i: btn_form(i['id']), "btn_form")
            .get()
        )

    @handle_error
    def detail_produk(self, id):
        # 1. Ambil PPN secara spesifik (Ganti 'persentase_ppn' dengan nama kolom asli di DB Anda)
        # Jika kolom PPN di tabel produk namanya 'ppn', gunakan: SELECT ppn FROM ...
        ppn_row = DB(request).setRawQuery("SELECT ppn FROM produk WHERE id = :id").bindparams(
            {"id": id}).execute().result.fetchone()
        
        try:
            # Jika ppn_row[0] adalah 11, maka jadi 0.11
            ppn_value = (float(ppn_row[0]) / 100) if (ppn_row and ppn_row[0] is not None) else 0.0
        except:
            ppn_value = 0.0

        # 2. Ambil data utama produk
        raw_data = Produk().fetch_detail_transaksi(id)
        if not raw_data:
            return None

        # Ambil dictionary pertama dari list
        if isinstance(raw_data, list) and len(raw_data) > 0:
            item = raw_data[0]
        else:
            item = raw_data

        # Kita susun manual tanpa Mapper agar tidak ada resiko None
        detail_list = [{
            "produk_id": item.get('produk_id'),
            "produk_nama": item.get('nama'),
            "produk_kode": item.get('kode_sku'),
            "produk_harga_beli": float(item.get('harga_beli', 0)),
            "order_id": None,
            "ppn": ppn_value
        }]

        # print("DEBUG DETAIL LIST MANUAL:", detail_list)

        if not detail_list:
            return None

        # 3. Ambil data UOM
        raw_uom = Produk().fetch_detail_transaksi_uom(id)
        if not raw_uom:
            return None

        # Helper functions (Tetap seperti milik Anda, sudah cukup aman)
        def harga_uom(i, j, d):
            try:
                produk_ref = d[0] if isinstance(d, list) else d
                hasil = Produk.konversi_harga(i, j, produk_ref)
                if isinstance(hasil, (tuple, list)): hasil = hasil[0]
                return float(hasil) if hasil is not None else 0.0
            except: return 0.0

        def harga_ppn(i, j, d):
            val_harga = harga_uom(i, j, d)
            return (val_harga * ppn_value) + val_harga

        jumlah = (
            Mapper(raw_uom)
            .to_dict()
            .add_col(lambda i: 0, "jumlah")
            .add_col(lambda i: None, "order_id")
            .add_col(lambda i: None, "subtotal")
            # Pastikan detail_list dilempar ke helper
            .add_col(lambda i, j: harga_uom(i, j, detail_list), "uom_harga_beli")
            .add_col(lambda i, j: harga_ppn(i, j, detail_list), "uom_harga_beli_ppn")
            .get()
        )

        # 4. Gabungkan
        res = detail_list[0]
        res['jumlah'] = jumlah
        
        return res

    @handle_error
    def detail_riwayat_laporan(self, id):
        with self.db.session.begin():
            order = (
                Mapper([Order.find(id)])
                .to_dict()
                .get()
            )[0]  # Get the first (and only) item from the list

            logs = (
                Mapper(OrderProsesLog.query.filter_by(order_id=id).order_by(OrderProsesLog.id).all())
                .to_dict()
                .get()
            )

            request_log = next((log for log in logs if log['proses_id_diselesaikan'] == 1), None)
            konfirmasi_log = next((log for log in logs if log['proses_id_diselesaikan'] == 2), None)

            jumlah = lambda id: (
                Mapper(self.fetch_detail_jumlah(id))
                .to_dict()
                .get()  # Hilangkan edit_col yang mengubah jumlah menjadi None
            )
            detail = (
                Mapper(OrderDetail.find_by(order_id=id))
                .to_dict()
                .add_col(lambda i: jumlah(i['id']), "jumlah")
                .get()
            )

            order['detail'] = detail
            order['request_log'] = request_log
            order['konfirmasi_log'] = konfirmasi_log

            # Ensure user_nama is included for both request and konfirmasi logs
            if request_log:
                request_log['user_nama'] = User.find(request_log['user_id']).nama if request_log['user_id'] else None
            if konfirmasi_log:
                konfirmasi_log['user_nama'] = User.find(konfirmasi_log['user_id']).nama if konfirmasi_log[
                    'user_id'] else None

            return order

    @handle_error
    def detail_riwayat(self, id, jumlah_none=True):
        with self.db.session.begin():
            order = (
                Mapper([Order.find(id)])
                .to_dict()
                .get()
            )
            if jumlah_none:
                jumlah = lambda id: (
                    Mapper(self.fetch_detail_jumlah(id))
                    .to_dict()
                    .get()
                )
            else:
                jumlah = lambda id: (
                    Mapper(self.fetch_detail_jumlah(id))
                    .to_dict()
                    .edit_col(lambda i: None, "jumlah")
                    .get()
                )
            detail = (
                Mapper(OrderDetail.find_by(order_id=id))
                .to_dict()
                .add_col(lambda i: jumlah(i['id']), "jumlah")
                .get()
            )
            log = (
                Mapper([self.fetch_log(id)])
                .to_dict()
                .get()
            )
            order[0]['detail'] = detail
            order[0]['log'] = log[0]
            return order[0]

    @handle_error_rollback
    def proses_request(self):
        try:
            # 1. Ambil payload (Handling JSON & Form-Data Laravel)
            if request.is_json:
                raw_payload = request.get_json()
            else:
                raw_payload = request.form.to_dict()
                
            if not raw_payload:
                raw_data = request.get_data(as_text=True)
                if raw_data:
                    try: raw_payload = json.loads(raw_data)
                    except: pass

            if not raw_payload:
                return {'status': 'error', 'message': 'Payload kosong atau format salah.'}

            # 2. RAPIKAN DATA (Laravel Parser)
            if any('[' in k for k in raw_payload.keys()):
                order_data = parse_laravel_payload(raw_payload)
            else:
                order_data = raw_payload

            # 3. Validasi Dasar
            details = order_data.get('detail', [])
            if not details:
                return {'status': 'error', 'message': 'Detail produk tidak ditemukan.'}

            # --- INISIALISASI VARIABEL UNTUK PUBSUB (DI LUAR SCOPE WITH) ---
            order_id = None
            payload_pubsub = None
            pubsub = getattr(current_app, 'pubsub', None)

            # 4. BLOK TRANSAKSI DATABASE (ATOMIC)
            with self.db.session.begin():
                current_app.logger.info(f"=== PROCESSING PO: {order_data.get('kode')} ===")
                
                # A. SIMPAN HEADER
                new_order = Order(order_data)
                new_order.proses_id_diselesaikan = 1
                new_order.proses_id_berjalan = 2
                new_order.add().flush() 
                order_id = new_order.id # ID didapat setelah flush

                # B. SIMPAN DETAIL & SATUAN
                for detail in details:
                    detail['order_id'] = order_id
                    rincian_jumlah = detail.get('jumlah', [])
                    
                    # Hitung Total Konversi
                    for jm in rincian_jumlah:
                        jm['jumlah'] = int(float(jm.get('jumlah', 0)))
                        jm['uom_faktor_konversi'] = float(jm.get('uom_faktor_konversi', 1))
                        jm['uom_id'] = int(jm.get('uom_id'))

                    total_order = Produk.konversi_jumlah_total(rincian_jumlah)
                    detail['total_order'] = total_order
                    detail['total_tersisa'] = total_order
                    
                    # Insert Detail
                    new_det = OrderDetail(detail)
                    new_det.add().flush() 
                    det_id = new_det.id

                    # Insert Rincian Satuan (UOM)
                    for jm in rincian_jumlah:
                        jm['order_id'] = order_id
                        jm['order_detail_id'] = det_id
                        jm['uom_level'] = int(float(jm.get('uom_level', 0)))
                        jm['uom_harga_beli'] = float(jm.get('uom_harga_beli', 0))
                        jm['uom_harga_beli_ppn'] = float(jm.get('uom_harga_beli_ppn', 0))
                        jm['subtotal'] = float(jm.get('subtotal', 0))
                        OrderDetailJumlah(jm).add()

                # C. LOG PROSES
                log_entry = {
                    'order_id': order_id,
                    'proses_id_diselesaikan': 1,
                    'proses_id_berjalan': 2,
                    'user_id': order_data.get('user_id'),
                    'keterangan': 'Pemesanan Berhasil (Auto Log)'
                }
                OrderProsesLog(log_entry).add()

                # D. AMBIL DATA UNTUK PUBSUB
                query_get_profile = """
                    SELECT p.id_perusahaan, p.id FROM principal p WHERE p.id = :principal_id
                """
                res_profile = self.db.session.execute(
                    text(query_get_profile), {"principal_id": order_data.get('principal_id')}
                ).mappings().fetchone()

                if res_profile:
                    payload_pubsub = {
                        "id_fitur_mal": 17,
                        "id_perusahaan": res_profile['id_perusahaan'],
                        "id_cabang": order_data.get('cabang_id'),
                        "id_principal": res_profile['id'],
                        "id_order": order_id,
                        "created_by": order_data.get("user_id")
                    }

            # --- DI LUAR BLOK WITH: DATABASE SUDAH AUTO-COMMIT DI SINI ---

            # 5. KIRIM PUBSUB (Hanya jika DB sukses commit)
            if order_id and payload_pubsub and pubsub:
                current_app.logger.info(f"Mengirim PubSub untuk PO ID: {order_id} (Setelah Commit)")
                pubsub.publish(topic='create_jurnal', data=payload_pubsub)
            elif not pubsub:
                current_app.logger.error("PubSub object tidak ditemukan di current_app")

            return {
                'status': 'success',
                'message': 'PO Berhasil diproses',
                'order_id': order_id
            }

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            return {'status': 'error', 'message': str(e)}

    @handle_error_rollback
    def proses_konfirmasi(self):
            res_data = None
            id_order = None
            payload_pubsub = None
            pubsub = getattr(current_app, 'pubsub', None)

            try:
                # 1. BLOK TRANSAKSI DATABASE (COMMIT OTOMATIS SAAT KELUAR BLOK 'WITH')
                with self.db.session.begin():
                    data = request.get_json(silent=True) or request.form.to_dict()
                    id_order = int(data.get('order_id'))
                    data['proses_id_diselesaikan'] = 2

                    order = Order.find(id_order)
                    ada_perubahan = any(
                        key in data for key in ['deleted_details', 'edited_details', 'added_details', 'total']
                    )

                    order.proses_id_berjalan = 3

                    if ada_perubahan:
                        if 'deleted_details' in data:
                            deleted = json.loads(data['deleted_details'])
                            for detail in deleted:
                                if id_detail := detail.get('order_detail_id'):
                                    OrderDetailJumlah.query.filter_by(order_detail_id=id_detail).delete()
                                    OrderDetail.query.filter_by(id=id_detail).delete()

                        if 'edited_details' in data:
                            edited = json.loads(data['edited_details'])
                            for detail in edited:
                                if (id_detail := detail.get('order_detail_id')) and (
                                        detail_order := OrderDetail.query.get(id_detail)):
                                    if total_order := detail.get('total_order'):
                                        detail_order.total_order = total_order
                                        detail_order.total_tersisa = total_order
                                    if subtotal := detail.get('subtotal'):
                                        detail_order.subtotal = subtotal

                                    for perubahan in detail.get('perubahan', []):
                                        if data_jumlah := OrderDetailJumlah.query.filter_by(
                                                id=perubahan.get('order_detail_jumlah_id')).first():
                                            data_jumlah.jumlah = perubahan.get('nilai_baru')
                                            data_jumlah.subtotal = perubahan.get('subtotal_baru')

                        if 'added_details' in data:
                            added = json.loads(data['added_details'])
                            for detail in added:
                                ppn_result = DB(request).setRawQuery(
                                    "SELECT ppn FROM produk WHERE id = :id"
                                ).bindparams({"id": detail['produk_id']}).execute().result.fetchone()

                                if ppn_result and ppn_result[0] is not None:
                                    ppn_value = ppn_result[0] / 100
                                else:
                                    ppn_value = 0

                                total_order = 0
                                subtotal = 0
                                produk_harga_beli = 0

                                for data_jumlah in detail.get('jumlah', []):
                                    if data_jumlah['uom_level'] == 1:
                                        produk_harga_beli = data_jumlah['uom_harga_beli']
                                        break

                                for data_jumlah in detail.get('jumlah', []):
                                    if (jumlah := data_jumlah.get('jumlah')) is not None:
                                        jumlah = float(jumlah)
                                        total_order += jumlah * data_jumlah['uom_faktor_konversi']
                                        subtotal += data_jumlah['subtotal']

                                detail_baru = OrderDetail({
                                    'order_id': id_order,
                                    'produk_id': detail['produk_id'],
                                    'produk_kode': detail['produk_kode'],
                                    'produk_nama': detail['produk_nama'],
                                    'produk_harga_beli': produk_harga_beli,
                                    'total_order': total_order,
                                    'total_tersisa': total_order,
                                    'total_terpenuhi': None,
                                    'subtotal': subtotal,
                                    'ppn': ppn_value
                                }).add().flush()

                                for data_jumlah in detail.get('jumlah', []):
                                    OrderDetailJumlah({
                                        'order_id': id_order,
                                        'order_detail_id': detail_baru.id,
                                        'uom_id': data_jumlah['uom_id'],
                                        'uom_kode': data_jumlah['uom_kode'],
                                        'uom_nama': data_jumlah['uom_nama'],
                                        'uom_level': data_jumlah['uom_level'],
                                        'uom_faktor_konversi': data_jumlah['uom_faktor_konversi'],
                                        'uom_harga_beli': data_jumlah['uom_harga_beli'],
                                        'uom_harga_beli_ppn': data_jumlah['uom_harga_beli_ppn'],
                                        'jumlah': data_jumlah.get('jumlah'),
                                        'subtotal': data_jumlah['subtotal']
                                    }).add().flush()

                    if 'total' in data:
                        order.total = float(data['total'])

                    OrderProsesLog(data).add().flush()

                    # PROSES STOK
                    purchase_order = self.db.session.query(Order).get(id_order)
                    order_details = self.db.session.query(OrderDetail).filter(
                        OrderDetail.order_id == id_order
                    ).all()

                    for detail in order_details:
                        existing_stok = self.db.session.query(Stok).filter(
                            Stok.produk_id == detail.produk_id,
                            Stok.cabang_id == purchase_order.cabang_id
                        ).first()

                        if existing_stok:
                            existing_stok.jumlah_incoming += int(detail.total_order)
                            existing_stok.tanggal_update = date_now()
                            existing_stok.waktu_update = time_now()
                        else:
                            new_stok = {
                                'produk_id': detail.produk_id,
                                'cabang_id': purchase_order.cabang_id,
                                'jumlah_incoming': int(detail.total_order),
                                'tanggal_update': date_now(),
                                'waktu_update': time_now(),
                                'jumlah_ready': 0,
                                'jumlah_booked': 0,
                                'jumlah_delivery': 0,
                                'jumlah_gudang': 0,
                                'jumlah_canvas': 0,
                                'jumlah_good': 0,
                                'jumlah_bad': 0,
                                'jumlah_picked': 0,
                                'transfer_out': 0,
                                'transfer_in': 0
                            }
                            Stok(new_stok).add()

                    # Publish to PubSub
                    query_get_profile = "SELECT p.id_perusahaan, p.id FROM principal p WHERE p.id = :pid"
                    res_profile = self.db.session.execute(text(query_get_profile), {"pid": order.principal_id}).mappings().fetchone()

                    if res_profile:
                        payload_pubsub = {
                            "id_fitur_mal": 18,
                            "id_perusahaan": res_profile['id_perusahaan'],
                            "id_cabang": order.cabang_id,
                            "id_principal": res_profile['id'],
                            "id_order": id_order,
                            "created_by": self.data.get("user_id")
                        }

                    res_data = {"message": "Konfirmasi Berhasil", "order_id": id_order}

                # 2. DI LUAR BLOK TRANSAKSI (DATA SUDAH TER-COMMIT KE DB)
                if payload_pubsub and pubsub:
                    # Gunakan copy_current_request_context agar thread baru punya akses ke request
                    @copy_current_request_context
                    def async_publish(p_topic, p_data):
                        try:
                            pubsub.publish(data=p_data, topic=p_topic)
                        except Exception as e:
                            print(f"Async PubSub Error: {str(e)}")

                    # Jalankan di background thread
                    threading.Thread(target=async_publish, args=('create_jurnal', payload_pubsub)).start()
                    print(f"DEBUG: Background thread dimulai untuk PO {id_order}. Thread utama siap return.")

                return handle_response_data(res_data)

            except Exception as e:
                current_app.logger.error(f"Error Konfirmasi: {str(e)}")
                return handle_response_data(None)

    @handle_error_rollback
    def proses_closed(self):
        # 1. Gunakan silent=True agar tidak error 400 jika Content-Type bukan JSON
        data = request.get_json(silent=True) or request.form.to_dict()
        
        if not data:
            return handle_response_data({"error": "Data tidak ditemukan"}), 400

        # Gunakan try-except untuk menangkap error tak terduga
        try:
            # 2. Blok ini akan otomatis COMMIT di akhir atau ROLLBACK jika ada error
            with self.db.session.begin():
                order_id = int(data.get('order_id'))
                user_id = data.get('user_id')
                
                self.data.update({
                    'order_id': order_id,
                    'user_id': user_id,
                    'proses_id_diselesaikan': 0,
                    'tanggal': date_now(),
                    'waktu': time_now()
                })

                order = Order.find(order_id)
                if not order:
                    return handle_response_data({"error": f"Order {order_id} tidak ditemukan"}), 404

                # Ambil detail order
                order_details = self.db.session.query(OrderDetail).filter(
                    OrderDetail.order_id == order_id
                ).all()

                for detail in order_details:
                    if detail.total_tersisa and detail.total_tersisa > 0:
                        # Filter stok berdasarkan produk dan CABANG order (lebih aman)
                        existing_stok = self.db.session.query(Stok).filter(
                            Stok.produk_id == detail.produk_id,
                            Stok.cabang_id == order.cabang_id
                        ).first()

                        if existing_stok:
                            existing_stok.jumlah_incoming -= int(detail.total_tersisa)
                            existing_stok.tanggal_update = date_now()
                            existing_stok.waktu_update = time_now()

                order.proses_id_berjalan = 4
                OrderProsesLog(self.data).add()
                
                # PENTING: JANGAN panggil self.db.session.commit() di sini!
                # Blok 'with self.db.session.begin()' akan melakukannya untuk Anda.

            # 3. Kembalikan menggunakan handler agar seragam
            return handle_response_data({'message': 'Order closed successfully', 'order_id': order_id})

        except Exception as e:
            current_app.logger.error(f"Error pada proses_closed: {str(e)}")
            # Session otomatis rollback di sini karena blok 'with begin'
            return handle_response_data(None)

