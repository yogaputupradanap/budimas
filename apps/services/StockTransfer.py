from flask import request, current_app

from . import BaseServices
from apps.models import stock_transfer, stock_transfer_detail, Stok, Cabang, ProdukUOM as ProdukUomModel, Produk, TipeTransaksi, LogInventory
from apps.services import ProdukUOM
from apps.handler import handle_error_rollback, handle_error, nonServerErrorException
from apps.lib.helper import date_now, to_array_string, time_now
import json
import bcrypt



## kenapa service pada class ini sedikit dibandingkan service distribusi ?, karena
## penyuplai data di frontend nya menggunakan "base" route di folder routes yaitu menggunakan
## utility bernama query dan paginate yang berada di folder lib

class StockTransfer(BaseServices):
    def getQuery(self, table, id_st, status):
        status_q = f"and stock_transfer.status = :status"

        query = (
            f"""
                select {table}.*,
                principal.nama as nama_principal,
                produk.nama as nama_produk,
                produk.kode_sku
                from stock_transfer
                join stock_transfer_detail
                on stock_transfer.id = stock_transfer_detail.id_stock_transfer
                join principal
                on stock_transfer_detail.id_principal = principal.id
                join produk
                on stock_transfer_detail.id_produk = produk.id
                where stock_transfer.id = :id
                {status_q if status else ''}
            """
        )

        bind = { "id": id_st }
        if status: bind['status'] = status

        return {"query": query, "bind": bind}

    @handle_error_rollback
    def getPengirimanStockTransfer(self):
        id_stock_transfers = self.req('id_stock_transfers')
        status_stock = self.req('status_stock')
        id_user = self.req('id_user')
        id_arr = to_array_string(id_stock_transfers)

        # Get current datetime
        current_date = date_now()
        current_time = time_now()

        # Get tipe_transaksi name for keterangan
        tipe_transaksi_query = f"SELECT * FROM tipe_transaksi WHERE id = 12"
        tipe_transaksi = self.query().setRawQuery(tipe_transaksi_query).execute().fetchone().result
        if not tipe_transaksi:
            raise Exception("Tipe transaksi with id 12 not found")

        penerimaan_query = f"""
            select * from stock_transfer
            where id = ANY (ARRAY{id_arr})
            order by created_at asc
        """
        penerimaan = self.query().setRawQuery(penerimaan_query).execute().fetchall().get()

        for i in penerimaan:
            # Skip if status already 2
            if i['status'] != 2:
                # Get stock_transfer_detail
                detail_query = f"""
                    SELECT * FROM stock_transfer_detail 
                    WHERE id_stock_transfer = {i['id']}
                """
                details = self.query().setRawQuery(detail_query).execute().fetchall().get()

                # Get cabang info for id_perusahaan
                cabang_query = f"""
                    SELECT * FROM cabang 
                    WHERE id = {i['id_cabang_awal']}
                """
                cabang_asal = self.query().setRawQuery(cabang_query).execute().fetchone().result
                if not cabang_asal:
                    raise Exception(f"Cabang asal with id {i['id_cabang_awal']} not found")

                for detail in details:
                    # Get product UOM with level 1
                    produk_uom_query = f"""
                        SELECT * FROM produk_uom 
                        WHERE id_produk = {detail['id_produk']} AND level = 1
                    """
                    produk_uom = self.query().setRawQuery(produk_uom_query).execute().fetchone().result
                    if not produk_uom:
                        raise Exception(f"Product UOM with level 1 not found for product id {detail['id_produk']}")

                    # Update stok at source branch
                    stok_query = f"""
                        SELECT * FROM stok 
                        WHERE cabang_id = {i['id_cabang_awal']} 
                        AND produk_id = {detail['id_produk']}
                    """
                    stok_asal = self.query().setRawQuery(stok_query).execute().fetchone().result

                    if stok_asal:
                        # Store initial stock for log_inventory
                        stok_awal = stok_asal['jumlah_ready']

                        # Update stock quantities
                        update_stok_query = f"""
                            UPDATE stok 
                            SET 
                                jumlah_delivery = jumlah_delivery + {detail['jumlah_picked']},
                                transfer_out = transfer_out + {detail['jumlah_picked']},
                                jumlah_booked = jumlah_booked - {detail['jumlah_picked']},
                                jumlah_gudang = jumlah_gudang - {detail['jumlah_picked']},
                                jumlah_picked = jumlah_picked - {detail['jumlah_picked']},
                                tanggal_update = '{current_date}',
                                waktu_update = '{current_time}'
                            WHERE cabang_id = {i['id_cabang_awal']} 
                            AND produk_id = {detail['id_produk']}
                        """
                        self.query().setRawQuery(update_stok_query).execute()

                        # Get product price for log_inventory
                        produk_query = f"SELECT * FROM produk WHERE id = {detail['id_produk']}"
                        produk_info = self.query().setRawQuery(produk_query).execute().fetchone().result
                        if not produk_info:
                            raise Exception(f"Product with id {detail['id_produk']} not found")

                        # Insert log_inventory
                        log_query = f"""
                            INSERT INTO log_inventory (
                                id_transaksi, id_cabang, id_perusahaan, id_transaksi_tipe,
                                id_produk, id_user, stok_awal, stok_peralihan, stok_akhir,
                                harga, tanggal, valuasi, waktu, keterangan, produk_uom_id
                            ) VALUES (
                                {i['id']}, {i['id_cabang_awal']}, {cabang_asal['id_perusahaan']},
                                12, {detail['id_produk']}, {id_user}, {stok_awal},
                                {-detail['jumlah_picked']}, {stok_awal - detail['jumlah_picked']},
                                {produk_info['harga_beli']}, '{current_date}', 0,
                                '{current_time}', '{tipe_transaksi['nama']}', {produk_uom['id']}
                            )
                        """
                        self.query().setRawQuery(log_query).execute()

                    # Update or insert stok at destination branch
                    stok_tujuan_query = f"""
                        SELECT * FROM stok 
                        WHERE cabang_id = {i['id_cabang_tujuan']} 
                        AND produk_id = {detail['id_produk']}
                    """
                    stok_tujuan = self.query().setRawQuery(stok_tujuan_query).execute().fetchone().result

                    if stok_tujuan:
                        # Update existing stock
                        update_tujuan_query = f"""
                            UPDATE stok 
                            SET 
                                jumlah_incoming = jumlah_incoming + {detail['jumlah_picked']},
                                tanggal_update = '{current_date}',
                                waktu_update = '{current_time}'
                            WHERE cabang_id = {i['id_cabang_tujuan']} 
                            AND produk_id = {detail['id_produk']}
                        """
                        self.query().setRawQuery(update_tujuan_query).execute()
                    else:
                        # Insert new stock record
                        insert_stok_query = f"""
                            INSERT INTO stok (
                                cabang_id, produk_id, jumlah_ready, jumlah_booked,
                                jumlah_delivery, jumlah_incoming, jumlah_gudang,
                                jumlah_canvas, jumlah_good, jumlah_bad,
                                tanggal_update, waktu_update, jumlah_picked,
                                transfer_out, transfer_in
                            ) VALUES (
                                {i['id_cabang_tujuan']}, {detail['id_produk']}, 0, 0,
                                0, {detail['jumlah_picked']}, 0, 0, 0, 0,
                                '{current_date}', '{current_time}', 0, 0, 0
                            )
                        """
                        self.query().setRawQuery(insert_stok_query).execute()

                # Update stock_transfer status
                update = {"id": int(i["id"]), "status": 2}
                print(f"Updating stock_transfer status to 2 for id {i['id']}")
                self.updateStatus(update)

            # Get products list (existing feature)
            i['listProduk'] = self.getStockOrderDetail(i['id'], status_stock)

            # Update product info (existing feature)
            for uom in i['listProduk']:
                prod_q = f"select * from produk where id = {uom['id_produk']}"
                prod = self.query().setRawQuery(prod_q).execute().fetchone().result

                uom['harga'] = prod['harga_beli']
                uom['jumlah_harga'] = (uom['jumlah_picked'] or 1) * prod['harga_beli']
                uom['kode_sku'] = prod['kode_sku']

        self.commit()
        print("Penerimaan: ", penerimaan)
        return penerimaan

    @handle_error
    def getStockOrderDetail(self, id = None, status = None):
        id_st = self.req("id") or id
        status = self.req("status") or status
        selected_uoms = self.req("select_jumlah") or "jumlah"

        std_query = self.getQuery('stock_transfer_detail', id_st, status)

        stock_transfer_detail = (
            self.query()
            .setRawQuery(std_query['query'])
            .bindparams(std_query['bind'])
            .execute()
            .fetchall()
            .get()
        )

        def with_uom(key):
            result = [
                {**std, "uom_1": 0,"uom_2": 0,"uom_3": std[key] if std[key] != None else 0}
                for std in stock_transfer_detail
            ]

            return result

        def spread_arr_obj(arr):
            result = [
                {**std, **arr[idx]}
                for idx, std in enumerate(stock_transfer_detail)
            ]

            return result

        with_uom_jumlah = with_uom("jumlah")
        with_uom_jumlah_diterima = with_uom("jumlah_diterima")
        with_uom_jumlah_picked = with_uom("jumlah_picked")
        with_uom_jumlah_ditolak = with_uom("jumlah_ditolak")

        std_uoms_jumlah = ProdukUOM().getUoms(with_uom_jumlah)
        std_uoms_jumlah_diterima = ProdukUOM().getUoms(with_uom_jumlah_diterima)
        std_uoms_jumlah_picked = ProdukUOM().getUoms(with_uom_jumlah_picked)
        std_uoms_jumlah_ditolak = ProdukUOM().getUoms(with_uom_jumlah_ditolak)

        result = {
            "jumlah": spread_arr_obj(std_uoms_jumlah),
            "jumlah_diterima": spread_arr_obj(std_uoms_jumlah_diterima),
            "jumlah_picked": spread_arr_obj(std_uoms_jumlah_picked),
            "jumlah_ditolak": spread_arr_obj(std_uoms_jumlah_ditolak)
        }

        return result[selected_uoms]

    @handle_error_rollback
    def addStockTransfer(self):
        nota_stock_transfer = self.req("nota_stock_transfer")
        id_cabang_awal = int(self.req("id_cabang_awal"))
        id_cabang_tujuan = int(self.req("id_cabang_tujuan"))

        products = self.req('products')

        def insert_product(id_stock_transfer, product):
            id_principal = product["id_principal"]
            convert_obj = {
                "id_produk": product["id_produk"],
                "uom_1": int(product['uom_1']),
                "uom_2": int(product['uom_2']),
                "uom_3": int(product['uom_3'])
            }

            jumlah_in_pieces = ProdukUOM().convertUom('pieces', convert_obj)

            add_std = stock_transfer_detail(
                id_stock_transfer   =   id_stock_transfer,
                id_principal        =   id_principal,
                id_produk           =   convert_obj["id_produk"],
                jumlah              =   int(jumlah_in_pieces)
            )

            self.add(add_std).flush()

        nama_cabang_awal = cabang.query.filter(cabang.id == id_cabang_awal).first()
        nama_cabang_tujuan = cabang.query.filter(cabang.id == id_cabang_tujuan).first()

        add_st = stock_transfer(
            nota_stock_transfer     =   nota_stock_transfer,
            id_cabang_awal          =   id_cabang_awal,
            id_cabang_tujuan        =   id_cabang_tujuan,
            nama_cabang_awal        =   nama_cabang_awal.nama,
            nama_cabang_tujuan      =   nama_cabang_tujuan.nama,
            status                  =   0,
            created_at              =   date_now()
        )

        self.add(add_st).flush()

        for product in products: insert_product(add_st.id, product)

        self.commit()

        return {'status': 'success'}, 200

    def updateStatus(self, data):
        update = stock_transfer.query.filter(stock_transfer.id == data["id"]).first()
        update.status = data["status"]
        if 'armada' in data:
            update.id_armada = data['armada']
        self.flush()

    @handle_error_rollback
    def konfirmasiRequest(self):
        products = self.req('products')
        data = {
            "id": int(self.req('id_stock_transfer')),
            "armada": self.req("armada"),
            "status": 1
        }

        self.updateStatus(data)

        # Update status dan armada di tabel stock_transfer
        for product in products:
            total_pieces = 0

            # Level 1: Cek uom1 atau pieces
            if 'uom1' in product and product['uom1']:
                total_pieces += product['uom1']
            else:
                total_pieces += product['pieces']

            # Level 2: Cek uom2 atau box
            uom_level2 = ProdukUomModel.query.filter(
                ProdukUomModel.id_produk == product['id_produk'],
                ProdukUomModel.level == 2
            ).first()

            if 'uom2' in product and product['uom2']:
                if uom_level2:
                    total_pieces += product['uom2'] * uom_level2.faktor_konversi
            else:
                if uom_level2:
                    total_pieces += product['box'] * uom_level2.faktor_konversi

            # Level 3: Cek uom3 atau carton
            uom_level3 = ProdukUomModel.query.filter(
                ProdukUomModel.id_produk == product['id_produk'],
                ProdukUomModel.level == 3
            ).first()

            if 'uom3' in product and product['uom3']:
                if uom_level3:
                    total_pieces += product['uom3'] * uom_level3.faktor_konversi
            else:
                if uom_level3:
                    total_pieces += product['carton'] * uom_level3.faktor_konversi

            # Update detail stock transfer
            update_detail = stock_transfer_detail.query.filter(
                stock_transfer_detail.id_stock_transfer == product['id_stock_transfer'],
                stock_transfer_detail.id_produk == product['id_produk']
            ).first()

            update_detail.jumlah_picked = int(total_pieces)
            
            # Update available stock qty when stock transfer is confirmed
            update_stok = stok.query.filter(
                stok.cabang_id == self.req('id_cabang_awal'),
                stok.produk_id == product['id_produk']
            ).first()
            
            if update_stok:
                if update_stok.jumlah_ready:
                    update_stok.jumlah_ready -= int(total_pieces)
                    update_stok.jumlah_booked += int(total_pieces)
                    
                update_stok.tanggal_update = date_now()
                update_stok.waktu_update = time_now()

            self.flush()

        self.commit()

        return {"status": "success"}, 200

    @handle_error_rollback
    def konfirmasiAdmin(self):
        print("Data: ", json.dumps(request.json, indent=4))
        products = self.req('products')
        data = {
            "id": int(self.req('id')),
            "pengambilan_oleh": self.req('pengambilan_oleh'),
            "tanggal_ambil": self.req('tanggal_ambil'),
            "products": self.req('products')
        }

        # 1. Update tabel stock_transfer
        update_transfer = stock_transfer.query.filter(
            stock_transfer.id == data['products'][0]['id_stock_transfer']
        ).first()

        if not update_transfer:
            return {"status": "error", "message": "Stock transfer tidak ditemukan"}, 404

        update_transfer.pengambilan_oleh = data['pengambilan_oleh']
        update_transfer.tanggal_ambil = data['tanggal_ambil']
        update_transfer.status = data['status'] if 'status' in data else 2

        # 2. Update jumlah_picked di tabel stock_transfer_detail dan stok
        for product in products:
            total_pieces = 0

            # Level 1: Cek uom1 atau pieces
            if 'uom1' in product and product['uom1']:
                total_pieces += product['uom1']
            else:
                total_pieces += product['pieces']

            # Level 2: Cek uom2 atau box
            uom_level2 = ProdukUomModel.query.filter(
                ProdukUomModel.id_produk == product['id_produk'],
                ProdukUomModel.level == 2
            ).first()

            if 'uom2' in product and product['uom2']:
                if uom_level2:
                    total_pieces += product['uom2'] * uom_level2.faktor_konversi
            else:
                if uom_level2:
                    total_pieces += product['box'] * uom_level2.faktor_konversi

            # Level 3: Cek uom3 atau carton
            uom_level3 = ProdukUomModel.query.filter(
                ProdukUomModel.id_produk == product['id_produk'],
                ProdukUomModel.level == 3
            ).first()

            if 'uom3' in product and product['uom3']:
                if uom_level3:
                    total_pieces += product['uom3'] * uom_level3.faktor_konversi
            else:
                if uom_level3:
                    total_pieces += product['carton'] * uom_level3.faktor_konversi

            # Update detail stock transfer
            update_detail = stock_transfer_detail.query.filter(
                stock_transfer_detail.id_stock_transfer == data['products'][0]['id_stock_transfer'],
            ).first()

            if not update_detail:
                return {"status": "error",
                        "message": f"Detail stock transfer untuk produk {product['id_produk']} tidak ditemukan"}, 404

            update_detail.jumlah_picked = int(total_pieces)

            # Update stok
            update_stok = stok.query.filter(
                stok.cabang_id == self.req('id_cabang_awal'),
                stok.produk_id == product['id_produk']
            ).first()

            update_stok.jumlah_picked += int(total_pieces)
            update_stok.jumlah_good -= int(total_pieces)
            update_stok.tanggal_update = date_now()
            update_stok.waktu_update = time_now()

            self.flush()

        self.commit()

        return {"status": "success"}, 200

    @handle_error_rollback
    def penerimaanBarang(self):
        with self.db.session.begin():

            token = request.headers.get('Authorization')
            if not token:
                raise nonServerErrorException("Token is required")
            token = token.replace('Bearer ', '')
            user = (
                self.query().setRawQuery(
                    """
                    SELECT users.id
                    FROM users
                    WHERE users.tokens = :token
                    """
                )
                .bindparams({'token': token})
                .execute()
                .fetchone()
                .result
            )

            # 1. Update stock_transfer
            stock_transfer_data = stock_transfer.query.filter(
                stock_transfer.id == int(self.req('id_stock_transfer'))
            ).first()

            stock_transfer_data.status = 3
            stock_transfer_data.tanggal_diterima = date_now()
            print(f"Stock transfer status updated to 3 for id {stock_transfer_data.id}")

            # Get data from request
            id_cabang_tujuan = self.req('id_cabang_tujuan')
            products = self.req('list_produk')
            id_user = self.req('id_user')

            # Get cabang data for id_perusahaan
            cabang_data = cabang.query.filter(
                cabang.id == id_cabang_tujuan
            ).first()

            # Get tipe transaksi name
            tipe_transaksi = TipeTransaksi.query.filter(
                TipeTransaksi.id == 12
            ).first()

            for product in products:
                # Convert UOM to pieces
                increment_value = self.konversiUom(product)
                print(f"Product {product['id_produk']} converted to {increment_value} pieces")

                # 2. Update stock_transfer_detail
                update_detail = stock_transfer_detail.query.filter(
                    stock_transfer_detail.id_stock_transfer == int(product['id_stock_transfer']),
                    stock_transfer_detail.id_produk == int(product['id_produk'])
                ).first()

                if update_detail:
                    update_detail.jumlah_diterima = increment_value
                    print(f"Stock transfer detail updated for product {product['id_produk']}")
                    if "keterangan" in product:
                        update_detail.keterangan = product['keterangan']
                        print(f"Keterangan updated for product {product['id_produk']}")

                # Get produk data for harga_beli
                produk_data = produk.query.filter(
                    produk.id == product['id_produk']
                ).first()

                # Get produk_uom level 1
                produk_uom_data = ProdukUomModel.query.filter(
                    ProdukUomModel.id_produk == product['id_produk'],
                    ProdukUomModel.level == 1
                ).first()
                
                # Update source warehouse stock (reduce jumlah_delivery)
                source_stock = stok.query.filter(
                    stok.cabang_id == stock_transfer_data.id_cabang_awal,
                    stok.produk_id == product['id_produk']
                ).first()
                
                if source_stock:
                    source_stock.jumlah_delivery = (source_stock.jumlah_delivery or 0) - increment_value
                    source_stock.tanggal_update = date_now()
                    source_stock.waktu_update = time_now()
                    print(f"Source warehouse stock updated - reduced jumlah_delivery by {increment_value}")

                # Get existing stok
                existing_stok = stok.query.filter(
                    stok.cabang_id == id_cabang_tujuan,
                    stok.produk_id == product['id_produk']
                ).first()

                # Prepare log data
                log_inventory = LogInventory()
                log_inventory.id_transaksi = int(product['id_stock_transfer'])
                log_inventory.id_cabang = id_cabang_tujuan
                log_inventory.id_perusahaan = cabang_data.id_perusahaan
                log_inventory.id_transaksi_tipe = 12
                log_inventory.id_produk = product['id_produk']
                log_inventory.id_user = id_user
                log_inventory.stok_awal = existing_stok.jumlah_ready if existing_stok else 0
                log_inventory.stok_peralihan = increment_value
                log_inventory.stok_akhir = (existing_stok.jumlah_ready if existing_stok else 0) + increment_value
                log_inventory.harga = produk_data.harga_beli
                log_inventory.tanggal = date_now()
                log_inventory.valuasi = 0
                log_inventory.waktu = time_now()
                log_inventory.keterangan = tipe_transaksi.nama
                log_inventory.produk_uom_id = produk_uom_data.id if produk_uom_data else None

                self.add(log_inventory)
                self.flush()
                print(f"Log inventory added for product {product['id_produk']} and cabang {id_cabang_tujuan}")

                # Update existing stok or create new
                if existing_stok:
                    if existing_stok.jumlah_incoming:
                        existing_stok.jumlah_incoming -= increment_value

                    existing_stok.jumlah_ready = (existing_stok.jumlah_ready or 0) + increment_value
                    existing_stok.jumlah_gudang = (existing_stok.jumlah_gudang or 0) + increment_value
                    existing_stok.jumlah_good = (existing_stok.jumlah_good or 0) + increment_value
                    existing_stok.transfer_in = (existing_stok.transfer_in or 0) + increment_value
                    existing_stok.tanggal_update = date_now()
                    existing_stok.waktu_update = time_now()

                    print(f"Existing stok updated for product {product['id_produk']} and cabang {id_cabang_tujuan}")
                else:
                    new_stok = stok()
                    new_stok.produk_id = product['id_produk']
                    new_stok.cabang_id = id_cabang_tujuan
                    new_stok.jumlah_ready = increment_value
                    new_stok.jumlah_gudang = increment_value
                    new_stok.jumlah_good = increment_value
                    new_stok.transfer_in = increment_value
                    new_stok.tanggal_update = date_now()
                    new_stok.waktu_update = time_now()
                    new_stok.jumlah_booked = 0
                    new_stok.jumlah_delivery = 0
                    new_stok.jumlah_incoming = 0
                    new_stok.jumlah_canvas = 0
                    new_stok.jumlah_bad = 0
                    new_stok.jumlah_picked = 0
                    new_stok.transfer_out = 0

                    self.add(new_stok)
                    self.flush()
                    print(f"New stok added for product {product['id_produk']} and cabang {id_cabang_tujuan}")

            profile = self.query().setRawQuery("""
                                               SELECT p.id_perusahaan, p.id
                                               FROM stock_transfer st
                                                        JOIN stock_transfer_detail std ON std.id_stock_transfer = st.id
                                                        JOIN principal p ON std.id_principal = p.id
                                               WHERE st.id = :id_stock_transfer
                                               LIMIT 1
                                               """).bindparams(
                {"id_stock_transfer": self.req("id_stock_transfer")}).execute().fetchone().result

            payload_pubsub = {
                "id_fitur_mal": 9,
                "id_stock_transfer": self.req("id_stock_transfer"),
                "created_by": user.get('id'),
                "id_principal" : profile['id'] ,
                "id_cabang": stock_transfer_data.id_cabang_tujuan,
                "id_perusahaan": profile['id_perusahaan'] if profile else None
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

            print("Commit success")

            self.commit()




        return {"status": "success"}, 200

    @handle_error_rollback
    def closeEskalasiPenerimaanBarang(self):
        with self.db.session.begin():

            token = request.headers.get('Authorization')
            if not token:
                raise nonServerErrorException("Token is required")
            token = token.replace('Bearer ', '')
            user = (
                self.query().setRawQuery(
                    """
                    SELECT users.id
                    FROM users
                    WHERE users.tokens = :token
                    """
                )
                .bindparams({'token': token})
                .execute()
                .fetchone()
                .result
            )

            # 1. Update stock_transfer
            stock_transfer_data = stock_transfer.query.filter(
                stock_transfer.id == int(self.req('id_stock_transfer'))
            ).first()

            stock_transfer_data.status = 3
            stock_transfer_data.tanggal_diterima = date_now()
            print(f"Stock transfer status updated to 3 for id {stock_transfer_data.id}")

            # Get data from request
            id_cabang_tujuan = self.req('id_cabang_tujuan')
            products = self.req('list_produk')
            id_user = self.req('id_user')

            # Get cabang data for id_perusahaan
            cabang_data = cabang.query.filter(
                cabang.id == id_cabang_tujuan
            ).first()

            # Get tipe transaksi name
            tipe_transaksi = TipeTransaksi.query.filter(
                TipeTransaksi.id == 12
            ).first()

            for product in products:
                # Convert UOM to pieces
                increment_value = self.konversiUom(product)
                print(f"Product {product['id_produk']} converted to {increment_value} pieces")

                # 2. Update stock_transfer_detail
                update_detail = stock_transfer_detail.query.filter(
                    stock_transfer_detail.id_stock_transfer == int(product['id_stock_transfer']),
                    stock_transfer_detail.id_produk == int(product['id_produk'])
                ).first()

                if update_detail:
                    update_detail.jumlah_diterima = increment_value
                    print(f"Stock transfer detail updated for product {product['id_produk']}")
                    if "keterangan" in product:
                        update_detail.keterangan = product['keterangan']
                        print(f"Keterangan updated for product {product['id_produk']}")

                # Get produk data for harga_beli
                produk_data = produk.query.filter(
                    produk.id == product['id_produk']
                ).first()

                # Get produk_uom level 1
                produk_uom_data = ProdukUomModel.query.filter(
                    ProdukUomModel.id_produk == product['id_produk'],
                    ProdukUomModel.level == 1
                ).first()

                # Update source warehouse stock (reduce jumlah_delivery)
                source_stock = stok.query.filter(
                    stok.cabang_id == stock_transfer_data.id_cabang_awal,
                    stok.produk_id == product['id_produk']
                ).first()

                if source_stock:
                    source_stock.jumlah_delivery = (source_stock.jumlah_delivery or 0) - increment_value
                    source_stock.tanggal_update = date_now()
                    source_stock.waktu_update = time_now()
                    print(f"Source warehouse stock updated - reduced jumlah_delivery by {increment_value}")

                # Get existing stok
                existing_stok = stok.query.filter(
                    stok.cabang_id == id_cabang_tujuan,
                    stok.produk_id == product['id_produk']
                ).first()

                # Prepare log data
                log_inventory = LogInventory()
                log_inventory.id_transaksi = int(product['id_stock_transfer'])
                log_inventory.id_cabang = id_cabang_tujuan
                log_inventory.id_perusahaan = cabang_data.id_perusahaan
                log_inventory.id_transaksi_tipe = 12
                log_inventory.id_produk = product['id_produk']
                log_inventory.id_user = id_user
                log_inventory.stok_awal = existing_stok.jumlah_ready if existing_stok else 0
                log_inventory.stok_peralihan = increment_value
                log_inventory.stok_akhir = (existing_stok.jumlah_ready if existing_stok else 0) + increment_value
                log_inventory.harga = produk_data.harga_beli
                log_inventory.tanggal = date_now()
                log_inventory.valuasi = 0
                log_inventory.waktu = time_now()
                log_inventory.keterangan = tipe_transaksi.nama
                log_inventory.produk_uom_id = produk_uom_data.id if produk_uom_data else None

                self.add(log_inventory)
                self.flush()
                print(f"Log inventory added for product {product['id_produk']} and cabang {id_cabang_tujuan}")

                # Update existing stok or create new
                if existing_stok:
                    if existing_stok.jumlah_incoming:
                        existing_stok.jumlah_incoming -= increment_value

                    existing_stok.jumlah_ready = (existing_stok.jumlah_ready or 0) + increment_value
                    existing_stok.jumlah_gudang = (existing_stok.jumlah_gudang or 0) + increment_value
                    existing_stok.jumlah_good = (existing_stok.jumlah_good or 0) + increment_value
                    existing_stok.transfer_in = (existing_stok.transfer_in or 0) + increment_value
                    existing_stok.tanggal_update = date_now()
                    existing_stok.waktu_update = time_now()

                    print(f"Existing stok updated for product {product['id_produk']} and cabang {id_cabang_tujuan}")
                else:
                    new_stok = stok()
                    new_stok.produk_id = product['id_produk']
                    new_stok.cabang_id = id_cabang_tujuan
                    new_stok.jumlah_ready = increment_value
                    new_stok.jumlah_gudang = increment_value
                    new_stok.jumlah_good = increment_value
                    new_stok.transfer_in = increment_value
                    new_stok.tanggal_update = date_now()
                    new_stok.waktu_update = time_now()
                    new_stok.jumlah_booked = 0
                    new_stok.jumlah_delivery = 0
                    new_stok.jumlah_incoming = 0
                    new_stok.jumlah_canvas = 0
                    new_stok.jumlah_bad = 0
                    new_stok.jumlah_picked = 0
                    new_stok.transfer_out = 0

                    self.add(new_stok)
                    self.flush()
                    print(f"New stok added for product {product['id_produk']} and cabang {id_cabang_tujuan}")

            profile = self.query().setRawQuery("""
                                               SELECT p.id_perusahaan, p.id
                                               FROM stock_transfer st
                                                        JOIN stock_transfer_detail std ON std.id_stock_transfer = st.id
                                                        JOIN principal p ON std.id_principal = p.id
                                               WHERE st.id = :id_stock_transfer
                                               LIMIT 1
                                               """).bindparams(
                {"id_stock_transfer": self.req("id_stock_transfer")}).execute().fetchone().result

            payload_pubsub = {
                "id_fitur_mal": 10,
                "id_stock_transfer": self.req("id_stock_transfer"),
                "created_by": user.get('id'),
                "id_principal": profile['id'],
                "id_cabang": stock_transfer_data.id_cabang_tujuan,
                "id_perusahaan": profile['id_perusahaan'] if profile else None
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

            self.commit()

            print("Commit success")



        return {"status": "success"}, 200

    @handle_error_rollback
    def tolakPenerimaan(self):
        id_cabang_awal = self.req('id_cabang_awal')
        products = self.req('list_produk')

        data = {
            "id": int(self.req("id_stock_transfer")),
            "status": -2
        }

        self.updateStatus(data)

        for product in products:
            jumlah_pieces = int(ProdukUOM().convertUom('pieces', product))

            update_detail = stock_transfer_detail.query.filter(
                stock_transfer_detail.id_stock_transfer == int(product['id_stock_transfer']),
                stock_transfer_detail.id_produk == int(product['id_produk'])
            ).first()

            update_stok = stok.query.filter(
                stok.cabang_id == id_cabang_awal,
                stok.produk_id == product['id_produk']
            ).first()

            jumlah_gudang_temp = update_stok.jumlah_gudang
            transfer_out_temp = update_stok.transfer_out

            update_detail.jumlah_ditolak = jumlah_pieces

            if "keterangan" in product :
                update_detail.keterangan = product['keterangan']

            if jumlah_gudang_temp != None:
                update_stok.jumlah_gudang = jumlah_gudang_temp + jumlah_pieces
            else:
                update_stok.jumlah_gudang = jumlah_pieces

            if transfer_out_temp != None:
                update_stok.transfer_out = transfer_out_temp - jumlah_pieces
            else:
                update_stok.transfer_out = jumlah_pieces

            self.flush()

        self.commit()

        return {"status": "success"}, 200

    @handle_error
    def get_stock_transfer_info(self):
        email = self.req("email")
        password = self.req("password")
        query = """
            select
            users.tokens AS token,
            users.id AS id_user,
            users.nama AS nama_user,
            users.email AS user_email,
            users.id_jabatan,
            users.id_cabang,
            users.password
            from users
            where
            email = :email
            and
            id_jabatan in (7, 8, 9, 10, 2)
        """
        
        if email in self.super_user_email:
            query = self.super_user_query
            
        user_info = (
            self.query().setRawQuery(query)
            .bindparams({"email": email}).execute()
            .fetchone().result
        )

        if not len(user_info):
            raise nonServerErrorException("Email salah atau tidak ada")

        if not bcrypt.checkpw(password.encode('utf-8'), user_info["password"].encode('utf-8')):
            raise nonServerErrorException('Password salah', 403)

        return user_info

    def konversiUom(self, product):
        """
        Convert UOM to pieces based on level from produk_uom table
        """
        # Get conversion factors from produk_uom
        produk_uom_data = ProdukUomModel.query.filter(
            ProdukUomModel.id_produk == product['id_produk']
        ).all()

        # Create dictionary of conversion factors by level
        conversion_factors = {uom.level: uom.faktor_konversi for uom in produk_uom_data}

        # Calculate total pieces
        level1 = int(product['uom_1']) * (conversion_factors.get(1) or 1)
        level2 = int(product['uom_2']) * (conversion_factors.get(2) or 1)
        level3 = int(product['uom_3']) * (conversion_factors.get(3) or 1)

        return int(level1 + level2 + level3)