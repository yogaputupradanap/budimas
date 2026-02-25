from flask import jsonify, request, current_app
from sqlalchemy.exc import IntegrityError
from apps import native_db as DB
from sqlalchemy import text
import time
import random
from apps.lib.helper import datetime_now, date_now, time_now, format_angka, format_rupiah, status_order, date_now_obj
from apps.models import (
    Plafon as Plafon,
    proses_picking as prosesPicking,
    faktur as Faktur,
    sales_order,
    sales_order_detail,
    Stok, draft_voucher, Customer, Plafon, setoran, Cabang, Principal, Perusahaan, faktur, faktur_detail,
    order_batch
)

from apps.models.faktur import faktur as Faktur
from apps.models.faktur import faktur

from apps.models.Plafon import Plafon
from apps.models.Plafon import Plafon as plafon

from apps.models.SalesOrder import sales_order
from apps.models.SalesOrderDetail import sales_order_detail
from apps.models.Stok import Stok
from apps.models.Stok import Stok as stok

from apps.models.draft_voucher import draft_voucher
from apps.models.order_batch import OrderBatchModel


from apps.handler import handle_error, handle_error_rollback, nonServerErrorException
from datetime import timedelta, time, datetime, date
from . import BaseServices
import bcrypt

from ..lib.paginateV2 import PaginateV2
from ..models.faktur_detail import FakturDetailModel


# from .. import redis_cache


