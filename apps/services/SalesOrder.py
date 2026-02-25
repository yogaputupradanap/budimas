from flask import jsonify
from apps.lib.helper import date_now_stamp, time_now_stamp, date_now, to_array_string
from datetime import datetime, timedelta
from apps.models import (
    sales_order,
    draft_sales,
    draft_voucher,
    sales_order_detail,
    faktur,
    produk as produk_model,
    plafon,
    stok,
    proses_picking, customer, cabang, perusahaan, principal, ReturRequest, ReturRequestDetail, OrderBatchModel
)
from . import BaseServices
from apps.handler import handle_error, handle_error_rollback, nonServerErrorException
from ..lib.utils import calculate_konversi
from ..models.faktur_detail import FakturDetailModel


class SalesOrder(BaseServices):
    def updateSisaPlafon(self, id_plafon, total_penjualan):
        get_plafon = plafon.query.filter(plafon.id == id_plafon).first()
        limit_plafon = get_plafon.limit_bon
        sisa_plafon = get_plafon.sisa_bon
        sisa_bon = None

        if sisa_plafon != None:
            sisa_bon = sisa_plafon - total_penjualan
            # if sisa_bon < 0: sisa_bon = 0
        else:
            sisa_bon = limit_plafon - total_penjualan

        get_plafon.sisa_bon = sisa_bon

    def searchIdPlafon(self, id_plafon):
        plafons = []

        for id in id_plafon:
            plafon = (
                self
                .query()
                .setRawQuery(
                    f"""
                        select * from plafon
                        where id = {id} 
                    """
                )
                .execute()
                .fetchone()
                .result
            )

            if not plafon:
                raise nonServerErrorException(f"Plafon dengan ID {id} tidak ditemukan")
            plafons.append(plafon)


        return plafons

    def searchIdPlafonByIdPrincipal(self, id_plafon, id_principal):
        plafon = {}

        for id in id_plafon:
            plafon = (
                self
                .query()
                .setRawQuery(
                    f"""
                        select * from plafon
                        where id = {id}
                        and id_principal = {id_principal}
                    """
                )
                .execute()
                .fetchone()
                .result
            )

            if len(plafon): return plafon

        return plafon

    @handle_error_rollback
    def SalesRequestWithDBT(self):
        """
         Generate sales request
         @return dict
        """
        current_date = datetime.now()
        # tanggal_jatuh_tempo = (
        #         current_date + timedelta(days=10)).strftime("%Y-%m-%d")


        products = self.req("products")

        # validate products
        for produk in products:
            data_produk = produk_model.query.get(produk["id_produk"])
            if not data_produk:
                raise nonServerErrorException(f"Produk dengan ID {produk['id_produk']} tidak ditemukan")

            data_stok = stok.query.filter(
                stok.produk_id == produk["id_produk"],
                stok.cabang_id == self.req("id_cabang")
            ).first()

            if not data_stok:
                raise nonServerErrorException(
                    f"Data stok untuk produk {data_produk.nama} di cabang ini tidak ditemukan"
                )

            total_pieces_dipesan = produk.get("total_pieces", 0)

            jumlah_ready = data_stok.jumlah_ready or 0
            if total_pieces_dipesan > jumlah_ready:
                raise nonServerErrorException(
                    f"Stok tidak mencukupi untuk produk {data_produk.nama}. "
                    f"Dipesan: {total_pieces_dipesan}, Tersedia: {jumlah_ready}"
                )

        data_product_by_principal = self.__filtered_by_id_principal(self.req("products"))

        if len(data_product_by_principal) > 1:
            plafon_arr = self.searchIdPlafon(self.req("id_plafon"))
            return self.__for_multiple_principal(plafon_arr, products)
        else:
            id_principal =products[0]["id_principal"]
            plafon_obj = self.searchIdPlafonByIdPrincipal(self.req("id_plafon"), id_principal)
            id_plafon = int(plafon_obj["id"])
            return self.__for_one_principal(id_plafon=id_plafon, products=products)

    def __for_multiple_principal(self, plafon_arr, products):
        # Kalkulasi total_order dari products.totalHarga all
        total_order = sum(produk["totalHarga"] for produk in products)

        new_order_batch = OrderBatchModel(
            id_sales=plafon_arr[0]["id_sales"],
            id_customer=plafon_arr[0]["id_customer"],
            status=0
        )

        data_product_by_principal = self.__filtered_by_id_principal(self.req("products"))

        self.add(new_order_batch).flush()

        # Faktur dibuat dengan no_faktur NULL
        faktur_sales = faktur(
            no_faktur=None,  # Set NULL dulu
            status_faktur=0,
            jenis_faktur='penjualan',
            subtotal_penjualan=total_order,
            subtotal_diskon=self.req("subtotal_diskon"),
            total_penjualan=self.req("total_penjualan"),
            total_dana_diterima=self.req("total_dana_diterima") or 0,
            pajak=self.req("pajak"),
            dpp=self.req("subtotal_penjualan"),
            id_order_batch=new_order_batch.id
        )

        self.add(faktur_sales)
        for plafon in plafon_arr:
            id_plafon = plafon["id"]
            if plafon["id_principal"] not in data_product_by_principal:
                continue
            draftSales = draft_sales(
                id_plafon=id_plafon,
                no_order=self.req("no_sales_order"),
                tanggal_order=self.req("tanggal_order"),
                # tanggal_jatuh_tempo=self.req(
                #     "tanggal_jatuh_tempo") or tanggal_jatuh_tempo,
                nama_sales=self.req("nama_sales"),
                status_order="0"
            )

            self.add(draftSales).flush()

            sales_order_id = draftSales.id

            is_periode_closed, next_date = self.check_is_periode_closed()
            tanggal_order = date_now()
            if is_periode_closed:
                tanggal_order = next_date.strftime("%Y-%m-%d")

            total_order_by_principal = sum(
                produk["totalHarga"] for produk in data_product_by_principal[plafon["id_principal"]])

            salesOrder = sales_order(
                id=sales_order_id,
                id_plafon=id_plafon,
                id_cabang=self.req("id_cabang"),
                no_order=self.req("no_sales_order"),
                tanggal_order=tanggal_order,
                # tanggal_jatuh_tempo=self.req(
                #     "tanggal_jatuh_tempo") or tanggal_jatuh_tempo,
                nama_sales=self.req("nama_sales"),
                status_order=0,
                total_order=total_order_by_principal,
                id_order_batch=new_order_batch.id
            )

            self.add(salesOrder)

            subtotal_diskon = sum(produk["totalDiskon"] for produk in data_product_by_principal[plafon["id_principal"]])
            pajak = sum(produk["ppn_value"] for produk in data_product_by_principal[plafon["id_principal"]])

            # Faktur dibuat dengan no_faktur NULL
            faktur_detail = FakturDetailModel(
                id_faktur=faktur_sales.id,
                id_sales_order=sales_order_id,
                id_principal=plafon["id_principal"],
                subtotal_diskon=subtotal_diskon,
                subtotal=total_order_by_principal,
                draft_total=total_order_by_principal - subtotal_diskon,
                pajak=pajak
            )

            self.add(faktur_detail)

            self.flush()

            total_kubikasi = 0
            # Add products to the list of produks
            for produk in data_product_by_principal[plafon["id_principal"]]:
                # calculate total kubikasi
                curr_produk = produk_model.query.get(produk["id_produk"])
                kubikasi_per_pieces = curr_produk.kubikasiperpieces or 0
                kubikasi_per_box = curr_produk.kubikasiperbox or 0
                kubikasi_per_karton = curr_produk.kubikasiperkarton or 0

                kubikasi_pieces = kubikasi_per_pieces * \
                                  produk["pieces_order"]
                kubikasi_box = kubikasi_per_box * produk["box_order"]
                kubikasi_karton = kubikasi_per_karton * \
                                  produk["karton_order"]

                curr_total = kubikasi_pieces + kubikasi_box + kubikasi_karton
                total_kubikasi += curr_total

                salesOrderDetail = sales_order_detail(
                    id_sales_order=sales_order_id,
                    id_produk=produk["id_produk"],
                    pieces_order=produk["pieces_order"],
                    box_order=produk["box_order"],
                    karton_order=produk["karton_order"],
                    hargaorder=produk["harga_jual"],
                    subtotalorder=produk["subtotalorder"],
                    vouchers=produk["vouchers"],
                    estimasi_kubikasi=curr_total,
                    total_nilai_discount=produk['totalDiskon']
                )

                self.add(salesOrderDetail).flush()

                # add proses picking
                picking = proses_picking(
                    id_order_detail=salesOrderDetail.id,
                    id_produk=produk["id_produk"]
                )

                self.add(picking)

                if 'voucherSelections' in produk:
                    # Voucher 1 Regular
                    if 'voucher1Regular' in produk['voucherSelections'] and produk['voucherSelections'][
                        'voucher1Regular']:
                        voucher1Regular = produk['voucherSelections']['voucher1Regular']
                        diskon1Regular = produk['discountDetails'][
                            'diskon1Regular'] if 'discountDetails' in produk and 'diskon1Regular' in \
                                                 produk['discountDetails'] else 0

                        draftVoucher1Regular = draft_voucher(
                            id_sales_order=sales_order_id,
                            id_sales_order_detail=salesOrderDetail.id,
                            id_voucher=voucher1Regular['id'],
                            tipe_voucher=1,
                            status_promo=0,
                            status_klaim=0,
                            jumlah_diskon=diskon1Regular,
                            kode_voucher=voucher1Regular['kode_voucher']
                        )

                        self.add(draftVoucher1Regular)

                    # Voucher 2 Regular
                    if 'voucher2Regular' in produk['voucherSelections'] and produk['voucherSelections'][
                        'voucher2Regular']:
                        voucher2Regular = produk['voucherSelections']['voucher2Regular']
                        diskon2Regular = produk['discountDetails'][
                            'diskon2Regular'] if 'discountDetails' in produk and 'diskon2Regular' in \
                                                 produk['discountDetails'] else 0

                        draftVoucher2Regular = draft_voucher(
                            id_sales_order=sales_order_id,
                            id_sales_order_detail=salesOrderDetail.id,
                            id_voucher=voucher2Regular['id'],
                            tipe_voucher=2,
                            status_promo=0,
                            status_klaim=0,
                            jumlah_diskon=diskon2Regular,
                            kode_voucher=voucher2Regular['kode_voucher']
                        )

                        self.add(draftVoucher2Regular)

                    # Voucher 3 Regular
                    if 'voucher3Regular' in produk['voucherSelections'] and produk['voucherSelections'][
                        'voucher3Regular']:
                        voucher3Regular = produk['voucherSelections']['voucher3Regular']
                        diskon3Regular = produk['discountDetails'][
                            'diskon3Regular'] if 'discountDetails' in produk and 'diskon3Regular' in \
                                                 produk['discountDetails'] else 0

                        draftVoucher3Regular = draft_voucher(
                            id_sales_order=sales_order_id,
                            id_sales_order_detail=salesOrderDetail.id,
                            id_voucher=voucher3Regular['id'],
                            tipe_voucher=3,
                            status_promo=0,
                            status_klaim=0,
                            jumlah_diskon=diskon3Regular,
                            kode_voucher=voucher3Regular['kode_voucher']
                        )

                        self.add(draftVoucher3Regular)

                    # Voucher 2 Product
                    if 'voucher2Product' in produk['voucherSelections'] and produk['voucherSelections'][
                        'voucher2Product']:
                        voucher2Product = produk['voucherSelections']['voucher2Product']
                        diskon2Product = produk['discountDetails'][
                            'diskon2Product'] if 'discountDetails' in produk and 'diskon2Product' in \
                                                 produk['discountDetails'] else 0

                        draftVoucher2Product = draft_voucher(
                            id_sales_order=sales_order_id,
                            id_sales_order_detail=salesOrderDetail.id,
                            id_voucher=voucher2Product['id'],
                            tipe_voucher=2,  # Tetap menggunakan tipe_voucher=2 karena ini adalah voucher level 2
                            status_promo=0,
                            status_klaim=0,
                            jumlah_diskon=diskon2Product,
                            kode_voucher=voucher2Product['kode_voucher']
                        )

                        self.add(draftVoucher2Product)

                    # Voucher 3 Product
                    if 'voucher3Product' in produk['voucherSelections'] and produk['voucherSelections'][
                        'voucher3Product']:
                        voucher3Product = produk['voucherSelections']['voucher3Product']
                        diskon3Product = produk['discountDetails'][
                            'diskon3Product'] if 'discountDetails' in produk and 'diskon3Product' in \
                                                 produk['discountDetails'] else 0

                        draftVoucher3Product = draft_voucher(
                            id_sales_order=sales_order_id,
                            id_sales_order_detail=salesOrderDetail.id,
                            id_voucher=voucher3Product['id'],
                            tipe_voucher=3,  # Tetap menggunakan tipe_voucher=3 karena ini adalah voucher level 3
                            status_promo=0,
                            status_klaim=0,
                            jumlah_diskon=diskon3Product,
                            kode_voucher=voucher3Product['kode_voucher']
                        )

                        self.add(draftVoucher3Product)

            get_sales_order = sales_order.query.get(sales_order_id)
            get_sales_order.total_kubikasi = total_kubikasi

            self.add(get_sales_order)
            self.flush()

        self.flush().commit()

        faktur_just_inserted = {
            "no_faktur": None,
            "id_sales_order": faktur_sales.id_sales_order,
            "status_faktur": faktur_sales.status_faktur,
            "jenis_faktur": faktur_sales.jenis_faktur,
            "subtotal_penjualan": faktur_sales.subtotal_penjualan,
            "subtotal_diskon": faktur_sales.subtotal_diskon,
            "total_penjualan": faktur_sales.total_penjualan,
            "total_dana_diterima": faktur_sales.total_dana_diterima,
            "pajak": faktur_sales.pajak
        }

        return jsonify(faktur_just_inserted)

    def __for_one_principal(self, id_plafon, products):
        # Kalkulasi total_order dari products.totalHarga all
        total_order = sum(produk["totalHarga"] for produk in products)

        draftSales = draft_sales(
            id_plafon=id_plafon,
            no_order=self.req("no_sales_order"),
            tanggal_order=self.req("tanggal_order"),
            # tanggal_jatuh_tempo=self.req(
            #     "tanggal_jatuh_tempo") or tanggal_jatuh_tempo,
            nama_sales=self.req("nama_sales"),
            status_order="0"
        )

        self.add(draftSales).flush()

        sales_order_id = draftSales.id

        is_periode_closed, next_date = self.check_is_periode_closed()
        tanggal_order = date_now()
        if is_periode_closed:
            tanggal_order = next_date.strftime("%Y-%m-%d")

        salesOrder = sales_order(
            id=sales_order_id,
            id_plafon=id_plafon,
            id_cabang=self.req("id_cabang"),
            no_order=self.req("no_sales_order"),
            tanggal_order=tanggal_order,
            # tanggal_jatuh_tempo=self.req(
            #     "tanggal_jatuh_tempo") or tanggal_jatuh_tempo,
            nama_sales=self.req("nama_sales"),
            status_order=0,
            total_order=total_order
        )

        self.add(salesOrder)

        # Faktur dibuat dengan no_faktur NULL
        faktur_sales = faktur(
            no_faktur=None,  # Set NULL dulu
            id_sales_order=sales_order_id,
            status_faktur=0,
            jenis_faktur='penjualan',
            subtotal_penjualan=total_order,
            subtotal_diskon=self.req("subtotal_diskon"),
            total_penjualan=self.req("total_penjualan"),
            total_dana_diterima=self.req("total_dana_diterima") or 0,
            pajak=self.req("pajak"),
            dpp=self.req("subtotal_penjualan")
        )

        self.add(faktur_sales)

        total_kubikasi = 0
        # Add products to the list of produks
        for produk in self.req("products"):
            # calculate total kubikasi
            curr_produk = produk_model.query.get(produk["id_produk"])
            kubikasi_per_pieces = curr_produk.kubikasiperpieces or 0
            kubikasi_per_box = curr_produk.kubikasiperbox or 0
            kubikasi_per_karton = curr_produk.kubikasiperkarton or 0

            kubikasi_pieces = kubikasi_per_pieces * \
                              produk["pieces_order"]
            kubikasi_box = kubikasi_per_box * produk["box_order"]
            kubikasi_karton = kubikasi_per_karton * \
                              produk["karton_order"]

            curr_total = kubikasi_pieces + kubikasi_box + kubikasi_karton
            total_kubikasi += curr_total

            salesOrderDetail = sales_order_detail(
                id_sales_order=sales_order_id,
                id_produk=produk["id_produk"],
                pieces_order=produk["pieces_order"],
                box_order=produk["box_order"],
                karton_order=produk["karton_order"],
                hargaorder=produk["harga_jual"],
                subtotalorder=produk["subtotalorder"],
                vouchers=produk["vouchers"],
                estimasi_kubikasi=curr_total,
                total_nilai_discount=produk['totalDiskon']
            )

            self.add(salesOrderDetail).flush()

            # add proses picking
            picking = proses_picking(
                id_order_detail=salesOrderDetail.id,
                id_produk=produk["id_produk"]
            )

            self.add(picking)

            if 'voucherSelections' in produk:
                # Voucher 1 Regular
                if 'voucher1Regular' in produk['voucherSelections'] and produk['voucherSelections'][
                    'voucher1Regular']:
                    voucher1Regular = produk['voucherSelections']['voucher1Regular']
                    diskon1Regular = produk['discountDetails'][
                        'diskon1Regular'] if 'discountDetails' in produk and 'diskon1Regular' in \
                                             produk['discountDetails'] else 0

                    draftVoucher1Regular = draft_voucher(
                        id_sales_order=sales_order_id,
                        id_sales_order_detail=salesOrderDetail.id,
                        id_voucher=voucher1Regular['id'],
                        tipe_voucher=1,
                        status_promo=0,
                        status_klaim=0,
                        jumlah_diskon=diskon1Regular,
                        kode_voucher=voucher1Regular['kode_voucher']
                    )

                    self.add(draftVoucher1Regular)

                # Voucher 2 Regular
                if 'voucher2Regular' in produk['voucherSelections'] and produk['voucherSelections'][
                    'voucher2Regular']:
                    voucher2Regular = produk['voucherSelections']['voucher2Regular']
                    diskon2Regular = produk['discountDetails'][
                        'diskon2Regular'] if 'discountDetails' in produk and 'diskon2Regular' in \
                                             produk['discountDetails'] else 0

                    draftVoucher2Regular = draft_voucher(
                        id_sales_order=sales_order_id,
                        id_sales_order_detail=salesOrderDetail.id,
                        id_voucher=voucher2Regular['id'],
                        tipe_voucher=2,
                        status_promo=0,
                        status_klaim=0,
                        jumlah_diskon=diskon2Regular,
                        kode_voucher=voucher2Regular['kode_voucher']
                    )

                    self.add(draftVoucher2Regular)

                # Voucher 3 Regular
                if 'voucher3Regular' in produk['voucherSelections'] and produk['voucherSelections'][
                    'voucher3Regular']:
                    voucher3Regular = produk['voucherSelections']['voucher3Regular']
                    diskon3Regular = produk['discountDetails'][
                        'diskon3Regular'] if 'discountDetails' in produk and 'diskon3Regular' in \
                                             produk['discountDetails'] else 0

                    draftVoucher3Regular = draft_voucher(
                        id_sales_order=sales_order_id,
                        id_sales_order_detail=salesOrderDetail.id,
                        id_voucher=voucher3Regular['id'],
                        tipe_voucher=3,
                        status_promo=0,
                        status_klaim=0,
                        jumlah_diskon=diskon3Regular,
                        kode_voucher=voucher3Regular['kode_voucher']
                    )

                    self.add(draftVoucher3Regular)

                # Voucher 2 Product
                if 'voucher2Product' in produk['voucherSelections'] and produk['voucherSelections'][
                    'voucher2Product']:
                    voucher2Product = produk['voucherSelections']['voucher2Product']
                    diskon2Product = produk['discountDetails'][
                        'diskon2Product'] if 'discountDetails' in produk and 'diskon2Product' in \
                                             produk['discountDetails'] else 0

                    draftVoucher2Product = draft_voucher(
                        id_sales_order=sales_order_id,
                        id_sales_order_detail=salesOrderDetail.id,
                        id_voucher=voucher2Product['id'],
                        tipe_voucher=2,  # Tetap menggunakan tipe_voucher=2 karena ini adalah voucher level 2
                        status_promo=0,
                        status_klaim=0,
                        jumlah_diskon=diskon2Product,
                        kode_voucher=voucher2Product['kode_voucher']
                    )

                    self.add(draftVoucher2Product)

                # Voucher 3 Product
                if 'voucher3Product' in produk['voucherSelections'] and produk['voucherSelections'][
                    'voucher3Product']:
                    voucher3Product = produk['voucherSelections']['voucher3Product']
                    diskon3Product = produk['discountDetails'][
                        'diskon3Product'] if 'discountDetails' in produk and 'diskon3Product' in \
                                             produk['discountDetails'] else 0

                    draftVoucher3Product = draft_voucher(
                        id_sales_order=sales_order_id,
                        id_sales_order_detail=salesOrderDetail.id,
                        id_voucher=voucher3Product['id'],
                        tipe_voucher=3,  # Tetap menggunakan tipe_voucher=3 karena ini adalah voucher level 3
                        status_promo=0,
                        status_klaim=0,
                        jumlah_diskon=diskon3Product,
                        kode_voucher=voucher3Product['kode_voucher']
                    )

                    self.add(draftVoucher3Product)

        get_sales_order = sales_order.query.get(sales_order_id)
        get_sales_order.total_kubikasi = total_kubikasi

        self.flush().commit()

        faktur_just_inserted = {
            "no_faktur": None,
            "id_sales_order": faktur_sales.id_sales_order,
            "status_faktur": faktur_sales.status_faktur,
            "jenis_faktur": faktur_sales.jenis_faktur,
            "subtotal_penjualan": faktur_sales.subtotal_penjualan,
            "subtotal_diskon": faktur_sales.subtotal_diskon,
            "total_penjualan": faktur_sales.total_penjualan,
            "total_dana_diterima": faktur_sales.total_dana_diterima,
            "pajak": faktur_sales.pajak
        }

        return jsonify(faktur_just_inserted)

    def __filtered_by_id_principal(self, data_products):
        data_filtered = {}
        for data_product in data_products:
            id_principal = data_product['id_principal']
            if id_principal not in data_filtered:
                data_filtered[id_principal] = []
            data_filtered[id_principal].append(data_product)
        return data_filtered


    @handle_error
    def SalesStockOpname(self):
        log_stockOpname = [
            {
                "id_sales": self.req("id_sales"),
                "id_principal": self.req("id_principal"),
                "id_customer": self.req("id_customer"),
                "id_produk": product["id_produk"],
                "pieces": product["pieces"],
                "box": product["box"],
                "karton": product["karton"],
            }
            for product in self.req("products")
        ]

        return (
            self.query()
            .setRawQuery(
                """
                    INSERT INTO log_stockopname_sales
                    (id_produk, id_sales, id_principal, id_customer, pieces, box, karton)
                    VALUES
                    (:id_produk, :id_sales, :id_principal, :id_customer, :pieces, :box, :karton)
                """
            )
            .bulkQuery(log_stockOpname)
            .result
        )

    @handle_error_rollback
    def salesSkipRequest(self):
        id_plafons = self.req("id_plafon")
        keterangan = self.req("keterangan")

        for id in id_plafons:
            add_sales_order = sales_order(id_plafon=id, status_order=-2, keterangan=keterangan)
            self.add(add_sales_order).flush()

        self.commit()

        return 'skip sales order', 200

    @handle_error
    def searchFaktur(self):
        id_plafon = self.req("id_plafon")
        search = self.req("search")
        status_faktur = self.req("status-faktur")
        array_id_plafon = to_array_string(id_plafon)

        fakturs = (
            self.query()
            .setRawQuery(
                f"""
                SELECT 
                sales_order.*,
                faktur.* 
                FROM sales_order
                JOIN faktur
                ON sales_order.id = faktur.id_sales_order
                WHERE 
                sales_order.id_plafon = any (array{array_id_plafon})
                AND faktur.no_faktur ILIKE '%{search}%'
                AND sales_order.status_order = {status_faktur or 6}
                AND faktur.jenis_faktur = 'penjualan'
            """
            )
            .execute()
            .fetchall()
            .get()
        )

        if not len(fakturs):
            return []

        for faktur in fakturs:
            faktur["products"] = (
                self.query()
                .setRawQuery(
                    """
                        SELECT * 
                        FROM sales_order_detail 
                        WHERE id_sales_order = :id_sales_order
                    """
                )
                .bindparams({"id_sales_order": faktur["id_sales_order"]})
                .execute()
                .fetchall()
                .get()
            )

            for fakturProduct in faktur["products"]:
                fakturProduct["produk"] = (
                    self.query()
                    .setRawQuery(
                        """
                            SELECT * 
                            FROM produk 
                            WHERE
                            id = :id_produk 
                        """
                    )
                    .bindparams({"id_produk": fakturProduct["id_produk"]})
                    .execute()
                    .fetchone()
                    .result
                )
                fakturProduct['konversi'] = (
                    self.query()
                    .setRawQuery(
                        """
                            SELECT * 
                            FROM produk_uom 
                            WHERE
                            id_produk = :id_produk 
                        """
                    )
                    .bindparams({"id_produk": fakturProduct["id_produk"]})
                    .execute()
                    .fetchall()
                    .get()
                )


        return fakturs

    @handle_error_rollback
    def createReturRequest(self):
        id_sales_order = self.req('id_sales_order')
        id_sales = self.req('id_sales')
        id_plafon = self.req('id_plafon')
        tanggal_retur_pengajuan = self.req('tanggal_retur_pengajuan')
        products = self.req('products')

        if not tanggal_retur_pengajuan:
            tanggal_retur_pengajuan = date_now()

        is_periode_closed, next_date = self.check_is_periode_closed()
        if is_periode_closed:
            tanggal_retur_pengajuan = next_date.strftime("%Y-%m-%d")

        if not id_sales_order or not id_sales or not id_plafon or not products:
            raise nonServerErrorException("ID Sales Order, ID Sales, ID Plafon, dan Products harus diisi")

        data_plafon = (
            self.db.session.query(plafon,
                                             principal,
                                             perusahaan.kode.label('kode_perusahan'))
                        .join(principal, plafon.id_principal == principal.id)
                          .join(perusahaan, principal.id_perusahaan == perusahaan.id)
                        .filter(plafon.id == id_plafon)
                        .first()
                       )
        if not data_plafon:
            raise nonServerErrorException(f"Plafon dengan ID {id_plafon} tidak ditemukan")
        plafon_data = data_plafon[0]  # instance model plafon
        principal_data = data_plafon[1]  # instance model principal
        kode_perusahaan = data_plafon[2]  # string kode dari perusahaan
        id_customer = plafon_data.id_customer
        id_principal = plafon_data.id_principal
        kode_perusahaan = kode_perusahaan

        prefix_kode_request = f"RT{kode_perusahaan}-"

        last_kode_request = (
            ReturRequest.query.filter(
                ReturRequest.kode_request.like(f"{prefix_kode_request}%")
            ).with_for_update().order_by(ReturRequest.kode_request.desc()).first()
        )

        if last_kode_request:
            last_kode = last_kode_request.kode_request
            last_number = int(last_kode.split('-')[-1])
            next_number = last_number + 1
        else:
            next_number = 1

        counter_str = f"{next_number:04d}"  # Format dengan 4 digit

        kode_request = f"{prefix_kode_request}{counter_str}"

        add_retur_request = ReturRequest(
            id_sales_order=id_sales_order,
            kode_request=kode_request,
            id_sales=id_sales,
            id_customer=id_customer,
            id_principal=id_principal,
            tanggal_request=tanggal_retur_pengajuan ,
            status_request=0,
        )

        self.add(add_retur_request).flush()

        datas_sales_order_detail = (
            self.query()
            .setRawQuery(
                """
                SELECT sod.pieces_delivered, sod.box_delivered, sod.karton_delivered, sod.id_produk, sod.id,
                       -- GROUP TO JSON DATA PRODUCT UOM
                       json_agg(
                               DISTINCT jsonb_build_object(
                               'id', produk_uom.id,
                               'level', produk_uom.level,
                               'faktor_konversi', produk_uom.faktor_konversi
                                        )
                       ) AS uom_list
                FROM sales_order_detail sod
                         JOIN produk_uom
                              ON sod.id_produk = produk_uom.id_produk
                WHERE id_sales_order = :id_sales_order
                GROUP BY sod.pieces_delivered, sod.box_delivered, sod.karton_delivered, sod.id_produk, sod.id                
                """
            ).bindparams(
                {"id_sales_order": id_sales_order}
            )
            .execute()
            .fetchall()
            .get()
        )

        if not datas_sales_order_detail:
            raise nonServerErrorException(f"Sales Order dengan ID {id_sales_order} tidak ditemukan atau tidak memiliki detail produk")

        for product in products:

            data_sales_order_detail = next((
                detail for detail in datas_sales_order_detail
                if detail['id_produk'] == product['id_produk']
            ), None)

            if not data_sales_order_detail:
                raise nonServerErrorException(f"Produk dengan ID {product['id_produk']} tidak ditemukan dalam Sales Order ini")

            data_retur = calculate_konversi(
                {
                    "pieces": product['pieces_retur_good'] + product['pieces_retur_bad'],
                    "box": product['box_retur_good'] + product['box_retur_bad'],
                    "karton": product['karton_retur_good'] + product['karton_retur_bad']
                },
                data_sales_order_detail['uom_list']
            )

            data_order = calculate_konversi(
                {
                    "pieces": data_sales_order_detail['pieces_delivered'],
                    "box": data_sales_order_detail['box_delivered'],
                    "karton": data_sales_order_detail['karton_delivered']
                },
                data_sales_order_detail['uom_list']
            )

            if data_retur['pieces'] > data_order['pieces']:
                raise nonServerErrorException(
                    f"Jumlah retur untuk produk {product['id_produk']} melebihi jumlah yang dipesan. "
                    f"Jumlah dipesan: {data_order['pieces']}, Jumlah retur: {data_retur['pieces']}"
                )

            add_retur_request_detail = ReturRequestDetail(
                id_request=add_retur_request.id_request,
                id_sales_order_detail=data_sales_order_detail['id'],
                id_produk=product['id_produk'],
                pieces_diajukan=product['pieces_retur_bad'],
                box_diajukan=product['box_retur_bad'],
                karton_diajukan=product['karton_retur_bad'],
                alasan_retur=product['keterangan_retur'],
                harga_satuan=product['harga_satuan'],
                pieces_retur=product['pieces_retur_bad'] + product['pieces_retur_good'],
                box_retur=product['box_retur_bad'] + product['box_retur_good'],
                karton_retur=product['karton_retur_bad'] + product['karton_retur_good'],
                pieces_good_diajukan=product['pieces_retur_good'],
                box_good_diajukan=product['box_retur_good'],
                karton_good_diajukan=product['karton_retur_good'],
            )

            self.add(add_retur_request_detail).flush()

        self.commit()

        return {"status": "success","message": "Request retur berhasil dibuat"}, 200

    @handle_error
    def checkReturRequest(self):
        id_sales_order = self.req('id_sales_order')

        if not id_sales_order:
            raise nonServerErrorException("ID Sales Order harus diisi")

        retur_request = self.query().setRawQuery(
            """
                SELECT *
                FROM retur_request
                    JOIN retur_request_detail 
                         ON
                             retur_request.id_request = retur_request_detail.id_request
                WHERE id_sales_order = :id_sales_order
            """
        ).bindparams({"id_sales_order": id_sales_order}).execute().fetchall().get()

        if not retur_request:
            return {"status": "not_found", "message": "Tidak ada request retur untuk sales order ini"}, 404

        return retur_request


    def __createNotaRetur(self):
        self.query().setRawQuery(
            """
                    UPDATE 
                    faktur 
                    SET 
                    perubahan_ke = :perubahan_ke 
                    WHERE id = :id
                """
        ).bindparams(
            {
                "id": self.req("id"),
                "perubahan_ke": 1,
            }
        ).execute()

        self.query().setRawQuery(
            """
                    UPDATE sales_order
                    SET status_order = 8
                    WHERE id = :id_sales_order
                """
        ).bindparams({
            "id_sales_order": self.req("id_sales_order")
        }).execute()

        (
            self.query()
            .setRawQuery(
                """
                    INSERT INTO 
                    faktur
                    (no_faktur, id_sales_order, status_faktur, jenis_faktur, total_penjualan, 
                    total_dana_diterima, tanggal_retur_pengajuan)
                    VALUES
                    (:no_faktur, :id_sales_order, :status_faktur, 'retur', :total_penjualan, 
                    :total_dana_diterima, :tanggal_retur_pengajuan)
                """
            )
            .bindparams(
                {
                    "no_faktur": self.req("no_faktur"),
                    "id_sales_order": self.req("id_sales_order"),
                    "total_penjualan": self.req("total_penjualan"),
                    "status_faktur": 0,
                    "total_dana_diterima": self.req("total_dana_diterima") or 0,
                    "tanggal_retur_pengajuan": date_now()
                }
            )
            .execute()
        )

        for product in self.req("products"):
            self.query().setRawQuery(
                """
                        UPDATE sales_order_detail 
                        SET 
                        pieces_retur = :pieces_retur,
                        box_retur = :box_retur,
                        karton_retur = :karton_retur,
                        keterangan_retur = :keterangan_retur
                        WHERE id = :id_sales_order_detail
                    """
            ).bindparams(
                {
                    "id_sales_order_detail": product["id_sales_order_detail"],
                    "pieces_retur": product["pieces_retur"],
                    "box_retur": product["box_retur"],
                    "karton_retur": product["karton_retur"],
                    "keterangan_retur": product["keterangan_retur"],
                }
            ).execute()

        return "success"

    @handle_error
    def lewatiSalesOrder(self):
        return (
            self.query().setRawQuery(
                """
                    INSERT INTO draft_sales 
                    (id_plafon, keterangan) 
                    VALUES
                    (:id_plafon, :keterangan)
                    RETURNING id
                """
            ).bindparams({
                "id_plafon": self.req("id_plafon"),
                "keterangan": self.req("keterangan")
            }).execute().getReturning()
        )