from . import BaseServices
from apps.handler import handle_error, handle_error_rollback, nonServerErrorException
from apps.models import sales_order, sales_order_detail, faktur, draft_voucher
from apps.lib.helper import date_now, time_now
from apps.lib.convert_uom import convert_uom
import bcrypt
from flask import request
from apps.lib.paginate import Paginate
from google.cloud import pubsub_v1
import json

class DMS(BaseServices):
    
    @handle_error
    def getDmsUser(self):
        email = self.req('email')
        password = self.req('password')

        login_query = f"""
            select 
            users.tokens AS token,
            users.id AS id_user,
            users.nama AS nama_user,
            users.email AS user_email,
            users.id_jabatan,
            users.password
            from users 
            where users.email = :email
        """
        login_bindparam = {'email': email}

        user = self.query().setRawQuery(login_query).bindparams(login_bindparam).execute().fetchone().result

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
    
    # @handle_error_rollback
    # def insertDms(self):            
    #     datas = request.json        

    #     publisher_options = pubsub_v1.types.PublisherOptions(enable_message_ordering=True)
    #     client_options = {"api_endpoint": "us-east1-pubsub.googleapis.com:443"}
    #     publisher = pubsub_v1.PublisherClient(
    #         publisher_options=publisher_options, client_options=client_options
    #     )
    #     topic_name = 'budimas-topic'        
    #     topic_path = publisher.topic_path('ptbudimas', topic_name)
        
    #     datas_str = json.dumps(datas)
        
    #     publisher.publish(topic_path, data=datas_str.encode("utf-8"))                
                        
    #     return {"status": "success"}, 200                           
    
    # @handle_error_rollback
    # def processDms(self):            
    #     datas = request.json
    #     datas = datas.get("data")

    #     datas = json.loads(datas)
        
    #     for data in datas:  
    #         id_user = self.query().setRawQuery("select id from users where nama = :nama").bindparams({"nama": data["route_name"].split('-')[1]}).execute().fetchone().result

    #         if id_user is None or id_user == {}:
    #             raise nonServerErrorException(f"sales dengan nama {data['route_name'].split('-')[1]} tidak ada", 400)
            
    #         id_sales = self.query().setRawQuery("select id from sales where id_user = :id_user").bindparams({"id_user": int(id_user["id"])}).execute().fetchone().result            

    #         id_customer = self.query().setRawQuery("select id from customer where kode = :kode").bindparams({"kode": data["customer_code"].split('-')[1]}).execute().fetchone().result
    #         if id_customer is None:
    #             raise nonServerErrorException(f"customer tidak tersedia pada sales order {data['invoice_no']}", 400)

    #         id_principal = None
    #         index = 0
    #         while id_principal is None:
    #             id_principal = self.query().setRawQuery("select id_principal from produk where kode_sku = :kode_sku").bindparams({"kode_sku": data["detail"][index]["product_code"]}).execute().fetchone().result
    #             index += 1                
    #             if id_principal is None and index == len(data["detail"]) - 1:
                    
    #                 raise nonServerErrorException(f"principal tidak tersedia pada sales order {data['invoice_no']}", 400)                                    
                                    
    #         id_plafon = self.query().setRawQuery("select id, id_principal, id_sales from plafon where id_sales = :id_sales and id_principal = :id_principal and id_customer = :id_customer").bindparams({"id_sales": id_sales['id'], "id_principal": id_principal['id_principal'], "id_customer": id_customer['id']}).execute().fetchone().result
    #         print(id_plafon)
    #         if id_plafon is None or id_plafon == {}:
    #             raise nonServerErrorException(f"plafon tidak tersedia pada sales order {data['invoice_no']}", 400)
                        
    #         if id_plafon is None:
    #             raise nonServerErrorException(f"plafon tidak tersedia pada sales order {data['invoice_no']}", 400)
            
    #         insert_sales_order = sales_order(
    #             id_plafon=id_plafon['id'],
    #             no_order=data["order_no"],
    #             tanggal_order=data["order_date"],                
    #         )
    #         self.add(insert_sales_order).flush()
            
    #         insert_faktur = faktur(
    #             id_sales_order=insert_sales_order.id,
    #             no_faktur=data["invoice_no"],
    #             status_faktur=0,
    #             subtotal_penjualan=data["total_amount_after_customer_discount"],
    #             pajak=float(data["tax_amount"]),
    #             total_penjualan=float(data["total_net_amount"]),
    #         )
    #         self.add(insert_faktur).flush()
    #         insert_draft_voucher = draft_voucher(
    #             id_sales_order=insert_sales_order.id,
    #             discount=float(data["customer_discount_percentage"]),
    #             jumlah_diskon=float(data["customer_discount_amount"]),
    #         )
    #         self.add(insert_draft_voucher).flush()                                    
            
    #         kode_sku_all = []
            
    #         for detail in data["detail"]:
    #             kode_sku_all.append(detail["product_code"])
                
    #         tuple_sku = ', '.join([f"'{i}'" for i in kode_sku_all])

    #         produk_uom_with_id = self.query().setRawQuery(
    #         "select produk.id, produk.kode_sku, produk_uom.faktor_konversi, produk_uom.level, produk_uom.id_produk from produk left join produk_uom on produk.id = produk_uom.id_produk where produk.kode_sku IN ("+tuple_sku+")"
    #         ).execute().fetchall().get()


            
    #         for detail in data["detail"]:
    #             id_produk = next((item["id"] for item in produk_uom_with_id if item["kode_sku"] == detail["product_code"]), None)
    #             print(id_produk)
    #             if id_produk is None:
    #                 raise nonServerErrorException(f"produk tidak tersedia pada sales order {data['invoice_no']}", 400)
    #             print(id_produk)
    #             faktor_konversi_level_2 = next((item["faktor_konversi"] for item in produk_uom_with_id if item["id_produk"] == id_produk and item["level"] == 2), None)
    #             print(faktor_konversi_level_2)
                
    #             faktor_konversi_level_3 = next((item["faktor_konversi"] for item in produk_uom_with_id if item["id_produk"] == id_produk and item["level"] == 3), None)
    #             print(faktor_konversi_level_3)
                
    #             qty_level_2 = 0 
    #             qty_level_3 = 0
                
    #             if faktor_konversi_level_2 is  None or faktor_konversi_level_3 is None:
    #                 raise nonServerErrorException(f"konversi uom tidak tersedia pada sales order {data['invoice_no']}", 400)
                
    #             qty_produk = detail["product_quantity"]
                                
    #             result_convert = convert_uom({
    #                     "pieces": qty_produk,
    #                 },{
    #                     "pieces":1,
    #                     "box":faktor_konversi_level_2,
    #                     "karton":faktor_konversi_level_3
    #                 }).to_uoms().get()
                
    #             if int(qty_produk) > faktor_konversi_level_2:
    #                 qty_level_2 = result_convert["box"]                    
                
    #             if int(qty_produk) > faktor_konversi_level_3:
    #                 qty_level_3 = result_convert["karton"]
                
                
                
    #             insert_sales_order_detail = sales_order_detail(
    #                 id_sales_order=insert_sales_order.id,
    #                 id_produk=int(id_produk),
    #                 subtotalorder=float(detail["amount_after_sku_disc"]),
    #                 total_nilai_discount=float(detail["discount_amount"]) +float( detail["customer_discount"]),
    #                 pieces_order=int(detail["product_quantity"]),
    #                 box_order=qty_level_2,
    #                 karton_order=qty_level_3,                    
    #             )
    #             self.add(insert_sales_order_detail).flush()

    #     self.commit()

    #     return {"status": "success"}, 200
    @handle_error_rollback
    def insertDms(self):            
        datas = request.json
        datas = datas.get("data")

        # datas = json.loads(datas)
        
        for data in datas:  
            id_user = self.query().setRawQuery("select id from users where nama = :nama").bindparams({"nama": data["route_name"].split('-')[1]}).execute().fetchone().result

            if id_user is None or id_user == {}:
                raise nonServerErrorException(f"sales dengan nama {data['route_name'].split('-')[1]} tidak ada", 400)
            
            id_sales = self.query().setRawQuery("select id from sales where id_user = :id_user").bindparams({"id_user": int(id_user["id"])}).execute().fetchone().result            

            id_customer = self.query().setRawQuery("select id from customer where kode = :kode").bindparams({"kode": data["customer_code"].split('-')[1]}).execute().fetchone().result
            if id_customer is None:
                raise nonServerErrorException(f"customer tidak tersedia pada sales order {data['invoice_no']}", 400)

            id_principal = None
            index = 0
            while id_principal is None:
                id_principal = self.query().setRawQuery("select id_principal from produk where kode_sku = :kode_sku").bindparams({"kode_sku": data["detail"][index]["product_code"]}).execute().fetchone().result
                index += 1                
                if id_principal is None and index == len(data["detail"]) - 1:
                    
                    raise nonServerErrorException(f"principal tidak tersedia pada sales order {data['invoice_no']}", 400)                                    
                                    
            id_plafon = self.query().setRawQuery("select id, id_principal, id_sales from plafon where id_sales = :id_sales and id_principal = :id_principal and id_customer = :id_customer").bindparams({"id_sales": id_sales['id'], "id_principal": id_principal['id_principal'], "id_customer": id_customer['id']}).execute().fetchone().result
            print(id_plafon)
            if id_plafon is None or id_plafon == {}:
                raise nonServerErrorException(f"plafon tidak tersedia pada sales order {data['invoice_no']}", 400)
                        
            if id_plafon is None:
                raise nonServerErrorException(f"plafon tidak tersedia pada sales order {data['invoice_no']}", 400)
            
            insert_sales_order = sales_order(
                id_plafon=id_plafon['id'],
                no_order=data["order_no"],
                tanggal_order=data["order_date"],                
            )
            self.add(insert_sales_order).flush()
            
            insert_faktur = faktur(
                id_sales_order=insert_sales_order.id,
                no_faktur=data["invoice_no"],
                status_faktur=0,
                subtotal_penjualan=data["total_amount_after_customer_discount"],
                pajak=float(data["tax_amount"]),
                total_penjualan=float(data["total_net_amount"]),
            )
            self.add(insert_faktur).flush()
            insert_draft_voucher = draft_voucher(
                id_sales_order=insert_sales_order.id,
                discount=float(data["customer_discount_percentage"]),
                jumlah_diskon=float(data["customer_discount_amount"]),
            )
            self.add(insert_draft_voucher).flush()                                    
            
            kode_sku_all = []
            
            for detail in data["detail"]:
                kode_sku_all.append(detail["product_code"])
                
            tuple_sku = ', '.join([f"'{i}'" for i in kode_sku_all])

            produk_uom_with_id = self.query().setRawQuery(
            "select produk.id, produk.kode_sku, produk_uom.faktor_konversi, produk_uom.level, produk_uom.id_produk from produk left join produk_uom on produk.id = produk_uom.id_produk where produk.kode_sku IN ("+tuple_sku+")"
            ).execute().fetchall().get()


            
            for detail in data["detail"]:
                id_produk = next((item["id"] for item in produk_uom_with_id if item["kode_sku"] == detail["product_code"]), None)
                print(id_produk)
                if id_produk is None:
                    raise nonServerErrorException(f"produk tidak tersedia pada sales order {data['invoice_no']}", 400)
                print(id_produk)
                faktor_konversi_level_2 = next((item["faktor_konversi"] for item in produk_uom_with_id if item["id_produk"] == id_produk and item["level"] == 2), None)
                print(faktor_konversi_level_2)
                
                faktor_konversi_level_3 = next((item["faktor_konversi"] for item in produk_uom_with_id if item["id_produk"] == id_produk and item["level"] == 3), None)
                print(faktor_konversi_level_3)
                
                qty_level_2 = 0 
                qty_level_3 = 0
                
                if faktor_konversi_level_2 is  None or faktor_konversi_level_3 is None:
                    raise nonServerErrorException(f"konversi uom tidak tersedia pada sales order {data['invoice_no']}", 400)
                
                qty_produk = detail["product_quantity"]
                                
                result_convert = convert_uom({
                        "pieces": qty_produk,
                    },{
                        "pieces":1,
                        "box":faktor_konversi_level_2,
                        "karton":faktor_konversi_level_3
                    }).to_uoms().get()
                
                if int(qty_produk) > faktor_konversi_level_2:
                    qty_level_2 = result_convert["box"]                    
                
                if int(qty_produk) > faktor_konversi_level_3:
                    qty_level_3 = result_convert["karton"]
                
                
                
                insert_sales_order_detail = sales_order_detail(
                    id_sales_order=insert_sales_order.id,
                    id_produk=int(id_produk),
                    subtotalorder=float(detail["amount_after_sku_disc"]),
                    total_nilai_discount=float(detail["discount_amount"]) +float( detail["customer_discount"]),
                    pieces_order=int(detail["product_quantity"]),
                    box_order=qty_level_2,
                    karton_order=qty_level_3,                    
                )
                self.add(insert_sales_order_detail).flush()

        self.commit()

        return {"status": "success"}, 200