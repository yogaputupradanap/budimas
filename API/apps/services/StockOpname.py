from . import BaseServices
from apps.handler import handle_error, handle_error_rollback, nonServerErrorException
from apps.models import stock_opname, stock_opname_detail, LogInventory, Stok
from apps.lib.helper import date_now, time_now
from flask import request, current_app
from apps.lib.paginate import Paginate
import bcrypt

class StockOpname(BaseServices):
    
    @handle_error
    def getStockOpnameUser(self):
        email = self.req('email')
        password = self.req('password')
        
        user_info = (
            self.query().setRawQuery(
                """
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
                    id_jabatan in (9,10,2)        
                """
            )
            .bindparams({"email":email})
            .execute()
            .fetchone()
            .result
        )
                        
        if not len(user_info):
            raise nonServerErrorException("Email salah atau tidak ada", 401)

        if not bcrypt.checkpw(password.encode("utf-8"), user_info["password"].encode()):
            raise nonServerErrorException("Password salah", 401)

        return user_info
    
    @handle_error
    def getProduksStockOpname(self):
        id_principal = self.req('id_principal')
        
        data_produks= self.query().setRawQuery(
                """
                    select
                    produk.id AS id_produk,
                    produk.nama AS nama_produk,
                    produk.harga_beli AS harga_produk,
                    produk.id_brand,
                    produk.id_principal,
                    produk.kode_sku AS sku,
                    produk_uom.*
                    from produk
                    left join produk_uom on produk.id = produk_uom.id_produk
                    where produk.id_principal = :id_principal
                """
            ).bindparams({"id_principal":id_principal}).execute().fetchall().get()                    
        
        datas = []
        
        if not data_produks:
            return datas
        for data_produk in data_produks:
            if datas:
                exits = list(filter(lambda x: x["id_produk"] == data_produk["id_produk"], datas))
                if not exits:
                    data = {
                            "id_produk":data_produk["id_produk"],
                            "nama_produk":data_produk["nama_produk"],
                            "harga_produk":data_produk["harga_produk"],
                            "id_principal":data_produk["id_principal"],
                            "sku":data_produk["sku"],
                            "jumlah_uom_1":0,
                            "keterangan":"",
                            "jumlah_uom_2":0,
                            "jumlah_uom_3":0,                                        
                            "bad_stock":0,
                            "total":0,
                            "id_brand":data_produk["id_brand"],
                            "stock":0
                    }
                    if data_produk["level"] == 1:
                        data["label_uom_1"] = data_produk["nama"]
                        data["konversi_uom_1"] = data_produk["faktor_konversi"]
                    elif data_produk["level"] == 2:
                        data["label_uom_2"] = data_produk["nama"]
                        data["konversi_uom_2"] = data_produk["faktor_konversi"]
                    elif data_produk["level"] == 3:
                        data["label_uom_3"] = data_produk["nama"]
                        data["konversi_uom_3"] = data_produk["faktor_konversi"]
                    datas.append(data)
                else:
                    if data_produk["level"] == 1:
                        exits[0]["label_uom_1"] = data_produk["nama"]
                        exits[0]["konversi_uom_1"] = data_produk["faktor_konversi"]
                    elif data_produk["level"] == 2:
                        exits[0]["label_uom_2"] = data_produk["nama"]
                        exits[0]["konversi_uom_2"] = data_produk["faktor_konversi"]
                    elif data_produk["level"] == 3:
                        exits[0]["label_uom_3"] = data_produk["nama"]                      
                        exits[0]["konversi_uom_3"] = data_produk["faktor_konversi"]                        
            else:
                data = {
                            "id_produk":data_produk["id_produk"],
                            "nama_produk":data_produk["nama_produk"],
                            "harga_produk":data_produk["harga_produk"],
                            "id_principal":data_produk["id_principal"],
                            "sku":data_produk["sku"],
                            "jumlah_uom_1":0,
                            "jumlah_uom_2":0,
                            "keterangan":"",
                            "jumlah_uom_3":0,                                        
                            "bad_stock":0,
                            "id_brand":data_produk["id_brand"],
                            "total":0,
                            "stock":0
                    }
                if data_produk["level"] == 1:
                    data["label_uom_1"] = data_produk["nama"]
                    data["konversi_uom_1"] = data_produk["faktor_konversi"]
                elif data_produk["level"] == 2:
                    data["label_uom_2"] = data_produk["nama"]
                    data["konversi_uom_2"] = data_produk["faktor_konversi"]
                elif data_produk["level"] == 3:
                    data["label_uom_3"] = data_produk["nama"]
                    data["konversi_uom_3"] = data_produk["faktor_konversi"]
                datas.append(data)
        return datas              
    
    @handle_error_rollback
    def createStockOpname(self):
        data_produks = self.req("data_produks")
        id_cabang = self.req("id_cabang")
        id_principal = self.req("id_principal")
        kode_so = self.req("kode_so")
        total = self.req("total")
        ket_so = self.req("keterangan")
        tanggal_so = date_now()
        status_so = "under review"
        id_user_input = self.req("id_user_input")            
        total_selisih = self.req("total_selisih")
        
        add_stock_opname = stock_opname(
            id_principal=id_principal,
            id_cabang=id_cabang,
            kode_so=kode_so,
            total=total,
            ket_so=ket_so,
            tanggal_so=tanggal_so,
            status_so=status_so,
            id_user_input=id_user_input   ,   
            total_selisih=total_selisih                  
        )
        
        self.add(add_stock_opname).flush()
        
        for data_produk in data_produks:            
            
            subtotal_selisih = (data_produk["stock"] - data_produk["stock_system"] ) * data_produk["harga_produk"]
            
            add_stock_opname_detail = stock_opname_detail(
                id_stock_opname=add_stock_opname.id_stock_opname,
                id_produk=data_produk["id_produk"],
                uom_1=data_produk["jumlah_uom_1"],
                uom_2=data_produk["jumlah_uom_2"],
                uom_3=data_produk["jumlah_uom_3"],
                bad_stock=data_produk["bad_stock"],
                harga=data_produk["harga_produk"],
                stok=data_produk["stock"],
                subtotal=data_produk["total"],
                ket_produk=data_produk["keterangan"],
                stok_sistem=data_produk["stock_system"],
                subtotal_selisih=subtotal_selisih
            )
            self.add(add_stock_opname_detail).flush()
        
        self.commit()
        
        return {"status":"success"}, 200

    @handle_error
    def getAllStockOpname(self):        
        bindParams = {"id_cabang":self.req('id_cabang')}
        status_so = self.req("status_so")

        where_clause = f"where stock_opname.id_cabang = :id_cabang"
        
        if status_so:
            where_clause += " AND stock_opname.status_so = :status_so"
            bindParams["status_so"] = status_so
        
        query = f"""
            SELECT stock_opname.*,
            principal.nama as nama_principal,
            COUNT(stock_opname_detail) as produk_count
            FROM stock_opname
            LEFT JOIN principal on stock_opname.id_principal = principal.id
            LEFT JOIN stock_opname_detail on stock_opname.id_stock_opname = stock_opname_detail.id_stock_opname
            {where_clause}
            GROUP BY  stock_opname.id_stock_opname,
        stock_opname.id_principal,
        stock_opname.id_cabang,
        stock_opname.kode_so,
        stock_opname.total,
        stock_opname.ket_so,
        stock_opname.tanggal_so,
        stock_opname.status_so,
        stock_opname.id_user_input, principal.nama
        """
        return Paginate(request, query, bindParams).paginate()
    
    @handle_error_rollback
    def stockOpnameDiterima(self):
        id_stock_opname = self.req("id_stock_opname")
        id_user = self.req("id_user")
        id_cabang = self.req("id_cabang")
        data_produks = self.req("data_produks")
        
        result_uom = self.query().setRawQuery("""
            SELECT 
            stock_opname_detail.*, 
            produk_uom.* 
            FROM 
            stock_opname_detail 
            LEFT JOIN 
            produk_uom 
            ON 
            stock_opname_detail.id_produk = produk_uom.id_produk 
            WHERE 
            stock_opname_detail.id_stock_opname = :id_stock_opname AND
            produk_uom.level = 1            
            """).bindparams({"id_stock_opname":int(id_stock_opname)}).execute().fetchall().get()
        
        
        for produk in data_produks:
            is_stock_produk_ready = stok.query.filter(
                stok.cabang_id == int(id_cabang),
                stok.produk_id == produk["id_produk"]
            ).first()
            level1 = list(filter(lambda x: x["id_produk"] == produk["id_produk"], result_uom))            
            if not is_stock_produk_ready:
                add_stock = stok(
                    cabang_id=id_cabang,
                    produk_id=produk["id_produk"],
                    jumlah_ready=produk["stok"],
                    jumlah_booked=0,
                    jumlah_delivery=0,
                    jumlah_incoming=0,
                    jumlah_gudang=produk["stok"],
                    jumlah_canvas = 0,
                    jumlah_good = produk["stok"],
                    jumlah_bad = produk["bad_stock"],
                    tanggal_update=date_now(),
                    waktu_update=time_now(),
                    jumlah_picked=0,
                    transfer_out=0,
                    transfer_in=0                    
                )
                self.add(add_stock).flush()
                add_log_invetory = log_inventory(
                    id_transaksi=id_stock_opname,
                    id_cabang=id_cabang,
                    id_transaksi_tipe=11,
                    id_produk=produk["id_produk"],
                    produk_uom_id=level1[0]["id"],
                    id_user=id_user,
                    stok_awal=0,
                    stok_peralihan=produk["stok"],
                    stok_akhir=produk["stok"],
                    harga=produk["harga"],
                    tanggal=date_now(),
                    valuasi=0,
                    waktu=time_now(),
                    keterangan="Stock Opname"
                )
                self.add(add_log_invetory).flush()
            else:
                add_log_invetory = log_inventory(
                    id_transaksi=id_stock_opname,
                    id_cabang=id_cabang,
                    id_transaksi_tipe=11,
                    id_produk=produk["id_produk"],
                    produk_uom_id=level1[0]["id"],
                    id_user=id_user,
                    stok_awal=is_stock_produk_ready.jumlah_ready,
                    stok_peralihan=produk["stok"]-is_stock_produk_ready.jumlah_ready,
                    stok_akhir=produk["stok"],
                    harga=produk["harga"],
                    tanggal=date_now(),
                    valuasi=0,
                    waktu=time_now(),
                    keterangan="Stock Opname"
                )
                self.add(add_log_invetory).flush()                           
                
                is_stock_produk_ready.jumlah_ready = produk["stok"]
                is_stock_produk_ready.jumlah_gudang = produk["stok"]
                is_stock_produk_ready.jumlah_good = produk["stok"]
                is_stock_produk_ready.jumlah_bad = produk["bad_stock"]
                is_stock_produk_ready.tanggal_update = date_now()
                is_stock_produk_ready.waktu_update = time_now()
                self.flush()     
            
        stock_opname_update = stock_opname.query.filter(
            stock_opname.id_stock_opname == int(id_stock_opname)
        ).first()

        if not stock_opname_update:
            raise nonServerErrorException("Stock Opname tidak ditemukan", 404)
        
        stock_opname_update.status_so = "completed"
        stock_opname_update.id_verifikator = id_user
        stock_opname_update.waktu_verifikasi = time_now()

        profile = self.query().setRawQuery("""
            SELECT p.id_perusahaan FROM
                principal p
                WHERE p.id = :id_principal
                """).bindparams({"id_principal": stock_opname_update.id_principal}).execute().fetchone().result

        pubsub = getattr(current_app, 'pubsub', None)
        payload_pubsub = {
            "id_fitur_mal": 7,
            "id_cabang": id_cabang,
            "id_perusahaan": profile["id_perusahaan"] if profile else None,
            "id_stock_opname": id_stock_opname,
            "id_principal": stock_opname_update.id_principal,
            "created_by": id_user,
        }

        if pubsub:
            success = pubsub.publish(data=payload_pubsub, topic="create_jurnal")
            if not success:
                current_app.logger.error(f'Gagal publish ke topic create_jurnal, payload: {payload_pubsub}')
                raise nonServerErrorException("Gagal publish ke topic create_jurnal", 500)
            else:
                current_app.logger.info(f'Sukses publish ke topic create_jurnal, payload: {payload_pubsub}')
        else:
            current_app.logger.error('Pubsub client tidak tersedia')
            raise nonServerErrorException(status_code=500, message='Gagal mengirim pesan ke sistem jurnal')

        self.commit()

        return {"status":"success"}, 200

    @handle_error_rollback
    def stockOpnameDitolak(self):
        id_stock_opname = self.req("id_stock_opname")
        id_user = self.req("id_user")        
        
        stock_opname_update = stock_opname.query.filter(
            stock_opname.id_stock_opname == int(id_stock_opname)
        ).first()
        
        if not stock_opname_update:
            raise nonServerErrorException("Stock Opname tidak ditemukan", 404)
        
        stock_opname_update.status_so = "rejected"
        stock_opname_update.id_verifikator = id_user
        stock_opname_update.waktu_verifikasi = time_now()

        self.commit()
        
        return {"status":"success"}, 200

    @handle_error_rollback
    def stockOpnameEskalasi(self):
        id_stock_opname = self.req("id_stock_opname")
        id_user = self.req("id_user")

        stock_opname_update = stock_opname.query.filter(
            stock_opname.id_stock_opname == int(id_stock_opname)
        ).first()

        if not stock_opname_update:
            raise nonServerErrorException("Stock Opname tidak ditemukan", 404)

        stock_opname_update.status_so = "eskalasi"
        stock_opname_update.id_verifikator = id_user
        stock_opname_update.waktu_verifikasi = time_now()

        self.commit()
        return { "status":"success" }, 200

    @handle_error_rollback
    def stockOpnameEskalasiClose(self):
        id_stock_opname = self.req("id_stock_opname")
        id_user = self.req("id_user")
        id_cabang = self.req("id_cabang")
        data_produks = self.req("data_produks")
        total = self.req("total")
        total_selisih = self.req("total_selisih")

        # Update StockOpname Record
        stock_opname_update = stock_opname.query.filter(
            stock_opname.id_stock_opname == int(id_stock_opname)
        ).first()

        if not stock_opname_update:
            raise nonServerErrorException("Stock Opname tidak ditemukan", 404)

        # Update main stockOpname Record
        stock_opname_update.status_so = "eskalasi closed"
        stock_opname_update.id_verifikator = id_user
        stock_opname_update.waktu_verifikasi = time_now()
        stock_opname_update.total = total
        stock_opname_update.total_selisih = total_selisih

        # Get UOM Data for Inventory log entries
        result_uom = self.query().setRawQuery("""
            SELECT
            stock_opname_detail.*,
            produk_uom.*
            FROM
            stock_opname_detail
            LEFT JOIN
            produk_uom
            ON
            stock_opname_detail.id_produk = produk_uom.id_produk
            WHERE
            stock_opname_detail.id_stock_opname = :id_stock_opname AND
            produk_uom.level = 1
            """).bindparams(
            {
            "id_stock_opname": int(id_stock_opname)
            }).execute().fetchall().get()

        # Update each product in StockOpnameDetail
        for produk in data_produks:
            detail = stock_opname_detail.query.filter(
                stock_opname_detail.id_stock_opname == int(id_stock_opname),
                stock_opname_detail.id_produk == produk["id_produk"]
            ).first()

            if detail:
                detail.uom_1 = produk["uom_1"]
                detail.uom_2 = produk["uom_2"]
                detail.uom_3 = produk["uom_3"]
                detail.stok = produk["stok"]
                detail.subtotal = produk["subtotal"]
                detail.subtotal_selisih = produk["subtotal_selisih"]

                # Update Stock Levels
                is_stock_produk_ready = stok.query.filter(
                    stok.cabang_id == int(id_cabang),
                    stok.produk_id == produk["id_produk"]
                ).first()

                level1 = list(filter(
                    lambda x: x["id_produk"] == produk["id_produk"], result_uom
                ))

                if not is_stock_produk_ready:
                    add_stock = stok(
                        cabang_id=id_cabang,
                        produk_id=produk["id_produk"],
                        jumlah_ready=produk["stok"],
                        jumlah_booked=0,
                        jumlah_delivery=0,
                        jumlah_incoming=0,
                        jumlah_gudang=produk["stok"],
                        jumlah_canvas = 0,
                        jumlah_good = produk["stok"],
                        jumlah_bad = produk["bad_stock"],
                        tanggal_update=date_now(),
                        waktu_update=time_now(),
                        jumlah_picked=0,
                        transfer_out=0,
                        transfer_in=0
                    )
                    self.add(add_stock).flush()
                else:
                    is_stock_produk_ready.jumlah_ready = produk["stok"]
                    is_stock_produk_ready.jumlah_gudang = produk["stok"]
                    is_stock_produk_ready.jumlah_good = produk["stok"]
                    is_stock_produk_ready.jumlah_bad = produk["bad_stock"]
                    is_stock_produk_ready.tanggal_update = date_now()
                    is_stock_produk_ready.waktu_update = time_now()

                add_log_invetory = log_inventory(
                    id_transaksi = id_stock_opname,
                    id_cabang = id_cabang,
                    id_transaksi_tipe = 11,
                    id_produk = produk["id_produk"],
                    produk_uom_id = level1[0]["id"] if level1 else None,
                    id_user = id_user,
                    stok_awal = is_stock_produk_ready.jumlah_ready if is_stock_produk_ready else 0,
                    stok_peralihan = produk["stok"] - (is_stock_produk_ready.jumlah_ready if is_stock_produk_ready else 0),
                    stok_akhir = produk["stok"],
                    harga = produk["harga"],
                    tanggal = date_now(),
                    valuasi = 0,
                    waktu = time_now(),
                    keterangan = "Stock Opname Eskalasi Close"
                )
                self.add(add_log_invetory).flush()

        profile = self.query().setRawQuery("""
                                           SELECT p.id_perusahaan
                                           FROM principal p
                                           WHERE p.id = :id_principal
                                           """).bindparams(
            {"id_principal": stock_opname_update.id_principal}).execute().fetchone().result

        pubsub = getattr(current_app, 'pubsub', None)
        payload_pubsub = {
            "id_fitur_mal": 8,
            "id_cabang": id_cabang,
            "id_perusahaan": profile["id_perusahaan"] if profile else None,
            "id_stock_opname": id_stock_opname,
            "id_principal": stock_opname_update.id_principal,
            "created_by": id_user,
        }
        if pubsub:
            success = pubsub.publish(data=payload_pubsub, topic="create_jurnal")
            if not success:
                current_app.logger.error(f'Gagal publish ke topic create_jurnal, payload: {payload_pubsub}')
                raise nonServerErrorException(status_code=500, message='Gagal mengirim pesan ke sistem jurnal')
            else:
                current_app.logger.info(f'Sukses publish ke topic create_jurnal, payload: {payload_pubsub}')
        else:
            current_app.logger.error('Pubsub client tidak tersedia')
            raise nonServerErrorException(status_code=500, message='Gagal mengirim pesan ke sistem jurnal')

        self.commit()



        return { "status":"success" }, 200