class Distribusi(BaseServices):
    def __init__(self):
        super().__init__()

        is_periode_close, next_date = self.check_is_periode_closed()

        if is_periode_close:
            self.current_date = next_date.strftime("%Y-%m-%d")
        else:
            self.current_date = date_now()

        self.before_this_date_query = (
            f"and sales_order.tanggal_order <= '{self.current_date}'"
            if self.is_production
            else ''
        )
        self.before_this_date_query_so = (
            f"and so.tanggal_order <= '{self.current_date}'"
            if self.is_production
            else ''
        )
    @handle_error
    # @redis_cache.multi_cached(['sales_order', 'faktur', 'customer', 'plafon', 'principal'], 'getListOrderKonfirmasi')
    def getListOrderKonfirmasi(self):
        id_cabang = self.req('id_cabang')

        query_single_principal = """
            select 
            sales_order.id as id_sales_order,
            faktur.no_faktur,
            sales_order.no_order,
            customer.kode as kode_customer,
            customer.nama as nama_customer,
            principal.kode as kode_principal,
            faktur.total_penjualan as total_bayar,
            faktur.status_faktur,
            sales_order.tanggal_order,
            users.nama as nama_sales
            from sales_order
            join faktur on sales_order.id = faktur.id_sales_order
            join plafon on plafon.id = sales_order.id_plafon
            join customer on plafon.id_customer = customer.id
            join principal on plafon.id_principal = principal.id
            join sales on plafon.id_sales = sales.id
            join users on sales.id_user = users.id
            where 
            sales_order.id_cabang = :id_cabang
            and sales_order.status_order = 0
            order by sales_order.tanggal_order desc;
        """

        query_multiple_principal = """
            SELECT
                array_agg(sales_order.id) AS id_sales_order,
                array_agg(DISTINCT sales_order.no_order) AS no_order,
                faktur.no_faktur,
                customer.kode AS kode_customer,
                customer.nama AS nama_customer,
                'MIX' AS kode_principal,
                faktur.total_penjualan AS total_bayar,
                faktur.status_faktur,
                order_batch.tanggal_submit AS tanggal_order,
                order_batch.id AS id_order_batch,
                users.nama AS nama_sales
            FROM sales_order
            JOIN order_batch ON order_batch.id = sales_order.id_order_batch
            JOIN faktur_detail ON faktur_detail.id_sales_order = sales_order.id
            JOIN faktur ON faktur_detail.id_faktur = faktur.id
            JOIN plafon ON plafon.id = sales_order.id_plafon
            JOIN customer ON plafon.id_customer = customer.id
            JOIN principal ON plafon.id_principal = principal.id
            JOIN sales ON plafon.id_sales = sales.id
            JOIN users ON sales.id_user = users.id
            WHERE sales_order.id_cabang = :id_cabang
            AND sales_order.status_order = 0
            GROUP BY faktur.no_faktur, customer.kode, customer.nama,
                    faktur.total_penjualan, faktur.status_faktur,
                    users.nama, order_batch.id, order_batch.tanggal_submit
        """

        data_order_single_principal = (
            self.query()
            .setRawQuery(query_single_principal)
            .bindparams({'id_cabang': id_cabang})
            .execute()
            .fetchall()
            .result or []
        )

        data_order_multiple_principal = (
            self.query()
            .setRawQuery(query_multiple_principal)
            .bindparams({'id_cabang': id_cabang})
            .execute()
            .fetchall()
            .result or []
        )

        data_all_orders = data_order_single_principal + data_order_multiple_principal

        def normalize_date(value):
            if isinstance(value, (list, tuple)) and value:
                value = value[0]

            if isinstance(value, date):
                return value

            if isinstance(value, str):
                try:
                    return datetime.strptime(value, "%Y-%m-%d").date()
                except ValueError:
                    return date.min

            return date.min


        sorted_data_all_orders = sorted(
            data_all_orders,
            key=lambda data: normalize_date(data['tanggal_order']),
            reverse=True
        )

        # convert Row -> dict
        result = [dict(row._mapping) for row in sorted_data_all_orders]

        return result


    @handle_error_rollback
    def konfirmasiOrder(self, status):
        # Ambil data mentah tanpa di-cast ke int dulu
        raw_id_batch = self.req('id_order_batch')
        
        # Jika id_order_batch ada isinya (bukan None atau string kosong)
        if raw_id_batch and str(raw_id_batch).strip() != "":
            try:
                id_order_batch = int(raw_id_batch)
                return self.__konfirmasi_order_multiple_principal(id_order_batch, status)
            except (ValueError, TypeError):
                return {"status": "error", "message": "Invalid batch ID format"}, 400
        else:
            return self.__konfirmasi_order_single_principal(status)

    def __products_by_id_sales_order(self, products):
        product_dict = {}
        for product in products:
            id_sales_order = product.get('id_sales_order')
            if id_sales_order not in product_dict:
                product_dict[id_sales_order] = []
            product_dict[id_sales_order].append(product)
        return product_dict

    def __konfirmasi_order_multiple_principal(self, id_order_batch, status):
        # Only get id_cabang if status is 1 (konfirmasi), not for status -1 (tolak)
        id_cabang = int(self.req('id_cabang')) if status == 1 else None
        vouchers = self.req('vouchers')
        update_faktur = db.session.query(Faktur).filter(Faktur.id_order_batch == int(id_order_batch)).first()
        products = self.req('products')
        products_by_sales_order = self.__products_by_id_sales_order(products)
        sales_orders = sales_order.query.with_entities(sales_order.id).filter(sales_order.id_order_batch == int(id_order_batch)).all()

        for so in sales_orders:
            id_sales_order = so.id
            update_sales_order = sales_order.query.filter(sales_order.id == id_sales_order).first()
            update_sales_order.status_order = status
            self.add(update_sales_order)

        if status == 1:  # Booked
            total_penjualan = format_angka(self.req('total_penjualan'))
            subtotal_diskon = format_angka(self.req('subtotal_diskon'))
            dpp = format_angka(self.req('dpp'))
            pajak = format_angka(self.req('pajak'))

            update_faktur.total_penjualan = total_penjualan
            update_faktur.draft_total_penjualan = total_penjualan
            update_faktur.subtotal_diskon = subtotal_diskon
            update_faktur.dpp = dpp
            update_faktur.pajak = pajak

            self.add(update_faktur)

            for so in sales_orders:
                id_sales_order = so.id

                pajak_by_sales_order = sum(products.get('subtotalorder',0) * (products.get('ppn',0)/100) for products in products_by_sales_order.get(id_sales_order, []))

                subtotal_penjualan_by_sales_order = sum(products.get('subtotalorder',0) for products in products_by_sales_order.get(id_sales_order, []))

                subtotal_diskon_by_sales_order = sum(
                    sum((products.get(field) or 0) for field in
                        ['v1r_diskon', 'v2p_diskon', 'v2r_diskon', 'v3r_diskon', 'v3p_diskon'])
                    for products in products_by_sales_order.get(id_sales_order, [])
                )

                total_penjualan_by_sales_order = subtotal_penjualan_by_sales_order + pajak_by_sales_order

                plafon_data = plafon.query.filter(plafon.id == update_sales_order.id_plafon).first()
                if plafon_data and plafon_data.sisa_bon is not None:
                    # Validasi lock_order
                    if plafon_data.lock_order == '1':
                        # Jika lock_order = 1, sisa_bon harus sama dengan limit_bon
                        if float(plafon_data.sisa_bon) != float(plafon_data.limit_bon):
                            return {
                                "status": "error",
                                "message": f"Plafon dalam status lock. Sisa bon (Rp {format_rupiah(plafon_data.sisa_bon)}) harus sama dengan limit bon (Rp {format_rupiah(plafon_data.limit_bon)}) untuk melanjutkan transaksi."
                            }, 400

                    if float(total_penjualan_by_sales_order) > float(plafon_data.sisa_bon):
                        return {
                            "status": "error",
                            "message": f"Total penjualan (Rp {format_rupiah(total_penjualan_by_sales_order)}) melebihi sisa plafon (Rp {format_rupiah(plafon_data.sisa_bon)}). Transaksi tidak dapat dilanjutkan."
                        }, 400

                    # Potong sisa_bon dengan total_penjualan
                    plafon_data.sisa_bon = float(plafon_data.sisa_bon) - float(total_penjualan_by_sales_order)

                    update_faktur_detail = FakturDetailModel.query.filter(FakturDetailModel.id_sales_order == int(id_sales_order)).first()
                    if update_faktur_detail:
                        update_faktur_detail.subtotal = subtotal_penjualan_by_sales_order
                        update_faktur_detail.pajak = pajak_by_sales_order
                        update_faktur_detail.subtotal_diskon = subtotal_diskon_by_sales_order
                        update_faktur_detail.total = total_penjualan_by_sales_order
                        update_faktur_detail.draft_total = total_penjualan_by_sales_order
                        self.add(update_faktur_detail)

                    self.add(plafon_data)

            product_discounts = {}

            if vouchers and 'voucher_product' in vouchers:
                voucher_products = vouchers.get('voucher_product', [])

                for product_item in voucher_products:
                    id_sales_order_detail = product_item.get('id_sales_order_detail')
                    if id_sales_order_detail:
                        original_subtotal = format_angka(product_item.get('subtotalorder', 0))

                        total_diskon_produk = 0

                        vouchers_list = product_item.get('vouchers', [])

                        for voucher in vouchers_list:
                            is_active = voucher.get('active', False)
                            if is_active:
                                diskon = format_angka(voucher.get('diskon', 0))
                                total_diskon_produk += diskon

                        product_discounts[int(id_sales_order_detail)] = {
                            'total_diskon': total_diskon_produk,
                            'original_subtotal': original_subtotal
                        }

            for detail_id, values in product_discounts.items():
                detail = sales_order_detail.query.filter(sales_order_detail.id == detail_id).first()
                if detail:
                    detail.total_nilai_discount = format_angka(values['total_diskon'])
                    detail.subtotalorder = format_angka(values['original_subtotal'] - values['total_diskon'])

            voucher_product_data = {}
            if vouchers and 'voucher_product' in vouchers:
                for product in vouchers.get('voucher_product', []):
                    id_sales_order_detail = product.get('id_sales_order_detail')
                    if id_sales_order_detail:
                        voucher_product_data[int(id_sales_order_detail)] = {
                            'id_produk': product.get('id_produk'),
                            'konversi_level1': product.get('konversi_level1', 1),
                            'konversi_level2': product.get('konversi_level2', 1),
                            'konversi_level3': product.get('konversi_level3', 1),
                            'puom1_packing_panjang': product.get('puom1_packing_panjang', 0),
                            'puom1_packing_lebar': product.get('puom1_packing_lebar', 0),
                            'puom1_packing_tinggi': product.get('puom1_packing_tinggi', 0),
                            'puom2_packing_panjang': product.get('puom2_packing_panjang', 0),
                            'puom2_packing_lebar': product.get('puom2_packing_lebar', 0),
                            'puom2_packing_tinggi': product.get('puom2_packing_tinggi', 0),
                            'puom3_packing_panjang': product.get('puom3_packing_panjang', 0),
                            'puom3_packing_lebar': product.get('puom3_packing_lebar', 0),
                            'puom3_packing_tinggi': product.get('puom3_packing_tinggi', 0)
                        }
            for so in sales_orders:
                detail_orders = sales_order_detail.query.filter(
                    sales_order_detail.id_sales_order == so.id
                ).all()

                for detail in detail_orders:
                    detail.pieces_booked = detail.pieces_order
                    detail.box_booked = detail.box_order
                    detail.karton_booked = detail.karton_order
                    konversi_data = voucher_product_data.get(detail.id, {})

                    if konversi_data:
                        volume_pieces = (
                                                float(konversi_data.get('puom1_packing_panjang', 0) or 0) *
                                                float(konversi_data.get('puom1_packing_lebar', 0) or 0) *
                                                float(konversi_data.get('puom1_packing_tinggi', 0) or 0) *
                                                (detail.pieces_order or 0)
                                        ) or 0

                        volume_box = (
                                             float(konversi_data.get('puom2_packing_panjang', 0) or 0) *
                                             float(konversi_data.get('puom2_packing_lebar', 0) or 0) *
                                             float(konversi_data.get('puom2_packing_tinggi', 0) or 0) *
                                             (detail.box_order or 0)
                                     ) or 0

                        volume_karton = (
                                                float(konversi_data.get('puom3_packing_panjang', 0) or 0) *
                                                float(konversi_data.get('puom3_packing_lebar', 0) or 0) *
                                                float(konversi_data.get('puom3_packing_tinggi', 0) or 0) *
                                                (detail.karton_order or 0)
                                        ) or 0

                        produk_kubikasi = (volume_pieces + volume_box + volume_karton) or 0

                        detail.estimasi_kubikasi = produk_kubikasi

                    stok_item = stok.query.filter(
                        stok.produk_id == detail.id_produk,
                        stok.cabang_id == id_cabang
                    ).first()
                    if not stok_item:
                        return {
                            "status": "error",
                            "message": f"Stok tidak ditemukan untuk produk ID {detail.id_produk} di cabang {id_cabang}"
                        }, 404

                    if stok_item:
                        konversi_data = voucher_product_data.get(detail.id, {})

                        konversi_level1 = konversi_data.get('konversi_level1', 1)
                        konversi_level2 = konversi_data.get('konversi_level2')
                        konversi_level3 = konversi_data.get('konversi_level3')

                        total_item_booked = (
                                (detail.pieces_booked * konversi_level1) +
                                (detail.box_booked * konversi_level2) +
                                (detail.karton_booked * konversi_level3)
                        )

                        stok_item.jumlah_booked += total_item_booked
                        stok_item.jumlah_ready -= total_item_booked

            if vouchers and 'voucher_product' in vouchers:
                voucher_products = vouchers.get('voucher_product', [])

                if voucher_products:
                    for product_item in voucher_products:
                        id_sales_order_detail = product_item.get('id_sales_order_detail')
                        vouchers_list = product_item.get('vouchers', [])

                        for voucher in vouchers_list:
                            id_dv = voucher.get('id_dv')
                            is_active = voucher.get('active', False)
                            jumlah_diskon = format_angka(voucher.get('diskon', 0))

                            if id_dv is not None:
                                status_promo = 1 if is_active else 3

                                draft_entry = draft_voucher.query.filter(
                                    draft_voucher.id == id_dv
                                ).first()

                                if draft_entry:
                                    draft_entry.status_promo = status_promo
                                    if is_active:
                                        draft_entry.jumlah_diskon = jumlah_diskon
                                    else:
                                        draft_entry.jumlah_diskon = 0

        elif status == -1:
            update_faktur.status_faktur = status
            self.add(update_faktur)
            draft_entries = (
                draft_voucher.query
                .filter(draft_voucher.id_sales_order.in_([so.id for so in sales_orders]))
                .all()
            )

            if draft_entries:
                for entry in draft_entries:
                    entry.status_promo = 3
                    entry.jumlah_diskon = 0
                    self.add(entry)
            self.flush()

        update_order_batch = OrderBatchModel.query.filter(OrderBatchModel.id == int(id_order_batch)).first()
        if update_order_batch:
            update_order_batch.status_order = 1
            self.add(update_order_batch).flush()

        self.commit()

        return {"status": "success"}, 200

    def __konfirmasi_order_single_principal(self,status):
        id_sales_order = int(self.req('id_sales_order'))
        # Only get id_cabang if status is 1 (konfirmasi), not for status -1 (tolak)
        id_cabang = int(self.req('id_cabang')) if status == 1 else None
        vouchers = self.req('vouchers')

        update_sales_order = sales_order.query.filter(sales_order.id == id_sales_order).first()
        update_faktur = Faktur.query.filter(Faktur.id_sales_order == int(id_sales_order)).first()
        plafon_data = plafon.query.filter(plafon.id == update_sales_order.id_plafon).first()

        update_sales_order.status_order = status

        if status == 1:  # Booked
            total_penjualan = format_angka(self.req('total_penjualan'))
            if plafon_data and plafon_data.sisa_bon is not None:
                # Validasi lock_order
                if plafon_data.lock_order == '1':
                    # Jika lock_order = 1, sisa_bon harus sama dengan limit_bon
                    if float(plafon_data.sisa_bon) != float(plafon_data.limit_bon):
                        return {
                            "status": "error",
                            "message": f"Plafon dalam status lock. Sisa bon (Rp {format_rupiah(plafon_data.sisa_bon)}) harus sama dengan limit bon (Rp {format_rupiah(plafon_data.limit_bon)}) untuk melanjutkan transaksi."
                        }, 400

                if float(total_penjualan) > float(plafon_data.sisa_bon):
                    return {
                        "status": "error",
                        "message": f"Total penjualan (Rp {format_rupiah(total_penjualan)}) melebihi sisa plafon (Rp {format_rupiah(plafon_data.sisa_bon)}). Transaksi tidak dapat dilanjutkan."
                    }, 400

                # Potong sisa_bon dengan total_penjualan
                plafon_data.sisa_bon = float(plafon_data.sisa_bon) - float(total_penjualan)
            subtotal_diskon = format_angka(self.req('subtotal_diskon'))
            dpp = format_angka(self.req('dpp'))
            pajak = format_angka(self.req('pajak'))

            update_faktur.total_penjualan = total_penjualan
            update_faktur.draft_total_penjualan = total_penjualan
            update_faktur.subtotal_diskon = subtotal_diskon
            update_faktur.dpp = dpp
            update_faktur.pajak = pajak

            product_discounts = {}

            if vouchers and 'voucher_product' in vouchers:
                voucher_products = vouchers.get('voucher_product', [])

                for product_item in voucher_products:
                    id_sales_order_detail = product_item.get('id_sales_order_detail')
                    if id_sales_order_detail:
                        original_subtotal = format_angka(product_item.get('subtotalorder', 0))

                        total_diskon_produk = 0

                        vouchers_list = product_item.get('vouchers', [])

                        for voucher in vouchers_list:
                            is_active = voucher.get('active', False)
                            if is_active:
                                diskon = format_angka(voucher.get('diskon', 0))
                                total_diskon_produk += diskon

                        product_discounts[int(id_sales_order_detail)] = {
                            'total_diskon': total_diskon_produk,
                            'original_subtotal': original_subtotal
                        }

            for detail_id, values in product_discounts.items():
                detail = sales_order_detail.query.filter(sales_order_detail.id == detail_id).first()
                if detail:
                    detail.total_nilai_discount = format_angka(values['total_diskon'])
                    detail.subtotalorder = format_angka(values['original_subtotal'] - values['total_diskon'])

            voucher_product_data = {}
            if vouchers and 'voucher_product' in vouchers:
                for product in vouchers.get('voucher_product', []):
                    id_sales_order_detail = product.get('id_sales_order_detail')
                    if id_sales_order_detail:
                        voucher_product_data[int(id_sales_order_detail)] = {
                            'id_produk': product.get('id_produk'),
                            'konversi_level1': product.get('konversi_level1', 1),
                            'konversi_level2': product.get('konversi_level2', 1),
                            'konversi_level3': product.get('konversi_level3', 1),
                            'puom1_packing_panjang': product.get('puom1_packing_panjang', 0),
                            'puom1_packing_lebar': product.get('puom1_packing_lebar', 0),
                            'puom1_packing_tinggi': product.get('puom1_packing_tinggi', 0),
                            'puom2_packing_panjang': product.get('puom2_packing_panjang', 0),
                            'puom2_packing_lebar': product.get('puom2_packing_lebar', 0),
                            'puom2_packing_tinggi': product.get('puom2_packing_tinggi', 0),
                            'puom3_packing_panjang': product.get('puom3_packing_panjang', 0),
                            'puom3_packing_lebar': product.get('puom3_packing_lebar', 0),
                            'puom3_packing_tinggi': product.get('puom3_packing_tinggi', 0)
                        }

            detail_orders = sales_order_detail.query.filter(
                sales_order_detail.id_sales_order == id_sales_order
            ).all()

            for detail in detail_orders:
                detail.pieces_booked = detail.pieces_order
                detail.box_booked = detail.box_order
                detail.karton_booked = detail.karton_order
                konversi_data = voucher_product_data.get(detail.id, {})

                if konversi_data:
                    volume_pieces = (
                                            float(konversi_data.get('puom1_packing_panjang', 0) or 0) *
                                            float(konversi_data.get('puom1_packing_lebar', 0) or 0) *
                                            float(konversi_data.get('puom1_packing_tinggi', 0) or 0) *
                                            (detail.pieces_order or 0)
                                    ) or 0

                    volume_box = (
                                         float(konversi_data.get('puom2_packing_panjang', 0) or 0) *
                                         float(konversi_data.get('puom2_packing_lebar', 0) or 0) *
                                         float(konversi_data.get('puom2_packing_tinggi', 0) or 0) *
                                         (detail.box_order or 0)
                                 ) or 0

                    volume_karton = (
                                            float(konversi_data.get('puom3_packing_panjang', 0) or 0) *
                                            float(konversi_data.get('puom3_packing_lebar', 0) or 0) *
                                            float(konversi_data.get('puom3_packing_tinggi', 0) or 0) *
                                            (detail.karton_order or 0)
                                    ) or 0

                    produk_kubikasi = (volume_pieces + volume_box + volume_karton) or 0

                    detail.estimasi_kubikasi = produk_kubikasi

                    self.add(detail)

                stok_item = (stok.query.filter(
                    stok.produk_id == detail.id_produk,
                    stok.cabang_id == id_cabang
                )
                . with_for_update()
                             .first())
                if not stok_item:
                    return {
                        "status": "error",
                        "message": f"Stok tidak ditemukan untuk produk ID {detail.id_produk} di cabang {id_cabang}"
                    }, 404

                if stok_item:
                    konversi_data = voucher_product_data.get(detail.id, {})

                    konversi_level1 = konversi_data.get('konversi_level1', 1)
                    konversi_level2 = konversi_data.get('konversi_level2')
                    konversi_level3 = konversi_data.get('konversi_level3')

                    total_item_booked = (
                            (detail.pieces_booked * konversi_level1) +
                            (detail.box_booked * konversi_level2) +
                            (detail.karton_booked * konversi_level3)
                    )

                    stok_item.jumlah_booked += total_item_booked
                    stok_item.jumlah_ready -= total_item_booked

                    self.add(stok_item)

            if vouchers and 'voucher_product' in vouchers:
                voucher_products = vouchers.get('voucher_product', [])

                if voucher_products:
                    for product_item in voucher_products:
                        id_sales_order_detail = product_item.get('id_sales_order_detail')
                        vouchers_list = product_item.get('vouchers', [])

                        for voucher in vouchers_list:
                            id_dv = voucher.get('id_dv')
                            is_active = voucher.get('active', False)
                            jumlah_diskon = format_angka(voucher.get('diskon', 0))

                            if id_dv is not None:
                                status_promo = 1 if is_active else 3

                                draft_entry = draft_voucher.query.filter(
                                    draft_voucher.id == id_dv
                                ).first()

                                if draft_entry:
                                    draft_entry.status_promo = status_promo
                                    if is_active:
                                        draft_entry.jumlah_diskon = jumlah_diskon
                                    else:
                                        draft_entry.jumlah_diskon = 0
                                    self.add(draft_entry)

        elif status == -1:
            update_faktur.status_faktur = status
            draft_entries = draft_voucher.query.filter(
                draft_voucher.id_sales_order == id_sales_order
            ).all()

            if draft_entries:
                for entry in draft_entries:
                    entry.status_promo = 3
                    entry.jumlah_diskon = 0

        self.commit()

        return {"status": "success"}, 200

    # @redis_cache.cached('produk_uom', 'getFactorKonversi')
    def getFactorKonversi(self, id_produk):
        return (
            self.query().setRawQuery(
                f"""
                    select faktor_konversi as fk, level
                    from produk_uom 
                    where id_produk = { id_produk }
                    order by level asc
                """
            )
            .execute()
            .fetchall()
            .get()
        )
        
    # def updateTenggatWaktuFaktur(self, id_sales_order):
    #     update_so = (
    #         self.db
    #         .session
    #         .query(sales_order)
    #         .filter(sales_order.id == id_sales_order)
    #         .first()
    #     )
            
    #     add_jatuh_tempo = (update_so.tanggal_jatuh_tempo + timedelta(days=10)).strftime("%Y-%m-%d")
    #     update_so.tanggal_jatuh_tempo = add_jatuh_tempo
    
    def getRoutes(self, id_cabang, status_order):

        order_one_principal_res = (
            self.query().setRawQuery(
                f"""
                    select
                        count (distinct c.nama) as jumlah_toko,
                        count (distinct f.id) as jumlah_nota,
                        coalesce(SUM(sod.estimasi_kubikasi)::NUMERIC, 0) as kubikal,
                        r.id as id_rute,
                        r.nama_rute,
                        r.kode,
                        c.id as id_customer,
                        a.nama as nama_armada,
                        u.nama as nama_driver,
                        d.id as id_driver,
                        pp.delivering_date,
                        a.id as id_armada
                    from rute r
                    join customer c on c.id_rute = r.id
                    join cabang cb on c.id_cabang = cb.id
                    join plafon p on p.id_customer = c.id
                    join sales_order so on so.id_plafon = p.id and so.status_order in {status_order}
                    join faktur f on f.id_sales_order = so.id and f.jenis_faktur = 'penjualan'
                    left join sales_order_detail sod on sod.id_sales_order = so.id
                    left join proses_picking pp on pp.id_order_detail = sod.id
                    left join armada a on a.id = pp.id_armada
                    left join driver d on d.id = pp.id_driver
                    left join users u on u.id = d.id_user
                    where cb.id = :id_cabang
                    {self.before_this_date_query_so}
                    group by r.id, r.nama_rute, r.kode, a.nama, u.nama,
                            pp.delivering_date , d.id, a.id, c.id
                """
            )
            .bindparams({"id_cabang": id_cabang})
            .execute()
            .get()
        )

        order_multiple_principal_res = (
            self.query().setRawQuery(
                f"""
                    select
                        count (distinct c.nama) as jumlah_toko,
                        count (distinct f.id) as jumlah_nota,
                        coalesce(SUM(sod.estimasi_kubikasi)::NUMERIC, 0) as kubikal,
                        r.id as id_rute,
                        r.nama_rute,
                        r.kode,
                        c.id as id_customer,
                        a.nama as nama_armada,
                        u.nama as nama_driver,
                        d.id as id_driver,
                        pp.delivering_date,
                        a.id as id_armada
                    from rute r
                    join customer c on c.id_rute = r.id
                    join cabang cb on c.id_cabang = cb.id
                    join plafon p on p.id_customer = c.id
                    join sales_order so on so.id_plafon = p.id
                    join faktur_detail fd on fd.id_sales_order = so.id
                    join faktur f on f.id = fd.id_faktur
                    left join sales_order_detail sod on sod.id_sales_order = so.id
                    left join proses_picking pp on pp.id_order_detail = sod.id
                    left join armada a on a.id = pp.id_armada
                    left join driver d on d.id = pp.id_driver
                    left join users u on u.id = d.id_user
                    where cb.id = :id_cabang
                    AND f.jenis_faktur = 'penjualan'
                    AND so.status_order in {status_order}
                    {self.before_this_date_query_so}
                    group by r.id, r.nama_rute, r.kode, a.nama, u.nama,
                            pp.delivering_date , d.id, a.id, c.id
                """
            )
            .bindparams({"id_cabang": id_cabang})
            .execute()
            .get()
        )

        order_one_principal = [
            dict(r._mapping) for r in order_one_principal_res.get("result", [])
        ]

        order_multiple_principal = [
            dict(r._mapping) for r in order_multiple_principal_res.get("result", [])
        ]

        merge_all_orders = [
            *order_one_principal,
            *order_multiple_principal
        ]

        grouped_data = []

        for entry in merge_all_orders:
            found = False

            for group in grouped_data:
                if (
                    group['id_rute'] == entry['id_rute']
                    and group['id_armada'] == entry['id_armada']
                    and group['id_driver'] == entry['id_driver']
                    and group['delivering_date'] == entry['delivering_date']
                ):
                    if group['id_customer'] != entry['id_customer']:
                        group['jumlah_toko'] += 1

                    group['jumlah_nota'] += entry['jumlah_nota']
                    group['kubikal'] += entry['kubikal']
                    found = True
                    break

            if not found:
                grouped_data.append(entry)
                

        return grouped_data





        
    @handle_error
    def getRuteArmada(self):
        id_cabang = self.req('id')
        status_order = '(1,9)'
        
        return self.getRoutes(id_cabang, status_order)

    @handle_error
    def getInfoRuteArmada(self):
        id_cabang = self.req('id_cabang')
        id_rute = self.req('id_rute')
        order_one_principal = (
            self.query().setRawQuery(
                f"""
                            select
                                count (distinct c.nama) as jumlah_toko,
                                count (distinct f.id) as jumlah_nota,
                                coalesce(SUM(sod.estimasi_kubikasi)::NUMERIC, 0) as jumlah_kubikal,
                                r.id as id_rute,
                                r.nama_rute,
                                r.kode as kode_rute,
                                c.id as id_customer,
                                a.nama as nama_armada,
                                u.nama as nama_driver,
                                d.id as id_driver,
                                pp.delivering_date,
                                a.id as id_armada
                            from rute r
                            join customer c on c.id_rute = r.id
                            join cabang cb on c.id_cabang = cb.id
                            join plafon p on p.id_customer = c.id
                            join sales_order so on so.id_plafon = p.id and so.status_order in (1,9)
                            join faktur f on f.id_sales_order = so.id and f.jenis_faktur = 'penjualan'
                            left join sales_order_detail sod on sod.id_sales_order = so.id
                            left join proses_picking pp on pp.id_order_detail = sod.id
                            left join armada a on a.id = pp.id_armada
                            left join driver d on d.id = pp.id_driver
                            left join users u on u.id = d.id_user
                            where cb.id = :id_cabang 
                            AND
                            r.id = :id_rute
                            {self.before_this_date_query_so}
                            group by r.id, r.nama_rute, r.kode, a.nama, u.nama, pp.delivering_date , d.id, a.id, c.id
                        """
            )
            .bindparams({
                "id_cabang": id_cabang,
                "id_rute": id_rute
            })
            .execute()
            .fetchall()
            .get()
        )
        order_multiple_principal = (
            self.query().setRawQuery(
                f"""
                            select
                                count (distinct c.nama) as jumlah_toko,
                                count (distinct f.id) as jumlah_nota,
                                coalesce(SUM(sod.estimasi_kubikasi)::NUMERIC, 0) as jumlah_kubikal,
                                r.id as id_rute,
                                r.nama_rute,
                                r.kode as kode_rute,
                                c.id as id_customer,
                                a.nama as nama_armada,
                                u.nama as nama_driver,
                                d.id as id_driver,
                                pp.delivering_date,
                                a.id as id_armada
                            from rute r
                            join customer c on c.id_rute = r.id
                            join cabang cb on c.id_cabang = cb.id
                            join plafon p on p.id_customer = c.id
                            join sales_order so on so.id_plafon = p.id 
                            join faktur_detail fd on fd.id_sales_order = so.id
                            join faktur f on f.id = fd.id_faktur  
                            left join sales_order_detail sod on sod.id_sales_order = so.id
                            left join proses_picking pp on pp.id_order_detail = sod.id
                            left join armada a on a.id = pp.id_armada
                            left join driver d on d.id = pp.id_driver
                            left join users u on u.id = d.id_user
                            where cb.id = :id_cabang
                            AND 
                            f.jenis_faktur = 'penjualan'
                            AND 
                            r.id = :id_rute
                            AND                             
                            so.status_order in (1,9)
                            {self.before_this_date_query_so}
                            group by r.id, r.nama_rute, r.kode, a.nama, u.nama, pp.delivering_date , d.id, a.id, c.id
                        """
            )
            .bindparams({
                "id_cabang": id_cabang,
                "id_rute": id_rute
            })
            .execute()
            .fetchall()
            .get()
        )

        merge_all_orders = [
            *order_one_principal,
            *order_multiple_principal
        ]

        # Menggabungkan dan mengelompokkan data berdasarkan id_rute, id_armada, id_driver, dan delivering_date
        grouped_data = []
        for entry in merge_all_orders:
            found = False
            for group in grouped_data:
                if group['id_rute'] == entry['id_rute']:
                    if group['id_customer'] != entry['id_customer']:
                        group['jumlah_toko'] += 1
                    group['jumlah_nota'] += entry['jumlah_nota']
                    group['jumlah_kubikal'] += entry['jumlah_kubikal']
                    found = True
                    break
            if not found:
                grouped_data.append({
                    **entry,
                })
        return grouped_data

    @handle_error_rollback
    def updateJadwalRute(self):
        id_sales_orders = self.req("id_sales_orders")
        id_driver = int(self.req("id_driver"))
        id_armada = int(self.req("id_armada"))
        tanggal_pengiriman = self.req("tanggal_pengiriman")

        first_sales_order = sales_order.query.filter(
            sales_order.id == id_sales_orders[0]
        ).join(
            Plafon, sales_order.id_plafon == Plafon.id
        ).join(
            customer, Plafon.id_customer == customer.id
        ).first()

        if not first_sales_order:
            raise nonServerErrorException("Data sales order tidak ditemukan", 404)

        id_rute = customer.query.filter(
            customer.id == Plafon.query.filter(
                Plafon.id == first_sales_order.id_plafon
            ).first().id_customer
        ).first().id_rute

        existing_jadwal = (
            self.query().setRawQuery("""
                SELECT COUNT(*) as count
                FROM proses_picking pp
                JOIN sales_order_detail sod ON sod.id = pp.id_order_detail
                JOIN sales_order so ON so.id = sod.id_sales_order
                JOIN plafon pl ON pl.id = so.id_plafon
                JOIN customer c ON c.id = pl.id_customer
                WHERE c.id_rute = :id_rute
                AND pp.id_armada = :id_armada
                AND pp.delivering_date = :delivering_date
                AND so.id != ALL(:id_sales_orders)
            """)
            .bindparams({
                "id_rute": id_rute,
                "id_armada": id_armada,
                "delivering_date": tanggal_pengiriman,
                "id_sales_orders": tuple(id_sales_orders)
            })
            .execute()
            .fetchone()
            .result
        )

        if existing_jadwal and existing_jadwal["count"] > 0:
            raise nonServerErrorException(
                "Jadwal dengan armada dan tanggal pengiriman di rute tersebut sudah terdaftar, mohon pilih armada atau tanggal pengiriman yang lain. <br> Anda juga bisa menghapus jadwal yang sudah ada, lalu jadwalkan ulang rute tersebut.",
                400
            )

        if not id_sales_orders or not id_driver or not id_armada:
            raise "Missing required fields"

        for id_sales_order in id_sales_orders:
            # Ambil update_sales_order di awal loop
            update_sales_order = sales_order.query.filter(
                sales_order.id == id_sales_order
            ).first()

            if not update_sales_order:
                raise nonServerErrorException(f"Sales order dengan ID {id_sales_order} tidak ditemukan", 404)

            order_details = sales_order_detail.query.filter(
                sales_order_detail.id_sales_order == id_sales_order
            ).all()

            for detail in order_details:
                product_conversions = self.query().setRawQuery(
                    """
                        SELECT level, faktor_konversi
                        FROM produk_uom
                        WHERE id_produk = :id_produk
                        ORDER BY level ASC
                    """
                ).bindparams({
                    "id_produk": detail.id_produk
                }).execute().fetchall().get()

                conversions = {1: 1}
                for conv in product_conversions:
                    level = conv["level"]
                    factor = conv["faktor_konversi"]
                    conversions[level] = factor

                pieces_contribution = (detail.pieces_booked or 0) * conversions.get(1, 1)
                box_contribution = (detail.box_booked or 0) * conversions.get(2, 1) if detail.box_booked else 0
                karton_contribution = (detail.karton_booked or 0) * conversions.get(3, 1) if detail.karton_booked else 0

                total_picked = int(pieces_contribution + box_contribution + karton_contribution)

                update_picking = prosesPicking.query.filter(
                    prosesPicking.id_order_detail == detail.id
                ).first()

                if update_picking:
                    update_picking.id_driver = id_driver
                    update_picking.id_armada = id_armada
                    update_picking.delivering_date = tanggal_pengiriman

                    # Hanya update jumlah_picked jika status_order sebelumnya bukan 9
                    if update_sales_order.status_order != 9:
                        update_picking.jumlah_picked = total_picked

                    self.flush()

            # Update status sales order berdasarkan status sebelumnya
            if update_sales_order.status_order == 1:
                update_sales_order.status_order = 2
            elif update_sales_order.status_order == 9:
                update_sales_order.status_order = 10
            self.flush()

        self.commit()

        return {"message": "Data updated successfully"}, 200

    @handle_error
    def getRuteListPicking(self):
        id_cabang = self.req('id')
        status_order = '(2)'
         
        return self.getRoutes(id_cabang, status_order)

    @handle_error
    def getListRuteRevisiFaktur(self):
        id_cabang = self.req('id_cabang')
        status_order = '(5)'

        return self.getRoutes(id_cabang, status_order)

    @handle_error
    def getAddpicking(self):
        id = self.req('id')
        rute_id = self.req('rute_id')
        id_armada = self.req("id_armada")
        id_driver = self.req("id_driver")
        delivering_date = self.req("delivering_date")

        # =========================
        # QUERY 1
        # =========================
        sql_one = text("""
            select
                    p.id as produk_id,
                    p.kode_sku,
                    p.nama as nama_produk,
                    string_agg(distinct c.id::text, ',') as id_customer,
                    string_agg(distinct c.nama, ',') as nama_customer,
                    coalesce(sum(pp.jumlah_picked), 0) as jumlah_picked,
                    MAX(CASE WHEN puom1.level = 1 THEN puom1.faktor_konversi ELSE 1 END) as konversi1,
                    MAX(CASE WHEN puom2.level = 2 THEN puom2.faktor_konversi ELSE 1 END) as konversi2,
                    MAX(CASE WHEN puom3.level = 3 THEN puom3.faktor_konversi ELSE 1 END) as konversi3,
                    COALESCE(
                    SUM(
                        (CASE WHEN puom1.level = 1 THEN puom1.faktor_konversi ELSE 1 END * sod.pieces_order) +
                        (CASE WHEN puom2.level = 2 THEN puom2.faktor_konversi ELSE 1 END * sod.box_order) +
                        (CASE WHEN puom3.level = 3 THEN puom3.faktor_konversi ELSE 1 END * sod.karton_order)
                    ), 0) as total_in_pieces,
                    string_agg(distinct pp.id_order_detail::text, ',') as id_order_detail,
                    string_agg(distinct pp.id::text, ',') as id_proses_picking,
                    string_agg(distinct f.id::text, ',') as id_faktur,
                    pp.delivering_date,
                    pp.id_driver,
                    pp.id_armada,
                    r.id as id_rute,
                    pr.nama as nama_principal,
                    coalesce(sum(sod.pieces_booked),0) as total_pieces,
                    coalesce(sum(sod.box_booked),0) as total_box,
                    coalesce(sum(sod.karton_booked),0) as total_karton,
                    coalesce(sum(pp.jumlah_picked), 0) as jumlah_picked,
                    stok.jumlah_good as stok,
                    MAX(CASE WHEN puom1.level = 1 THEN puom1.nama ELSE 'pieces' END) as pieces
                    from produk p
                    join proses_picking pp on p.id = pp.id_produk
                    join sales_order_detail sod on sod.id = pp.id_order_detail
                    join sales_order so on so.id = sod.id_sales_order and so.status_order in (2)
                    join plafon pl on pl.id = so.id_plafon
                    join customer c on c.id = pl.id_customer and c.id_cabang = :id
                    join principal pr on pr.id = p.id_principal
                    join rute r on r.id = c.id_rute and r.id = :rute_id
                    join faktur f on f.id_sales_order = so.id
                    left join produk_uom puom1 on puom1.id_produk = p.id and puom1.level = 1
                    left join produk_uom puom2 on puom2.id_produk = p.id and puom2.level = 2
                    left join produk_uom puom3 on puom3.id_produk = p.id and puom3.level = 3
                    join stok on stok.produk_id = p.id and stok.cabang_id = c.id_cabang
                    where pp.id_armada = :id_armada and pp.id_driver = :id_driver and pp.delivering_date = :delivering_date
                    group by
                    p.id,
                    p.kode_sku,
                    p.nama,
                    pp.delivering_date,
                    pp.id_driver,
                    pp.id_armada,
                    r.id,
                    pr.nama,
                    stok.jumlah_good
        """)

        result_one = DB.session.execute(sql_one, {
            "id": id,
            "rute_id": rute_id,
            "id_armada": id_armada,
            "id_driver": id_driver,
            "delivering_date": delivering_date
        }).mappings().all()

        add_picking_one_principal = [dict(row) for row in result_one]

        # =========================
        # QUERY 2
        # =========================
        sql_two = text("""
            select
                    p.id as produk_id,
                    p.kode_sku,
                    p.nama as nama_produk,
                    string_agg(distinct c.id::text, ',') as id_customer,
                    string_agg(distinct c.nama, ',') as nama_customer,
                    coalesce(sum(pp.jumlah_picked), 0) as jumlah_picked,
                    MAX(CASE WHEN puom1.level = 1 THEN puom1.faktor_konversi ELSE 1 END) as konversi1,
                    MAX(CASE WHEN puom2.level = 2 THEN puom2.faktor_konversi ELSE 1 END) as konversi2,
                    MAX(CASE WHEN puom3.level = 3 THEN puom3.faktor_konversi ELSE 1 END) as konversi3,
                    COALESCE(
                    SUM(
                        (CASE WHEN puom1.level = 1 THEN puom1.faktor_konversi ELSE 1 END * sod.pieces_order) +
                        (CASE WHEN puom2.level = 2 THEN puom2.faktor_konversi ELSE 1 END * sod.box_order) +
                        (CASE WHEN puom3.level = 3 THEN puom3.faktor_konversi ELSE 1 END * sod.karton_order)
                    ), 0) as total_in_pieces,
                    string_agg(distinct pp.id_order_detail::text, ',') as id_order_detail,
                    string_agg(distinct pp.id::text, ',') as id_proses_picking,
                    string_agg(distinct f.id::text, ',') as id_faktur,
                    pp.delivering_date,
                    pp.id_driver,
                    pp.id_armada,
                    r.id as id_rute,
                    pr.nama as nama_principal,
                    coalesce(sum(sod.pieces_booked),0) as total_pieces,
                    coalesce(sum(sod.box_booked),0) as total_box,
                    coalesce(sum(sod.karton_booked),0) as total_karton,
                    coalesce(sum(pp.jumlah_picked), 0) as jumlah_picked,
                    stok.jumlah_good as stok,
                    MAX(CASE WHEN puom1.level = 1 THEN puom1.nama ELSE 'pieces' END) as pieces
                    from produk p
                    join proses_picking pp on p.id = pp.id_produk
                    join sales_order_detail sod on sod.id = pp.id_order_detail
                    join sales_order so on so.id = sod.id_sales_order and so.status_order in (2)
                    join plafon pl on pl.id = so.id_plafon
                    join customer c on c.id = pl.id_customer and c.id_cabang = :id
                    join principal pr on pr.id = p.id_principal
                    join rute r on r.id = c.id_rute and r.id = :rute_id
					join faktur_detail fd on fd.id_sales_order =so.id 
                    join faktur f on f.id = fd.id_faktur
                    left join produk_uom puom1 on puom1.id_produk = p.id and puom1.level = 1
                    left join produk_uom puom2 on puom2.id_produk = p.id and puom2.level = 2
                    left join produk_uom puom3 on puom3.id_produk = p.id and puom3.level = 3
                    join stok on stok.produk_id = p.id and stok.cabang_id = c.id_cabang
                    where pp.id_armada = :id_armada and pp.id_driver = :id_driver and pp.delivering_date = :delivering_date
                    group by
                    p.id,
                    p.kode_sku,
                    p.nama,
                    pp.delivering_date,
                    pp.id_driver,
                    pp.id_armada,
                    r.id,
                    pr.nama,
                    stok.jumlah_good
        """)

        result_two = DB.session.execute(sql_two, {
            "id": id,
            "rute_id": rute_id,
            "id_armada": id_armada,
            "id_driver": id_driver,
            "delivering_date": delivering_date
        }).mappings().all()

        add_picking_multiple_principal = [dict(row) for row in result_two]

        # =========================
        # MERGE
        # =========================
        add_picking = [
            *add_picking_one_principal,
            *add_picking_multiple_principal
        ]

        merge_data_add_picking = []
        for entry in add_picking:
            found = False
            for group in merge_data_add_picking:
                if group['produk_id'] == entry['produk_id']:
                    if group['id_customer'] != entry['id_customer']:
                        group['nama_customer'] += f", {entry['nama_customer']}"
                        group['id_customer'] += f", {entry['id_customer']}"
                    group['jumlah_picked'] += entry['jumlah_picked']
                    group['total_in_pieces'] += entry['total_in_pieces']
                    group['total_pieces'] += entry['total_pieces']
                    group['total_box'] += entry['total_box']
                    group['total_karton'] += entry['total_karton']
                    group['id_order_detail'] += f", {entry['id_order_detail']}"
                    group['id_proses_picking'] += f", {entry['id_proses_picking']}"
                    group['id_faktur'] += f", {entry['id_faktur']}"

                    found = True
                    break
            if not found:
                merge_data_add_picking.append({
                    **entry,
                })

        return merge_data_add_picking

    @handle_error
    def getDaftarTokoPicking(self):
        id_cabang = self.req("id_cabang")
        id_rute = self.req("id_rute")
        id_produk = self.req("id_produk")
        id_order_detail = self.req("id_order_detail")

        # Buat string dari list id_order_detail untuk query
        id_order_detail_list_str = ','.join([str(int(id.strip())) for id in str(id_order_detail).split(',')])

        daftarToko_one_principal = (
            self.query().setRawQuery(
                f"""
                    select
                    customer.nama as nama_customer,
                    customer.id as id_customer,
                    produk.nama as nama_produk,
                    produk.id as produk_id,
                    proses_picking.id_armada,
                    proses_picking.id_driver,
                    proses_picking.delivering_date,
                    coalesce(sum(sales_order_detail.pieces_order),0) as pieces_order,
                    coalesce(sum(sales_order_detail.box_order),0) as box_order,
                    coalesce(sum(sales_order_detail.karton_order),0) as karton_order,
                    coalesce(proses_picking.jumlah_picked, 0) as jumlah_picked,
                    COALESCE(SUM( (CASE WHEN puom1.level = 1 THEN puom1.faktor_konversi ELSE 1 END * sales_order_detail.pieces_order) + 
                    (CASE WHEN puom2.level = 2 THEN puom2.faktor_konversi ELSE 1 END * sales_order_detail.box_order) + 
                    (CASE WHEN puom3.level = 3 THEN puom3.faktor_konversi ELSE 1 END * sales_order_detail.karton_order) ), 0) as total_in_pieces,
                    proses_picking.id_order_detail,
                    faktur.no_faktur,
                    sales_order.no_order
                    from customer
                    join rute on customer.id_rute = rute.id
                    join cabang on customer.id_cabang = cabang.id
                    join plafon on plafon.id_customer = customer.id
                    join sales_order on sales_order.id_plafon = plafon.id
                    left join faktur on faktur.id_sales_order = sales_order.id
                    join sales_order_detail on sales_order_detail.id_sales_order = sales_order.id
                    join proses_picking on proses_picking.id_order_detail = sales_order_detail.id
                    join produk on sales_order_detail.id_produk = produk.id
                    left join produk_uom puom1 on puom1.id_produk = produk.id and puom1.level = 1
                    left join produk_uom puom2 on puom2.id_produk = produk.id and puom2.level = 2
                    left join produk_uom puom3 on puom3.id_produk = produk.id and puom3.level = 3
                    where customer.id_cabang = :id_cabang
                    and rute.id = :id_rute
                    and produk.id = :id_produk
                    and (sales_order.status_order = 2 OR sales_order.status_order IS NULL)
                    and proses_picking.id_order_detail IN ({id_order_detail_list_str})
                    {self.before_this_date_query}
                    group by nama_customer, nama_produk, produk_id, jumlah_picked, customer.id, proses_picking.id_order_detail, proses_picking.id_armada, proses_picking.id_driver, proses_picking.delivering_date, faktur.no_faktur, sales_order.no_order
                """
            )
            .bindparams({
                "id_cabang": id_cabang,
                "id_rute": id_rute,
                "id_produk": id_produk
            })
            .execute()
            .fetchall()
            .get()
        )

        daftarToko_multiple_principal = (
            self.query().setRawQuery(
                f"""
                    select
                    customer.nama as nama_customer,
                    customer.id as id_customer,
                    produk.nama as nama_produk,
                    produk.id as produk_id,
                    proses_picking.id_armada,
                    proses_picking.id_driver,
                    proses_picking.delivering_date,
                    coalesce(sum(sales_order_detail.pieces_order),0) as pieces_order,
                    coalesce(sum(sales_order_detail.box_order),0) as box_order,
                    coalesce(sum(sales_order_detail.karton_order),0) as karton_order,
                    coalesce(proses_picking.jumlah_picked, 0) as jumlah_picked,
                    COALESCE(SUM( (CASE WHEN puom1.level = 1 THEN puom1.faktor_konversi ELSE 1 END * sales_order_detail.pieces_order) + 
                    (CASE WHEN puom2.level = 2 THEN puom2.faktor_konversi ELSE 1 END * sales_order_detail.box_order) + 
                    (CASE WHEN puom3.level = 3 THEN puom3.faktor_konversi ELSE 1 END * sales_order_detail.karton_order) ), 0) as total_in_pieces,
                    proses_picking.id_order_detail,
                    faktur.no_faktur,
                    sales_order.no_order
                    from customer
                    join rute on customer.id_rute = rute.id
                    join cabang on customer.id_cabang = cabang.id
                    join plafon on plafon.id_customer = customer.id
                    join sales_order on sales_order.id_plafon = plafon.id
                    join faktur_detail on sales_order.id = faktur_detail.id_sales_order
                    left join faktur on faktur.id = faktur_detail.id_faktur
                    join sales_order_detail on sales_order_detail.id_sales_order = sales_order.id
                    join proses_picking on proses_picking.id_order_detail = sales_order_detail.id
                    join produk on sales_order_detail.id_produk = produk.id
                    left join produk_uom puom1 on puom1.id_produk = produk.id and puom1.level = 1
                    left join produk_uom puom2 on puom2.id_produk = produk.id and puom2.level = 2
                    left join produk_uom puom3 on puom3.id_produk = produk.id and puom3.level = 3
                    where customer.id_cabang = :id_cabang
                    and rute.id = :id_rute
                    and produk.id = :id_produk
                    and (sales_order.status_order = 2 OR sales_order.status_order IS NULL)
                    and proses_picking.id_order_detail IN ({id_order_detail_list_str})
                    {self.before_this_date_query}
                    group by nama_customer, nama_produk, produk_id, jumlah_picked, customer.id, proses_picking.id_order_detail, proses_picking.id_armada, proses_picking.id_driver, proses_picking.delivering_date, faktur.no_faktur, sales_order.no_order
                """
            )
            .bindparams({
                "id_cabang": id_cabang,
                "id_rute": id_rute,
                "id_produk": id_produk
            })
            .execute()
            .fetchall()
            .get()
        )

        daftarToko = [
            *daftarToko_one_principal,
            *daftarToko_multiple_principal
        ]
        return daftarToko

    @handle_error_rollback
    def submitProdukPicking(self):
        list_picking = self.req("picking")

        if not list_picking or not isinstance(list_picking, list):
            raise nonServerErrorException("Data picking tidak valid atau kosong", 400)

        for pick in list_picking:
            picking_value = pick.get('picking')

            if picking_value is None or not isinstance(picking_value, int) or picking_value < 0:
                raise nonServerErrorException("Nilai picking tidak valid", 400)

            id_order_detail = pick.get("id_order_detail")

            if id_order_detail is None:
                raise nonServerErrorException("Invalid or missing 'id_order_detail'", 400)

            if not isinstance(id_order_detail, int):
                raise nonServerErrorException(f"Nilai id_order_detail tidak valid: {id_order_detail}", 400)

            proses_picking_picked = prosesPicking.query.filter(prosesPicking.id_order_detail == id_order_detail).first()

            if not proses_picking_picked:
                raise nonServerErrorException(
                    f"Data proses picking dengan ID detail order {id_order_detail} tidak ditemukan", 404)

            proses_picking_picked.jumlah_picked = picking_value

            self.flush()

        self.commit()

        return {'status': 'success'}, 200

    @handle_error_rollback
    def __submitProdukPicking(self):
        list_picking = self.req("picking") 
        id_produk = int(list_picking[0]["idProduk"])
        id_cabang = self.req('id_cabang')
    
        # loop produk yamh telah di pick dari frontend
        for picking in list_picking:
            pick = picking["picking"]
    
            # melakukan loop untuk id detail order
            for id_detail in picking["id_detail_sales"]:
                # mendapatkan proses picking yang sesuai dengan id order detail
                proses_picking_picked = prosesPicking.query.filter(prosesPicking.id_order_detail == id_detail).first()
                # mendapatkan jumlah picked dari hasil mendapatkan proses picking di atas
                proses_picking_picked.jumlah_picked = pick

            self.flush()

            # melakukan loop terhadap array id_faktur
            for id_faktur in picking["id_faktur"]:
                # melakuakan check terhadap jumlah picking yang mana disimpan di variabel pick
                # jika tidak null maka akan melakuakn perhitunga seperti dibawah
                if pick != None and pick != "" :
                    # mendapatkan hasil joinan proses picking, sales_order_detail, sales_order, dan faktur
                    # berdasarkan variabel id_faktur
                    get_picking_null = (
                        self.db.session
                        .query(
                            prosesPicking
                        )
                        .join(
                            sales_order_detail,
                            sales_order_detail.id == prosesPicking.id_order_detail
                        )
                        .join(
                            sales_order,
                            sales_order_detail.id_sales_order == sales_order.id
                        )
                        .join(
                            Faktur,
                            Faktur.id_sales_order == sales_order.id
                        )
                        .filter(Faktur.id == id_faktur)
                        .all()
                    )

                    get_picking_null_array, check_all_null = [], False

                    # melakukan loop terhadap variabel get_picking_null, dan mendapatkan jumlah_picked
                    for picking in get_picking_null:
                        jumlah_pick = picking.jumlah_picked

                        # jika jumlah_picked non atau 0 maka melakukan push True ke get_picking_null_array
                        if jumlah_pick is None or jumlah_pick == 0:
                            get_picking_null_array.append(True)
                        else:
                            get_picking_null_array.append(False)

                    # jika ada satu nilai di get_picking_null_array yang true maka check_all_null akan berisi True
                    check_all_null = any(get_picking_null_array)

                    faktur = Faktur.query.filter(Faktur.id == id_faktur).first()

                    # jika check_all_null False maka melakukan update status_faktur menjadi 3 (picked)
                    if not check_all_null:
                        faktur.status_faktur = 3
                    else:
                        faktur.status_faktur = 1

                    self.flush()

        stok_picked = stok.query.filter(stok.produk_id == id_produk, stok.cabang_id == id_cabang).first()
        total_produk_picked = (
            self.db.session.query(Plafon.id_customer, prosesPicking.jumlah_picked)
            .join(sales_order, sales_order.id_plafon == Plafon.id)
            .join(sales_order_detail, sales_order_detail.id_sales_order == sales_order.id)
            .join(prosesPicking, prosesPicking.id_order_detail == sales_order_detail.id)
            .filter(prosesPicking.id_produk == id_produk)
            .group_by(prosesPicking.jumlah_picked, Plafon.id_customer)
            .distinct()
            .all()
        )

        # mendapatkan hasil kalkulasi dari semua jumlah_picked yang telah didapatkan dari variabel total_produk_picked diatas
        total_picked = sum([result[1] for result in total_produk_picked if isinstance(result[1], int)])

        # mendapatkan jumlah_picked dari stok yang telah didapatkan berdasarkan id_produk saat ini
        stok_jumlah_picked = stok_picked.jumlah_picked if isinstance(stok_picked.jumlah_picked, int) else 0

        # mendapatkan hasil yang akan digunakan untuk melakukan pengurangan terhadap jumlah_ready di tabel stok
        subtract_value = total_picked - stok_jumlah_picked

        update_stok = stok.query.filter(stok.produk_id == id_produk, stok.cabang_id == id_cabang).first()
        stok_jumlah_ready = update_stok.jumlah_ready

        # jika kolom jumlah_ready tidak null maka akan melakuak update jumlah_ready dan jumlah_picked
        if isinstance(stok_jumlah_ready, int):
            update_stok.jumlah_ready = stok_jumlah_ready - subtract_value
            update_stok.jumlah_picked = total_picked

        self.commit()
        return {"status": "success"}, 200

    @handle_error
    def getShippingRuteList(self, id_cabang, isRealisasi=False):

        if isRealisasi:
            status_order = "(4,11)"
        else:
            status_order = "(3,10)"

        return self.getRoutes(id_cabang, status_order)

    @handle_error
    def getListFakturShipping(self, isRealisasi = 0):
        id_cabang = self.req("id_cabang")
        id_rute = self.req('id_rute')
        id_armada = self.req('id_armada')
        id_driver = self.req('id_driver')
        delivering_date = self.req('delivering_date')

        status_map = {
            0: '(3,10)',  # get shipping
            1: '(4,11)',  # get realisasi
            2: '(5)'  # get revisi faktur
        }
        status = status_map.get(isRealisasi, '(3)')

        list_faktur_shipping_info = (
            self.query().setRawQuery(
                f"""
                    select
                    armada.id,
                    rute.kode as kode_rute,
                    armada.no_pelat,
                    users.nama,
                    coalesce(sum(DISTINCT faktur.total_penjualan)::numeric,0) as total_penjualan,
                    proses_picking.id_armada as id_armada,
                    proses_picking.id_driver as id_driver,
                    proses_picking.delivering_date,
                    rute.id as id_rute
                    from customer
                    join rute on customer.id_rute = rute.id 
                    join cabang on customer.id_cabang = cabang.id
                    join plafon on plafon.id_customer = customer.id
                    join sales_order on sales_order.id_plafon = plafon.id
                    join faktur on faktur.id_sales_order = sales_order.id
                    join sales_order_detail on sales_order_detail.id_sales_order = sales_order.id
                    join proses_picking on proses_picking.id_order_detail = sales_order_detail.id
                    join armada on proses_picking.id_armada = armada.id
                    join driver on driver.id = proses_picking.id_driver
                    join users on users.id = driver.id_user
                    where customer.id_cabang = :id_cabang
                    and rute.id = :id_rute
                    and faktur.jenis_faktur = 'penjualan'
                    and sales_order.status_order in {status}
                    and proses_picking.id_armada = :id_armada
                    and proses_picking.id_driver = :id_driver
                    and proses_picking.delivering_date = :delivering_date
                    
                    {self.before_this_date_query}
                    group by armada.id, rute.kode, armada.no_pelat, users.nama, proses_picking.id_armada, proses_picking.id_driver, proses_picking.delivering_date, rute.id
                """
            )
            .bindparams({
                "id_cabang": id_cabang,
                "id_rute": id_rute,
                "id_armada": id_armada,
                "id_driver": id_driver,
                "delivering_date": delivering_date
            })
            .execute()
            .fetchone()
            .result
        )
    
        list_faktur_shipping_one_principal = (
            self.query().setRawQuery(
                f"""
                    select
					customer.kode as kode_customer,
                    sales_order.id as id_sales_order,
					wilayah4.nama as area,
					sales_order.no_order,
                    faktur.no_faktur,
                    sales_order.tanggal_order as tanggal_order,
                    rute.nama_rute,
                    rute.id as id_rute,
                    rute.kode as kode_rute,
                    customer.nama as nama_customer,
                    coalesce(sum(sales_order_detail.estimasi_kubikasi)::NUMERIC,0) as kubikal,
                    plafon.tempo_label as terms,
                    faktur.total_penjualan,
                    sales_order.status_order,
                    string_agg(distinct sales_order_detail.id::text, ',') as id_sales_order_detail
                    from customer
                    join rute on customer.id_rute = rute.id
                    join cabang on customer.id_cabang = cabang.id
                    join plafon on plafon.id_customer = customer.id
                    join sales_order on sales_order.id_plafon = plafon.id
                    left join faktur on faktur.id_sales_order = sales_order.id
					left join wilayah4 on wilayah4.id = customer.id_wilayah4
                    join sales_order_detail on sales_order.id = sales_order_detail.id_sales_order
                    join proses_picking on sales_order_detail.id = proses_picking.id_order_detail
                    where customer.id_cabang = :id_cabang
                    and rute.id = :id_rute
                    and faktur.jenis_faktur = 'penjualan'
                    and sales_order.status_order in {status}
                    and proses_picking.id_armada = :id_armada
                    and proses_picking.id_driver = :id_driver
                    and proses_picking.delivering_date = :delivering_date
                    {self.before_this_date_query}
                    group by customer.kode, sales_order.id, wilayah4.nama, sales_order.no_order, faktur.no_faktur, sales_order.tanggal_order, rute.nama_rute, rute.id, rute.kode, customer.nama, plafon.tempo_label, faktur.total_penjualan, sales_order.status_order

                """
            )
            .bindparams({
                "id_cabang": id_cabang,
                "id_rute": id_rute,
                "id_armada": id_armada,
                "id_driver": id_driver,
                "delivering_date": delivering_date
            })
            .execute()
            .fetchall()
            .get()
        )

        list_faktur_shipping_multiple_principal = (
            self.query().setRawQuery(
                f"""
                 select
					customer.kode as kode_customer,
                    string_agg(sales_order.id::text, ',') as id_sales_order,
					wilayah4.nama as area,
					sales_order.no_order,
                    faktur.no_faktur,
                    sales_order.tanggal_order as tanggal_order,
                    rute.nama_rute,
                    rute.id as id_rute,
                    order_batch.id as id_order_batch,
                    rute.kode as kode_rute,
                    customer.nama as nama_customer,
                    coalesce(sum(sales_order_detail.estimasi_kubikasi)::NUMERIC,0) as kubikal,
                    plafon.tempo_label as terms,
                    faktur.total_penjualan,
                    sales_order.status_order,
                    string_agg(distinct sales_order_detail.id::text, ',') as id_sales_order_detail
                    from customer
                    join rute on customer.id_rute = rute.id
                    join cabang on customer.id_cabang = cabang.id
                    join plafon on plafon.id_customer = customer.id                    
                    join sales_order on sales_order.id_plafon = plafon.id
                    join faktur_detail on faktur_detail.id_sales_order = sales_order.id
                    join order_batch on order_batch.id = sales_order.id_order_batch
                    left join faktur on faktur.id = faktur_detail.id_faktur
					left join wilayah4 on wilayah4.id = customer.id_wilayah4
                    join sales_order_detail on sales_order.id = sales_order_detail.id_sales_order
                    join proses_picking on sales_order_detail.id = proses_picking.id_order_detail
                    where customer.id_cabang = :id_cabang
                    and rute.id = :id_rute
                    and faktur.jenis_faktur = 'penjualan'
                    and sales_order.status_order in {status}
                    and proses_picking.id_armada = :id_armada
                    and proses_picking.id_driver = :id_driver
                    and proses_picking.delivering_date = :delivering_date
                    {self.before_this_date_query}
                    group by customer.kode, wilayah4.nama, sales_order.no_order, faktur.no_faktur, sales_order.tanggal_order, rute.nama_rute, rute.id, rute.kode, customer.nama, plafon.tempo_label, faktur.total_penjualan, sales_order.status_order, order_batch.id
""")
            .bindparams({
                "id_cabang": id_cabang,
                "id_rute": id_rute,
                "id_armada": id_armada,
                "id_driver": id_driver,
                "delivering_date": delivering_date
            })
            .execute()
            .fetchall()
            .get()
        )

        # print(type(list_faktur_shipping_one_principal))
        # print(list_faktur_shipping_one_principal)

        list_faktur_shipping = [
            *list_faktur_shipping_one_principal.get("result", []),
            *list_faktur_shipping_multiple_principal.get("result", [])
        ]
        
        return {
            "list_faktur_shipping_info": list_faktur_shipping_info,
            "list_faktur_shipping": list_faktur_shipping
        }

    @handle_error
    def getDetailFakturShipping(self, id_sales_order, jenisFaktur=None ):
        id_order_batch = self.req('id_order_batch')
        if id_order_batch:
            id_sales_orders = self.req("id_sales_orders")
            if not id_sales_orders:
                raise nonServerErrorException("ID sales order tidak valid atau kosong", 400)
            id_sales_orders = [int(id) for id in id_sales_orders.split(",")]
            return self.__get_detail_faktur_by_id_sales_order_batch(id_order_batch=id_order_batch, id_sales_order=id_sales_orders, jenisFaktur=jenisFaktur)
        else:
            return self.__get_detail_faktur_by_id_sales_order(id_sales_order, jenisFaktur)

    def __get_detail_faktur_by_id_sales_order(self, id_sales_order, jenisFaktur=None):
        list_detail_order = (
            self.query().setRawQuery(
                f"""
                            -- CTE to get voucher information
                            WITH v_info AS (
                                SELECT 
                                    dv.id_sales_order_detail,
                                    -- Voucher 1 (Reguler)
                                    MAX(CASE WHEN dv.tipe_voucher = 1 THEN dv.id ELSE NULL END) AS v1r_id_dv,
                                    MAX(CASE WHEN dv.tipe_voucher = 1 THEN v1.nama_voucher ELSE NULL END) AS v1r_nama,
                                    MAX(CASE WHEN dv.tipe_voucher = 1 THEN dv.jumlah_diskon ELSE NULL END) AS v1r_diskon,
                                    MAX(CASE WHEN dv.tipe_voucher = 1 THEN v1.kode_voucher ELSE NULL END) AS v1r_kode,
                                    MAX(CASE WHEN dv.tipe_voucher = 1 THEN v1.persentase_diskon_1 ELSE NULL END) AS v1r_persen,
                                    MAX(CASE WHEN dv.tipe_voucher = 1 THEN v1.minimal_subtotal_pembelian ELSE NULL END) AS v1r_minimal_subtotal_pembelian,

                                    -- Voucher 2 Reguler (tipe_voucher = 2 AND is_reguler = 1)
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 1 THEN dv.id ELSE NULL END) AS v2r_id_dv,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 1 THEN v2.nama_voucher ELSE NULL END) AS v2r_nama,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 1 THEN dv.jumlah_diskon ELSE NULL END) AS v2r_diskon,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 1 THEN v2.kode_voucher ELSE NULL END) AS v2r_kode,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 1 THEN v2.persentase_diskon_2 ELSE NULL END) AS v2r_persen,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 1 THEN v2.minimal_subtotal_pembelian ELSE NULL END) AS v2r_minimal_subtotal_pembelian,

                                    -- Voucher 2 Produk (tipe_voucher = 2 AND is_reguler = 0)
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN dv.id ELSE NULL END) AS v2p_id_dv,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.nama_voucher ELSE NULL END) AS v2p_nama,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN dv.jumlah_diskon ELSE NULL END) AS v2p_diskon,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.kode_voucher ELSE NULL END) AS v2p_kode,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.kategori_voucher ELSE NULL END) AS v2p_kategori_voucher,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.persentase_diskon_2 ELSE NULL END) AS v2p_persen,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.nominal_diskon ELSE NULL END) AS v2p_nominal_diskon,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.minimal_subtotal_pembelian ELSE NULL END) AS v2p_minimal_subtotal_pembelian,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.minimal_jumlah_produk ELSE NULL END) AS v2p_minimal_jumlah_produk,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.level_uom ELSE NULL END) AS v2p_level_uom,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.budget_diskon ELSE NULL END) AS v2p_budget_diskon,

                                    -- Voucher 3 Reguler (tipe_voucher = 3 AND is_reguler = 1)
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 1 THEN dv.id ELSE NULL END) AS v3r_id_dv,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 1 THEN v3.nama_voucher ELSE NULL END) AS v3r_nama,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 1 THEN dv.jumlah_diskon ELSE NULL END) AS v3r_diskon,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 1 THEN v3.kode_voucher ELSE NULL END) AS v3r_kode,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 1 THEN v3.persentase_diskon_3 ELSE NULL END) AS v3r_persen,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 1 THEN v3.minimal_subtotal_pembelian ELSE NULL END) AS v3r_minimal_subtotal_pembelian,

                                    -- Voucher 3 Produk (tipe_voucher = 3 AND is_reguler = 0)
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 0 THEN dv.id ELSE NULL END) AS v3p_id_dv,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 0 THEN v3.nama_voucher ELSE NULL END) AS v3p_nama,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 0 THEN dv.jumlah_diskon ELSE NULL END) AS v3p_diskon,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 0 THEN v3.kode_voucher ELSE NULL END) AS v3p_kode,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 0 THEN v3.kategori_voucher ELSE NULL END) AS v3p_kategori_voucher,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 0 THEN v3.persentase_diskon_3 ELSE NULL END) AS v3p_persen,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 0 THEN v3.nominal_diskon ELSE NULL END) AS v3p_nominal_diskon,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 0 THEN v3.budget_diskon ELSE NULL END) AS v3p_budget_diskon
                                FROM draft_voucher dv
                                LEFT JOIN voucher_1 v1 ON dv.id_voucher = v1.id AND dv.tipe_voucher = 1
                                LEFT JOIN voucher_2 v2 ON dv.id_voucher = v2.id AND dv.tipe_voucher = 2
                                LEFT JOIN voucher_3 v3 ON dv.id_voucher = v3.id AND dv.tipe_voucher = 3
                                WHERE dv.id_sales_order = :id_sales_order and dv.status_promo in (0,1)
                                GROUP BY dv.id_sales_order_detail
                            )

                            SELECT
                                sod.id as id_order_detail,
                                sod.id_sales_order,
                                p.nama as nama_produk,
                                p.id as id_produk,
                                p.kode_sku,
                                p.ppn,
                                sod.pieces_order,
                                sod.box_order,
                                sod.karton_order,
                                sod.pieces_retur,
                                sod.box_retur,
                                sod.karton_retur,
                                sod.keterangan_retur,
                                sod.pieces_picked,
                                sod.box_picked,
                                sod.karton_picked,
                                sod.pieces_shipped,
                                sod.box_shipped,
                                sod.karton_shipped,
                                sod.pieces_delivered,
                                sod.box_delivered,
                                sod.karton_delivered,
                                phj.harga as harga_jual,
                                sod.subtotalorder,
                                puom1.nama as puom1_nama,
                                puom1.kode as puom1_kode,
                                puom2.nama as puom2_nama,
                                puom3.nama as puom3_nama,
                                puom1.faktor_konversi as konversi_level1,
                                puom2.faktor_konversi as konversi_level2,
                                puom3.faktor_konversi as konversi_level3,
                                puom1.packing_lebar as puom1_packing_lebar,
                                puom1.packing_panjang as puom1_packing_panjang,
                                puom1.packing_tinggi as puom1_packing_tinggi,
                                puom2.packing_lebar as puom2_packing_lebar,
                                puom2.packing_panjang as puom2_packing_panjang,
                                puom2.packing_tinggi as puom2_packing_tinggi,
                                puom3.packing_lebar as puom3_packing_lebar,
                                puom3.packing_panjang as puom3_packing_panjang,
                                puom3.packing_tinggi as puom3_packing_tinggi,
                                -- Voucher 1 (Reguler)
                                v.v1r_id_dv,
                                v.v1r_nama,
                                v.v1r_diskon,
                                v.v1r_kode,
                                v.v1r_persen,
                                v.v1r_minimal_subtotal_pembelian,
                                -- Voucher 2 Reguler
                                v.v2r_id_dv,
                                v.v2r_nama,
                                v.v2r_diskon,
                                v.v2r_kode,
                                v.v2r_persen,
                                v.v2r_minimal_subtotal_pembelian,
                                -- Voucher 2 Produk
                                v.v2p_id_dv,
                                v.v2p_nama,
                                v.v2p_diskon,
                                v.v2p_kode,
                                v.v2p_kategori_voucher,
                                v.v2p_persen,
                                v.v2p_nominal_diskon,
                                v.v2p_minimal_subtotal_pembelian,
                                v.v2p_minimal_jumlah_produk,
                                v.v2p_level_uom,
                                v.v2p_budget_diskon,
                                -- Voucher 3 Reguler
                                v.v3r_id_dv,
                                v.v3r_nama,
                                v.v3r_diskon,
                                v.v3r_kode,
                                v.v3r_persen,
                                v.v3r_minimal_subtotal_pembelian,
                                -- Voucher 3 Produk
                                v.v3p_id_dv,
                                v.v3p_nama,
                                v.v3p_diskon,
                                v.v3p_kode,
                                v.v3p_kategori_voucher,
                                v.v3p_persen,
                                v.v3p_nominal_diskon,
                                v.v3p_budget_diskon
                            FROM sales_order so
                            LEFT JOIN faktur f ON f.id_sales_order = so.id
                            LEFT JOIN sales_order_detail sod ON sod.id_sales_order = so.id
                            LEFT JOIN plafon pl ON so.id_plafon = pl.id
                            LEFT JOIN produk p ON sod.id_produk = p.id
                            LEFT JOIN produk_harga_jual phj ON p.id = phj.id_produk AND phj.id_tipe_harga = pl.id_tipe_harga
                            LEFT JOIN produk_uom puom1 on p.id = puom1.id_produk and puom1.level = 1
                            LEFT JOIN produk_uom puom2 on p.id = puom2.id_produk and puom2.level = 2
                            LEFT JOIN produk_uom puom3 on p.id = puom3.id_produk and puom3.level = 3
                            LEFT JOIN v_info v ON v.id_sales_order_detail = sod.id
                            WHERE so.id = :id_sales_order
                            AND f.jenis_faktur = :jenis_faktur
                            {self.before_this_date_query_so}
                        """
            )
            .bindparams({
                "id_sales_order": id_sales_order,
                "jenis_faktur": jenisFaktur or 'penjualan'
            })
            .execute()
            .fetchall()
            .get()
        )

        detail_faktur = (
            self.query().setRawQuery(
                f"""
                            select
                            distinct customer.nama as nama_customer,
                            customer.alamat as alamat_customer,
                            customer.telepon as telepon_customer,
                            customer.kode as kode_customer,
                            sales_order.*,
                            faktur.*,
                            rute.kode as kode_rute,
                            principal.kode as kode_principal,
                            principal.nama as nama_principal,
                            faktur.id as id_faktur,
                            faktur.no_faktur as nomor_faktur,
                            users.nama as nama_driver,
                            plafon.tempo_label
                            from customer
                            left join rute
                            on rute.id = customer.id_rute
                            join plafon
                            on plafon.id_customer = customer.id
                            join principal
                            on principal.id = plafon.id_principal
                            join sales_order
                            on sales_order.id_plafon = plafon.id
                            join faktur
                            on sales_order.id = faktur.id_sales_order
                            join sales_order_detail
                            on sales_order_detail.id_sales_order = sales_order.id
                            join proses_picking
                            on proses_picking.id_order_detail = sales_order_detail.id
                            left join driver
                            on driver.id = proses_picking.id_driver
                            left join users
                            on users.id = driver.id_user
                            where faktur.id_sales_order = :id_sales_order 
                            and faktur.jenis_faktur = :jenis_faktur
                            {self.before_this_date_query}
                        """
            )
            .bindparams({
                "id_sales_order": id_sales_order,
                "jenis_faktur": jenisFaktur or 'penjualan'
            })
            .execute()
            .fetchone()
            .result
        )

        if len(list(detail_faktur)):
            detail_faktur["status_order_str"] = status_order(detail_faktur["status_order"])

        detail_faktur_obj = {
            "list_detail_order": list_detail_order,
            "detail_faktur": detail_faktur
        }

        return detail_faktur_obj

    def __get_detail_faktur_by_id_sales_order_batch(self, id_order_batch,id_sales_order, jenisFaktur=None):
        list_detail_order = (
            self.query().setRawQuery(
                """
                WITH v_info AS (
                                SELECT 
                                    dv.id_sales_order_detail,
                                    -- Voucher 1 (Reguler)
                                    MAX(CASE WHEN dv.tipe_voucher = 1 THEN dv.id ELSE NULL END) AS v1r_id_dv,
                                    MAX(CASE WHEN dv.tipe_voucher = 1 THEN v1.nama_voucher ELSE NULL END) AS v1r_nama,
                                    MAX(CASE WHEN dv.tipe_voucher = 1 THEN dv.jumlah_diskon ELSE NULL END) AS v1r_diskon,
                                    MAX(CASE WHEN dv.tipe_voucher = 1 THEN v1.kode_voucher ELSE NULL END) AS v1r_kode,
                                    MAX(CASE WHEN dv.tipe_voucher = 1 THEN v1.persentase_diskon_1 ELSE NULL END) AS v1r_persen,
                                    MAX(CASE WHEN dv.tipe_voucher = 1 THEN v1.minimal_subtotal_pembelian ELSE NULL END) AS v1r_minimal_subtotal_pembelian,

                                    -- Voucher 2 Reguler (tipe_voucher = 2 AND is_reguler = 1)
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 1 THEN dv.id ELSE NULL END) AS v2r_id_dv,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 1 THEN v2.nama_voucher ELSE NULL END) AS v2r_nama,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 1 THEN dv.jumlah_diskon ELSE NULL END) AS v2r_diskon,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 1 THEN v2.kode_voucher ELSE NULL END) AS v2r_kode,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 1 THEN v2.persentase_diskon_2 ELSE NULL END) AS v2r_persen,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 1 THEN v2.minimal_subtotal_pembelian ELSE NULL END) AS v2r_minimal_subtotal_pembelian,

                                    -- Voucher 2 Produk (tipe_voucher = 2 AND is_reguler = 0)
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN dv.id ELSE NULL END) AS v2p_id_dv,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.nama_voucher ELSE NULL END) AS v2p_nama,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN dv.jumlah_diskon ELSE NULL END) AS v2p_diskon,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.kode_voucher ELSE NULL END) AS v2p_kode,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.kategori_voucher ELSE NULL END) AS v2p_kategori_voucher,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.persentase_diskon_2 ELSE NULL END) AS v2p_persen,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.nominal_diskon ELSE NULL END) AS v2p_nominal_diskon,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.minimal_subtotal_pembelian ELSE NULL END) AS v2p_minimal_subtotal_pembelian,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.minimal_jumlah_produk ELSE NULL END) AS v2p_minimal_jumlah_produk,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.level_uom ELSE NULL END) AS v2p_level_uom,
                                    MAX(CASE WHEN dv.tipe_voucher = 2 AND v2.is_reguler = 0 THEN v2.budget_diskon ELSE NULL END) AS v2p_budget_diskon,

                                    -- Voucher 3 Reguler (tipe_voucher = 3 AND is_reguler = 1)
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 1 THEN dv.id ELSE NULL END) AS v3r_id_dv,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 1 THEN v3.nama_voucher ELSE NULL END) AS v3r_nama,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 1 THEN dv.jumlah_diskon ELSE NULL END) AS v3r_diskon,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 1 THEN v3.kode_voucher ELSE NULL END) AS v3r_kode,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 1 THEN v3.persentase_diskon_3 ELSE NULL END) AS v3r_persen,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 1 THEN v3.minimal_subtotal_pembelian ELSE NULL END) AS v3r_minimal_subtotal_pembelian,

                                    -- Voucher 3 Produk (tipe_voucher = 3 AND is_reguler = 0)
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 0 THEN dv.id ELSE NULL END) AS v3p_id_dv,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 0 THEN v3.nama_voucher ELSE NULL END) AS v3p_nama,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 0 THEN dv.jumlah_diskon ELSE NULL END) AS v3p_diskon,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 0 THEN v3.kode_voucher ELSE NULL END) AS v3p_kode,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 0 THEN v3.kategori_voucher ELSE NULL END) AS v3p_kategori_voucher,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 0 THEN v3.persentase_diskon_3 ELSE NULL END) AS v3p_persen,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 0 THEN v3.nominal_diskon ELSE NULL END) AS v3p_nominal_diskon,
                                    MAX(CASE WHEN dv.tipe_voucher = 3 AND v3.is_reguler = 0 THEN v3.budget_diskon ELSE NULL END) AS v3p_budget_diskon
                                FROM draft_voucher dv
                                LEFT JOIN voucher_1 v1 ON dv.id_voucher = v1.id AND dv.tipe_voucher = 1
                                LEFT JOIN voucher_2 v2 ON dv.id_voucher = v2.id AND dv.tipe_voucher = 2
                                LEFT JOIN voucher_3 v3 ON dv.id_voucher = v3.id AND dv.tipe_voucher = 3
                                WHERE dv.id_sales_order IN :id_sales_order and dv.status_promo in (0,1)
                                GROUP BY dv.id_sales_order_detail
                            )

                            SELECT
                                sod.id as id_order_detail,
                                sod.id_sales_order,
                                p.nama as nama_produk,
                                p.id as id_produk,
                                p.kode_sku,
                                p.ppn,
                                f.id as id_faktur,
                                sod.pieces_order,
                                sod.box_order,
                                sod.karton_order,
                                sod.pieces_retur,
                                sod.box_retur,
                                sod.karton_retur,
                                sod.keterangan_retur,
                                sod.pieces_picked,
                                sod.box_picked,
                                sod.karton_picked,
                                sod.pieces_shipped,
                                sod.box_shipped,
                                sod.karton_shipped,
                                sod.pieces_delivered,
                                sod.box_delivered,
                                sod.karton_delivered,
                                phj.harga as harga_jual,
                                sod.subtotalorder,
                                puom1.nama as puom1_nama,
                                puom1.kode as puom1_kode,
                                puom2.nama as puom2_nama,
                                puom3.nama as puom3_nama,
                                puom1.faktor_konversi as konversi_level1,
                                puom2.faktor_konversi as konversi_level2,
                                puom3.faktor_konversi as konversi_level3,
                                puom1.packing_lebar as puom1_packing_lebar,
                                puom1.packing_panjang as puom1_packing_panjang,
                                puom1.packing_tinggi as puom1_packing_tinggi,
                                puom2.packing_lebar as puom2_packing_lebar,
                                puom2.packing_panjang as puom2_packing_panjang,
                                puom2.packing_tinggi as puom2_packing_tinggi,
                                puom3.packing_lebar as puom3_packing_lebar,
                                puom3.packing_panjang as puom3_packing_panjang,
                                puom3.packing_tinggi as puom3_packing_tinggi,
                                -- Voucher 1 (Reguler)
                                v.v1r_id_dv,
                                v.v1r_nama,
                                v.v1r_diskon,
                                v.v1r_kode,
                                v.v1r_persen,
                                v.v1r_minimal_subtotal_pembelian,
                                -- Voucher 2 Reguler
                                v.v2r_id_dv,
                                v.v2r_nama,
                                v.v2r_diskon,
                                v.v2r_kode,
                                v.v2r_persen,
                                v.v2r_minimal_subtotal_pembelian,
                                -- Voucher 2 Produk
                                v.v2p_id_dv,
                                v.v2p_nama,
                                v.v2p_diskon,
                                v.v2p_kode,
                                v.v2p_kategori_voucher,
                                v.v2p_persen,
                                v.v2p_nominal_diskon,
                                v.v2p_minimal_subtotal_pembelian,
                                v.v2p_minimal_jumlah_produk,
                                v.v2p_level_uom,
                                v.v2p_budget_diskon,
                                -- Voucher 3 Reguler
                                v.v3r_id_dv,
                                v.v3r_nama,
                                v.v3r_diskon,
                                v.v3r_kode,
                                v.v3r_persen,
                                v.v3r_minimal_subtotal_pembelian,
                                -- Voucher 3 Produk
                                v.v3p_id_dv,
                                v.v3p_nama,
                                v.v3p_diskon,
                                v.v3p_kode,
                                v.v3p_kategori_voucher,
                                v.v3p_persen,
                                v.v3p_nominal_diskon,
                                v.v3p_budget_diskon
                            FROM order_batch ob
							JOIN sales_order so ON so.id_order_batch = ob.id
							JOIN faktur_detail fd ON fd.id_sales_order = so.id
                            LEFT JOIN faktur f ON fd.id_faktur = f.id
                            LEFT JOIN sales_order_detail sod ON sod.id_sales_order = so.id
                            LEFT JOIN plafon pl ON so.id_plafon = pl.id
                            LEFT JOIN produk p ON sod.id_produk = p.id
                            LEFT JOIN produk_harga_jual phj ON p.id = phj.id_produk AND phj.id_tipe_harga = pl.id_tipe_harga
                            LEFT JOIN produk_uom puom1 on p.id = puom1.id_produk and puom1.level = 1
                            LEFT JOIN produk_uom puom2 on p.id = puom2.id_produk and puom2.level = 2
                            LEFT JOIN produk_uom puom3 on p.id = puom3.id_produk and puom3.level = 3
                            LEFT JOIN v_info v ON v.id_sales_order_detail = sod.id
                               WHERE ob.id = :id_order_batch
                            AND f.jenis_faktur = :jenis_faktur
                """
            )
            .bindparams_v2({
                "id_order_batch": id_order_batch,
                "jenis_faktur": jenisFaktur or 'penjualan',
                "id_sales_order": id_sales_order
            },
                expanding_keys=['id_sales_order']
        )
            .execute()
            .fetchall()
            .get()
        )

        id_faktur = list_detail_order[0]['id_faktur'] if len(list_detail_order) else None

        detail_faktur = (
            self.query().setRawQuery(
                f"""
                                    select
                                    distinct customer.nama as nama_customer,
                                    customer.alamat as alamat_customer,
                                    customer.telepon as telepon_customer,
                                    customer.kode as kode_customer,
                                    sales_order.*,
                                    faktur.*,
                                    rute.kode as kode_rute,
                                    principal.kode as kode_principal,
                                    principal.nama as nama_principal,
                                    faktur.id as id_faktur,
                                    faktur.no_faktur as nomor_faktur,
                                    users.nama as nama_driver,
                                    plafon.tempo_label
                                    from customer
                                    left join rute
                                    on rute.id = customer.id_rute
                                    join plafon
                                    on plafon.id_customer = customer.id
                                    join principal
                                    on principal.id = plafon.id_principal
                                    join sales_order
                                    on sales_order.id_plafon = plafon.id
                                    join faktur_detail
                                    on faktur_detail.id_sales_order = sales_order.id
                                    join faktur
                                    on faktur.id = faktur_detail.id_faktur
                                    join sales_order_detail
                                    on sales_order_detail.id_sales_order = sales_order.id
                                    join proses_picking
                                    on proses_picking.id_order_detail = sales_order_detail.id
                                    left join driver
                                    on driver.id = proses_picking.id_driver
                                    left join users
                                    on users.id = driver.id_user
                                    where faktur.id = :id_faktur 
                                    and faktur.jenis_faktur = :jenis_faktur
                                    {self.before_this_date_query}
                                """
            )
            .bindparams({
                "id_faktur":id_faktur,
                "jenis_faktur": jenisFaktur or 'penjualan'
            })
            .execute()
            .fetchone()
            .result
        )

        if len(list(detail_faktur)):
            detail_faktur["status_order_str"] = status_order(detail_faktur["status_order"])
        detail_faktur_obj = {
            "list_detail_order": list_detail_order,
            "detail_faktur": detail_faktur
        }
        return detail_faktur_obj

    def __mapping_produk_by_sales_order(self,detail_produk_list):
        mapping = {}
        for item in detail_produk_list:
            id_sales_order = item['id_sales_order']
            if id_sales_order not in mapping:
                mapping[id_sales_order] = [
                    item
                ]

            else:
                mapping[id_sales_order] = [
                    *mapping[id_sales_order], item
                ]

        return mapping

    @handle_error_rollback
    def submitShipping(self):
        token = request.headers.get('Authorization')
        if not token:
            raise nonServerErrorException("Token tidak ditemukan", 403)
        token = token.replace("Bearer ", "")
        if not token:
            raise nonServerErrorException("Token tidak ditemukan", 403)
        user = (
            self.query().setRawQuery(
                "SELECT id,id_cabang FROM users WHERE tokens = :token",
            ).bindparams({
                'token': token
            }).execute().fetchone().result
        )

        # Ambil parameter dari request

        id_rute = self.req('id_rute')
        id_cabang = int(self.req('id_cabang'))
        id_armada = int(self.req('id_armada'))
        id_driver = int(self.req('id_driver'))
        delivering_date = self.req('delivering_date')
        faktur_ids = self.req('faktur_ids')
        faktur_data = self.req('faktur_data')
        nama_fakturist = self.req('nama_fakturist')

        is_periode_closed, next_date = self.check_is_periode_closed()

        # Validasi data
        if not faktur_ids or not faktur_data or not isinstance(faktur_data, list):
            raise nonServerErrorException("Data faktur tidak valid", 400)

        # Set tanggal saat ini
        tanggal_sekarang = date_now()
        if is_periode_closed:
            tanggal_sekarang = next_date.strftime('%Y-%m-%d')

        # Validasi kesesuaian data faktur
        faktur_ids_set = set(map(int, faktur_ids))
        faktur_data_ids = {
            int(x.strip())
            for faktur in faktur_data
            for x in (
                [str(faktur["id_sales_order"])] if isinstance(faktur["id_sales_order"], int)
                else str(faktur["id_sales_order"]).split(',')
            )
            if x.strip().isdigit()
        }

        if faktur_ids_set != faktur_data_ids:
            raise nonServerErrorException("Data faktur tidak sesuai dengan IDs yang diberikan", 400)

        data_mapping_by_faktur = {}

        # Proses setiap faktur
        for faktur_item in faktur_data:

            id_sales_orders = []

            if isinstance(faktur_item['id_sales_order']  ,str):
                ids = faktur_item['id_sales_order'].split(',')
                id_sales_orders = [int(id_.strip()) for id_ in ids if id_.strip().isdigit()]
            elif isinstance(faktur_item['id_sales_order'],int):
                id_sales_orders = [faktur_item['id_sales_order']]


            for id_sales_order in id_sales_orders:

                # Dapatkan sales_order
                so = sales_order.query.filter(sales_order.id == id_sales_order).first()
                if not so:
                    raise nonServerErrorException(f"Sales Order dengan ID {id_sales_order} tidak ditemukan", 404)

                # Update status sales_order
                so.status_order = 4
                so.tanggal_faktur = tanggal_sekarang
                self.flush()

            # Update faktur
            id_order_batch = faktur_item['faktur_info'].get('id_order_batch', None)
            faktur_terkait = None
            if id_order_batch:
                faktur_terkait = Faktur.query.filter(Faktur.id_order_batch == id_order_batch).first()
                data_mapping_by_faktur[faktur_terkait.id] = self.__get_data_profile_by_order_batch( id_order_batch )
            else:
                faktur_terkait = Faktur.query.filter(Faktur.id_sales_order == id_sales_order).first()
                data_mapping_by_faktur[faktur_terkait.id] = self.__get_data_profile_by_sales_order( id_sales_order )

            if faktur_terkait:
                faktur_terkait.status_faktur = 1
                faktur_terkait.nama_fakturist = nama_fakturist

                # Update nilai faktur dari rincian_pembayaran
                if 'rincian_pembayaran' in faktur_item:
                    rincian = faktur_item['rincian_pembayaran']

                    if 'subtotal' in rincian:
                        faktur_terkait.subtotal_penjualan = format_angka(rincian['subtotal'])

                        so.total_order = format_angka(rincian['subtotal'])

                    if 'total_penjualan' in rincian:
                        faktur_terkait.total_penjualan = format_angka(rincian['total_penjualan'])

                    if 'diskon_nota' in rincian:
                        faktur_terkait.subtotal_diskon = format_angka(rincian['diskon_nota'])

                    if 'pajak' in rincian:
                        faktur_terkait.pajak = format_angka(rincian['pajak'])

                    # Hitung DPP (subtotal - diskon_nota)
                    if 'subtotal' in rincian and 'diskon_nota' in rincian:
                        subtotal = format_angka(rincian['subtotal'])
                        diskon_nota = format_angka(rincian['diskon_nota'])
                        faktur_terkait.dpp = format_angka(subtotal - diskon_nota)



                self.flush()

            # Update data faktur detail for batch order
            if id_order_batch:
                new_detail_produk_list = []
                for detail_produk in faktur_item.get('detail_produk', []):
                    data_faktur = next( (fd for fd in faktur_item.get('detail_faktur', []) if fd['id_produk'] == detail_produk['id_produk']), None)
                    if data_faktur:
                        new_detail_produk_list.append(
                            {
                                'id_sales_order': data_faktur['id_sales_order'],
                                **detail_produk
                            }
                        )
                mapping_produk = self.__mapping_produk_by_sales_order(new_detail_produk_list)
                for id_so, detail_produk in mapping_produk.items():
                    update_faktur_detail = FakturDetailModel.query.filter(
                        FakturDetailModel.id_sales_order == id_so,
                    ).first()
                    subtotal_all_product = sum(
                        format_angka(dp.get('subtotal',0)) - format_angka(dp.get('total_diskon',0))
                        for dp in detail_produk
                    )
                    subtotal_diskon_all_product = sum(
                        format_angka(dp.get('total_diskon',0))
                        for dp in detail_produk
                    )
                    pajak_all_product = sum(
                        format_angka(dp.get('ppn',0))
                        for dp in detail_produk
                    )
                    update_faktur_detail.subtotal = subtotal_all_product
                    update_faktur_detail.pajak = pajak_all_product
                    update_faktur_detail.subtotal_diskon = subtotal_diskon_all_product
                    update_faktur_detail.total = format_angka(subtotal_all_product) + format_angka(pajak_all_product)

                    self.flush()


            # Buat mapping produk untuk mempermudah akses data
            produk_mapping = {item['id_produk']: item for item in faktur_item.get('detail_produk', [])}

            # Proses detail faktur
            for detail_faktur in faktur_item['detail_faktur']:
                id_order_detail = detail_faktur['id_order_detail']
                id_produk = detail_faktur['id_produk']

                # Dapatkan detail order
                detail = sales_order_detail.query.filter(sales_order_detail.id == id_order_detail).first()
                if not detail:
                    raise nonServerErrorException(f"Detail order dengan ID {id_order_detail} tidak ditemukan", 404)

                # Update nilai total_nilai_discount dan subtotalorder
                produk_detail = produk_mapping.get(id_produk)
                if produk_detail:
                    if 'total_diskon' in produk_detail:
                        detail.total_nilai_discount = format_angka(produk_detail['total_diskon'])

                    if 'subtotal' in produk_detail and 'total_diskon' in produk_detail:
                        subtotal = format_angka(produk_detail['subtotal'])
                        total_diskon = format_angka(produk_detail['total_diskon'])
                        detail.subtotalorder = format_angka(subtotal - total_diskon)

                # Salin nilai dari picked ke shipped
                detail.pieces_shipped = detail.pieces_picked
                detail.box_shipped = detail.box_picked
                detail.karton_shipped = detail.karton_picked
                self.flush()

                # Dapatkan proses_picking terkait
                picking = prosesPicking.query.filter(prosesPicking.id_order_detail == detail.id).first()
                if picking:
                    # Update date_on_delivery
                    picking.date_on_delivery = tanggal_sekarang
                    self.flush()

                    # Dapatkan produk_id
                    produk_id = picking.id_produk
                    jumlah_picked = picking.jumlah_picked

                    if jumlah_picked and produk_id:
                        # Update stok
                        stok_item = stok.query.filter(
                            stok.produk_id == produk_id,
                            stok.cabang_id == id_cabang
                        ).first()

                        if stok_item:
                            # Kurangi jumlah_picked
                            stok_item.jumlah_picked -= jumlah_picked

                            # Tambah jumlah_delivery
                            stok_item.jumlah_delivery = (stok_item.jumlah_delivery or 0) + jumlah_picked

                            # Update tanggal dan waktu
                            stok_item.tanggal_update = tanggal_sekarang
                            stok_item.waktu_update = time_now()
                            self.flush()

                if produk_detail and 'voucher_detail' in produk_detail:
                    voucher_info = produk_detail['voucher_detail']

                    voucher_fields = [
                        ('v1r_id_dv', 'v1r_diskon'),
                        ('v2r_id_dv', 'v2r_diskon'),
                        ('v3r_id_dv', 'v3r_diskon'),
                        ('v2p_id_dv', 'v2p_diskon'),
                        ('v3p_id_dv', 'v3p_diskon')
                    ]

                    for id_field, diskon_field in voucher_fields:
                        id_dv = detail_faktur.get(id_field)

                        if id_dv is not None:
                            # Ambil nilai diskon dari voucher_detail
                            diskon_value = voucher_info.get(diskon_field, 0)
                            formatted_diskon = format_angka(diskon_value) if diskon_value is not None else 0

                            # Dapatkan draft voucher
                            dv_entry = draft_voucher.query.filter(draft_voucher.id == id_dv).first()

                            if dv_entry:
                                # Update status jika diskon = 0
                                if formatted_diskon == 0:
                                    dv_entry.status_promo = 3

                                # Update jumlah diskon
                                dv_entry.jumlah_diskon = formatted_diskon
                                self.flush()

            # Update tenggat waktu faktur (delivering_date + plafon.top)
            # Get sales_order with related plafon data
            for id_sales_order in id_sales_orders:
                sales_order_data = (
                    self.db
                    .session
                    .query(sales_order, plafon)
                    .join(plafon, sales_order.id_plafon == plafon.id)
                    .filter(sales_order.id == id_sales_order)
                    .first()
                )

                if sales_order_data:
                    update_so, plafon_data = sales_order_data

                    # Get delivering_date from proses_picking
                    delivering_date_result = (
                        self.db
                        .session
                        .query(prosesPicking.delivering_date)
                        .join(sales_order_detail, prosesPicking.id_order_detail == sales_order_detail.id)
                        .filter(sales_order_detail.id_sales_order == id_sales_order)
                        .first()
                    )

                    if delivering_date_result and delivering_date_result.delivering_date:
                        delivering_date_from_db = delivering_date_result.delivering_date
                        top_days = plafon_data.top or 0
                        if is_periode_closed:
                            # Jika periode akuntansi ditutup, gunakan next_date sebagai delivering_date
                            top_days += 1

                        # Calculate tanggal_jatuh_tempo = delivering_date + top
                        tanggal_jatuh_tempo = (delivering_date_from_db + timedelta(days=top_days)).strftime("%Y-%m-%d")
                        update_so.tanggal_jatuh_tempo = tanggal_jatuh_tempo
                        update_so.tanggal_cetak_jatuh_tempo = tanggal_jatuh_tempo

                        self.flush()

        payload_pubsub = {
            "created_by": user['id'],
            "id_fitur_mal": 4,
            "data": data_mapping_by_faktur
        }

        pubsub = getattr(current_app, 'pubsub', None)
        if pubsub:
            success = pubsub.publish(data=payload_pubsub, topic='create_jurnal')
            if success:
                current_app.logger.info("Published to PubSub successfully")
            else:
                current_app.logger.error("Failed to publish to PubSub")
                raise nonServerErrorException(status_code=500, message='Gagal mengirim pesan ke sistem jurnal')
        else:
            current_app.logger.error("PubSub client not found")
            raise nonServerErrorException(status_code=500, message='Gagal mengirim pesan ke sistem jurnal')

        # Commit perubahan
        self.commit()

        return {
            "status": "success",
            "message": "Pengiriman berhasil diproses",
            "data": {
                "tanggal": datetime.strptime(tanggal_sekarang, "%Y-%m-%d").strftime('%d/%m/%Y'),
            }
        }, 200
            
    @handle_error
    def getListRuteHistory(self, id_cabang):
        return (
            self.query().setRawQuery(
                """
                    select 
                    count(distinct customer.nama) as jumlah_toko,
                    count(distinct faktur.id) as jumlah_nota,
                    coalesce(sum(sales_order_detail.estimasi_kubikasi), 0) as kubikal,
                    count(distinct case 
                        when faktur.status_faktur = 5  or faktur.status_faktur = 8
                        then faktur.id  
                    end) as nota_terkirim,
                    count(distinct case 
                        when faktur.status_faktur = 4
                        then faktur.id  
                    end) as nota_proses,
                    count(distinct case 
                        when faktur.status_faktur = 7 
                        then faktur.id  
                    end) as nota_gagal,
                    rute.id as id_rute,
                    rute.nama_rute,
                    rute.kode,
                    armada.nama as nama_armada,
                    users.nama as nama_driver
                    
                    from customer
                    join rute on customer.id_rute = rute.id 
                    join cabang on customer.id_cabang = cabang.id
                    join plafon on plafon.id_customer = customer.id
                    join sales_order on sales_order.id_plafon = plafon.id
                    join faktur on faktur.id_sales_order = sales_order.id
                    join sales_order_detail on sales_order_detail.id_sales_order = sales_order.id
                    join proses_picking on proses_picking.id_order_detail = sales_order_detail.id
                    join armada on armada.id = proses_picking.id_armada
                    join driver on driver.id = proses_picking.id_driver
                    join users on users.id = driver.id_user
                    where customer.id_cabang = :id_cabang
                    and
                    faktur.status_faktur in (4, 3, 7, 8)
                    group by
                    rute.kode,
                    rute.id, 
                    rute.nama_rute, 
                    armada.nama,
                    users.nama;

                """
            )
            .bindparams({
                "id_cabang": id_cabang
            })
            .execute()
            .fetchall()
            .get()
        )

    @handle_error
    def getListNota(self):
        id_cabang = self.req("id_cabang")
        id_rute = self.req("id_rute")
        status_faktur = self.req("status_faktur")
        
        return (
            self.query().setRawQuery(
                """
                    select
                    sales_order.id as id_sales_order,
                    faktur.no_faktur,
                    sales_order.tanggal_order as tanggal_order,
                    rute.nama_rute,
                    rute.id as id_rute,
                    customer.nama as nama_customer,                                  
                    sales_order.total_kubikasi as kubikal,
                    faktur.jenis_faktur
                    from customer
                    join rute on customer.id_rute = rute.id 
                    join cabang on customer.id_cabang = cabang.id
                    join plafon on plafon.id_customer = customer.id
                    join sales_order on sales_order.id_plafon = plafon.id
                    join faktur on faktur.id_sales_order = sales_order.id
                    where customer.id_cabang = :id_cabang
                    and rute.id = :id_rute
                    and faktur.status_faktur = :status_faktur
                """
            )
            .bindparams({
                "id_cabang": id_cabang,
                "id_rute": id_rute,
                "status_faktur": status_faktur 
            })
            .execute()
            .fetchall()
            .get()
        )

    @handle_error  
    def getListOrder(self, id_cabang):
        listOrder = (
            self.query().setRawQuery(
                f"""
                    select 
                    distinct faktur.id as id_faktur,
                    sales_order.no_order,
                    sales_order.tanggal_order,
                    faktur.status_faktur,
                    customer.nama as nama_customer,
                    principal.nama as nama_principal
                    from customer
                    join cabang on customer.id_cabang = cabang.id
                    join plafon on plafon.id_customer = customer.id
                    join principal on principal.id = plafon.id_principal
                    join sales_order on sales_order.id_plafon = plafon.id
                    join faktur on faktur.id_sales_order = sales_order.id
                    where 
                    customer.id_cabang = :id_cabang
                    and 
                    faktur.status_faktur in (1, 2, 3, 4, 5)
                    and 
                    faktur.jenis_faktur = 'penjualan'
                    {self.before_this_date_query}
                """
            )
            .bindparams({
                "id_cabang": id_cabang,
            })
            .execute()
            .fetchall()
            .get()
        )
        
        return {
            "listOrder": listOrder,
            "last_update": datetime_now()
        }

    @handle_error
    def getRealisasiDetail(self):
        id_cabang = self.req("id_cabang")
        id_rute = self.req("id_rute")
        id_sales_order = self.req("id_sales_order")
        id_armada = self.req("id_armada")
        id_driver = self.req("id_driver")
        delivering_date = self.req("delivering_date")
        
        result = (
            self.query().setRawQuery(
                f"""
                    SELECT
                    DISTINCT produk.nama AS nama_produk,
                    rute.id AS id_rute,
                    faktur.id as id_faktur,
                    produk.id AS produk_id,
                    produk.kode_sku,
                    produk.isiperbox AS isi_per_box_produk,
                    produk.isiperkarton AS isi_per_karton_produk,
                    coalesce(SUM(sales_order_detail.pieces_picked),0) AS total_pieces,
                    coalesce(SUM(sales_order_detail.box_picked),0) AS total_box,
                    coalesce(SUM(sales_order_detail.karton_picked),0) AS total_karton,
                    coalesce(SUM(sales_order_detail.pieces_delivered),0) AS realisasi,
                    COALESCE(proses_picking.jumlah_picked::integer, 0) AS jumlah_picked,
                    ARRAY_AGG(sales_order_detail.id) AS id_detail_sales_array,
                    MAX(CASE WHEN puom1.level = 1 THEN puom1.faktor_konversi ELSE 1 END) as konversi1,
                    MAX(CASE WHEN puom2.level = 2 THEN puom2.faktor_konversi ELSE 1 END) as konversi2,
                    MAX(CASE WHEN puom3.level = 3 THEN puom3.faktor_konversi ELSE 1 END) as konversi3
                    FROM customer
                    JOIN rute ON customer.id_rute = rute.id
                    JOIN cabang ON customer.id_cabang = cabang.id
                    JOIN plafon ON plafon.id_customer = customer.id
                    JOIN sales_order ON sales_order.id_plafon = plafon.id
                    JOIN faktur on faktur.id_sales_order = sales_order.id
                    JOIN sales_order_detail ON sales_order_detail.id_sales_order = sales_order.id
                    JOIN produk ON sales_order_detail.id_produk = produk.id
                    LEFT JOIN proses_picking ON proses_picking.id_order_detail = sales_order_detail.id
                    left join produk_uom puom1 on puom1.id_produk = produk.id and puom1.level = 1
                    left join produk_uom puom2 on puom2.id_produk = produk.id and puom2.level = 2
                    left join produk_uom puom3 on puom3.id_produk = produk.id and puom3.level = 3
                    WHERE customer.id_cabang = :id_cabang
                    AND rute.id = :id_rute
                    AND sales_order.id = :id_sales_order
                    and faktur.jenis_faktur = 'penjualan'
                    and proses_picking.id_armada = :id_armada
                    and proses_picking.id_driver = :id_driver
                    and proses_picking.delivering_date = :delivering_date
                    and sales_order.status_order in (4,11)
                    {self.before_this_date_query}
                    GROUP BY 
                    nama_produk, 
                    rute.id, 
                    produk_id, 
                    produk.kode_sku, 
                    isi_per_box_produk, 
                    isi_per_karton_produk, 
                    jumlah_picked,
                    faktur.id
                """
            )
            .bindparams({
                "id_cabang": id_cabang,
                "id_rute": id_rute,
                "id_sales_order": id_sales_order,
                "id_armada": id_armada,
                "id_driver": id_driver,
                "delivering_date": delivering_date
            })
            .execute()
            .fetchall()
            .get()
        )
        
        return jsonify(result)

    @handle_error_rollback
    def submitRealisasiDetail(self):
        # Ambil data dari request

        token = request.headers.get('Authorization')
        if not token:
            raise nonServerErrorException("Token tidak ditemukan", 403)
        token = token.replace("Bearer ", "")
        if not token:
            raise nonServerErrorException("Token tidak ditemukan", 403)
        user = (
            self.query().setRawQuery(
                "SELECT id,id_cabang FROM users WHERE tokens = :token",
            ).bindparams({
                'token': token
            }).execute().fetchone().result
        )

        realisasi_list = self.req("realisasi")
        id_cabang = int(self.req("id_cabang"))
        id_fitur_mal = 5
        id_setoran = None
        id_sales_order = self.req("id_sales_order")
        id_order_batch = self.req("id_order_batch")
        nama_user = self.req("nama_user")
        pembayaran_via_dropper = self.req("pembayaran_via_dropper")
        no_faktur = self.req("no_faktur")

        # Validasi data
        if not realisasi_list or not isinstance(realisasi_list, list):
            raise nonServerErrorException("Data realisasi tidak valid atau kosong", 400)

        is_periode_closed, next_date = self.check_is_periode_closed()
        # Tanggal saat ini
        current_date = date_now()
        if is_periode_closed:
            current_date = next_date.strftime('%Y-%m-%d')
        current_time = time_now()

        # Kumpulkan semua ID faktur untuk diproses
        faktur_ids = set()
        need_revision = False

        # Proses setiap item realisasi untuk validasi dan perbandingan
        for item in realisasi_list:
            realisasi_value = item.get("realisasi")
            id_produk = item.get("id_produk")
            id_faktur = item.get("id_faktur")
            id_detail_sales = item.get("id_detail_sales", [])

            # KONVERSI id_detail_sales ke list jika berupa integer
            if isinstance(id_detail_sales, int):
                id_detail_sales = [id_detail_sales]
            elif isinstance(id_detail_sales, str):
                id_detail_sales = [int(x.strip()) for x in id_detail_sales.split(',')]
            elif not isinstance(id_detail_sales, list):
                id_detail_sales = []

            # Nilai konversi
            konversi1 = item.get("konversi1", 1)
            konversi2 = item.get("konversi2", 1)
            konversi3 = item.get("konversi3", 1)

            # Validasi nilai realisasi
            if not isinstance(realisasi_value, (int, float)) or realisasi_value < 0:
                raise nonServerErrorException(f"Nilai realisasi tidak valid untuk produk {id_produk}", 400)

            faktur_ids.add(id_faktur)

            # Hitung total shipped dalam pieces untuk item ini
            total_shipped_pieces = 0
            for id_detail in id_detail_sales:
                detail = sales_order_detail.query.filter(sales_order_detail.id == id_detail).first()
                if detail:
                    shipped_pieces = (
                            (detail.pieces_shipped or 0) * konversi1 +
                            (detail.box_shipped or 0) * konversi2 +
                            (detail.karton_shipped or 0) * konversi3
                    )
                    total_shipped_pieces += shipped_pieces

            # Validasi: realisasi tidak boleh lebih besar dari shipped
            if realisasi_value > total_shipped_pieces:
                raise nonServerErrorException(
                    f"Realisasi ({realisasi_value}) tidak boleh lebih besar dari jumlah yang dikirim ({total_shipped_pieces}) untuk produk ID {id_produk}",
                    400
                )

            # Cek apakah ada perbedaan (perlu revisi)
            if realisasi_value != total_shipped_pieces:
                need_revision = True

        # Proses setiap item realisasi
        for item in realisasi_list:
            realisasi_value = item.get("realisasi")
            id_produk = item.get("id_produk")
            id_faktur = item.get("id_faktur")
            id_detail_sales = item.get("id_detail_sales", [])

            # KONVERSI id_detail_sales ke list jika berupa integer (ulangi untuk safety)
            if isinstance(id_detail_sales, int):
                id_detail_sales = [id_detail_sales]
            # Nilai konversi
            konversi1 = item.get("konversi1", 1)
            konversi2 = item.get("konversi2", 1)
            konversi3 = item.get("konversi3", 1)

            # Hitung delivered berdasarkan konversi (dari level tertinggi ke terendah)
            sisa = realisasi_value

            # Karton (level 3)
            karton_delivered = sisa // konversi3
            sisa = sisa % konversi3

            # Box (level 2)
            box_delivered = sisa // konversi2
            sisa = sisa % konversi2

            # Pieces (level 1)
            pieces_delivered = sisa

            # Update sales_order_detail
            for id_detail in id_detail_sales:
                detail = sales_order_detail.query.filter(sales_order_detail.id == id_detail).first()

                if not detail:
                    continue

                # Update jumlah delivered
                detail.pieces_delivered = pieces_delivered
                detail.box_delivered = box_delivered
                detail.karton_delivered = karton_delivered

                # Update subtotaldelivered (realisasi × harga order)
                detail.subtotaldelivered = int(realisasi_value * detail.hargaorder)

                # Update proses_picking
                picking = prosesPicking.query.filter(prosesPicking.id_order_detail == id_detail).first()
                if picking:
                    picking.date_delivered = current_date

                self.flush()

            # Update stok berdasarkan kondisi revisi
            stok_item = stok.query.filter(
                stok.produk_id == id_produk,
                stok.cabang_id == id_cabang
            ).first()
            if stok_item:
                if need_revision:
                    # Hitung total shipped dalam pieces untuk item ini
                    total_shipped_pieces = 0
                    for id_detail in id_detail_sales:
                        detail = sales_order_detail.query.filter(sales_order_detail.id == id_detail).first()
                        if detail:
                            shipped_pieces = (
                                    (detail.pieces_shipped or 0) * konversi1 +
                                    (detail.box_shipped or 0) * konversi2 +
                                    (detail.karton_shipped or 0) * konversi3
                            )
                            total_shipped_pieces += shipped_pieces

                    # Kurangi jumlah_booked dan jumlah_delivery sesuai shipped_pieces
                    stok_item.jumlah_booked -= total_shipped_pieces
                    stok_item.jumlah_delivery -= total_shipped_pieces

                    # Hitung selisih (barang yang dikembalikan ke gudang)
                    selisih = total_shipped_pieces - realisasi_value

                    # Tambah jumlah_good dan jumlah_ready dari selisih
                    stok_item.jumlah_good = (stok_item.jumlah_good or 0) + selisih
                    stok_item.jumlah_ready = (stok_item.jumlah_ready or 0) + selisih

                else:
                    # Tidak ada revisi, proses normal
                    stok_item.jumlah_booked -= realisasi_value
                    stok_item.jumlah_delivery -= realisasi_value

                # Update tanggal dan waktu
                stok_item.tanggal_update = current_date
                stok_item.waktu_update = current_time
                self.flush()

        # Tambah setoran jika ada pembayaran_via_dropper (TIDAK peduli ada revisi atau tidak)
        if pembayaran_via_dropper:
            id_fitur_mal = 16
            new_setoran = None
            if id_order_batch:
                new_setoran = setoran(
                    id_order_batch=id_order_batch,
                    draft_tanggal_input=current_date,
                    draft_jumlah_setor=pembayaran_via_dropper,
                    nama_pj=nama_user,
                    tipe_setoran=1,
                    status_setoran=0,
                    pj_setoran=2
                )
            else:
                new_setoran = setoran(
                    id_sales_order=id_sales_order,
                    draft_tanggal_input=current_date,
                    draft_jumlah_setor=pembayaran_via_dropper,
                    nama_pj=nama_user,
                    tipe_setoran=1,
                    status_setoran=0,
                    pj_setoran=2
                )
            self.add(new_setoran).flush()

            id_setoran = new_setoran.id

        # Update status faktur dan sales order untuk semua faktur yang terlibat
        for id_faktur in faktur_ids:
            faktur_obj = Faktur.query.filter(Faktur.id == id_faktur).first()
            if faktur_obj:
                # Update plafon jika tidak ada revisi
                if not need_revision:
                    # Validasi draft_total_penjualan harus lebih besar dari total_penjualan
                    if faktur_obj.draft_total_penjualan < faktur_obj.total_penjualan:
                        raise nonServerErrorException(
                            f"Draft total penjualan ({faktur_obj.draft_total_penjualan}) tidak boleh lebih kecil dari total penjualan ({faktur_obj.total_penjualan}) untuk faktur ID {id_faktur}",
                            400
                        )

                    # Hitung selisih
                    selisih = faktur_obj.draft_total_penjualan - faktur_obj.total_penjualan

                    # Dapatkan sales_order untuk mendapatkan id_plafon
                    sales_orders = []
                    if faktur_obj.id_order_batch:
                        sales_orders = sales_order.query.filter(sales_order.id_order_batch == faktur_obj.id_order_batch).all()
                    else:
                        sales_orders = sales_order.query.filter(sales_order.id == faktur_obj.id_sales_order).all()
                    for so in sales_orders:
                        if faktur_obj.id_order_batch:
                            data_detail_faktur = FakturDetailModel.query.filter(
                                FakturDetailModel.id_sales_order == so.id
                            ).first()
                            selisih_by_faktur_detail = data_detail_faktur.draft_total - data_detail_faktur.total
                            if so and so.id_plafon:
                                # Validasi plafon exists
                                plafon_obj = plafon.query.filter(plafon.id == so.id_plafon).first()
                                if plafon_obj:
                                    # Update sisa_bon plafon
                                    plafon_obj.sisa_bon = (plafon_obj.sisa_bon or 0) + selisih_by_faktur_detail
                                    self.flush()
                        else:
                            if so and so.id_plafon:
                                # Validasi plafon exists
                                plafon_obj = plafon.query.filter(plafon.id == so.id_plafon).first()
                                if plafon_obj:
                                    # Update sisa_bon plafon
                                    plafon_obj.sisa_bon = (plafon_obj.sisa_bon or 0) + selisih
                                    self.flush()

                    # Status faktur tidak berubah jika ada revisi
                    faktur_obj.status_faktur = 2  # Status faktur unpaid
                if faktur_obj.id_order_batch:
                    sales_orders = sales_order.query.filter(sales_order.id_order_batch == faktur_obj.id_order_batch).all()
                else:
                    sales_orders = sales_order.query.filter(sales_order.id == faktur_obj.id_sales_order).all()
                for so in sales_orders:
                    if so:
                        if need_revision:
                            so.status_order = 5  # Status need revision
                        else:
                            so.status_order = 6  # Status delivered
                        so.tanggal_terkirim = current_date

                        self.flush()

        data_profile = {}

        if id_order_batch:
            data_profile = self.__get_data_profile_by_order_batch(id_order_batch)
        else:
            data_profile = self.__get_data_profile_by_sales_order(id_sales_order)

        if not need_revision:
            pubsub = getattr(current_app, 'pubsub', None)
            if pubsub:
                payload_pubsub = {
                    "created_by": user.get('id'),
                    "id_fitur_mal": id_fitur_mal,
                    "id_perusahaan": data_profile.get("id_perusahaan"),
                    "id_cabang": id_cabang,
                    "id_setoran": id_setoran,
                    "id_principal": data_profile.get("id_principal"),
                    "id_order_batch": id_order_batch,
                    "id_sales_order": id_sales_order,
                }

                success = pubsub.publish(data=payload_pubsub, topic='create_jurnal')
                if success:
                    current_app.logger.info("Published to PubSub successfully")
                else:
                    current_app.logger.error("Failed to publish to PubSub")
                    raise nonServerErrorException(status_code=500, message='Gagal mengirim pesan ke sistem jurnal')
            else:
                current_app.logger.error("PubSub client not found")
                raise nonServerErrorException(status_code=500, message='Gagal mengirim pesan ke sistem jurnal')

        # Commit semua perubahan
        self.commit()

        # Update pesan response untuk mencakup kasus setoran dengan revisi
        if pembayaran_via_dropper and need_revision:
            return {"status": "success",
                    "message": f"Proses realisasi belum selesai, Faktur dengan No Faktur: {no_faktur} ini lanjut ke proses revisi faktur. Setoran via dropper berhasil ditambahkan."}, 200
        elif pembayaran_via_dropper:
            return {"status": "success",
                    "message": f"Realisasi pengiriman dengan No Faktur: {no_faktur} berhasil dikonfirmasi. Setoran via dropper berhasil ditambahkan."}, 200
        else:
            if need_revision:
                return {"status": "success",
                        "message": f"Proses realisasi belum selesai, Faktur dengan No Faktur: {no_faktur} ini lanjut ke proses revisi faktur"}, 200
            return {"status": "success",
                    "message": f"Realisasi pengiriman dengan No Faktur: {no_faktur} berhasil dikonfirmasi"}, 200

    @handle_error
    def get_distribusi_info(self):
        email = self.req("email")
        password = self.req("password")
        print("LOGIN ROUTE Distribusi")
        user_info = (
            self.query().setRawQuery(
                """
                    select 
                    users.tokens AS token, 
                    users.id AS id_user, 
                    users.nama AS nama_user, 
                    users.email AS user_email, 
                    users.id_cabang AS id_cabang,
                    users.password,
                    cabang.nama as nama_cabang,
                    cabang.alamat as alamat_cabang,
                    cabang.telepon as telepon_cabang,
                    cabang.npwp as npwp_cabang,
                    jabatan.nama as nama_jabatan,
                    wilayah1.nama as nama_wilayah1,
                    wilayah2.nama as nama_wilayah2,
                    wilayah3.nama as nama_wilayah3,
                    wilayah4.nama as nama_wilayah4
                    from users 
                    join jabatan
                    on jabatan.id = users.id_jabatan
                    join cabang
                    on cabang.id = users.id_cabang
                    left join wilayah1
                    on wilayah1.id = cabang.id_wilayah1
                    left join wilayah2
                    on wilayah1.id = cabang.id_wilayah2
                    left join wilayah3
                    on wilayah3.id = cabang.id_wilayah3
                    left join wilayah4
                    on wilayah4.id = cabang.id_wilayah4
                    where 
                    email = :email 
                    and
                    id_jabatan in (1, 6, 8, 12, 13, 14, 2) 
                """
            )
            .bindparams({
                "email": email
            })
            .execute()
            .fetchone()
            .result
        )

        if not len(user_info) :
            raise nonServerErrorException("Email salah atau tidak ada")

        if not bcrypt.checkpw(password.encode('utf-8'), user_info["password"].encode('utf-8')):
            raise nonServerErrorException('Password salah', 403)

        return user_info

    @handle_error
    def getUserInfo(self, id_user):
        user_info = (
            self.query().setRawQuery(
                """
                    select 
                    users.*,
                    cabang.nama as nama_cabang,
                    cabang.alamat as alamat_cabang,
                    cabang.telepon as telepon_cabang,
                    cabang.npwp as npwp_cabang,
                    jabatan.nama as nama_jabatan,
                    wilayah1.nama as nama_wilayah1,
                    wilayah2.nama as nama_wilayah2,
                    wilayah3.nama as nama_wilayah3,
                    wilayah4.nama as nama_wilayah4
                    from users 
                    join jabatan
                    on jabatan.id = users.id_jabatan
                    join cabang
                    on cabang.id = users.id_cabang
                    left join wilayah1
                    on wilayah1.id = cabang.id_wilayah1
                    left join wilayah2
                    on wilayah1.id = cabang.id_wilayah2
                    left join wilayah3
                    on wilayah3.id = cabang.id_wilayah3
                    left join wilayah4
                    on wilayah4.id = cabang.id_wilayah4
                    where
                    users.id = :id_user
                    and
                    users.id_jabatan in (1, 6, 8, 12, 13, 14)
                """
            )
            .bindparams({"id_user": id_user})
            .execute()
            .fetchone()
            .result
        )
        
        user_info['last_update'] = datetime_now()
        
        return user_info

    @handle_error_rollback
    def batalRealisasi(self):
        id_faktur = self.req("id_faktur")
        keterangan_batal = self.req("keterangan_batal")
        status_faktur = self.req("status_faktur")

        # array of object : [{id_produk: int, jumlah_kembali_ke_gudang: int}]
        produk = self.req("produk")

        update_faktur = Faktur.query.filter(Faktur.id == id_faktur).first()

        if update_faktur.id_order_batch:
            id_sales_order_detail_array = (
                self.query()
                .setRawQuery(
                    """
                    select sales_order_detail.id as id_detail_oder
                    from sales_order                             
                             join sales_order_detail
                                  on sales_order.id = sales_order_detail.id_sales_order
                    where sales_order.id_order_batch = :id_order_batch
                    """
                )
                .bindparams({
                    "id_order_batch": update_faktur.id_order_batch
                })
                .execute()
                .fetchall()
                .get()
            )

            for idd in id_sales_order_detail_array:
                id_detail = idd['id_detail_oder']
                update_sales_order = prosesPicking.query.filter(prosesPicking.id_order_detail == id_detail).first()
                update_sales_order.jumlah_picked = 0

                self.flush()
        else:
            id_sales_order_detail_array = (
                self.query()
                .setRawQuery(
                    """
                        select sales_order_detail.id as id_detail_oder from sales_order 
                        join faktur 
                        on faktur.id_sales_order = sales_order.id
                        join sales_order_detail 
                        on sales_order.id = sales_order_detail.id_sales_order
                        where faktur.id = :id_faktur
                    """
                )
                .bindparams({
                    "id_faktur": id_faktur
                })
                .execute()
                .fetchall()
                .get()
            )

            for idd in id_sales_order_detail_array:
                id_detail = idd['id_detail_oder']
                update_sales_order = prosesPicking.query.filter(prosesPicking.id_order_detail == id_detail).first()
                update_sales_order.jumlah_picked = 0

                self.flush()

        for retur in produk:
            id_produk = retur['id_produk']
            jumlah = retur['jumlah_kembali_ke_gudang']

            update_stok = stok.query.filter(stok.produk_id == id_produk).first()
            stok_jumlah_ready = update_stok.jumlah_ready if isinstance(update_stok.jumlah_ready, int) else 0

            update_stok.jumlah_ready = stok_jumlah_ready + jumlah

            self.flush()

        update_faktur.status_faktur = status_faktur
        update_faktur.keterangan_batal = keterangan_batal
        
        self.commit()
        
        return {"status": "success"}, 200


    @handle_error
    def getListFakturJadwal(self):
        id_cabang = self.req('id_cabang')
        id_rute = self.req('id_rute')
        query_one_principal = f"""
                select 
                    so.id as id_sales_order,
                    f.no_faktur,
                    f.id as id_faktur,
                    so.no_order,
                    c.kode as kode_customer,
                    c.nama as nama_customer,
                    c.id as id_customer,
                    pr.nama as nama_principal,
                    pr.id as id_principal,
                    f.total_penjualan as total_bayar,
                    so.status_order,
                    so.tanggal_order,
                    coalesce(sum(sod.estimasi_kubikasi),0) as estimasi_kubikasi,
                    r.id as id_rute
                from 
                    sales_order as so
                join faktur f on so.id = f.id_sales_order
                join plafon p on so.id_plafon = p.id
                join customer c on p.id_customer = c.id
                join principal pr on p.id_principal = pr.id
                join sales_order_detail sod on sod.id_sales_order = so.id
                join rute r on r.id = c.id_rute
                where c.id_cabang = :id_cabang
                and so.status_order in (1,9) and r.id = :id_rute
                GROUP BY 
                    so.id,
                    f.no_faktur,
                    f.id,
                    so.no_order,
                    c.kode,
                    c.nama,
                    c.id,
                    pr.nama,
                    pr.id,
                    f.total_penjualan,
                    so.status_order,
                    so.tanggal_order,
                    r.id
                order by so.tanggal_order ASC

               """

        query_multi_principal = f"""
                select 
                    array_agg(so.id) as id_sales_order,
                    f.no_faktur,
                    f.id as id_faktur,
                    so.no_order,
                    c.kode as kode_customer,
                    c.nama as nama_customer,    
                    c.id as id_customer,
                    'MIX' as nama_principal,                    
                    f.total_penjualan as total_bayar,
                    so.status_order,
                    so.tanggal_order,   
                    coalesce(sum(sod.estimasi_kubikasi),0) as estimasi_kubikasi,
                    r.id as id_rute
                from 
                    sales_order as so
					join faktur_detail  fd on fd.id_sales_order = so.id
                join faktur f on f.id = fd.id_faktur
                join plafon p on so.id_plafon = p.id
                join customer c on p.id_customer = c.id
                join sales_order_detail sod on sod.id_sales_order = so.id
                join rute r on r.id = c.id_rute
                where c.id_cabang = :id_cabang
                and so.id_order_batch is not null
                and so.status_order in (1,9) and r.id = :id_rute
                GROUP BY 
                    f.no_faktur,
                    f.id,
                    so.no_order,
                    c.kode,
                    c.nama,                    
                    c.id,
                    f.total_penjualan,
                    so.status_order,
                    so.tanggal_order,
                    r.id
                order by  so.tanggal_order ASC
               """


        data_order_one_principal = self.query().setRawQuery(query_one_principal).bindparams({'id_cabang': id_cabang,'id_rute':id_rute }).execute().fetchall().get()
        data_order_multi_principal = self.query().setRawQuery(query_multi_principal).bindparams({'id_cabang': id_cabang,'id_rute':id_rute }).execute().fetchall().get()
        data_order = [
            *data_order_one_principal,
            *data_order_multi_principal
        ]

        sorted_data_order = sorted(data_order, key=lambda x: (x['tanggal_order']))

        return sorted_data_order

    @handle_error
    def getJadwalArmada(self):
        id_cabang = self.req('id_cabang')
        query_one_principal = """
            SELECT
                string_agg(DISTINCT pp.id::text, ',') as id_proses_picking,
                string_agg(DISTINCT pp.id_order_detail::text, ',') as id_order_detail,
                string_agg(DISTINCT pp.id_produk::text, ',') as id_produk,
                pp.id_armada,
                pp.id_driver,
                pp.delivering_date,
                a.nama as nama_armada,
                u.nama as nama_driver,
                string_agg(DISTINCT so.status_order::text, ',') as status_order,
                string_agg(DISTINCT f.id::text, ',') as id_faktur,
                string_agg(DISTINCT so.id::text, ',') as id_sales_order,
                r.id as id_rute,
                r.nama_rute,
                r.kode as kode_rute,
                string_agg(DISTINCT pp.id::text, ',') as id_proses_picking,
                coalesce(sum(sod.estimasi_kubikasi),0) as estimasi_kubikasi
                
            FROM proses_picking pp
            JOIN armada a ON a.id = pp.id_armada
            JOIN driver d ON d.id = pp.id_driver
            JOIN users u ON u.id = d.id_user
            JOIN sales_order_detail sod ON sod.id = pp.id_order_detail
            JOIN sales_order so ON so.id = sod.id_sales_order AND so.status_order IN (2,3,10)
            JOIN faktur f ON f.id_sales_order = so.id 
            JOIN plafon pl ON pl.id = so.id_plafon
            JOIN customer c ON c.id = pl.id_customer and c.id_cabang = :id_cabang
            JOIN rute r ON r.id = c .id_rute
            GROUP BY r.id, pp.delivering_date, pp.id_armada, pp.id_driver, a.nama, u.nama, r.nama_rute, r.kode
        """

        query_multi_principal = """
          SELECT
                string_agg(DISTINCT pp.id::text, ',') as id_proses_picking,
                string_agg(DISTINCT pp.id_order_detail::text, ',') as id_order_detail,
                string_agg(DISTINCT pp.id_produk::text, ',') as id_produk,
                pp.id_armada,
                pp.id_driver,
                pp.delivering_date,
                a.nama as nama_armada,
                u.nama as nama_driver,
                string_agg(DISTINCT so.status_order::text, ',') as status_order,
                string_agg(DISTINCT f.id::text, ',') as id_faktur,
                string_agg(DISTINCT so.id::text, ',') as id_sales_order,
                r.id as id_rute,
                r.nama_rute,
                r.kode as kode_rute,
                string_agg(DISTINCT pp.id::text, ',') as id_proses_picking,
                coalesce(sum(sod.estimasi_kubikasi),0) as estimasi_kubikasi
                
            FROM proses_picking pp
            JOIN armada a ON a.id = pp.id_armada
            JOIN driver d ON d.id = pp.id_driver
            JOIN users u ON u.id = d.id_user
            JOIN sales_order_detail sod ON sod.id = pp.id_order_detail
            JOIN sales_order so ON so.id = sod.id_sales_order AND so.status_order IN (2,3,10)
			JOIN faktur_detail fd ON so.id = fd.id_sales_order			
            JOIN faktur f ON f.id = fd.id_faktur
            JOIN plafon pl ON pl.id = so.id_plafon
            JOIN customer c ON c.id = pl.id_customer and c.id_cabang = :id_cabang
            JOIN rute r ON r.id = c .id_rute
            GROUP BY r.id, pp.delivering_date, pp.id_armada, pp.id_driver, a.nama, u.nama, r.nama_rute, r.kode
            """

        res1 = self.query().setRawQuery(query_one_principal)\
            .bindparams({'id_cabang': id_cabang}).execute().get()

        res2 = self.query().setRawQuery(query_multi_principal)\
            .bindparams({'id_cabang': id_cabang}).execute().get()

        data_order_one_principal = [
            dict(row) for row in res1.get("result", [])
        ]

        data_order_multi_principal = [
            dict(row) for row in res2.get("result", [])
        ]

        data_order = [
            *data_order_one_principal,
            *data_order_multi_principal
        ]


        merge_data_order = []
        for item in data_order:
            # Cek apakah ada item dengan id_rute dan delivering_date yang sama
            existing_item = next((x for x in merge_data_order if x['id_rute'] == item['id_rute'] and x['id_armada'] == item['id_armada'] and x['id_driver'] == item['id_driver'] and x['delivering_date'] == item['delivering_date']), None)
            if existing_item:
                # Jika ada, gabungkan field yang perlu digabungkan
                existing_item['id_proses_picking'] += ',' + item['id_proses_picking']
                existing_item['id_order_detail'] += ',' + item['id_order_detail']
                if item['id_produk'] not in existing_item['id_produk'].split(','):
                    existing_item['id_produk'] += ',' + item['id_produk']
                existing_item['status_order'] += ',' + item['status_order']
                existing_item['id_faktur'] += ',' + item['id_faktur']
                existing_item['id_sales_order'] += ',' + item['id_sales_order']
                existing_item['estimasi_kubikasi'] += item['estimasi_kubikasi']
            else:
                # Jika tidak ada, tambahkan item baru ke daftar hasil
                merge_data_order.append(item)


        return merge_data_order



    @handle_error_rollback
    def deleteJadwal(self):
        id_fakturs = self.req("id_faktur")
        id_proses_pickings = self.req("id_proses_picking")
        id_sales_orders = self.req("id_sales_order")

        # Convert comma-separated strings to lists if needed
        if isinstance(id_fakturs, str):
            id_fakturs = [int(id_faktur.strip()) for id_faktur in id_fakturs.split(',')]
        elif isinstance(id_fakturs, int):
            id_fakturs = [id_fakturs]

        if isinstance(id_proses_pickings, str):
            id_proses_pickings = [int(id_picking.strip()) for id_picking in id_proses_pickings.split(',')]
        elif isinstance(id_proses_pickings, int):
            id_proses_pickings = [id_proses_pickings]

        if isinstance(id_sales_orders, str):
            id_sales_orders = [int(id_so.strip()) for id_so in id_sales_orders.split(',')]
        elif isinstance(id_sales_orders, int):
            id_sales_orders = [id_sales_orders]

        # Cek status_order untuk setiap sales_order dan update sesuai kondisi
        for id_sales_order in id_sales_orders:
            sales_order_record = sales_order.query.filter(sales_order.id == id_sales_order).first()
            if not sales_order_record:
                raise nonServerErrorException(f"Sales Order dengan ID {id_sales_order} tidak ditemukan", 404)

            current_status = sales_order_record.status_order

            # Update status berdasarkan kondisi
            if current_status == 10:
                sales_order_record.status_order = 9
            elif current_status == 2:
                sales_order_record.status_order = 1

            self.flush()

        # Update proses_picking records berdasarkan status_order
        for id_picking in id_proses_pickings:
            picking_record = prosesPicking.query.filter(prosesPicking.id == id_picking).first()
            if picking_record:
                # Cari sales_order yang terkait dengan proses_picking ini
                detail_record = sales_order_detail.query.filter(
                    sales_order_detail.id == picking_record.id_order_detail
                ).first()

                if detail_record:
                    so_record = sales_order.query.filter(
                        sales_order.id == detail_record.id_sales_order
                    ).first()

                    if so_record:
                        # Reset delivery info untuk semua kasus
                        picking_record.delivering_date = None
                        picking_record.id_armada = None
                        picking_record.id_driver = None

                        # Update jumlah_picked berdasarkan status sebelumnya
                        # Jika status berubah dari 2 ke 1, reset jumlah_picked
                        # Jika status berubah dari 10 ke 9, tetap pertahankan jumlah_picked
                        if so_record.status_order == 1:  # Berarti sebelumnya status 2
                            picking_record.jumlah_picked = None
                        # Jika status_order == 9 (sebelumnya 10), jumlah_picked tetap tidak diubah

                        self.flush()

        self.commit()
        return {"message": "Jadwal berhasil dihapus."}, 200

    @handle_error_rollback
    def editJadwal(self):
        # Mengambil data dari request
        id_proses_picking = self.req("id_proses_picking")
        id_driver = self.req("id_driver")
        id_armada = self.req("id_armada")
        tanggal_pengiriman = self.req("tanggal_pengiriman")

        # Validasi data yang diterima
        if not id_proses_picking or not id_driver or not id_armada or not tanggal_pengiriman:
            raise nonServerErrorException("Data tidak lengkap", 400)

        # Mengonversi string id_proses_picking menjadi list jika dikirim dalam format "98,99"
        id_proses_picking_list = id_proses_picking.split(',') if isinstance(id_proses_picking, str) else [
            id_proses_picking]

        # Mengubah format tanggal jika dalam format ISO
        if 'T' in tanggal_pengiriman:
            tanggal_pengiriman = tanggal_pengiriman.split('T')[0]

        # Update setiap proses_picking berdasarkan ID
        for id_picking in id_proses_picking_list:
            # Cari record proses_picking berdasarkan ID
            picking_record = prosesPicking.query.filter(prosesPicking.id == int(id_picking)).first()

            if not picking_record:
                continue

            # Update data dengan nilai baru
            picking_record.id_driver = int(id_driver)
            picking_record.id_armada = int(id_armada)
            picking_record.delivering_date = tanggal_pengiriman

            self.flush()

        self.commit()
        return {"status": "success", "message": "Jadwal pengiriman berhasil diubah"}, 200

    @handle_error_rollback
    def submitPicking(self):

        token = request.headers.get('Authorization')
        if not token:
            raise nonServerErrorException("Token tidak ditemukan", 403)
        token = token.replace("Bearer ", "")
        if not token:
            raise nonServerErrorException("Token tidak ditemukan", 403)
        user = (
            self.query().setRawQuery(
                "SELECT id,id_cabang FROM users WHERE tokens = :token",
            ).bindparams({
                'token': token
            }).execute().fetchone().result
        )

        nama_picked = self.req('nama_picked')
        list_picking = self.req('list_picking')
        id_cabang = self.req('id_cabang')


        # Validasi data input
        if not nama_picked:
            raise nonServerErrorException("Nama picker tidak boleh kosong", 400)

        if not list_picking or not isinstance(list_picking, list) or len(list_picking) == 0:
            raise nonServerErrorException("Data picking tidak valid atau kosong", 400)

        if not id_cabang:
            raise nonServerErrorException("ID cabang tidak boleh kosong", 400)

        # Set tanggal picking saat ini
        tanggal_picking = date_now()
        waktu_picking = time_now()

        is_periode_closed, next_date = self.check_is_periode_closed()
        if is_periode_closed:
            tanggal_picking = next_date.strftime('%Y-%m-%d')

        data_mapping_by_faktur = {}

        # Set untuk menyimpan id_faktur yang unik
        unique_fakturs = set()
        # Iterasi untuk setiap item picking
        for item in list_picking:
            # Validasi item wajib
            if 'id_order_detail' not in item:
                raise nonServerErrorException("ID order detail tidak ditemukan", 400)
            if 'id_faktur' not in item:
                raise nonServerErrorException("ID faktur tidak ditemukan", 400)
            if 'produk_id' not in item:
                raise nonServerErrorException("ID produk tidak ditemukan", 400)

            # Parsing id_order_detail dan id_faktur yang mungkin berupa string dengan format '1,2,3'
            id_order_detail_list = str(item['id_order_detail']).split(',')
            id_faktur_list = str(item['id_faktur']).split(',')
            try:
                produk_id = int(item['produk_id'])
            except (ValueError, TypeError):
                raise nonServerErrorException(f"ID produk tidak valid: {item['produk_id']}", 400)

            # Validasi produk ada di database
            produk_exists = self.query().setRawQuery(
                "SELECT COUNT(*) as count FROM produk WHERE id = :id_produk"
            ).bindparams({"id_produk": produk_id}).execute().fetchone().result

            if not produk_exists or produk_exists["count"] == 0:
                raise nonServerErrorException(f"Produk dengan ID {produk_id} tidak ditemukan", 404)

            # Ambil nilai konversi dari frontend
            konversi1 = int(item.get('konversi1', 1))
            konversi2 = int(item.get('konversi2', 1))
            konversi3 = int(item.get('konversi3', 1))

            # Iterasi untuk setiap id_order_detail
            for i in range(len(id_order_detail_list)):
                try:
                    id_order_detail = int(id_order_detail_list[i].strip())
                except (ValueError, TypeError):
                    raise nonServerErrorException(f"ID order detail tidak valid: {id_order_detail_list[i]}", 400)

                # Mendapatkan sales_order_detail
                detail = sales_order_detail.query.filter(sales_order_detail.id == id_order_detail).first()
                if not detail:
                    raise nonServerErrorException(f"Detail sales order dengan ID {id_order_detail} tidak ditemukan",
                                                  404)

                # Mendapatkan proses_picking berdasarkan id_order_detail
                picking = prosesPicking.query.filter(prosesPicking.id_order_detail == id_order_detail).first()
                if not picking:
                    raise nonServerErrorException(
                        f"Proses picking untuk ID order detail {id_order_detail} tidak ditemukan", 404)

                # Dapatkan jumlah_picked dari database
                jumlah_picked = picking.jumlah_picked
                if not jumlah_picked or jumlah_picked <= 0:
                    raise nonServerErrorException(f"Jumlah picking untuk ID order detail {id_order_detail} tidak valid",
                                                  400)

                # Cek stok produk untuk validasi
                stok_item = stok.query.filter(
                    stok.produk_id == produk_id,
                    stok.cabang_id == id_cabang
                ).first()

                if not stok_item:
                    raise nonServerErrorException(f"Stok untuk produk ID {produk_id} tidak ditemukan di cabang ini",
                                                  404)

                # VALIDASI: Cek apakah stok mencukupi
                if stok_item.jumlah_good < jumlah_picked:
                    nama_produk = item.get('nama_produk')

                    raise nonServerErrorException(
                        f"Stok tidak mencukupi untuk produk '{nama_produk}'. "
                        f"Tersedia: {stok_item.jumlah_good}, Dibutuhkan: {jumlah_picked}",
                        400
                    )

                # Kalkulasi dari jumlah_picked dan nilai konversi dari frontend
                remaining = jumlah_picked

                # Hitung jumlah karton
                calculated_karton = 0
                if konversi3 > 0:
                    calculated_karton = remaining // konversi3
                    remaining -= calculated_karton * konversi3

                # Hitung jumlah box
                calculated_box = 0
                if konversi2 > 0:
                    calculated_box = remaining // konversi2
                    remaining -= calculated_box * konversi2

                # Sisanya menjadi pieces
                calculated_pieces = remaining

                # Update sales_order_detail
                detail.pieces_picked = calculated_pieces
                detail.box_picked = calculated_box
                detail.karton_picked = calculated_karton
                self.flush()

                # Update proses_picking
                picking.date_picked = tanggal_picking
                picking.pickers = nama_picked
                self.flush()

                # Update stok
                stok_item = stok.query.filter(
                    stok.produk_id == produk_id,
                    stok.cabang_id == id_cabang
                ).first()

                if stok_item:
                    stok_item.jumlah_picked += jumlah_picked
                    stok_item.jumlah_good -= jumlah_picked
                    stok_item.tanggal_update = tanggal_picking
                    stok_item.waktu_update = waktu_picking
                    self.flush()

                # Tambahkan id_faktur ke set unik jika ada
                if i < len(id_faktur_list):
                    id_faktur = int(id_faktur_list[i].strip())
                    unique_fakturs.add(id_faktur)

        # GENERATE NO_FAKTUR untuk semua faktur yang terlibat
        for id_faktur in unique_fakturs:
            fak = Faktur.query.filter(Faktur.id == id_faktur).first()
            if fak and not fak.no_faktur:  # Hanya generate jika no_faktur masih NULL
                # Get customer data untuk PPN
                so = None
                if fak.id_order_batch:
                    so = sales_order.query.filter(sales_order.id_order_batch == fak.id_order_batch).first()
                else:
                    so = sales_order.query.filter(sales_order.id == fak.id_sales_order).first()
                if so:
                    # Get plafon dan customer
                    plafon_data = plafon.query.filter(plafon.id == so.id_plafon).first()
                    customer_data = customer.query.filter(customer.id == plafon_data.id_customer).first()

                    # Get cabang data
                    cabang_data = cabang.query.filter(cabang.id == so.id_cabang).first()

                    # Get perusahaan data through principal
                    principal_data = principal.query.filter(principal.id == plafon_data.id_principal).first()
                    perusahaan_data = perusahaan.query.filter(perusahaan.id == principal_data.id_perusahaan).first()

                    # Generate PPN prefix
                    ppn_prefix = "PJ" if customer_data.is_ppn == 1 else "NP"

                    # Get current date components
                    current_date_str = date_now()  # YYYY-MM-DD format
                    if is_periode_closed:
                        current_date_str = next_date.strftime("%Y-%m-%d")  # Gunakan next_date jika periode closed
                    year = current_date_str[2:4]  # Get last 2 digits of year (25 for 2025)
                    month = current_date_str[5:7]  # Get month (05 for May)

                    # Generate no_faktur dengan retry mechanism
                    max_retries = 5
                    no_faktur = None

                    for attempt in range(max_retries):
                        try:
                            # Generate prefix for counter search
                            faktur_prefix = f"{ppn_prefix}{perusahaan_data.kode}{cabang_data.kode}-{year}{month}"

                            # Get the last counter for this prefix with database lock
                            last_faktur = faktur.query.filter(
                                faktur.no_faktur.like(f"{faktur_prefix}%")
                            ).with_for_update().order_by(faktur.no_faktur.desc()).first()

                            # Generate new counter
                            if last_faktur:
                                # Extract counter from last faktur (last 6+ digits)
                                last_counter_str = last_faktur.no_faktur.split('-')[1][4:]  # Remove year+month part
                                last_counter = int(last_counter_str)
                                new_counter = last_counter + 1
                            else:
                                new_counter = 1

                            # Format counter with minimum 6 digits
                            counter_str = f"{new_counter:06d}"

                            # Generate new faktur format: PPN+kode_perusahaan+kode_cabang-tahun+bulan+counter
                            no_faktur = f"{ppn_prefix}{perusahaan_data.kode}{cabang_data.kode}-{year}{month}{counter_str}"

                            # Test if this no_faktur already exists
                            existing_faktur = faktur.query.filter(faktur.no_faktur == no_faktur).first()
                            if existing_faktur:
                                raise IntegrityError("Duplicate no_faktur", None, None)

                            # Update faktur dengan no_faktur yang baru di-generate
                            fak.no_faktur = no_faktur
                            self.flush()
                            break  # Success, exit retry loop

                        except IntegrityError:
                            if attempt == max_retries - 1:
                                raise nonServerErrorException("Failed to generate unique no_faktur after 5 attempts")

                            time.sleep(random.uniform(0.01, 0.05))

            # Update status sales order
            if fak:
                if fak.id_order_batch:

                    so = sales_order.query.filter(sales_order.id_order_batch == fak.id_order_batch).all()
                    if so:

                        data_mapping_by_faktur[fak.id] = self.__get_data_profile_by_order_batch(id_order_batch=fak.id_order_batch)

                        for s in so:
                            s.status_order = 3
                            self.flush()
                else:
                    so = sales_order.query.filter(sales_order.id == fak.id_sales_order).first()
                    if so:

                        data_mapping_by_faktur[fak.id] = self.__get_data_profile_by_sales_order(id_sales_order=fak.id_sales_order)

                        so.status_order = 3
                        self.flush()

        payload_pubsub = {
            "created_by": user['id'],
            "id_fitur_mal":3,
            "data": data_mapping_by_faktur
        }

        pubsub = getattr(current_app, 'pubsub', None)
        if pubsub:
            success = pubsub.publish(data=payload_pubsub, topic='create_jurnal')
            if success:
                current_app.logger.info("Published to PubSub successfully")
            else:
                current_app.logger.error("Failed to publish to PubSub")
                raise nonServerErrorException(500,"Failed to publish to PubSub")
        else:
            current_app.logger.error("PubSub client not found")
            raise nonServerErrorException(status_code=500, message='Gagal mengirim pesan ke sistem jurnal')

        # Commit perubahan
        self.commit()

        return {
            "status": "success",
            "message": "Pesanan ini berhasil disiapkan"
        }, 200

    def __get_data_profile_by_order_batch(self, id_order_batch:int):
        query_get_profile = """
                                    SELECT pc.id_perusahaan, so.id_cabang, p.id_principal 
                                    FROM sales_order so 
                                             JOIN plafon p ON so.id_plafon = p.id 
                                             JOIN public.principal pc on p.id_principal = pc.id
                                    WHERE so.id_order_batch = :id_order_batch 
                                    """

        profile = self.query().setRawQuery(query_get_profile).bindparams({
            "id_order_batch": id_order_batch
        }).execute().fetchone().result

        return {
            'id_order_batch': id_order_batch,
            'id_perusahaan': profile['id_perusahaan'],
            'id_principal': profile['id_principal'],
            'id_cabang': profile['id_cabang']
        }

    def __get_data_profile_by_sales_order(self, id_sales_order:int):
        query_get_profile = """
                                    SELECT pc.id_perusahaan, so.id_cabang, p.id_principal
                                    FROM sales_order so \
                                             JOIN plafon p ON so.id_plafon = p.id \
                                             JOIN public.principal pc on p.id_principal = pc.id
                                    WHERE so.id = :id_sales_order \
                                    """

        profile = self.query().setRawQuery(query_get_profile).bindparams({
            "id_sales_order": id_sales_order
        }).execute().fetchone().result

        return{
            'id_sales_order': id_sales_order,
            'id_perusahaan': profile['id_perusahaan'],
            'id_principal': profile['id_principal'],
            'id_cabang': profile['id_cabang']
        }

    @handle_error_rollback
    def submitRevisiFaktur(self):
        faktur_ids = self.req('faktur_ids')
        faktur_data = self.req('faktur_data')
        nama_fakturist = self.req('nama_fakturist')

        is_periode_closed, next_date = self.check_is_periode_closed()

        # Validasi data
        if not faktur_ids or not faktur_data or not isinstance(faktur_data, list):
            raise nonServerErrorException("Data faktur tidak valid", 400)

        # Set tanggal saat ini
        tanggal_sekarang = date_now()
        if is_periode_closed:
            tanggal_sekarang = next_date.strftime('%Y-%m-%d')

        # Validasi kesesuaian data faktur
        faktur_ids_set = set(map(int, faktur_ids))
        faktur_data_ids = {
            int(x.strip())
            for faktur in faktur_data
            for x in (
                [str(faktur["id_sales_order"])] if isinstance(faktur["id_sales_order"], int)
                else str(faktur["id_sales_order"]).split(',')
            )
            if x.strip().isdigit()
        }


        if faktur_ids_set != faktur_data_ids:
            raise nonServerErrorException("Data faktur tidak sesuai dengan IDs yang diberikan", 400)

        # Proses setiap faktur
        for faktur_item in faktur_data:

            id_sales_orders = []

            if isinstance(faktur_item['id_sales_order'], str):
                ids = faktur_item['id_sales_order'].split(',')
                id_sales_orders = [int(id_.strip()) for id_ in ids if id_.strip().isdigit()]
            elif isinstance(faktur_item['id_sales_order'], int):
                id_sales_orders = [faktur_item['id_sales_order']]

            for id_sales_order in id_sales_orders:

                # Dapatkan sales_order
                so = sales_order.query.filter(sales_order.id == id_sales_order).first()
                if not so:
                    raise nonServerErrorException(f"Sales Order dengan ID {id_sales_order} tidak ditemukan", 404)

            # Update status sales_order
            so.status_order = 6
            self.flush()

            # Update faktur
            id_order_batch = faktur_item['faktur_info'].get('id_order_batch', None)
            faktur_terkait = None
            if id_order_batch:
                faktur_terkait = Faktur.query.filter(Faktur.id_order_batch == id_order_batch).first()
            else:
                faktur_terkait = Faktur.query.filter(Faktur.id_sales_order == id_sales_order).first()

            if faktur_terkait:
                faktur_terkait.status_faktur = 2

                # Update nilai faktur dari rincian_pembayaran
                if 'rincian_pembayaran' in faktur_item:
                    rincian = faktur_item['rincian_pembayaran']

                    if 'subtotal' in rincian:
                        faktur_terkait.subtotal_penjualan = format_angka(rincian['subtotal'])

                        so.total_order = format_angka(rincian['subtotal'])

                    if 'total_penjualan' in rincian:
                        faktur_terkait.total_penjualan = format_angka(rincian['total_penjualan'])

                    if 'diskon_nota' in rincian:
                        faktur_terkait.subtotal_diskon = format_angka(rincian['diskon_nota'])

                    if 'pajak' in rincian:
                        faktur_terkait.pajak = format_angka(rincian['pajak'])

                    # Hitung DPP (subtotal - diskon_nota)
                    if 'subtotal' in rincian and 'diskon_nota' in rincian:
                        subtotal = format_angka(rincian['subtotal'])
                        diskon_nota = format_angka(rincian['diskon_nota'])
                        faktur_terkait.dpp = format_angka(subtotal - diskon_nota)


                    # Update plafon - logika yang sama seperti submitRealisasiDetail
                    if 'total_penjualan' in rincian:
                        # Validasi draft_total_penjualan harus lebih besar dari total_penjualan
                        total_penjualan_baru = format_angka(rincian['total_penjualan'])
                        if faktur_terkait.draft_total_penjualan < total_penjualan_baru:
                            raise nonServerErrorException(
                                f"Draft total penjualan ({faktur_terkait.draft_total_penjualan}) tidak boleh lebih kecil dari total penjualan ({total_penjualan_baru}) untuk faktur ID {faktur_terkait.id}",
                                400
                            )

                        # Hitung selisih
                        selisih = faktur_terkait.draft_total_penjualan - total_penjualan_baru

                        # Dapatkan sales_order untuk mendapatkan id_plafon
                        if faktur_terkait.id_order_batch:
                            new_detail_produk_list = []
                            for detail_produk in faktur_item.get('detail_produk', []):
                                data_faktur = next( (fd for fd in faktur_item.get('detail_faktur', []) if fd['id_produk'] == detail_produk['id_produk']), None)
                                if data_faktur:
                                    new_detail_produk_list.append(
                                        {
                                            'id_sales_order': data_faktur['id_sales_order'],
                                            **detail_produk
                                        }
                                    )

                            mapping_produk = self.__mapping_produk_by_sales_order(new_detail_produk_list)
                            for id_so, detail_produk in mapping_produk.items():
                                update_faktur_detail = FakturDetailModel.query.filter(
                                    FakturDetailModel.id_sales_order == id_so,
                                ).first()
                                subtotal_all_product = sum(
                                    format_angka(dp.get('subtotal', 0)) - format_angka(dp.get('total_diskon', 0))
                                    for dp in detail_produk
                                )
                                subtotal_diskon_all_product = sum(
                                    format_angka(dp.get('total_diskon', 0))
                                    for dp in detail_produk
                                )
                                pajak_all_product = sum(
                                    format_angka(dp.get('ppn', 0))
                                    for dp in detail_produk
                                )
                                update_faktur_detail.subtotal = subtotal_all_product
                                update_faktur_detail.pajak = pajak_all_product
                                update_faktur_detail.subtotal_diskon = subtotal_diskon_all_product
                                update_faktur_detail.total = format_angka(subtotal_all_product) + format_angka(
                                    pajak_all_product)


                                self.flush()

                        else:
                            if so and so.id_plafon:
                                # Validasi plafon exists
                                plafon_obj = plafon.query.filter(plafon.id == so.id_plafon).first()
                                if plafon_obj:
                                    # Update sisa_bon plafon
                                    plafon_obj.sisa_bon = (plafon_obj.sisa_bon or 0) + selisih
                                    self.flush()

                self.flush()

            # Buat mapping produk untuk mempermudah akses data
            produk_mapping = {item['id_produk']: item for item in faktur_item.get('detail_produk', [])}

            # Proses detail faktur
            for detail_faktur in faktur_item['detail_faktur']:
                id_order_detail = detail_faktur['id_order_detail']
                id_produk = detail_faktur['id_produk']

                # Dapatkan detail order
                detail = sales_order_detail.query.filter(sales_order_detail.id == id_order_detail).first()
                if not detail:
                    raise nonServerErrorException(f"Detail order dengan ID {id_order_detail} tidak ditemukan", 404)

                # Update nilai total_nilai_discount
                produk_detail = produk_mapping.get(id_produk)
                if produk_detail:
                    if 'total_diskon' in produk_detail:
                        detail.total_nilai_discount = format_angka(produk_detail['total_diskon'])

                    if 'subtotal' in produk_detail and 'total_diskon' in produk_detail:
                        subtotal = format_angka(produk_detail['subtotal'])
                        total_diskon = format_angka(produk_detail['total_diskon'])
                        detail.subtotalorder = format_angka(subtotal - total_diskon)

                self.flush()

                # Proses voucher jika ada
                if produk_detail and 'voucher_detail' in produk_detail:
                    voucher_info = produk_detail['voucher_detail']

                    voucher_fields = [
                        ('v1r_id_dv', 'v1r_diskon'),
                        ('v2r_id_dv', 'v2r_diskon'),
                        ('v3r_id_dv', 'v3r_diskon'),
                        ('v2p_id_dv', 'v2p_diskon'),
                        ('v3p_id_dv', 'v3p_diskon')
                    ]

                    for id_field, diskon_field in voucher_fields:
                        id_dv = detail_faktur.get(id_field)

                        if id_dv is not None:
                            # Ambil nilai diskon dari voucher_detail
                            diskon_value = voucher_info.get(diskon_field, 0)
                            formatted_diskon = format_angka(diskon_value) if diskon_value is not None else 0

                            # Dapatkan draft voucher
                            dv_entry = draft_voucher.query.filter(draft_voucher.id == id_dv).first()

                            if dv_entry:
                                # Update status jika diskon = 0
                                if formatted_diskon == 0:
                                    dv_entry.status_promo = 3

                                # Update jumlah diskon
                                dv_entry.jumlah_diskon = formatted_diskon
                                self.flush()

            # Tambah setoran jika ada pembayaran_via_dropper
            # if pembayaran_via_dropper and 'rincian_pembayaran' in faktur_item:
            #     rincian = faktur_item['rincian_pembayaran']
            #     if 'total_penjualan' in rincian:
            #         new_setoran = setoran(
            #             id_sales_order=id_sales_order,
            #             draft_tanggal_input=current_date,
            #             draft_jumlah_setor=format_angka(rincian['total_penjualan']),
            #             nama_pj=nama_fakturist,
            #             tipe_setoran=1,
            #             status_setoran=0,
            #             pj_setoran=2
            #         )
            #         self.add(new_setoran).flush()

        # Commit perubahan
        self.commit()

        return {
            "status": "success",
            "message": "Revisi faktur berhasil diproses"
        }, 200

    @handle_error_rollback
    def jadwalkanUlangFaktur(self):
        id_sales_orders = self.req("id_sales_order")

        for id_sales_order in id_sales_orders:

            # Validasi sales order exists
            so = sales_order.query.filter(sales_order.id == id_sales_order).first()
            if not so:
                raise nonServerErrorException(f"Sales Order dengan ID {id_sales_order} tidak ditemukan", 404)

            # Update status sales order
            so.status_order = 9
            self.flush()

            # Hapus data delivery dari proses_picking yang terkait dengan sales_order
            proses_picking_records = (
                prosesPicking.query
                .join(sales_order_detail, prosesPicking.id_order_detail == sales_order_detail.id)
                .filter(sales_order_detail.id_sales_order == id_sales_order)
                .all()
            )

            for picking in proses_picking_records:
                picking.delivering_date = None
                picking.date_on_delivery = None
                picking.id_armada = None
                picking.id_driver = None
                self.flush()

        self.commit()

        return {
            "status": "success",
            "message": "Faktur siap dijadwalkan ulang"
        }, 200

    @handle_error_rollback
    def submitReshipping(self):
        reshipping_data = self.req("reshipping_data")  # Sesuai dengan body dari FE

        # Validasi data
        if not reshipping_data or not isinstance(reshipping_data, list):
            raise nonServerErrorException("Data reshipping tidak valid", 400)

        # Set tanggal saat ini
        current_date = date_now()
        is_periode_closed, next_date = self.check_is_periode_closed()
        if is_periode_closed:
            current_date = next_date.strftime('%Y-%m-%d')

        # Proses setiap item reshipping
        for item in reshipping_data:
            id_sales_orders = []
            if isinstance(item.get('id_sales_order'), str):
                ids = item.get('id_sales_order').split(',')
                id_sales_orders = [int(id_.strip()) for id_ in ids if id_.strip().isdigit()]
            elif isinstance(item.get('id_sales_order'), int):
                id_sales_orders = [item.get('id_sales_order')]

            for id_sales_order in id_sales_orders:
                # Validasi sales order exists

                id_sales_order_detail = item.get('id_sales_order_detail')

                # Validasi data
                if not id_sales_order:
                    raise nonServerErrorException("ID sales order tidak ditemukan", 400)
                if not id_sales_order_detail:
                    raise nonServerErrorException("ID sales order detail tidak ditemukan", 400)

                # Update status sales_order menjadi 11
                sales_order_data = (
                    self.db
                    .session
                    .query(sales_order, plafon)
                    .join(plafon, sales_order.id_plafon == plafon.id)
                    .filter(sales_order.id == id_sales_order)
                    .first()
                )
                if not sales_order_data:
                    raise nonServerErrorException(f"Sales Order dengan ID {id_sales_order} tidak ditemukan", 404)
                so, plafon_data  = sales_order_data
                if not so:
                    raise nonServerErrorException(f"Sales Order dengan ID {id_sales_order} tidak ditemukan", 404)

                so.status_order = 11
                self.flush()

                # Parse id_sales_order_detail yang berupa string dengan format "316,317,318"
                id_detail_list = [int(id_detail.strip()) for id_detail in str(id_sales_order_detail).split(',')]

                # Update proses_picking untuk setiap detail
                for id_detail in id_detail_list:
                    # Cari proses_picking berdasarkan id_order_detail
                    picking = prosesPicking.query.filter(prosesPicking.id_order_detail == id_detail).first()

                    if picking:
                        picking.date_on_delivery = current_date
                        self.flush()
                    else:
                        # Optional: log warning jika proses_picking tidak ditemukan
                        print(f"Warning: Proses picking untuk detail order {id_detail} tidak ditemukan")

                # Update jatuh tempo
                if plafon_data:
                    top_days = plafon_data.top or 0
                    if is_periode_closed:
                        top_days += 1
                    tanggal_jatuh_tempo = (date_now_obj() + timedelta(days=top_days)).strftime('%Y-%m-%d')
                    so.tanggal_jatuh_tempo = tanggal_jatuh_tempo
                    self.flush()

        # Commit perubahan
        self.commit()

        return {
            "status": "success",
            "message": "Reshipping berhasil diproses, dan draft berhasil dicetak"
        }, 200

    @handle_error
    def getListHistoryDistribusi(self):
        id_cabang = self.req('id_cabang')
        query = """
                WITH first_detail AS (
                    SELECT DISTINCT ON (sod.id_sales_order)
                        sod.id_sales_order,
                        pp.id_armada,
                        pp.delivering_date
                    FROM sales_order_detail sod
                             JOIN proses_picking pp ON pp.id_order_detail = sod.id
                    ORDER BY sod.id_sales_order, sod.id -- ambil 1 per id_sales_order (yang paling awal)
                )

                SELECT
                    f.no_faktur,                    
                    so.status_order,
                    fd.delivering_date 
                        AS
                     tanggal_terkirim,
                    r.kode as kode_rute,
                    a.nama as nama_armada
                FROM sales_order so
                         JOIN plafon p
                              ON p.id = so.id_plafon
                         JOIN customer c
                              ON c.id = p.id_customer
                         JOIN rute r
                              ON r.id = c.id_rute
                         JOIN first_detail fd
                              ON fd.id_sales_order = so.id
                         JOIN armada a
                              ON a.id = fd.id_armada
                         JOIN faktur f
                              ON f.id_sales_order = so.id
                WHERE
                    so.status_order in (4, 9)
                    AND 
                    so.id_cabang = :id_cabang
                """


        return PaginateV2(request=request,query=query,bindParams={
            "id_cabang": id_cabang
        }).paginate()