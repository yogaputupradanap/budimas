from apps.handler import handle_error
from flask import abort, request
import bcrypt

from apps.services import BaseServices
from apps.lib.helper import (
    date_now, 
    extract_data, 
    query_with_filters, 
    format_result_response,
    format_paginated_response, 
)

class SalesCanvas(BaseServices):
    def __init__(self):
        super().__init__()
     
    @handle_error
    def get_token_by_credential(self):
        email = self.req('email')
        password = self.req('password')
        
        baseQuery = """
            SELECT
                users.tokens AS token,
                users.id AS id_user,
                users.nama AS nama_user,    
                users.email AS user_email,
                users.id_jabatan,
                users.password
            FROM users
            JOIN sales ON users.id = sales.id_user
            WHERE users.email = :email
            AND users.id_jabatan IN (22)
        """
        
        loginBindParam = { "email": email }
        user = self._fetching(baseQuery, loginBindParam, fetch_type="one")

        # print(user)
            
        if not user:
            abort(401, "Email atau password salah")

        password_bytes = password.encode('utf-8')
        stored_hash = user['password'].encode('utf-8') if isinstance(user['password'], str) else user['password']
        
        if not bcrypt.checkpw(password_bytes, stored_hash):
            abort(401, "Password salah")
        
        return user

    # Base method to handle raw query execution
    def _fetching(self, query, params, fetch_type=None, with_result=True):
        execution = (
            self.query().setRawQuery(query)
            .bindparams(params).execute()
        )
        
        if fetch_type is None:
            return execution

        fetch_methods = { "all": 'fetchall', "one": 'fetchone' }
        fetch_method = fetch_methods.get(fetch_type, 'fetchall')
        fetched = getattr(execution, fetch_method)()

        if hasattr(fetched, 'result'):
            return fetched.result if with_result else fetched
        
        return fetched
   
    # Update Quantity stock based on status 
    def update_stock(self, id_produk, qty, status):
        qty = int(qty)
        
        if status == 1: # Requested
            query = """
                UPDATE stok 
                SET jumlah_ready = jumlah_ready - :qty,
                    jumlah_booked = jumlah_booked + :qty
                WHERE produk_id = :id_produk
            """
            self._fetching(query, { "qty": qty, "id_produk": id_produk })
        elif status == 2: # Approve
            query = """
                UPDATE stok 
                SET jumlah_good = jumlah_good - :qty,
                    jumlah_booked = jumlah_booked - :qty
                WHERE produk_id = :id_produk
            """
            self._fetching(query, { "qty": qty, "id_produk": id_produk })
            
            insert_stock_canvas = """
                INSERT INTO stock_canvas (id_produk, stock_canvas)
                VALUES (:id_produk, :qty)
                ON CONFLICT (id_produk) 
                DO UPDATE SET 
                    stock_canvas = stock_canvas.stock_canvas + EXCLUDED.stock_canvas,
                    id_sales = EXCLUDED.id_sales
            """
            
            self._fetching(insert_stock_canvas, { "qty": qty, "id_produk": id_produk })
    
    # Get Product with UOM and Stock Info
    @handle_error
    def _getProductWithUOM(self, id_produk):
        produk_query = """
            SELECT
                p.harga_beli,
                p.ppn as ppn,
                p.nama as nama_produk,
                pu1.nama as uom1_nama,
                COALESCE(pu1.faktor_konversi, 1) as uom1_factor,
                COALESCE(pu2.faktor_konversi, 1) as uom2_factor,
                COALESCE(pu3.faktor_konversi, 1) as uom3_factor,
                COALESCE(st.jumlah_ready, 0) as stock_gudang
            FROM produk p
            LEFT JOIN produk_uom pu1 ON p.id = pu1.id_produk AND pu1.level = 1
            LEFT JOIN produk_uom pu2 ON p.id = pu2.id_produk AND pu2.level = 2  
            LEFT JOIN produk_uom pu3 ON p.id = pu3.id_produk AND pu3.level = 3
            LEFT JOIN stok st ON st.produk_id = p.id
            WHERE p.id = :id_produk
        """
        
        produk_data = query_with_filters(
            self, produk_query, {"id_produk": id_produk},
            raw_data=True
        )
        
        if not produk_data:
            abort(404, "Produk tidak ditemukan")
        
        return produk_data[0]
    
    # Calculate UOM Pricing and Quantity
    @handle_error
    def _calculateUOMPricing(self, produk_data, qty_uom1, qty_uom2, qty_uom3):
        harga_beli = produk_data.get('harga_beli') or 0
        uom1_factor = produk_data.get('uom1_factor') or 1
        uom2_factor = produk_data.get('uom2_factor') or 1
        uom3_factor = produk_data.get('uom3_factor') or 1
        
        # Konversi ke pieces
        qty_request = (qty_uom1 * uom1_factor) + (qty_uom2 * uom2_factor) + (qty_uom3 * uom3_factor)
        harga_per_pieces = harga_beli * uom1_factor
        total_permintaan = qty_request * harga_per_pieces
        
        return {
            "uom1_factor": uom1_factor,
            "uom2_factor": uom2_factor,
            "uom3_factor": uom3_factor,
            "qty_request": qty_request,
            "harga_per_pieces": harga_per_pieces,
            "total_permintaan": total_permintaan,
        }
    
    # Get Sales and Principal by User
    @handle_error
    def getSalesAndPrincipalByUser(self, id_user: int):    
        query = """
            SELECT
                s.id as sales_id,
                s.id_principal,
                u.id_cabang,
                u.nama as nama_sales
            FROM sales s
            JOIN users u ON s.id_user = u.id
            WHERE u.id = :id_user
        """
        
        result = self._fetching(query, { "id_user": id_user }, fetch_type="one")
        return result if result else None
    
    # Get Stock Canvas
    def getStockCanvas(self, id_produk, id_sales):
        query = """
            SELECT stock_canvas
            FROM stock_canvas
            WHERE id_produk = :id_produk AND id_sales = :id_sales
        """
        result = self._fetching(query, { 
            "id_produk": id_produk, 
            "id_sales": id_sales 
        }, fetch_type="one")

        if not result:
            return 0
        if isinstance(result, (list, tuple)):
            return result[0]
        if hasattr(result, "stock_canvas"):
            return result.stock_canvas
        if isinstance(result, dict):
            return result.get("stock_canvas", 0)
        if isinstance(result, int):
            return result
        return 0

    @handle_error
    def getAllCanvasRequest(self):
        id_user = request.args.get('id_user') or self.req('id_user')
        print(f"DEBUG BACKEND: id_user dari URL adalah {id_user}")
        
        
        sales_result = self.getSalesAndPrincipalByUser(id_user)
        if not sales_result: 
            abort(404, "Data sales tidak ditemukan")
        
        sales_query = """ SELECT plafon_limit FROM sales WHERE id = :sales_id"""
        sales_data = self._fetching(
            sales_query, 
            {"sales_id": sales_result['sales_id']}, 
            fetch_type="one"
        )
        
        sales_data = self._fetching(
            sales_query, 
            {"sales_id": sales_result['sales_id']}, 
            fetch_type="one"
        )
        
        # PERBAIKAN: Gunakan .get() dan pastikan defaultnya 0 jika None
        plafon_limit = 0
        if sales_data:
            plafon_limit = sales_data.get('plafon_limit') or 0
        
        baseQuery = """
            SELECT
                cr.id,
                cr.tanggal_request,
                cr.total_request,
                cr.status,
                s.plafon_limit as plafon_limit
            FROM canvas_request cr
            JOIN sales s ON cr.id_sales = s.id
            WHERE s.id_user = :id_user
        """
        
        result = query_with_filters(
            self, baseQuery, {"id_user": id_user},
            search_in = ['tanggal_request', 'plafon_limit', 'total_request', 'status'],
            filter_by = {'tanggal_request': 'tanggal_request', 'status': 'status'},
            table_alias = 'cr',
            order_by = 'ORDER BY cr.tanggal_request DESC',
            raw_data = True
        )

        data = list(result)
        
        if data and len(data) > 0:
            # Pastikan row['total_request'] juga tidak None saat dijumlahkan
            total_requests = [
                row['total_request'] for row in data 
                if row.get('total_request') is not None and row.get('status') == 2
            ]
            total_approved = sum(total_requests)
            
            # Sekarang operasi ini aman karena plafon_limit sudah diproteksi 'or 0'
            sisa_plafon = plafon_limit - total_approved
        else:
            sisa_plafon = plafon_limit

        return format_paginated_response(
            self, data,
            sisa_plafon = sisa_plafon,
            plafon_limit = plafon_limit
        )
        
    @handle_error
    def getListProductCanvas(self):
        id_user = self.req('id') or self.req('id_user')
        if not id_user: 
            abort(404, "User tidak ditemukan")
        
        sales_result = self.getSalesAndPrincipalByUser(id_user)
        if not sales_result: 
            abort(404, "Data sales tidak ditemukan")

        print(f"DEBUG sales: {id_user}")
        principal_id = sales_result['id_principal']

        baseQuery = """
            SELECT 
                p.id, 
                p.harga_beli,
                p.id_principal,                 
                p.nama as nama_produk,
                pu1.nama as uom1_nama,
                pu2.nama as uom2_nama,
                pu3.nama as uom3_nama,
                pr.nama as nama_principal,
                COALESCE(pu1.faktor_konversi, 1) as uom1_factor,
                COALESCE(pu2.faktor_konversi, 1) as uom2_factor,
                COALESCE(pu3.faktor_konversi, 1) as uom3_factor,
                COALESCE(st.jumlah_ready, 0) as stock_gudang
            FROM produk p
            JOIN principal pr ON p.id_principal = pr.id
            LEFT JOIN produk_uom pu1 ON p.id = pu1.id_produk AND pu1.level = 1
            LEFT JOIN produk_uom pu2 ON p.id = pu2.id_produk AND pu2.level = 2
            LEFT JOIN produk_uom pu3 ON p.id = pu3.id_produk AND pu3.level = 3
            LEFT JOIN stok st ON st.produk_id = p.id
            WHERE p.id_principal = :principal_id
        """
        
        result = query_with_filters(
            self, baseQuery, { "principal_id": principal_id },
            search_in = ['nama_produk', 'uom1_nama', 'uom2_nama', 'uom3_nama', 'nama_principal'],
            filter_by = {'nama_produk': 'p.nama', 'nama_principal': 'pr.nama'},
            table_alias = 'p',
            order_by = 'ORDER BY p.nama ASC',
        )

        data = extract_data(result)

        for row in data:
            harga_beli = row.get('harga_beli') or 0
            uom1_factor = row.get('uom1_factor') or 1
            
            row['qty_uom1'] = 0 
            row['qty_uom2'] = 0 
            row['qty_uom3'] = 0 
            row['total_satuan'] = 0 
            row['total_permintaan'] = 0 
            row['harga_per_uom1'] = harga_beli * uom1_factor
            
        return format_result_response(self, result, data)
        
    @handle_error
    def getDetailCanvasRequest(self):
        id_user = self.req('id') or self.req('id_user')
        id_canvas = self.req('id_canvas')
        tanggal_request = self.req('tanggal_request')
        
        if not id_user: return []
        if not id_canvas: return []
        
        sales_result = self.getSalesAndPrincipalByUser(id_user)
        if not sales_result: 
            abort(404, "Data sales tidak ditemukan")

        principal_id = sales_result['id_principal']

        baseQuery = """
            SELECT 
                p.id,
                p.harga_beli,
                p.id_principal,                 
                p.nama as nama_produk,
                pu1.nama as uom1_nama,
                pu2.nama as uom2_nama,
                pu3.nama as uom3_nama,
                pr.nama as nama_principal,
                COALESCE(pu1.faktor_konversi, 1) as uom1_factor,
                COALESCE(pu2.faktor_konversi, 1) as uom2_factor,
                COALESCE(pu3.faktor_konversi, 1) as uom3_factor,
                COALESCE(crd.qty_request, 0) as qty_request_today,
                COALESCE(st.jumlah_ready, 0) as stock_gudang,
                COALESCE(cr.status) as status_canvas
            FROM produk p
            JOIN principal pr ON p.id_principal = pr.id
            LEFT JOIN produk_uom pu1 ON p.id = pu1.id_produk AND pu1.level = 1
            LEFT JOIN produk_uom pu2 ON p.id = pu2.id_produk AND pu2.level = 2
            LEFT JOIN produk_uom pu3 ON p.id = pu3.id_produk AND pu3.level = 3
            LEFT JOIN stok st ON st.produk_id = p.id
            LEFT JOIN canvas_request_detail crd ON crd.id_produk = p.id AND crd.id_canvas = :id_canvas
            LEFT JOIN canvas_request cr ON crd.id_canvas = cr.id
            WHERE p.id_principal = :principal_id AND cr.id = :id_canvas
        """
        
        if tanggal_request:
            baseQuery += " AND DATE(cr.tanggal_request) = DATE(:tanggal_request) "
            
        params = {
            "principal_id": principal_id,
            "id_canvas": id_canvas,
            "tanggal_request": tanggal_request
        }
        
        result = query_with_filters(
            self, baseQuery, params,
            search_in = ['nama_produk', 'uom1_nama', 'uom2_nama', 'uom3_nama', 'nama_principal'],
            filter_by = {'nama_produk': 'p.nama', 'nama_principal': 'pr.nama'},
            table_alias = 'p',
            order_by = 'ORDER BY p.nama ASC',
        )



        data = extract_data(result)
        
        for row in data:
            harga_beli = row.get('harga_beli') or 0
            uoms = [
                {"name": row.get('uom1_nama'), "factor": row.get('uom1_factor'), "key": "qty_uom1"},
                {"name": row.get('uom2_nama'), "factor": row.get('uom2_factor'), "key": "qty_uom2"},
                {"name": row.get('uom3_nama'), "factor": row.get('uom3_factor'), "key": "qty_uom3"},
            ]
            
            harga_per_pieces = harga_beli * uoms[0]['factor']
            row['harga_per_uom1'] = harga_per_pieces
            
            qty_request_today = row.get('qty_request_today')
            row['total_permintaan'] = qty_request_today * harga_per_pieces
            row['total_satuan'] = qty_request_today
            
            remaining_qty = qty_request_today
            
            for uom in reversed(uoms):
               factor = uom['factor']
               qty = int(remaining_qty // factor)
               remaining_qty = remaining_qty % factor if factor > 0 else remaining_qty
               row[uom['key']] = qty

        return format_result_response(self, result, data)

    @handle_error
    def updateCanvasRequestTemp(self, **kwargs):
        id_produk = self.req('id_produk')
        id_user = self.req('id_user') or self.req('id')
        qty_uom1 = int(self.req('qty_uom1') or 0)
        qty_uom2 = int(self.req('qty_uom2') or 0)
        qty_uom3 = int(self.req('qty_uom3') or 0)
        
        if not id_produk:
            abort(400, "ID Produk tidak boleh kosong")
        
        sales_result = self.getSalesAndPrincipalByUser(id_user)
        if not sales_result:
            abort(404, "Data sales tidak ditemukan")

        produk_data = self._getProductWithUOM(id_produk)
        calculation = self._calculateUOMPricing(produk_data, qty_uom1, qty_uom2, qty_uom3)
        
        temp_data = {
            "id_produk": id_produk,
            "nama_produk": produk_data.get('nama_produk'),
            "stock_gudang": produk_data.get('stock_gudang'),
            "uom1_factor": calculation["uom1_factor"],
            "uom2_factor": calculation["uom2_factor"],
            "uom3_factor": calculation["uom3_factor"],
            "qty_uom1": qty_uom1,
            "qty_uom2": qty_uom2,
            "qty_uom3": qty_uom3,
            "qty_request": calculation["qty_request"],
            "harga_per_pieces": calculation["harga_per_pieces"],
            "total_permintaan": calculation["total_permintaan"],
        }

        if kwargs:
            temp_data.update(kwargs)

        try:
            data = self.reqs() 
        except AttributeError:
            from flask import request
            data = request.get_json() or {}

        for key, value in data.items():
            if key not in temp_data:
                temp_data[key] = value

        return format_paginated_response(self, [temp_data])
        
    @handle_error   
    def updateCanvasData(self):
        canvas_request_id = self.req('canvas_request_id')
        id_produk = self.req('id_produk')
        qty_uom1 = int(self.req('qty_uom1'))
        qty_uom2 = int(self.req('qty_uom2'))
        qty_uom3 = int(self.req('qty_uom3'))

        if not canvas_request_id:
            abort(400, "ID Canvas Request tidak boleh kosong")

        if not id_produk:
            abort(400, "ID Produk tidak boleh kosong")

        produk_data = self._getProductWithUOM(id_produk)
        calculation = self._calculateUOMPricing(produk_data, qty_uom1, qty_uom2, qty_uom3)
        
        qty_request = calculation["qty_request"]
        harga_per_pieces = calculation["harga_per_pieces"]
        
        check_detail_query = """
            SELECT id, qty_request 
            FROM canvas_request_detail 
            WHERE id_canvas = :canvas_request_id AND id_produk = :id_produk
        """

        checkParams = { "canvas_request_id": canvas_request_id, "id_produk": id_produk }
        detail = self._fetching(check_detail_query, checkParams, fetch_type="one")
        
        if not detail:
            abort(404, "Produk pada Detail canvas Request tidak ditemukan")
        
        differenceQty = qty_request - detail['qty_request']
        
        update_detail_query = """
            UPDATE canvas_request_detail
            SET qty_request = :qty_request
            WHERE id = :detail_id
        """
        
        self._fetching(update_detail_query, { "qty_request": qty_request, "detail_id": detail['id'] })
        
        update_canvas_query = """
            UPDATE canvas_request
            SET total_request = total_request + :diff_total,
                status = 1
            WHERE id = :canvas_request_id
        """

        updateCanvasParams = { 
            "diff_total": differenceQty * harga_per_pieces, 
            "canvas_request_id": canvas_request_id
        }
        self._fetching(update_canvas_query, updateCanvasParams)
        
        if differenceQty != 0:
            self.update_stock(id_produk, differenceQty, status=1)
            
        return format_paginated_response(self, [{
            "detail_id": detail['id'],
            "qty_request": qty_request,
            "difference_qty": differenceQty,
        }])

    @handle_error
    def createCanvasRequest(self):
        id_produk = self.req('id_produk')
        id_user = self.req('id_user') or self.req('id')
        qty_uom1 = int(self.req('qty_uom1') or 0)
        qty_uom2 = int(self.req('qty_uom2') or 0)
        qty_uom3 = int(self.req('qty_uom3') or 0)
        
        if not id_produk:
            abort(400, "ID Produk tidak boleh kosong")

        if qty_uom1 == 0 and qty_uom2 == 0 and qty_uom3 == 0:
            abort(400, "Quantity tidak boleh kosong semua")

        sales_result = self.getSalesAndPrincipalByUser(id_user)
        if not sales_result:
            abort(404, "Data sales tidak ditemukan")

        sales_id = sales_result['sales_id']
        
        produk_data = self._getProductWithUOM(id_produk)
        calculation = self._calculateUOMPricing(produk_data, qty_uom1, qty_uom2, qty_uom3)
        
        qty_request = calculation["qty_request"]
        total_harga = calculation["total_permintaan"]
        
        canvas_request_query = """
            SELECT id, total_request, plafon_limit
            FROM canvas_request
            WHERE id_sales = :sales_id 
            AND DATE(tanggal_request) = DATE(:tanggal_request)
            ORDER BY id DESC
        """
        
        existing_canvas = query_with_filters(
            self, canvas_request_query, 
            {"sales_id": sales_id, "tanggal_request": date_now()}, 
            raw_data=True
        )
            
        if existing_canvas and len(existing_canvas) > 0:
            canvas_request_id = existing_canvas[0]['id']
            current_total = existing_canvas[0]['total_request'] or 0
            new_total_request = current_total + total_harga
            
            update_canvas_query = """
                UPDATE canvas_request
                SET total_request = :total_request
                WHERE id = :canvas_request_id
            """

            bindParams = { "total_request": new_total_request, "canvas_request_id": canvas_request_id }
            self._fetching(update_canvas_query, bindParams)
        else:
            # Gunakan RETURNING id agar lebih pasti dan efisien
            insert_canvas_query = """
                INSERT INTO canvas_request (id_sales, tanggal_request, total_request, status)
                VALUES (:sales_id, :tanggal_request, :total_request, :status)
                RETURNING id
            """
            
            # Eksekusi insert dan ambil ID-nya langsung
            res_insert = self.query().setRawQuery(insert_canvas_query).bindparams({
                "sales_id": sales_id, 
                "tanggal_request": date_now(), 
                "total_request": total_harga, 
                "status": 1 
            }).execute().get()
            
            # Sesuaikan cara ambil ID berdasarkan hasil fetch library Anda
            if isinstance(res_insert, list) and len(res_insert) > 0:
                canvas_request_id = res_insert[0]['id']
            elif isinstance(res_insert, dict):
                canvas_request_id = res_insert.get('id')
            else:
                abort(500, "Gagal membuat header Canvas Request")

        # VALIDASI: Jangan lanjut jika ID tetap tidak ditemukan
        if not canvas_request_id:
            # Jangan biarkan lanjut jika ID null, ini akan menyebabkan error FK 23502
            abort(500, "Gagal mengidentifikasi ID Request Canvas")

        insert_detail_query = """
            INSERT INTO canvas_request_detail (
                id_canvas, id_produk, qty_request
            ) VALUES (:id_canvas, :id_produk, :qty_request)
        """

        # Jika database sudah diperbaiki dengan Solusi 1, baris ini tidak akan error lagi
        self._fetching(insert_detail_query, {  
            "id_canvas": canvas_request_id,
            "id_produk": id_produk,
            "qty_request": qty_request,
        })

        return format_paginated_response(self, [{
            "status": "success",
            "message": "Canvas request berhasil dibuat",
            "canvas_request_id": canvas_request_id
        }])
        
    @handle_error
    def getAllCanvasOrder(self):
        # Gunakan get_json atau args secara konsisten
        id_user = self.req('id') or self.req('id_user')
        tanggal_order = self.req('tanggal_order')
        status = self.req('status')
        
        sales_result = self.getSalesAndPrincipalByUser(id_user)
        if not sales_result: 
            abort(404, "Data sales tidak ditemukan")
        
        baseQuery = """
            SELECT
                co.id,
                co.tanggal_order,
                co.nama_customer,
                co.total_order,
                co.status_order
            FROM canvas_order co
            JOIN canvas_request cr ON co.id_canvas_request = cr.id
            JOIN sales s ON cr.id_sales = s.id
            WHERE s.id_user = :id_user
        """
        
        params = { "id_user": id_user }
        if tanggal_order:
            baseQuery += " AND DATE(co.tanggal_order) = DATE(:tanggal_order) "
            params["tanggal_order"] = tanggal_order
            
        if status:
            baseQuery += " AND co.status_order = :status_order "
            params["status_order"] = status
        
        # PERBAIKAN: search_in harus sesuai dengan kolom yang di SELECT
        result = query_with_filters(
            self, baseQuery, params,
            search_in = ['co.nama_customer', 'co.total_order'], # Sesuaikan kolom
            filter_by = {'tanggal_order': 'co.tanggal_order', 'status_order': 'co.status_order'},
            table_alias = 'co',
            order_by = 'ORDER BY co.tanggal_order DESC',
        )

        # Standarisasi pengambilan data
        if isinstance(result, dict):
            data = result.get('pages', [])
        else:
            data = list(result) if result else []
        
        # Iterasi aman jika data ada
        for row in data:
            setoran_query = """
                SELECT jumlah_setoran FROM setoran_customer
                WHERE id_canvas_order = :id_canvas_order
            """
            setoran_result = self._fetching(
                setoran_query, 
                { "id_canvas_order": row["id"] },
                fetch_type="all"
            )
            
            jumlah_setoran = sum(item["jumlah_setoran"] for item in setoran_result) if setoran_result else 0
            # Gunakan total_order jika belum ada setoran
            row["total_dibayarkan"] = jumlah_setoran if jumlah_setoran > 0 else row.get('total_order', 0)
        
        # PERBAIKAN: Jangan abort 404 jika data kosong, biarkan frontend merender "Data Tidak Tersedia"
        if isinstance(result, dict):
            result['pages'] = data
            return result
        else:
            return format_paginated_response(self, data)
    
    @handle_error
    def getDetailCanvasOrder(self):
        id_canvas_order = self.req('id_canvas_order') or self.req('id')
        if not id_canvas_order:
            abort(400, "ID Canvas Order tidak ditemukan")

        baseQuery = """
            SELECT 
                p.id,
                p.ppn,
                p.harga_beli,
                p.nama AS nama_produk,
                pu1.nama AS uom1_nama,
                pu2.nama AS uom2_nama,
                pu3.nama AS uom3_nama,
                cod.pcs_order AS qty_uom1,
                cod.box_order AS qty_uom2,
                cod.carton_order AS qty_uom3,
                cod.harga AS harga_per_uom1,
                cod.diskon AS total_diskon,
                cod.total AS jumlah_harga,
                cod.subtotal AS subtotal_harga,
                COALESCE(pu1.faktor_konversi, 1) AS uom1_factor,
                COALESCE(pu2.faktor_konversi, 1) AS uom2_factor,
                COALESCE(pu3.faktor_konversi, 1) AS uom3_factor,
                COALESCE(st.jumlah_ready, 0) AS stock_gudang,
                co.id AS id_canvas_order,
                co.id_voucher_2,
                co.id_voucher_3,
                co.tanggal_order AS tanggal_order,
                co.nama_customer AS nama_customer
            FROM canvas_order co
            JOIN canvas_order_detail cod ON cod.id_canvas_order = co.id
            JOIN produk p ON cod.id_produk = p.id
            LEFT JOIN produk_uom pu1 ON p.id = pu1.id_produk AND pu1.level = 1
            LEFT JOIN produk_uom pu2 ON p.id = pu2.id_produk AND pu2.level = 2
            LEFT JOIN produk_uom pu3 ON p.id = pu3.id_produk AND pu3.level = 3
            LEFT JOIN stok st ON st.produk_id = p.id
            WHERE co.id = :id_canvas_order
            ORDER BY cod.id ASC
        """

        result = query_with_filters(
            self, baseQuery, {"id_canvas_order": id_canvas_order},
            raw_data=True
        )
        
        data = list(result)
        for row in data:
            row["v1r"] = 0
            row["v2r"] = 0
            row["v3r"] = 0
            row["v2p"] = 0
            row["v3p"] = 0
            
        # Voucher 2
        if row.get("id_voucher_2"):
            v2 = self.query().setRawQuery(
                """
                    SELECT is_reguler, persentase_diskon_2, persentase_diskon_1, nominal_diskon 
                    FROM voucher_2 WHERE id = :id
                """
            ).bindparams({ "id": row["id_voucher_2" ]}
            ).execute().fetchone().result
            
            if v2:
                if v2["is_reguler"] == 1:
                    row["v2r"] = v2.get("persentase_diskon_2", 0)
                    row["v1r"] = v2.get("persentase_diskon_1", 0)
                else:
                    row["v2p"] = v2.get("persentase_diskon_2", 0) or v2.get("nominal_diskon", 0)
        
        # Voucher 3
        if row.get("id_voucher_3"):
            v3 = self.query().setRawQuery(
                """
                    SELECT is_reguler, persentase_diskon_3, nominal_diskon 
                    FROM voucher_3 WHERE id = :id
                """
            ).bindparams({"id": row["id_voucher_3"]}
            ).execute().fetchone().result
            
            if v3:
                if v3["is_reguler"] == 1:
                    row["v3r"] = v3.get("persentase_diskon_3", 0)
                else:
                    row["v3p"] = v3.get("persentase_diskon_3", 0) or v3.get("nominal_diskon", 0)

        return format_result_response(self, result, data)
    
    @handle_error
    def getListOrderCanvas(self):
        id_user = self.req('id') or self.req('id_user')
        if not id_user: return []
        
        sales_result = self.getSalesAndPrincipalByUser(id_user)
        if not sales_result: return []


        principal_id = sales_result['id_principal']
        # print(f"DEBUG SALES: {principal_id}")

        baseQuery = """
            SELECT 
                p.id, 
                p.ppn as ppn,
                p.harga_beli,
                p.id_principal,                 
                p.nama as nama_produk,
                pu1.nama as uom1_nama,
                pu2.nama as uom2_nama,
                pu3.nama as uom3_nama,
                pr.nama as nama_principal,
                COALESCE(pu1.faktor_konversi, 1) as uom1_factor,
                COALESCE(pu2.faktor_konversi, 1) as uom2_factor,
                COALESCE(pu3.faktor_konversi, 1) as uom3_factor,
                COALESCE(sc.stock_canvas, 0) as stock_canvas
            FROM produk p
            JOIN principal pr ON p.id_principal = pr.id
            LEFT JOIN produk_uom pu1 ON p.id = pu1.id_produk AND pu1.level = 1
            LEFT JOIN produk_uom pu2 ON p.id = pu2.id_produk AND pu2.level = 2
            LEFT JOIN produk_uom pu3 ON p.id = pu3.id_produk AND pu3.level = 3
            LEFT JOIN stok st ON st.produk_id = p.id
            LEFT JOIN stock_canvas sc ON p.id = sc.id_produk
            WHERE p.id_principal = :principal_id
        """
        
        result = query_with_filters(
            self, baseQuery, { "principal_id": principal_id },
            search_in = ['nama_produk', 'uom1_nama', 'uom2_nama', 'uom3_nama', 'nama_principal'],
            filter_by = {'nama_produk': 'p.nama', 'nama_principal': 'pr.nama'},
            table_alias = 'p',
            order_by = 'ORDER BY p.nama ASC',
        )

        data = extract_data(result)

        for row in data:
            harga_beli = row.get('harga_beli') or 0
            uom1_factor = row.get('uom1_factor') or 1
            
            row['qty_uom1'] = 0 
            row['qty_uom2'] = 0 
            row['qty_uom3'] = 0 
            row['total_diskon'] = 0 
            row['jumlah_harga'] = 0 
            row['harga_per_uom1'] = harga_beli * uom1_factor
                
            row['v1r'] = row.get('v1r') or 0
            
            v2_is_reguler = row.get('v2_is_reguler') or 0
            v2_discount = row.get('v2r_discount_2') or 0
            v3_is_reguler = row.get('v3_is_reguler') or 0
            v3_discount = row.get('v3r_discount_3') or 0
        
            if v2_is_reguler == 1:
                row['v2r'] = v2_discount
                row['v2p'] = 0           
            else:
                row['v2r'] = 0           
                row['v2p'] = v2_discount  
            if v3_is_reguler == 1:
                row['v3r'] = v3_discount  
                row['v3p'] = 0           
            else:
                row['v3r'] = 0          
                row['v3p'] = v3_discount

            total_discount_percentage = (
                row['v1r'] + row['v2r'] + row['v3r'] + row['v2p'] + row['v3p']
            ) / 100
            
            subtotal_default = row['harga_per_uom1'] * 0  # qty_uom1 = 0
            row['total_diskon'] = subtotal_default * total_discount_percentage
            row['jumlah_harga'] = subtotal_default - row['total_diskon']
            
            for temp_field in [
                'v2r_discount_2', 
                'v3r_discount_3', 
                'v2_is_reguler', 
                'v3_is_reguler'
            ]:
                row.pop(temp_field, None)
            # print(f"DEBUG SALES: {data}")
            
        return format_result_response(self, result, data)
    
    @handle_error
    def createCanvasOrder(self):
        id_user = self.req('id_user') or self.req('id')
        nama_customer = self.req('nama_customer')
        id_voucher_2 = self.req('id_voucher_2')
        id_voucher_3 = self.req('id_voucher_3')
        total_diskon = self.req('total_diskon')
        list_items = self.req('list_items')

        if not nama_customer:
            abort(400, "Nama Customer tidak boleh kosong")

        if not list_items or len(list_items) == 0:
            abort(400, "List items tidak boleh kosong")

        sales_result = self.getSalesAndPrincipalByUser(id_user)
        if not sales_result:
            abort(404, "Data sales tidak ditemukan")

        sales_id = sales_result['sales_id']

        canvas_request_query = """
            SELECT id
            FROM canvas_request
            WHERE id_sales = :sales_id
            AND DATE(tanggal_request) = DATE(:tanggal_request)
            AND status = 2
            ORDER BY id DESC
        """

        canvas_request = query_with_filters(
            self, canvas_request_query,
            {"sales_id": sales_id, "tanggal_request": date_now()},
            raw_data=True
        )
        
        if not canvas_request:
            abort(404, "Canvas request approved tidak ditemukan")

        canvas_request_id = canvas_request[0]['id']
        order_details = []
        total_order = 0
        total_diskon = 0
        sub_total_order = 0

        for item in list_items:
            id_produk = int(item['id_produk'])
            qty_uom1 = int(item['qty_uom1'])
            qty_uom2 = int(item['qty_uom2'])
            qty_uom3 = int(item['qty_uom3'])

            if (qty_uom1 + qty_uom2 + qty_uom3) == 0:
                continue

            stock_canvas = self.getStockCanvas(id_produk, sales_id)
            if not stock_canvas:
                abort(400, f"Stok canvas untuk produk {id_produk} tidak tersedia")

            produk_data = self._getProductWithUOM(id_produk)
            calculation = self._calculateUOMPricing(produk_data, qty_uom1, qty_uom2, qty_uom3)

            total_qty_pieces = calculation['qty_request']
            available_stock = stock_canvas
            
            if total_qty_pieces > available_stock:
                abort(400, f"Stok canvas untuk produk {id_produk} tidak mencukupi")

            harga_per_pieces = calculation['harga_per_pieces']
            subtotal = total_qty_pieces * harga_per_pieces
            
            if not id_voucher_2 and list_items and len(list_items) > 0:
                id_voucher_2 = list_items[0].get('id_voucher_2')
                
            if not id_voucher_3 and list_items and len(list_items) > 0:
                id_voucher_3 = list_items[0].get('id_voucher_3')

            v1r = float(item.get('v1r', 0))
            v2r = float(item.get('v2r', 0))
            v3r = float(item.get('v3r', 0))
            v2p = float(item.get('v2p', 0))
            v3p = float(item.get('v3p', 0))

            # Calculate discount, item, etc.
            ppn = produk_data['ppn']
            total_diskon = (v1r + v2r + v3r + v2p + v3p)
            total_per_item = subtotal - total_diskon
            ppnRate = total_per_item * (ppn / 100)
            finalTotal = subtotal + ppnRate

            sub_total_order += subtotal
            total_order += finalTotal

            order_details.append({
                'id_produk': id_produk,
                'pcs_order': qty_uom1,
                'box_order': qty_uom2,
                'carton_order': qty_uom3,
                'harga': harga_per_pieces,
                'subtotal': subtotal,
                'diskon': total_diskon,
                'total': finalTotal,
                'total_qty_pieces': total_qty_pieces
            })
            
        if len(order_details) == 0:
            abort(400, "Tidak ada item yang dipesan")
            
        insert_order_query = """
            INSERT INTO canvas_order (
                id_canvas_request, nama_customer, tanggal_order,
                tanggal_faktur, total_order, sub_total_order,
                id_voucher_2, id_voucher_3, total_diskon, status_order
            ) VALUES (
                :id_canvas_request, :nama_customer, :tanggal_order,
                :tanggal_faktur, :total_order, :sub_total_order,
                :id_voucher_2, :id_voucher_3, :total_diskon, :status_order
            ) RETURNING id
        """
        
        print(f"Debug vouchers: id_voucher_2={id_voucher_2}, id_voucher_3={id_voucher_3}") 

        order_result = self._fetching(insert_order_query, {
            "id_canvas_request": canvas_request_id,
            "nama_customer": nama_customer,
            "tanggal_order": date_now(),
            "tanggal_faktur": date_now(),
            "total_order": total_order,
            "sub_total_order": sub_total_order,
            "id_voucher_2": id_voucher_2,
            "id_voucher_3": id_voucher_3,
            "total_diskon": total_diskon,
            "status_order": 2
        }, fetch_type="one")

        canvas_order_id = None
        if order_result:
            if isinstance(order_result, dict):
                canvas_order_id = order_result.get('id')
            elif isinstance(order_result, (list, tuple)):
                canvas_order_id = order_result[0] if len(order_result) > 0 else None
            elif hasattr(order_result, 'id'):
                canvas_order_id = order_result.id

        if not canvas_order_id:
            abort(500, "Gagal membuat canvas order")
            
        is_direct_payment = self.req('is_direct_payment')
        jumlah_setoran = self.req('jumlah_setoran')
            
        if is_direct_payment and jumlah_setoran:
            insert_setoran_customer_query = """
                INSERT INTO setoran_customer (
                    id_sales, id_canvas_order, jumlah_setoran, tipe_setoran, tanggal_input, is_rekap
                ) VALUES (
                    :id_sales, :id_canvas_order, :jumlah_setoran, :tipe_setoran, :tanggal_input, :is_rekap
                )
            """
            self._fetching(insert_setoran_customer_query, {
                "id_sales": sales_id,
                "id_canvas_order": canvas_order_id,
                "jumlah_setoran": jumlah_setoran,
                "tipe_setoran": 1, 
                "tanggal_input": date_now(),
                "is_rekap": 0
            })
            
        # Insert details
        for detail in order_details:
            insert_detail_query = """
                INSERT INTO canvas_order_detail (
                    id_canvas_order, id_produk, pcs_order, box_order, 
                    carton_order, harga, subtotal, diskon, total
                ) VALUES (
                    :id_canvas_order, :id_produk, :pcs_order, :box_order, 
                    :carton_order, :harga, :subtotal, :diskon, :total
                )
            """

            self._fetching(insert_detail_query, {
                "id_canvas_order": canvas_order_id,
                "id_produk": detail['id_produk'],
                "pcs_order": detail['pcs_order'],
                "box_order": detail['box_order'],
                "carton_order": detail['carton_order'],
                "harga": detail['harga'],
                "subtotal": detail['subtotal'],
                "diskon": detail['diskon'],
                "total": detail['total']
            })

            # Update stock canvas (kurangi stok)
            update_stock_query = """
                UPDATE stock_canvas
                SET stock_canvas = stock_canvas - :qty
                WHERE id_produk = :id_produk AND id_sales = :id_sales
            """

            self._fetching(update_stock_query, {
                "qty": detail['total_qty_pieces'],
                "id_produk": detail['id_produk'],
                "id_sales": sales_id
            })

        return format_paginated_response(self, [{
            "canvas_order_id": canvas_order_id,
            "total_order": total_order,
            "sub_total_order": sub_total_order,
            "total_items": len(order_details)
        }])
        