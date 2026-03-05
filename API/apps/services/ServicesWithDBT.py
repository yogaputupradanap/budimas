from apps import native_db
from flask import request, abort
from apps.models import (
    sales_order,
    draft_sales,
    voucher_1,
    voucher_2,
    voucher_3,
    draft_voucher,
    draft_voucher_2,
    sales_order_detail,
    faktur,
    produk as produk_model,
    proses_picking
)
from apps.query import DB
from apps.helper import date_now_stamp, time_now_stamp, parseJson
from datetime import datetime, timedelta


def req(param): return parseJson(request).json(param)


def SalesRequestWithDBT():
    current_date = datetime.now()
    tanggal_jatuh_tempo = (
        current_date + timedelta(days=10)).strftime("%Y-%m-%d")

    plafon = (
        DB()
        .setRawQuery(
            """
            SELECT id_sales, id_principal, id_customer FROM plafon WHERE id = :id_plafon
        """
        )
        .bindparams({"id_plafon": req("id_plafon")})
        .execute()
        .fetchall()
        .get()
    )

    no_sales_order = f"NR-{date_now_stamp()}{plafon[0]['id_sales']}{plafon[0]['id_principal']}{plafon[0]['id_customer']}"
    no_faktur = f"NF-{date_now_stamp()}{plafon[0]['id_sales']}{plafon[0]['id_principal']}{plafon[0]['id_customer']}-{time_now_stamp()}"

    try:
        draftSales = draft_sales(
            id_plafon=req("id_plafon"),
            no_order=req("no_sales_order") or no_sales_order,
            tanggal_order=req("tanggal_order"),
            tanggal_jatuh_tempo=req(
                "tanggal_jatuh_tempo") or tanggal_jatuh_tempo,
            nama_sales=req("nama_sales"),
            status_order="0"
        )

        native_db.session.add(draftSales)
        native_db.session().flush()

        sales_order_id = draftSales.id

        salesOrder = sales_order(
            id=sales_order_id,
            id_plafon=req("id_plafon"),
            no_order=req("no_sales_order") or no_sales_order,
            tanggal_order=req("tanggal_order"),
            tanggal_jatuh_tempo=req(
                "tanggal_jatuh_tempo") or tanggal_jatuh_tempo,
            nama_sales=req("nama_sales"),
            status_order=0
        )

        native_db.session.add(salesOrder)

        faktur_sales = faktur(
            no_faktur=no_faktur,
            id_sales_order=sales_order_id,
            status_faktur=0,
            jenis_faktur='penjualan',
            subtotal_penjualan=req("subtotal_penjualan"),
            subtotal_diskon=req("subtotal_diskon"),
            total_penjualan=req("total_penjualan"),
            total_dana_diterima=req("total_dana_diterima") or 0,
            pajak=req("pajak")
        )

        native_db.session.add(faktur_sales)

        if len(req("kode_vouchers")):
            for voucher in req("kode_vouchers"):

                voucher_table = int(voucher["kode_voucher"][len(
                    voucher["kode_voucher"]) - 1])

                voucher_object = (
                    voucher_1
                    if voucher_table == 1
                    else (
                        voucher_2
                        if voucher_table == 2
                        else (
                            voucher_3
                            if voucher_table == 3
                            else None
                        )
                    )
                )

                budgetDiskon = native_db.session.query(
                    voucher_object.budget_diskon
                ).filter_by(
                    kode_voucher=voucher["kode_voucher"]
                ).scalar()
                
                # if budgetDiskon <= voucher["nilai_diskon"] : return
                        
                draftVoucher = draft_voucher(
                    id_sales_order=sales_order_id,
                    id_voucher=voucher["id"],
                    discount=voucher["diskon"] if "diskon" in voucher else 0,
                    jumlah_diskon=voucher["nilai_diskon"] if "nilai_diskon" in voucher else 0,
                    kode_voucher=voucher["kode_voucher"]
                )

                # updateVoucher = voucher_object.query.get(voucher["id"])
                # updateVoucher.budget_diskon = budgetDiskon - \
                #     int(voucher["nilai_diskon"])

                # native_db.session().flush()
                native_db.session.add(draftVoucher)

        
        total_kubikasi = 0
        for produk in req("products"):

            # calculate total kubikasi
            curr_produk = produk_model.query.get(produk["id_produk"])

            kubikasi_pieces = curr_produk.kubikasiperpieces * \
                produk["pieces_order"]
            kubikasi_box = curr_produk.kubikasiperbox * produk["box_order"]
            kubikasi_karton = curr_produk.kubikasiperkarton * \
                produk["karton_order"]

            curr_total = kubikasi_pieces + kubikasi_box + kubikasi_karton
            total_kubikasi += curr_total

            salesOrderDetail = sales_order_detail(
                id_sales_order=sales_order_id,
                id_produk=produk["id_produk"],
                pieces_order=produk["pieces_order"],
                box_order=produk["box_order"],
                karton_order=produk["karton_order"],
                subtotalorder=produk["subtotalorder"],
                vouchers=produk["vouchers"]
            )

            native_db.session.add(salesOrderDetail)
            native_db.session().flush()

            # add proses picking
            picking = proses_picking(
                id_order_detail=salesOrderDetail.id,
                id_produk=produk["id_produk"]
            )

            native_db.session.add(picking)

            if len(produk["vouchers"]):
                for voucher in produk["vouchers"]:
                    voucher_table = int(
                        voucher["kode"][len(voucher["kode"]) - 1])
                    voucher_object = (
                        voucher_1
                        if voucher_table == 1
                        else (
                            voucher_2
                            if voucher_table == 2
                            else (
                                voucher_3
                                if voucher_table == 3
                                else None
                            )
                        )
                    )

                    budgetDiskon = native_db.session.query(
                        voucher_object.budget_diskon
                    ).filter_by(
                        kode_voucher=voucher["kode"]
                    ).scalar()
                    
                    # if budgetDiskon <= voucher["nilai_diskon"]: return
                    
                    draftVoucher2 = draft_voucher_2(
                        id_detail_sales=salesOrderDetail.id,
                        id_voucher=voucher["id"],
                        status_klaim=0,
                        discount=voucher["diskon"] if "diskon" in voucher else 0,
                        jumlah_diskon=voucher["nilai_diskon"] if "nilai_diskon" in voucher else 0,
                        kode_voucher=voucher["kode"]
                    )

                    # updateVoucher = voucher_object.query.get(voucher["id"])
                    # updateVoucher.budget_diskon = budgetDiskon - \
                    #     int(voucher["nilai_diskon"])

                    # native_db.session().flush()
                    native_db.session.add(draftVoucher2)

        get_sales_order = sales_order.query.get(sales_order_id)
        get_sales_order.total_kubikasi = total_kubikasi

        native_db.session().flush()
        native_db.session.commit()

        print('success insert sales order')
        return faktur_sales

    except Exception as e:
        print(f"Rollback with error : {e}")
        native_db.session.rollback()
        return abort(500, description=str(e))
    finally:
        native_db.session.close()
