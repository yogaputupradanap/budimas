from .BaseServices import BaseServices
from apps.handler import handle_error, handle_error_rollback
from apps.models import (
    voucher_1,
    voucher_2,
    voucher_3,
    draft_voucher,
    draft_voucher_2,
    draft_voucher_detail,
    faktur,
    sales_order_detail,
    global_table,
    voucher_2_produk,
    voucher_3_produk,
    voucher_1_produk, voucher_2_cabang, voucher_3_cabang, voucher_3_customer
)
from apps.handler import nonServerErrorException
from apps.lib.paginate import Paginate
from flask import request
from apps.lib.helper import datetime_now_stamp, date_now
import json
import bcrypt

class Voucher(BaseServices):

    @handle_error
    def getMasterVoucherUser(self):
        email = self.req('email')
        password = self.req('password')

        login_query = f"""
            select 
            users.tokens AS token,
            users.id AS id_user,
            users.nama AS nama_user,
            users.email AS user_email,
            users.id_jabatan,
            users.id_cabang,
            users.password
            from users 
            where users.email = :email
        """
        login_bindparam = {'email': email}

        user = self.query().setRawQuery(login_query).bindparams(login_bindparam).execute().fetchone().result
        print(user)
        if not user:
            raise nonServerErrorException(401, "Email salah atau tidak ada")

        # Convert password input to bytes
        password_bytes = password.encode('utf-8')
        # Convert stored hash from database to bytes if it's not already
        stored_hash = user['password'].encode('utf-8') if isinstance(user['password'], str) else user['password']

        # Verify password using bcrypt
        if not bcrypt.checkpw(password_bytes, stored_hash):
            raise nonServerErrorException(401, "Password Salah")

        return user
        
    @handle_error
    def getVouchers(self):
        tipe_voucher = int(self.req('tipe-voucher'))

        if tipe_voucher not in [1, 2, 3]:
            raise nonServerErrorException('not a valid voucher type')

        voucher_table = f"voucher_{tipe_voucher}"

        # Define common SELECT fields
        select_fields = [
            f"{voucher_table}.*",
            "principal.nama as nama_principal",
            "principal.kode as kode_principal"
        ]

        # Add conditional fields based on tipe_voucher
        if tipe_voucher >= 2:
            sub_query = f"""(
                select 
                json_agg(
                    json_build_object(
                        'id_produk', produk.id,
                        'nama_produk', produk.nama
                    )
                )
                from produk
                where produk.id = {voucher_table}.id_produk
            ) as id_produk"""
            select_fields.append(sub_query)

        select_query = ", ".join(select_fields)

        # Define common FROM and JOIN clauses
        join_clauses = [
            f"join principal on principal.id = {voucher_table}.id_principal"
        ]
        if tipe_voucher >= 2:
            join_clauses.append(f"left join produk on produk.id = {voucher_table}.id_produk")

        from_query = f"{voucher_table} " + " ".join(join_clauses)

        query = f"select {select_query} from {from_query}"

        return Paginate(request, query).paginate()

    @handle_error_rollback
    def insertVoucher(self, tipe):
        kode_voucher = f"VC-{datetime_now_stamp()}-{tipe}"

        # Convert `tipe` to integer and validate it
        integer_tipe = int(tipe)
        if integer_tipe not in [1, 2, 3]:
            raise nonServerErrorException("Invalid voucher type provided.")

        # Base parameters common to all voucher types
        parameter = {
            "id_principal": self.req("id_principal"),
            "nama_voucher": self.req("nama"),
            "keterangan": self.req("keterangan"),
            "status_voucher": self.req("status_diskon"),
            "syarat_ketentuan": self.req("syarat_ketentuan"),
            "syarat_wajib": self.req("syarat_wajib"),
            "pic_voucher": self.req("upload_file"),
            "kode_voucher": kode_voucher
        }

        # Cek jenis_voucher untuk v2 dan v3
        jenis_voucher = None
        if integer_tipe in [2, 3]:
            jenis_voucher = self.req("jenis_voucher")
            parameter["is_reguler"] = 1 if jenis_voucher == 1 else 0

        # Logika untuk voucher reguler (v1, atau v2/v3 dengan jenis_voucher=1)
        if integer_tipe == 1 or (jenis_voucher == 1):
            parameter.update({
                "tanggal_mulai": self.req("tanggal_mulai"),
                "tanggal_kadaluarsa": self.req("tanggal_kadaluarsa"),
                "persentase_diskon_1": self.req("persen_diskon") if integer_tipe == 1 else None,
                "persentase_diskon_2": self.req("persen_diskon") if integer_tipe == 2 else None,
                "persentase_diskon_3": self.req("persen_diskon") if integer_tipe == 3 else None,
                "minimal_subtotal_pembelian": self.req("minimal_subtotal_pembelian")
            })
        # Logika untuk voucher produk (v2/v3 dengan jenis_voucher=0)
        elif jenis_voucher == 0:
            parameter.update({
                "tanggal_mulai": self.req("tanggal_mulai"),
                "tanggal_kadaluarsa": self.req("tanggal_kadaluarsa"),
                "kategori_voucher": self.req("kategori_voucher"),
                "minimal_subtotal_pembelian": self.req("minimal_subtotal_pembelian"),
                "budget_diskon": self.req("limit"),
                "current_budget_diskon": self.req("limit")
            })

            # Tambahan khusus untuk v2 produk
            if integer_tipe == 2:
                parameter.update({
                    "level_uom": self.req("level_uom"),
                    "minimal_jumlah_produk": self.req("minimal_jumlah_produk")
                })

            # Add persentase_diskon atau nominal_diskon based on kategori_voucher
            if self.req("kategori_voucher") == 1:
                if integer_tipe == 2:
                    parameter["persentase_diskon_2"] = self.req("persen_diskon")
                else:
                    parameter["persentase_diskon_3"] = self.req("persen_diskon")
            else:
                parameter["nominal_diskon"] = self.req("nilai_diskon")

        # Map `tipe` to the correct voucher model
        voucher_models = {1: voucher_1, 2: voucher_2, 3: voucher_3}
        voucher_object = voucher_models.get(integer_tipe)
        if not voucher_object:
            raise nonServerErrorException("Failed to determine the voucher model.")

        # Create and add the voucher
        add_voucher = voucher_object(**parameter)
        self.add(add_voucher).flush()

        # Handle products for all voucher types
        voucher_produk_models = {
            1: voucher_1_produk,
            2: voucher_2_produk,
            3: voucher_3_produk
        }

        if len(self.req('id_produk')):
            voucher_produk_object = voucher_produk_models.get(integer_tipe)
            for produk in self.req('id_produk'):
                produk_param = {
                    "id_produk": produk['id'],
                    "id_voucher": add_voucher.id
                }
                add_produk_voucher = voucher_produk_object(**produk_param)
                self.add(add_produk_voucher).flush()

        # Handle cabang for voucher type 2 and 3
        if integer_tipe in [2, 3]:
            voucher_cabang_model = voucher_2_cabang if integer_tipe == 2 else voucher_3_cabang
            if len(self.req('id_cabang')):
                for cabang in self.req('id_cabang'):
                    cabang_param = {
                        "id_cabang": cabang['id'],
                        "id_voucher": add_voucher.id
                    }
                    add_cabang_voucher = voucher_cabang_model(**cabang_param)
                    self.add(add_cabang_voucher).flush()

        # Handle customer for voucher type 3
        if integer_tipe == 3 and len(self.req('id_customer')):
            for customer in self.req('id_customer'):
                customer_param = {
                    "id_customer": customer['id'],
                    "id_voucher": add_voucher.id
                }
                add_customer_voucher = voucher_3_customer(**customer_param)
                self.add(add_customer_voucher).flush()

        self.commit()

        return parameter

    @handle_error_rollback
    def updateVoucher(self, tipe):
        # Convert `tipe` to integer and validate it
        integer_tipe = int(tipe)
        if integer_tipe not in [1, 2, 3]:
            raise nonServerErrorException("Invalid voucher type provided.")

        # Base parameters common to all voucher types
        parameter = {
            "id_principal": self.req("id_principal"),
            "nama_voucher": self.req("nama"),
            "keterangan": self.req("keterangan"),
            "status_voucher": self.req("status_diskon"),
            "syarat_ketentuan": self.req("syarat_ketentuan"),
            "syarat_wajib": self.req("syarat_wajib"),
            "pic_voucher": self.req("upload_file")
        }

        # Cek jenis_voucher untuk v2 dan v3
        jenis_voucher = None
        if integer_tipe in [2, 3]:
            jenis_voucher = self.req("jenis_voucher")
            parameter["is_reguler"] = 1 if jenis_voucher == 1 else 0

        # Logika untuk voucher reguler (v1, atau v2/v3 dengan jenis_voucher=1)
        if integer_tipe == 1 or (jenis_voucher == 1):
            parameter.update({
                "tanggal_mulai": self.req("tanggal_mulai"),
                "tanggal_kadaluarsa": self.req("tanggal_kadaluarsa"),
                "persentase_diskon_1": self.req("persen_diskon") if integer_tipe == 1 else None,
                "persentase_diskon_2": self.req("persen_diskon") if integer_tipe == 2 else None,
                "persentase_diskon_3": self.req("persen_diskon") if integer_tipe == 3 else None,
                "minimal_subtotal_pembelian": self.req("minimal_subtotal_pembelian")
            })
        # Logika untuk voucher produk (v2/v3 dengan jenis_voucher=0)
        elif jenis_voucher == 0:
            parameter.update({
                "tanggal_mulai": self.req("tanggal_mulai"),
                "tanggal_kadaluarsa": self.req("tanggal_kadaluarsa"),
                "kategori_voucher": self.req("kategori_voucher"),
                "minimal_subtotal_pembelian": self.req("minimal_subtotal_pembelian"),
                "budget_diskon": self.req("limit"),
                "current_budget_diskon": self.req("limit")
            })

            # Tambahan khusus untuk v2 produk
            if integer_tipe == 2:
                parameter.update({
                    "level_uom": self.req("level_uom"),
                    "minimal_jumlah_produk": self.req("minimal_jumlah_produk")
                })

            # Add persentase_diskon atau nominal_diskon based on kategori_voucher
            if self.req("kategori_voucher") == 1:
                if integer_tipe == 2:
                    parameter["persentase_diskon_2"] = self.req("persen_diskon")
                else:
                    parameter["persentase_diskon_3"] = self.req("persen_diskon")
            else:
                parameter["nominal_diskon"] = self.req("nilai_diskon")

        # Map `tipe` to the correct voucher model
        voucher_models = {1: voucher_1, 2: voucher_2, 3: voucher_3}
        voucher_object = voucher_models.get(integer_tipe)
        if not voucher_object:
            raise nonServerErrorException("Failed to determine the voucher model.")

        # Get and update the voucher
        update_voucher = voucher_object.query.filter(voucher_object.id == int(self.req("id"))).first()
        if not update_voucher:
            raise nonServerErrorException("Voucher not found.")

        # Update voucher fields
        for key, value in parameter.items():
            if hasattr(update_voucher, key):
                setattr(update_voucher, key, value)

        self.flush()

        # Handle products for all voucher types
        voucher_produk_models = {
            1: voucher_1_produk,
            2: voucher_2_produk,
            3: voucher_3_produk
        }

        voucher_produk_object = voucher_produk_models.get(integer_tipe)
        # Delete existing product associations
        existing_products = voucher_produk_object.query.filter(
            getattr(voucher_produk_object, 'id_voucher') == update_voucher.id
        ).all()

        for product in existing_products:
            self.delete(product).flush()

        # Add new product associations
        if len(self.req('id_produk')):
            for produk in self.req('id_produk'):
                produk_id = produk.get('id', produk.get('id_produk'))
                produk_param = {
                    "id_produk": produk_id,
                    "id_voucher": update_voucher.id
                }
                add_produk_voucher = voucher_produk_object(**produk_param)
                self.add(add_produk_voucher).flush()

        # Handle cabang for voucher type 2 and 3
        if integer_tipe in [2, 3]:
            voucher_cabang_model = voucher_2_cabang if integer_tipe == 2 else voucher_3_cabang

            # Delete existing cabang associations
            existing_cabang = voucher_cabang_model.query.filter(
                getattr(voucher_cabang_model, 'id_voucher') == update_voucher.id
            ).all()

            for cabang in existing_cabang:
                self.delete(cabang).flush()

            # Add new cabang associations
            if len(self.req('id_cabang')):
                for cabang in self.req('id_cabang'):
                    cabang_param = {
                        "id_cabang": cabang['id'],
                        "id_voucher": update_voucher.id
                    }
                    add_cabang_voucher = voucher_cabang_model(**cabang_param)
                    self.add(add_cabang_voucher).flush()

        # Handle customer for voucher type 3
        if integer_tipe == 3:
            # Delete existing customer associations
            existing_customers = voucher_3_customer.query.filter(
                voucher_3_customer.id_voucher == update_voucher.id
            ).all()

            for customer in existing_customers:
                self.delete(customer).flush()

            # Add new customer associations
            if len(self.req('id_customer')):
                for customer in self.req('id_customer'):
                    customer_param = {
                        "id_customer": customer['id'],
                        "id_voucher": update_voucher.id
                    }
                    add_customer_voucher = voucher_3_customer(**customer_param)
                    self.add(add_customer_voucher).flush()

        self.commit()
        return parameter

    @handle_error_rollback
    def deleteVoucher(self, tipe):
        id_voucher = self.req("id_voucher")
        
        voucher_object = voucher_1 if tipe == 1 else (voucher_2 if tipe == 2 else (voucher_3 if tipe == 3 else None))
        
        if not voucher_object :
            raise nonServerErrorException("cant select null variable model")
        
        delete_voucher = voucher_object.query.filter(voucher_object.id == int(id_voucher)).first()
        
        nama_voucher = delete_voucher.nama_voucher
        self.delete(delete_voucher).commit()
        
        return {
            "status": "success",
            "message": f"success update voucher with name : {nama_voucher} and ID : {id_voucher}"
        }, 200
    
    @handle_error_rollback
    def declineRegularVoucher(self):
        # kolom kolom maupun tabel yang akan berubah menggunakan method ini :
        # sales_order_detail.subtotalorder, sales_order_detail.total_nilai_discount
        # faktur.pajak, faktur.total_penjualan, faktur.subtotal_diskon, draft_voucher, draft_voucher_detail
        
        # Fetch required parameters
        id_draft_voucher = int(self.req('id'))
        id_sales_order = int(self.req('id_sales_order'))
        nilai_diskon = float(self.req('nilai_diskon'))  # Ensure numeric type
        voucher_regular_detail = self.req('draft_voucher_detail')  # List of details

        # Fetch tax percentage
        tax_entry = global_table.query.filter(global_table.key_column == "pajak").first()
        if not tax_entry:
            raise ValueError("Tax configuration not found.")
        persen_pajak = int(tax_entry.value_column)

        # Update faktur
        faktur_entry = faktur.query.filter(faktur.id_sales_order == id_sales_order).first()
        if not faktur_entry:
            raise ValueError(f"Faktur for sales order ID {id_sales_order} not found.")
        
        faktur_entry.subtotal_diskon -= nilai_diskon
        faktur_entry.subtotal_penjualan += nilai_diskon

        self.flush()
        
        # Recalculate and update tax and total_penjualan
        new_tax = (persen_pajak / 100) * faktur_entry.subtotal_penjualan
        faktur_entry.pajak = new_tax
        faktur_entry.total_penjualan = faktur_entry.subtotal_penjualan + new_tax

        # Update draft voucher status
        draft_voucher_entry = draft_voucher.query.filter(draft_voucher.id == id_draft_voucher).first()
        if not draft_voucher_entry:
            raise ValueError(f"Draft voucher with ID {id_draft_voucher} not found.")
        draft_voucher_entry.status_klaim = 2

        # Fetch and process draft voucher details
        draft_voucher_details = draft_voucher_detail.query.filter(
            draft_voucher_detail.id_draft_voucher == id_draft_voucher
        ).all()

        # Aggregate changes for sales_order_detail updates
        changes = {}
        for detail in draft_voucher_details:
            if detail.id_produk not in changes:
                changes[detail.id_produk] = {"add_subtotal": 0, "subtract_discount": 0}
            changes[detail.id_produk]["add_subtotal"] += detail.nilai_discount
            changes[detail.id_produk]["subtract_discount"] -= detail.nilai_discount

        # Process voucher regular details
        for vd in voucher_regular_detail:
            if vd['id_produk'] not in changes:
                changes[vd['id_produk']] = {"add_subtotal": 0, "subtract_discount": 0}
            changes[vd['id_produk']]["add_subtotal"] += vd['nilai_discount']

        # Bulk update sales_order_detail
        for id_produk, change in changes.items():
            sales_detail = sales_order_detail.query.filter(
                sales_order_detail.id_produk == id_produk,
                sales_order_detail.id_sales_order == id_sales_order
            ).first()
            if not sales_detail:
                raise ValueError(f"Sales order detail for product ID {id_produk} not found.")
            
            sales_detail.subtotalorder += change["add_subtotal"]
            sales_detail.total_nilai_discount -= change["subtract_discount"]

        # Commit transaction
        self.flush().commit()
        return {"status": "success"}, 200
        
    @handle_error_rollback
    def declineProductVoucher(self):
        # kolom kolom maupun tabel yang akan berubah menggunakan method ini :
        # draft_voucher_2.status_klaim, sales_order_detail.subtotalorder, sales_order_detail.total_nilai_discount
        # faktur.pajak, faktur.total_penjualan, faktur.subtotal_diskon, sales_order_detail.vouchers
        
        # Fetch required parameters
        id_draft_voucher_2 = self.req('id_draft_voucher_2')
        id_sales_order = int(self.req('id_sales_order'))
        id_order_detail = int(self.req('id_order_detail'))
        kode_voucher = self.req('kode')
        nilai_diskon = self.req('nilai_diskon')

        # Fetch tax percentage
        tax_entry = global_table.query.filter(global_table.key_column == "pajak").first()
        if not tax_entry:
            raise ValueError("Tax configuration not found.")
        persen_pajak = int(tax_entry.value_column)

        # Update voucher status to declined (2)
        draft_voucher = draft_voucher_2.query.filter(draft_voucher_2.id == id_draft_voucher_2).first()
        if not draft_voucher:
            raise ValueError(f"Draft voucher with ID {id_draft_voucher_2} not found.")
        draft_voucher.status_klaim = 2

        # Update sales_order_detail
        order_detail = sales_order_detail.query.filter(sales_order_detail.id == id_order_detail).first()
        if not order_detail:
            raise ValueError(f"Order detail with ID {id_order_detail} not found.")
        
        order_detail.subtotalorder += nilai_diskon
        order_detail.total_nilai_discount -= nilai_diskon

        # Recalculate total order and update related fields
        sales_details = sales_order_detail.query.filter(
            sales_order_detail.id_sales_order == id_sales_order
        ).all()
        subtotal_order = sum(detail.subtotalorder for detail in sales_details)

        faktur_entry = faktur.query.filter(faktur.id_sales_order == id_sales_order).first()
        if not faktur_entry:
            raise ValueError(f"Faktur for sales order ID {id_sales_order} not found.")
        
        new_tax = (persen_pajak / 100) * subtotal_order
        faktur_entry.pajak = new_tax
        faktur_entry.total_penjualan = subtotal_order + new_tax
        faktur_entry.subtotal_diskon -= nilai_diskon
        faktur_entry.subtotal_penjualan += nilai_diskon

        # Update voucher list in sales_order_detail
        vouchers = [json.loads(item) for item in order_detail.vouchers]
        updated_vouchers = [json.dumps(v) for v in vouchers if v.get("kode") != kode_voucher]
        order_detail.vouchers = updated_vouchers

        # Commit the transaction
        self.flush().commit()
        return {"status": "success"}, 200

    @handle_error_rollback
    def useVoucher(self):
        """
        Memproses status voucher produk berdasarkan status active dari frontend.
        Mengubah status_promo pada draft_voucher menjadi 1 jika active, dan 3 jika tidak active.
        """
        # Ambil data dari request
        vouchers_data = self.req('vouchers')
        id_sales_order = self.req('id_sales_order')

        # Default result dan status code
        result = {"status": "Sukses memperbarui status voucher"}
        status_code = 200

        # Cek apakah ada data voucher produk
        if not vouchers_data or 'voucher_product' not in vouchers_data or not vouchers_data['voucher_product']:
            return {
                "status": "success with message",
                "message": "Tidak ada voucher yang perlu diperbarui"
            }, 200

        voucher_product_list = vouchers_data['voucher_product']

        # Iterasi setiap item voucher produk
        for product_item in voucher_product_list:
            id_sales_order_detail = product_item['id_sales_order_detail']
            voucher_status = product_item.get('voucher_status', {})

            # Proses status voucher berdasarkan tipe
            for voucher_type, is_active in voucher_status.items():
                # Tentukan tipe_voucher berdasarkan key (v1_active -> 1, v2_active -> 2, v3_active -> 3)
                tipe_voucher = int(voucher_type[1])  # Ekstrak angka dari 'v1_active', 'v2_active', dll

                # Tentukan status_promo berdasarkan nilai active
                status_promo = 1 if is_active else 3

                # Update status_promo di draft_voucher
                draft_entries = draft_voucher.query.filter(
                    draft_voucher.id_sales_order_detail == id_sales_order_detail,
                    draft_voucher.tipe_voucher == tipe_voucher,
                    draft_voucher.id_sales_order == id_sales_order
                ).all()

                if draft_entries:
                    for entry in draft_entries:
                        entry.status_promo = status_promo
                        self.flush()

        # Commit perubahan setelah memproses semua voucher
        self.commit()

        return result, status_code

    @handle_error
    def get_voucher_free_products(self, voucher_list_temp, tableName, columnName):
        voucher_list = []
        # get vouchers free products
        for voucher in voucher_list_temp:
            free_produk_with_produk = []
            free_product = (
                self.query()
                .setRawQuery(
                f"""
                    SELECT * FROM {tableName} WHERE {columnName} = :id_voucher
                """
                )
                .bindparams({"id_voucher": voucher["id"]})
                .execute()
                .fetchall()
                .get()
            )

            for produk in free_product:
                produk["produk"] = (
                    self.query()
                    .setRawQuery(
                    """
                        SELECT * FROM produk WHERE id = :id_produk
                    """
                    )
                    .bindparams({"id_produk": produk["id_produk"]})
                    .execute()
                    .fetchone()
                    .result
                )

                free_produk_with_produk.append(produk)

            voucher["free_produk"] = free_produk_with_produk
            voucher_list.append(voucher)

        return voucher_list

    @handle_error
    def getVoucher_1_reguler(self):
        voucher_list = (
            self.query()
            .setRawQuery(
                """
                    SELECT
                        v1.*
                    FROM
                        voucher_1 v1
                    WHERE v1.status_voucher = 1
                """
            )
            .execute()
            .fetchall()
            .get()
        )
        for voucher in voucher_list:
            voucher["tipe_voucher"] = 1
        return self.get_voucher_free_products(
            voucher_list, "voucher_1_free_produk", "id_voucher_1"
        )

    @handle_error
    def getVoucher_2_produk(self,id_produk):
        id_cabang = self.req("id_cabang")
        current_date = date_now()


        if not id_produk or not id_cabang:
            raise nonServerErrorException("id_produk and id_cabang are required")
        voucher_list = (
            self.query()
            .setRawQuery(
                """
                    SELECT
                        v2.*,
                        p.id as id_produk_asli,
                        p.nama as nama_produk,
                        v2c.id_cabang
                    FROM 
                        voucher_2 v2
                    LEFT JOIN voucher_2_produk v2p ON v2.id = v2p.id_voucher
                    LEFT JOIN produk p ON v2p.id_produk = p.id 
                    LEFT JOIN voucher_2_cabang v2c ON v2.id = v2c.id_voucher
                    WHERE 
                        p.id = :id_produk 
                        AND v2c.id_cabang = :id_cabang 
                        AND :current_date >= v2.tanggal_mulai
                        AND :current_date <= v2.tanggal_kadaluarsa
                        and v2.status_voucher = 1
                """
            )
            .bindparams({
                "id_produk": id_produk,
                "id_cabang": id_cabang,
                "current_date": current_date
            })
            .execute()
            .fetchall()
            .get()
        )

        return self.get_voucher_free_products(
            voucher_list, "voucher_2_free_produk", "id_voucher_2"
        )

    @handle_error
    def getVoucher_2_reguler(self):
        voucher_list = (
            self.query()
            .setRawQuery(
                """
                    SELECT
                        v2.*
                    FROM 
                        voucher_2 v2
                    where v2.is_reguler = 1 and status_voucher = 1
                """
            )
            .execute()
            .fetchall()
            .get()
        )
        for voucher in voucher_list:
            voucher["tipe_voucher"] = 2
        return self.get_voucher_free_products(
            voucher_list, "voucher_2_free_produk", "id_voucher_2"
        )

    @handle_error
    def getVoucher_3_produk(self,id_produk):
        id_cabang = self.req("id_cabang")
        id_customer = self.req("id_customer")
        current_date = date_now()

        if not id_produk or not id_cabang or not id_customer:
            raise nonServerErrorException("id_produk, id_cabang, and id_customer are required")

        voucher_list = (
            self.query()
            .setRawQuery(
                """
                    SELECT
                        v3.*,
                        p.id as id_produk_asli,
                        p.nama as nama_produk,
                        v3c.id_cabang,
                        v3cu.id_customer
                    FROM 
                        voucher_3 v3
                    LEFT JOIN voucher_3_produk v3p ON v3.id = v3p.id_voucher
                    LEFT JOIN produk p ON v3p.id_produk = p.id 
                    LEFT JOIN voucher_3_cabang v3c ON v3.id = v3c.id_voucher
                    LEFT JOIN voucher_3_customer v3cu ON v3.id = v3cu.id_voucher
                    WHERE 
                        p.id = :id_produk 
                        AND v3c.id_cabang = :id_cabang 
                        AND v3cu.id_customer = :id_customer 
                        AND :current_date >= v3.tanggal_mulai
                        AND :current_date <= v3.tanggal_kadaluarsa
                        and v3.status_voucher = 1
                """
            )
            .bindparams({
                "id_produk": id_produk,
                "id_cabang": id_cabang,
                "id_customer": id_customer,
                "current_date": current_date
            })
            .execute()
            .fetchall()
            .get()
        )

        return self.get_voucher_free_products(
            voucher_list, "voucher_3_free_produk", "id_voucher_3"
        )

    @handle_error
    def getVoucher_3_reguler(self):
        voucher_list = (
            self.query()
            .setRawQuery(
                """
                    SELECT
                        v3.*
                    FROM 
                        voucher_3 v3
                 
                    WHERE v3.is_reguler = 1 and v3.status_voucher = 1
                """
            )
            .execute()
            .fetchall()
            .get()
        )
        for voucher in voucher_list:
            voucher["tipe_voucher"] = 3
        return self.get_voucher_free_products(
            voucher_list, "voucher_3_free_produk", "id_voucher_3"
        )

    @handle_error
    def getVoucher_2_produk_all(self):
        current_date = date_now()
        voucher_list = (
            self.query()
            .setRawQuery(
                """
                    SELECT 
                        v2.*,
                        ARRAY_AGG(DISTINCT p.id) AS produk_ids,
                        ARRAY_AGG(DISTINCT p.nama) AS produk_names,
                        ARRAY_AGG(DISTINCT c.id) AS cabang_ids,
                        ARRAY_AGG(DISTINCT c.nama) AS cabang_names
                    FROM 
                        voucher_2 v2
                    LEFT JOIN voucher_2_produk v2p ON v2.id = v2p.id_voucher
                    LEFT JOIN produk p ON v2p.id_produk = p.id 
                    LEFT JOIN voucher_2_cabang v2c ON v2.id = v2c.id_voucher
                    LEFT JOIN cabang c ON v2c.id_cabang = c.id
                    WHERE 
                        :current_date >= v2.tanggal_mulai
                        AND :current_date <= v2.tanggal_kadaluarsa
                        AND v2.status_voucher = 1
                    GROUP BY v2.id
                """
            ).bindparams({"current_date": current_date})
            .execute()
            .fetchall()
            .get()
        )
        for voucher in voucher_list:
            voucher["tipe_voucher"] = 2
        return self.get_voucher_free_products(
            voucher_list, "voucher_2_free_produk", "id_voucher_2"
        )

    @handle_error
    def getVoucher_3_produk_all(self):
        current_date = date_now()
        voucher_list = (
            self.query()
            .setRawQuery(
                """
                    SELECT 
                        v3.*,
                        ARRAY_AGG(DISTINCT p.id) AS produk_ids,
                        ARRAY_AGG(DISTINCT p.nama) AS produk_names,
                        ARRAY_AGG(DISTINCT c.id) AS cabang_ids,
                        ARRAY_AGG(DISTINCT c.nama) AS cabang_names,
                        ARRAY_AGG(DISTINCT cu.id) AS customer_ids,
                        ARRAY_AGG(DISTINCT cu.nama) AS customer_names
                    FROM 
                        voucher_3 v3
                    LEFT JOIN voucher_3_produk v3p ON v3.id = v3p.id_voucher
                    LEFT JOIN produk p ON v3p.id_produk = p.id 
                    LEFT JOIN voucher_3_cabang v3c ON v3.id = v3c.id_voucher
                    LEFT JOIN cabang c ON v3c.id_cabang = c.id
                    LEFT JOIN voucher_3_customer v3cu ON v3.id = v3cu.id_voucher
                    LEFT JOIN customer cu ON v3cu.id_customer = cu.id
                    WHERE 
                        :current_date >= v3.tanggal_mulai
                        AND :current_date <= v3.tanggal_kadaluarsa
                        AND v3.status_voucher = 1
                    GROUP BY v3.id
                """
            ).bindparams({"current_date": current_date})
            .execute()
            .fetchall()
            .get()
        )
        for voucher in voucher_list:
            voucher["tipe_voucher"] = 3
        return self.get_voucher_free_products(
            voucher_list, "voucher_3_free_produk", "id_voucher_3"
        )

    @handle_error
    def getVoucherById(self, tipe):
        id_voucher = int(self.req("id_voucher"))
        voucher_models = {1: voucher_1, 2: voucher_2, 3: voucher_3}
        voucher_object = voucher_models.get(tipe)
        if not voucher_object:
            raise nonServerErrorException("Tipe voucher tidak valid.")

        voucher = voucher_object.query.filter(voucher_object.id == id_voucher).first()
        if not voucher:
            raise nonServerErrorException("Voucher tidak ditemukan.")

        # Konversi objek voucher ke dictionary untuk menampilkan semua atribut
        voucher_dict = {}
        for column in voucher_object.__table__.columns:
            voucher_dict[column.name] = getattr(voucher, column.name)

        # Tambahkan daftar kosong untuk produk, cabang, dan customer
        voucher_dict["produk"] = []
        voucher_dict["cabang"] = []
        voucher_dict["customer"] = []

        # Ambil data produk untuk semua tipe voucher (1, 2, 3)
        if tipe == 1:
            produk_list = (
                self.query()
                .setRawQuery(
                    """
                    SELECT vp.id_produk
                    FROM voucher_1_produk vp
                    WHERE vp.id_voucher = :id_voucher
                    """
                )
                .bindparams({"id_voucher": id_voucher})
                .execute()
                .fetchall()
                .get()
            )
            voucher_dict["produk"] = [p["id_produk"] for p in produk_list]

        elif tipe == 2:
            # Ambil data produk untuk tipe voucher 2
            produk_list = (
                self.query()
                .setRawQuery(
                    """
                    SELECT vp.id_produk
                    FROM voucher_2_produk vp
                    WHERE vp.id_voucher = :id_voucher
                    """
                )
                .bindparams({"id_voucher": id_voucher})
                .execute()
                .fetchall()
                .get()
            )
            voucher_dict["produk"] = [p["id_produk"] for p in produk_list]

            # Ambil data cabang untuk tipe voucher 2
            cabang_list = (
                self.query()
                .setRawQuery(
                    """
                    SELECT vc.id_cabang
                    FROM voucher_2_cabang vc
                    WHERE vc.id_voucher = :id_voucher
                    """
                )
                .bindparams({"id_voucher": id_voucher})
                .execute()
                .fetchall()
                .get()
            )
            voucher_dict["cabang"] = [c["id_cabang"] for c in cabang_list]

        elif tipe == 3:
            # Ambil data produk untuk tipe voucher 3
            produk_list = (
                self.query()
                .setRawQuery(
                    """
                    SELECT vp.id_produk
                    FROM voucher_3_produk vp
                    WHERE vp.id_voucher = :id_voucher
                    """
                )
                .bindparams({"id_voucher": id_voucher})
                .execute()
                .fetchall()
                .get()
            )
            voucher_dict["produk"] = [p["id_produk"] for p in produk_list]

            # Ambil data cabang untuk tipe voucher 3
            cabang_list = (
                self.query()
                .setRawQuery(
                    """
                    SELECT vc.id_cabang
                    FROM voucher_3_cabang vc
                    WHERE vc.id_voucher = :id_voucher
                    """
                )
                .bindparams({"id_voucher": id_voucher})
                .execute()
                .fetchall()
                .get()
            )
            voucher_dict["cabang"] = [c["id_cabang"] for c in cabang_list]

            # Ambil data customer untuk tipe voucher 3
            customer_list = (
                self.query()
                .setRawQuery(
                    """
                    SELECT vc.id_customer
                    FROM voucher_3_customer vc
                    WHERE vc.id_voucher = :id_voucher
                    """
                )
                .bindparams({"id_voucher": id_voucher})
                .execute()
                .fetchall()
                .get()
            )
            voucher_dict["customer"] = [cust["id_customer"] for cust in customer_list]

        return voucher_dict