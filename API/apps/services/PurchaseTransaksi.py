from flask import current_app, request
from sqlalchemy import text
import json

from apps.handler import *
from apps.models import (
    Cabang,
    Principal,
    User,
    UserJabatan,
    PurchaseOrder as Order,
    PurchaseOrderDetail as OrderDetail,
    PurchaseOrderDetailJumlah as OrderDetailJumlah,
    PurchaseTransaksi as Transaksi,
    PurchaseTransaksiDetail as TransaksiDetail,
    PurchaseTransaksiDetailJumlah as TransaksiDetailJumlah,
    PurchaseTransaksiProsesLog as TransaksiProsesLog,
    Stok,
    LogInventory,
    TipeTransaksi
)
from apps.widget import *
from . import Base
import re



class PurchaseTransaksi(Base):

    def __init__(self):
        super().__init__()

    @handle_error
    def query(self):
        return (
            self.db.session.query(
                Transaksi.id,
                Transaksi.no_transaksi,
                Transaksi.keterangan,
                Transaksi.proses_id_berjalan,
                Transaksi.subtotal,
                Transaksi.potongan,
                Transaksi.batch,
                Transaksi.biaya_lainnya,
                Transaksi.total,
                Transaksi.status_pembayaran,
                TransaksiProsesLog.proses_id_diselesaikan,
                TransaksiProsesLog.tanggal,
                TransaksiProsesLog.waktu,
                Order.id.label('order_id'),
                Order.kode.label('order_kode'),
                Cabang.id.label('cabang_id'),
                Cabang.nama.label('cabang_nama'),
                Principal.id.label('principal_id'),
                Principal.nama.label('principal_nama'),
                User.id.label('user_id'),
                User.nama.label('user_nama'),
                UserJabatan.id.label('user_jabatan_id'),
                UserJabatan.nama.label('user_jabatan_nama')
            )
            .outerjoin(Transaksi.order)
            .outerjoin(Transaksi.proses_log)
            .outerjoin(Order.cabang)
            .outerjoin(Order.principal)
            .outerjoin(TransaksiProsesLog.user)
            .outerjoin(TransaksiProsesLog.user_jabatan)
            .distinct(Transaksi.id)
        )

    @handle_error
    def query_laporan(self):
        # Subquery untuk PIC Penerimaan
        penerimaan_log = self.db.session.query(
            TransaksiProsesLog.transaksi_id,
            User.nama.label('penerimaan_user_nama')
        ).join(User).filter(TransaksiProsesLog.proses_id_diselesaikan == 1).subquery()

        return (
            self.db.session.query(
                Transaksi.id,
                Transaksi.no_transaksi,
                Transaksi.keterangan,
                Transaksi.proses_id_berjalan,
                Transaksi.subtotal,
                Transaksi.potongan,
                Transaksi.biaya_lainnya,
                Transaksi.total,
                Transaksi.jatuh_tempo,
                Transaksi.status_pembayaran,
                TransaksiProsesLog.proses_id_diselesaikan,
                TransaksiProsesLog.tanggal,
                TransaksiProsesLog.waktu,
                Order.id.label('order_id'),
                Order.kode.label('order_kode'),
                Cabang.id.label('cabang_id'),
                Cabang.nama.label('cabang_nama'),
                Principal.id.label('principal_id'),
                Principal.nama.label('principal_nama'),
                penerimaan_log.c.penerimaan_user_nama
            )
            .outerjoin(Transaksi.order)
            .outerjoin(Transaksi.proses_log)
            .outerjoin(Order.cabang)
            .outerjoin(Order.principal)
            .outerjoin(penerimaan_log, Transaksi.id == penerimaan_log.c.transaksi_id)
            .distinct(Transaksi.id)
        )

    @handle_error
    def query_by_order(self, order_id):
        # Subquery untuk PIC Penerimaan
        penerimaan_log = self.db.session.query(
            TransaksiProsesLog.transaksi_id,
            User.nama.label('penerimaan_user_nama')
        ).join(User).filter(TransaksiProsesLog.proses_id_diselesaikan == 1).subquery()

        return (
            self.db.session.query(
                Transaksi.id,
                Transaksi.no_transaksi,
                Transaksi.keterangan,
                Transaksi.proses_id_berjalan,
                Transaksi.subtotal,
                Transaksi.potongan,
                Transaksi.biaya_lainnya,
                Transaksi.total,
                Transaksi.jatuh_tempo,  # Ditambahkan
                Transaksi.status_pembayaran,
                TransaksiProsesLog.proses_id_diselesaikan,  # Ditambahkan
                TransaksiProsesLog.tanggal,
                TransaksiProsesLog.waktu,
                Order.id.label('order_id'),
                Order.kode.label('order_kode'),
                Cabang.id.label('cabang_id'),  # Ditambahkan
                Cabang.nama.label('cabang_nama'),  # Ditambahkan
                Principal.id.label('principal_id'),  # Ditambahkan
                Principal.nama.label('principal_nama'),  # Ditambahkan
                penerimaan_log.c.penerimaan_user_nama
            )
            .outerjoin(Transaksi.order)
            .outerjoin(Transaksi.proses_log)
            .outerjoin(Order.cabang)  # Ditambahkan
            .outerjoin(Order.principal)  # Ditambahkan
            .outerjoin(penerimaan_log, Transaksi.id == penerimaan_log.c.transaksi_id)
            .filter(Order.id == order_id)
            .distinct(Transaksi.id)
        )

    @handle_error
    def query_detail(self, transaksi_id):
        return (
            self.db.session.query(
                TransaksiDetail.id,
                TransaksiDetail.tanggal_expired,
                TransaksiDetail.batch_number,
                TransaksiDetail.subtotal,
                TransaksiDetail.order_detail_id,
                OrderDetail.produk_kode,
                OrderDetail.produk_nama,
                OrderDetail.produk_harga_beli
            )
            .outerjoin(TransaksiDetail.order_detail)
            .filter(TransaksiDetail.transaksi_id == transaksi_id)
        )

    @handle_error
    def query_detail_jumlah(self, detail_id):
        return (
            self.db.session.query(
                TransaksiDetailJumlah.jumlah,
                TransaksiDetailJumlah.subtotal,
                OrderDetailJumlah.uom_id,
                OrderDetailJumlah.uom_kode,
                OrderDetailJumlah.uom_nama,
                OrderDetailJumlah.uom_level,
                OrderDetailJumlah.uom_faktor_konversi,
                OrderDetailJumlah.uom_harga_beli,
                OrderDetailJumlah.uom_harga_beli_ppn,
            )
            .outerjoin(TransaksiDetailJumlah.order_detail_jumlah)
            .filter(TransaksiDetailJumlah.transaksi_detail_id == detail_id)
            .order_by(desc(OrderDetailJumlah.uom_level))
        )

    @handle_error
    def all(self):
        with self.db.session.begin():
            def status(id):
                # Dictionary untuk mapping status
                status_mapping = {
                    1: ("Penerimaan Brg.", "info"),
                    2: ("Konf. Purchase", "danger"),
                    3: ("Pem. Tagihan", "warning"),
                    4: ("Pelunasan", "info"),
                    5: ("Lunas", "success"),
                }

                # Get status text dan warna, default ke "Unknown" dan "secondary" jika id tidak ditemukan
                status_text, color = status_mapping.get(id, ("Unknown", "secondary"))

                return create_status_button(status_text, color)

            return (
                Mapper(self.query_laporan().all())
                .to_dict()
                .add_col(lambda i: "", "")
                .add_col(lambda i: btn_details(i['id']), "btn_detail")
                .add_col(lambda i: btn_cetak(i['id']), "btn_cetak")
                .add_col(lambda i: status(i['proses_id_berjalan']), "btn_status")
                .get()
            )

    @handle_error
    def daftar_transaksi_by_order(self, order_id):
        with self.db.session.begin():
            def status(id):
                # Dictionary untuk mapping status
                status_mapping = {
                    1: ("Penerimaan Brg.", "info"),
                    2: ("Konf. Purchase", "danger"),
                    3: ("Pem. Tagihan", "warning"),
                    4: ("Pelunasan", "info"),
                    5: ("Lunas", "success"),
                }

                # Get status text dan warna, default ke "Unknown" dan "secondary" jika id tidak ditemukan
                status_text, color = status_mapping.get(id, ("Unknown", "secondary"))

                return create_status_button(status_text, color)

            return (
                Mapper(self.query_by_order(order_id).all())
                .to_dict()
                .add_col(lambda i: "", "")
                .add_col(lambda i: btn_details(i['id']), "btn_detail")
                .add_col(lambda i: btn_cetak(i['id']), "btn_cetak")
                .add_col(lambda i: status(i['proses_id_berjalan']), "btn_status")
                .get()
            )

    @handle_error
    def daftar_konfirmasi(self):
        with self.db.session.begin():
            return (
                Mapper(
                    self.query()
                    .filter(Transaksi.proses_id_berjalan == 2)
                    .filter(TransaksiProsesLog.proses_id_diselesaikan == 1)
                    .all()
                ).to_dict()
                .add_col(lambda i: "", "")
                .add_col(lambda i: btn_details(i['id']), "btn_detail")
                .get()
            )

    @handle_error
    def daftar_tagihan(self):
        with self.db.session.begin():
            return (
                Mapper(
                    self.query()
                    .filter(Transaksi.proses_id_berjalan == 3)
                    .filter(TransaksiProsesLog.proses_id_diselesaikan == 2)
                    .all()
                ).to_dict()
                .add_col(lambda i: "", "")
                .add_col(lambda i: in_checkbox(i['id']), "btn_check")
                .get()
            )

    @handle_error
    def detail_riwayat(self, id):
        transaksi = (
            Mapper(
                self.query()
                .filter(Transaksi.id == id)
                .all()
            ).to_dict()
            .get()
        )
        detail = (
            Mapper(self.query_detail(id).all())
            .to_dict()
            .add_col(lambda i: i['subtotal'], "subtotal")
            .get()
        )
        for item in detail:
            item['jumlah'] = (
                Mapper(self.query_detail_jumlah(item['id']).all())
                .to_dict()
                .get()
            )
        transaksi[0]['detail'] = detail

        # Fetch logs for the transaction
        logs = (
            self.db.session.query(
                TransaksiProsesLog.proses_id_diselesaikan,
                TransaksiProsesLog.tanggal,
                TransaksiProsesLog.waktu,
                User.id.label('user_id'),
                User.nama.label('user_nama')
            )
            .join(User, TransaksiProsesLog.user_id == User.id)
            .filter(TransaksiProsesLog.transaksi_id == id)
            .filter(TransaksiProsesLog.proses_id_diselesaikan.in_([1, 2]))
            .all()
        )
        print(logs)
        # Map the logs to a dictionary
        logs_dict = {}
        for log in logs:
            logs_dict[log.proses_id_diselesaikan] = {
                'tanggal': log.tanggal.strftime('%Y-%m-%d') if log.tanggal else '',
                'user_nama': log.user_nama or ''
            }
        # Assign logs to the transaction
        transaksi[0]['penerimaan_log'] = logs_dict.get(1, {'tanggal': '', 'user_nama': ''})
        transaksi[0]['konfirmasi_log'] = logs_dict.get(2, {'tanggal': '', 'user_nama': ''})

        return transaksi[0]


    def nest_dict(self, flat_dict):
        """Mengubah dictionary flat 'detail[0][id]' menjadi nested structure"""
        result = {}
        for key, value in flat_dict.items():
            # Cari semua kunci dalam bracket, misal: detail, 0, jumlah, 0
            parts = re.findall(r'[^\[\]]+', key)
            if not parts:
                continue

            curr = result
            for i in range(len(parts) - 1):
                part = parts[i]
                next_part = parts[i + 1]

                # Tentukan tipe kontainer berikutnya: List jika digit, Dict jika string
                if next_part.isdigit():
                    if part not in curr:
                        curr[part] = {} # Gunakan dict sementara untuk menampung indeks
                    curr = curr[part]
                else:
                    if part not in curr:
                        curr[part] = {}
                    curr = curr[part]

            curr[parts[-1]] = value
        
        # Konversi dict dengan kunci angka menjadi list sungguhan (Recursive)
        return self._convert_to_list(result)
    
    def _convert_to_list(self, obj):
        """Helper untuk mengubah dict berindeks angka menjadi list"""
        if isinstance(obj, dict):
            # Cek apakah semua key adalah angka
            if obj and all(k.isdigit() for k in obj.keys()):
                # Urutkan berdasarkan index dan jadikan list
                sorted_keys = sorted(obj.keys(), key=int)
                return [self._convert_to_list(obj[k]) for k in sorted_keys]
            else:
                # Rekursi untuk isi dictionary
                return {k: self._convert_to_list(v) for k, v in obj.items()}
        return obj

    def proses_penerimaan_barang(self):
        # 1. Ambil data mentah
        raw_data = request.get_json(silent=True) or request.form.to_dict()
        
        # 2. Rekonstruksi data
        if any('[' in k for k in raw_data):
            nested_data = self.nest_dict(raw_data)
        else:
            nested_data = raw_data
        
        # Gabungkan data
        transaksi_data = {**self.data, **nested_data} if hasattr(self, 'data') else nested_data
        
        current_app.logger.info(f"=== DEBUG START: PENERIMAAN BARANG ===")
        current_app.logger.info(f"Data Terstruktur: {json.dumps(transaksi_data, indent=2)}")
        
        try:
            with self.db.session.begin():
                # A. Header Transaksi
                transaksi_obj = Transaksi(transaksi_data)
                transaksi_obj.proses_id_berjalan = 2
                transaksi_obj.status_pembayaran = 1
                transaksi_obj.add().flush()
                
                transaksi_id = transaksi_obj.id
                current_app.logger.info(f"[1] Tersimpan di Transaksi ID: {transaksi_id}")

                # B. Detail Produk
                # Pastikan key 'detail' ada dan berbentuk list
                detail_list = transaksi_data.get('detail', [])
                if isinstance(detail_list, dict): # Jika gagal jadi list, paksa konversi
                    detail_list = [v for k, v in sorted(detail_list.items(), key=lambda x: int(x[0]))]

                for detail in detail_list:
                    if not detail: continue
                    
                    detail['transaksi_id'] = transaksi_id
                    detail_obj = TransaksiDetail(detail)
                    detail_obj.add().flush()
                    current_app.logger.info(f"  [2] Tersimpan Detail Produk (ID: {detail_obj.id})")

                    total_terpenuhi_increment = 0
                    
                    # C. Rincian Jumlah
                    jumlah_list = detail.get('jumlah', [])
                    if isinstance(jumlah_list, dict):
                        jumlah_list = [v for k, v in sorted(jumlah_list.items(), key=lambda x: int(x[0]))]

                    for jumlah in jumlah_list:
                        if not jumlah or 'jumlah' not in jumlah: continue
                        
                        jumlah['transaksi_id'] = transaksi_id
                        jumlah['transaksi_detail_id'] = detail_obj.id
                        jumlah_obj = TransaksiDetailJumlah(jumlah)
                        jumlah_obj.add().flush()

                        # Hitung UOM
                        uom_konversi = self.db.session.query(OrderDetailJumlah.uom_faktor_konversi) \
                            .filter(OrderDetailJumlah.id == int(jumlah['order_detail_jumlah_id'])).scalar()
                        
                        val_jumlah = int(jumlah.get('jumlah') or 0)
                        total_terpenuhi_increment += val_jumlah * (uom_konversi or 1)

                    # D. Update Order Detail
                    order_detail_id = detail.get('order_detail_id')
                    if order_detail_id:
                        order_detail = self.db.session.query(OrderDetail).get(int(order_detail_id))
                        if order_detail:
                            order_detail.total_terpenuhi = (order_detail.total_terpenuhi or 0) + total_terpenuhi_increment
                            order_detail.total_tersisa = max(0, (order_detail.total_tersisa or 0) - total_terpenuhi_increment)
                            current_app.logger.info(f"  [3] Update Order Detail ID {order_detail.id}: +{total_terpenuhi_increment}")

                # E. Log Proses
                log_data = {
                    'transaksi_id': transaksi_id,
                    'proses_id_diselesaikan': 1,
                    'tanggal': date_now(),
                    'waktu': time_now(),
                    'user_id': transaksi_data.get('user_id'),
                    'user_jabatan_id': transaksi_data.get('user_jabatan_id'),
                }
                TransaksiProsesLog(log_data).add().flush()
                current_app.logger.info(f"[5] Log Proses Selesai.")

            return handle_response_data({'status': 'success', 'id': transaksi_id})

        except Exception as e:
            import traceback
            current_app.logger.error(f"!!! DEBUG ERROR: {str(e)}")
            current_app.logger.error(traceback.format_exc())
            return handle_response_data(None)

    @handle_error_rollback
    @handle_error_rollback
    def konfirmasi_purchase(self): # Hapus 'data' dari sini
        from flask import request
        print("!!! TRACE: Fungsi konfirmasi_purchase DIMULAI !!!")
        
        # 1. Ambil data secara fleksibel (Form atau JSON)
        raw_data = request.form.to_dict() if request.form else (request.get_json(silent=True) or {})
        print("!!! DATA DITERIMA:", raw_data)

        transaksi_id = raw_data.get('order_id')
        user_id = raw_data.get('user_id')
        
        if not transaksi_id:
            return {'error': 'order_id tidak ditemukan', 'status': 'failed'}

        try:
            payload_pubsub = None
            total_final = 0

            with self.db.session.begin():
                # Pastikan transaksi_id dikonversi ke integer jika perlu
                purchase_transaksi = Transaksi.query.get(transaksi_id)
                if not purchase_transaksi:
                    return {'error': f'Transaksi {transaksi_id} tidak ditemukan'}

                # Update Jatuh Tempo
                jatuh_tempo_str = raw_data.get('jatuh_tempo')
                if jatuh_tempo_str:
                    purchase_transaksi.jatuh_tempo = datetime_to_string(jatuh_tempo_str)

                # Perhitungan dengan konversi float yang aman
                def safe_float(val):
                    try: return float(val) if val else 0.0
                    except: return 0.0

                potongan = safe_float(raw_data.get('potongan'))
                biaya_lainnya = safe_float(raw_data.get('biaya_lainnya'))
                subtotal = safe_float(purchase_transaksi.subtotal)

                # Rumus Total
                total_before_ppn = subtotal - potongan
                ppn = total_before_ppn * 0.11
                total_final = total_before_ppn + ppn + biaya_lainnya

                # Update DB
                purchase_transaksi.potongan = potongan
                purchase_transaksi.biaya_lainnya = biaya_lainnya
                purchase_transaksi.total = total_final
                purchase_transaksi.proses_id_berjalan = 3
                
                self.db.session.flush()

                # Log Proses
                new_log = TransaksiProsesLog()
                new_log.transaksi_id = transaksi_id
                new_log.proses_id_diselesaikan = 2
                new_log.tanggal = date_now()
                new_log.waktu = time_now()
                new_log.user_id = user_id
                new_log.user_jabatan_id = raw_data.get('user_jabatan_id')

                self.db.session.add(new_log)
                self.db.session.flush()

                # Query Profile untuk PubSub
                query_get_profile = """
                    SELECT p.id_perusahaan, p.id as principal_id, po.cabang_id 
                    FROM principal p
                    JOIN purchase_order po ON p.id = po.principal_id
                    JOIN purchase_transaksi pt ON po.id = pt.order_id
                    WHERE pt.id = :id_transaksi
                """
                profile = self.db.session.execute(text(query_get_profile), {'id_transaksi': transaksi_id}).mappings().fetchone()

                if profile:
                    id_fitur_mals = [1]
                    if potongan > 0: id_fitur_mals.append(20)

                    payload_pubsub = {
                        "id_fitur_mal": id_fitur_mals,
                        "id_perusahaan": int(profile['id_perusahaan']),
                        "id_cabang": int(profile['cabang_id']),
                        "id_principal": int(profile['principal_id']),
                        # ✅ PERBAIKAN: Kirim sebagai INT murni agar SQL tidak error
                        "id_order": int(transaksi_id), 
                        "created_by": user_id,
                    }

            # 2. Publish di luar blok 'with'
            if payload_pubsub:
                pubsub = getattr(current_app, 'pubsub', None)
                if pubsub:
                    pubsub.publish(data=payload_pubsub, topic='create_jurnal')
                    print(f"DEBUG: Jurnal Fitur {payload_pubsub['id_fitur_mal']} dikirim.")

            # 3. Return response (Pastikan data sederhana agar JSON serializable)
            return {
                'status': 'success',
                'message': 'Konfirmasi Berhasil',
                'transaksi_id': str(transaksi_id),
                'total': float(total_final)
            }

        except Exception as e:
            print(f"!!! ERROR: {str(e)}")
            return {'error': str(e), 'status': 'failed'}

    @handle_error
    def get_last_batch_number(self, order_id):
        """Get the last batch number for a given order_id"""
        with self.db.session.begin():
            last_batch = (
                self.db.session.query(Transaksi.batch)
                .filter(Transaksi.order_id == order_id)
                .order_by(desc(Transaksi.batch))
                .first()
            )
            return (last_batch[0] if last_batch else 0) + 1
