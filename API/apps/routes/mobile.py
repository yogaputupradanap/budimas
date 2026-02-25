
# @app.route('/api/mobile/login', methods=['POST'])
# def mobile_1(): 
#     '''
#         Mendapatkan Token User berdasarkan Username dan Password untuk Autentikasi.  
#         @exception Jangan dikasih `@token_auth`.
#         @param `username & password` dari User `request.form | form.body`.
#         @result `dict` `token` User.
#     '''
#     with db.connect() as conn:

#         uname  = request.form.get('username')
#         paswd  = request.form.get('password')
#         paswd  = hashlib.sha256(paswd.encode('utf-8')).hexdigest()

#         # Building Query
        
#         query  = text("""
#             SELECT tokens FROM users 
#                 WHERE username=:username 
#                     AND encode(digest(password, 'sha256'), 'hex')=:password 
#                     AND id_jabatan=4
#         """).bindparams(username = uname, password = paswd)

#         result = conn.execute(query).fetchone()
#         if result is not None : result = {"tokens":result['tokens'], "status":200} 
#         elif result is None : result = {"message":'No Token Found Or Jabatan is not Sales', "status":200} 
#         else : abort(HTTPException)
        
#         return result



# @app.route('/api/mobile/getUserProfile')
# @token_auth.login_required
# def mobile_2():
#     '''
#         Mendapatkan Data User berdasarkan Id.
#         @param `id` dari User `request.form | form.body`.
#         @result `dict` User.
#     '''

#     with db.connect() as conn:
        
#         tokens = request.headers['Authorization'].split(' ')[1]
#         query  = ""

#         query = text("""
#             SELECT users.alamat, users.email, users.id, users.id_cabang, 
#                 users.id_jabatan, users.nama, users.nik, users.npwp,
#                 users.tanggal_lahir, users.telepon, users.username,
#                 cabang.nama AS nama_cabang, 
#                 jabatan.nama AS nama_jabatan
#             FROM users 
#                 LEFT JOIN cabang ON users.id_cabang = cabang.id 
#                 LEFT JOIN jabatan ON users.id_jabatan = jabatan.id 
#             WHERE users.tokens = :tokens AND users.id_jabatan = 4
#             ORDER BY users.id
#         """).bindparams(tokens = tokens)

#         result = conn.execute(query).fetchall()
#         result = set(result) if result or len(list(result)) == 0 else abort(HTTPException)

#         return result



# @app.route('/api/mobile/getListKunjungan')
# @token_auth.login_required
# def mobile_3():
#     '''
#         Mendapatkan List Customer berdasarkan Id User.
#         @param `id` dari User `request.argument | query.param` (opsional).
#         @result `dict` List Plafon join Customer Distinct.
#     '''
#     with db.connect() as conn:
        
#         id      = request.args.get('id')
#         x       = datetime.datetime.now(timezone('Asia/Jakarta'))
#         tanggal = x.strftime('%Y-%m-%d')
#         hari    = x.strftime('%w')
#         minggu  = getPlafonWeek()['minggu']
        
#         query = text("""
#             SELECT  PL.id_customer,
#                     CS.nama AS nama_customer,
#                     CS.kode AS kode_customer,
#                     CASE WHEN PLJ.id_tipe_kunjungan = 1 THEN 'Terjadwal'
#                          WHEN PLJ.id_tipe_kunjungan = 2 THEN 'Tidak Terjadwal'
#                          WHEN PLJ.id_tipe_kunjungan = 3 THEN 'Spesial/Pengganti'
#                     END AS tipe_kunjungan,
#                     COALESCE((SELECT  status FROM sales_kunjungan
#                               WHERE   id_customer = PL.id_customer
#                                       AND id_user = :id 
#                                       AND tanggal = :tanggal
#                               ORDER BY id DESC LIMIT 1 
#                     ),0) AS status,
#                     COALESCE((SELECT  id FROM sales_kunjungan
#                               WHERE   id_customer = PL.id_customer
#                                       AND id_user = :id
#                                       AND tanggal = :tanggal
#                               ORDER BY id DESC LIMIT 1 
# 		            ),0) AS id_sales_kunjungan

#             FROM    plafon PL
#                     LEFT JOIN customer CS ON PL.id_customer =  CS.id
#                     LEFT JOIN plafon_jadwal PLJ ON PL.id = PLJ.id_plafon

#             WHERE   PL.id_user = :id 
#                     AND PLJ.id_status = 1
#                     AND PLJ.id_hari = :hari
#                     AND (CASE WHEN PLJ.id_minggu = 5 THEN  :minggu IN (1,2)
#                               WHEN PLJ.id_minggu = 6 THEN  :minggu IN (1,3) 
#                               WHEN PLJ.id_minggu = 7 THEN  :minggu IN (1,4) 
#                               WHEN PLJ.id_minggu = 8 THEN  :minggu IN (2,3) 
#                               WHEN PLJ.id_minggu = 9 THEN  :minggu IN (2,4)
#                               WHEN PLJ.id_minggu = 10 THEN :minggu IN (3,4) 
#                               WHEN PLJ.id_minggu = 11 THEN :minggu IN (1,2,3,4)
#                               ELSE PLJ.id_minggu = :minggu END)
                    
#             GROUP BY PL.id_customer, CS.nama, CS.kode, PLJ.id_tipe_kunjungan
#         """).bindparams(id=id, tanggal=tanggal, hari=hari, minggu=minggu)

#         result = conn.execute(query).fetchall()
#         result = set(result) if result or len(list(result)) == 0 else abort(HTTPException)

#         return result



# @app.route('/api/mobile/getDetailCustomer')
# @token_auth.login_required
# def mobile_4():
#     '''
#         Mendapatkan Detail Customer berdasarkan Id.
#         @param `id` dari Customer `request.argument | query.param` (opsional).
#         @result `dict` Data Customer.
#     '''

#     with db.connect() as conn:
        
#         id = request.args.get('id')

#         query  = text("""
#             SELECT customer.id, customer.id_cabang, customer.id_tipe,
#                 customer.nama, cabang.nama AS nama_cabang, 
#                 customer_tipe.nama AS tipe, customer.kode, 
#                 customer.no_rekening, customer.npwp, 
#                 customer.pic, customer.telepon, customer.telepon2,
#                 customer.longitude, customer.latitude, customer.alamat,
#                 wilayah1.nama AS provinsi, wilayah2.nama AS kota_kab,
#                 wilayah3.nama AS kecamatan, wilayah4.nama AS kelurahan
#             FROM customer
#                 LEFT JOIN cabang ON customer.id_cabang = cabang.id
#                 LEFT JOIN customer_tipe ON customer.id_tipe = customer_tipe.id
#                 LEFT JOIN wilayah1 ON customer.id_wilayah1 = wilayah1.id
#                 LEFT JOIN wilayah2 ON customer.id_wilayah1 = wilayah2.id
#                 LEFT JOIN wilayah3 ON customer.id_wilayah1 = wilayah3.id
#                 LEFT JOIN wilayah4 ON customer.id_wilayah1 = wilayah4.id
#             WHERE customer.id = :id
#         """).bindparams(id = id)

#         result = conn.execute(query).fetchall()
#         result = set(result) if result or len(list(result)) == 0 else abort(HTTPException)

#         return result



# @app.route('/api/mobile/create/customer', methods=['POST'])
# @token_auth.login_required
# def mobile_5():
#     '''
#         Insert Customer.
#         @param data dari Customer `request.form | form.body`.
#         @result `dict` `Success | Error` Message.
#     '''

#     with db.connect() as conn:

#         return insertHelper('customer', request.form, conn)



# @app.route('/api/mobile/update/customer', methods=['PUT'])
# @token_auth.login_required
# def mobile_6():
#     '''
#         Update Customer By Id.
#         @param `id` dari Customer `request.args | query.param`.
#         @param data dari Customer `request.form | form.body`.
#         @result `dict` `Success | Error` Message.
#     '''

#     with db.connect() as conn:
#         id = request.args.get('id')
#         return updateHelper('customer', id, request.form, conn)



# @app.route('/api/mobile/update/profile', methods=['PUT'])
# @token_auth.login_required
# def mobile_7():
#     '''
#         Update Users By Id.
#         @param `id` dari Users `request.args | query.param`.
#         @param data dari Users `request.form | form.body`.
#         @result `dict` `Success | Error` Message.
#     '''

#     with db.connect() as conn:
#         id = request.args.get('id')
#         return updateHelper('users', id, request.form, conn)



# @app.route('/api/mobile/getListTipeCustomer')
# @token_auth.login_required
# def mobile_8():
#     '''
#         Mendapatkan List Tipe Customer
#         @result `dict` Tipe Customer.
#     '''

#     with db.connect() as conn:
        
#         query = text("SELECT * FROM customer_tipe")

#         result = conn.execute(query).fetchall()
#         result = set(result) if result or len(list(result)) == 0 else abort(HTTPException)

#         return result



# @app.route('/api/mobile/getListWilayah1')
# @token_auth.login_required
# def mobile_9():
#     '''
#         Mendapatkan List Wilayah 1 (Provinsi)
#         @result `dict` List Wilayah 1.
#     '''

#     with db.connect() as conn:
        
#         query = text("SELECT * FROM wilayah1")

#         result = conn.execute(query).fetchall()
#         result = set(result) if result or len(list(result)) == 0 else abort(HTTPException)

#         return result



# @app.route('/api/mobile/getListWilayah2')
# @token_auth.login_required
# def mobile_10():
#     '''
#         Mendapatkan List Wilayah 2 (Kabupaten / Kota)
#         @param `id` dari Wilayah 1 `request.argument | query.param`.
#         @result `dict` List Wilayah 2.
#     '''

#     with db.connect() as conn:
        
#         id = request.args.get('id')
        
#         query = text("SELECT * FROM wilayah2 WHERE id_wilayah1 = :id").bindparams(id = id)

#         result = conn.execute(query).fetchall()
#         result = set(result) if result or len(list(result)) == 0 else abort(HTTPException)

#         return result



# @app.route('/api/mobile/getListWilayah3')
# @token_auth.login_required
# def mobile_11():
#     '''
#         Mendapatkan List Wilayah 3 (Kecamatan)
#         @param `id` dari Wilayah 2 `request.argument | query.param`.
#         @result `dict` List Wilayah 3.
#     '''

#     with db.connect() as conn:
        
#         id = request.args.get('id')
        
#         query = text("SELECT * FROM wilayah3 WHERE id_wilayah2 = :id").bindparams(id = id)

#         result = conn.execute(query).fetchall()
#         result = set(result) if result or len(list(result)) == 0 else abort(HTTPException)

#         return result



# @app.route('/api/mobile/getListWilayah4')
# @token_auth.login_required
# def mobile_12():
#     '''
#         Mendapatkan List Wilayah 4 (Kelurahan)
#         @param `id` dari Wilayah 3 `request.argument | query.param`.
#         @result `dict` List Wilayah 4.
#     '''

#     with db.connect() as conn:
        
#         id = request.args.get('id')
        
#         query = text("SELECT * FROM wilayah4 WHERE id_wilayah3 = :id").bindparams(id = id)

#         result = conn.execute(query).fetchall()
#         result = set(result) if result or len(list(result)) == 0 else abort(HTTPException)

#         return result



# @app.route('/api/mobile/getListProduk')
# @token_auth.login_required
# def mobile_13():
#     '''
#         Mendapatkan Daftar dari Produk Berdasarkan Id Principal.
#         @result `dict` List Produk join ProdukHarga.
#     '''
#     with db.connect() as conn:

#         id_principal = request.args.get('id_principal')
#         id_tipe_harga = request.args.get('id_tipe_harga')

#         query = text("""
#             SELECT produk.*, 
#                 produk_harga.harga 
#             FROM produk
#                 LEFT JOIN produk_harga ON produk.id = produk_harga.id_produk
#             WHERE id_principal=:id_principal AND id_tipe_harga=:id_tipe_harga
#             ORDER BY produk.id
#         """).bindparams(id_principal = id_principal, id_tipe_harga = id_tipe_harga)

#         result = conn.execute(query).fetchall()
#         result = set(result) if result or len(list(result)) == 0 else abort(HTTPException)

#         return result



# @app.route('/api/mobile/getListDetailKunjungan')
# @token_auth.login_required
# def mobile_14():
#     '''
#         Mendapatkan List Customer berdasarkan Id User.
#         @param `id` dari User `request.argument | query.param` (opsional).
#         @result `dict` List Plafon join Customer Distinct.
#     '''
#     with db.connect() as conn:
        
#         id       = request.args.get('id')
#         hari     = datetime.datetime.now().strftime('%w')
#         minggu   = getPlafonWeek()['minggu']
        
#         query = text("""
#             SELECT 	PL.id AS id_plafon, PL.id_principal, 
#                     PR.nama AS nama_principal,
#                     COALESCE(SKD.is_proses1, 0) AS is_proses1,
#                     COALESCE(SKD.is_proses2, 0) AS is_proses2,
#                     COALESCE(SKD.is_proses3, 0) AS is_proses3
                    
#             FROM    plafon PL
#                     LEFT JOIN principal PR ON PL.id_principal = PR.id
#                     LEFT JOIN plafon_jadwal PLJ ON PL.id = PLJ.id_plafon
#                     LEFT JOIN sales_kunjungan_detail SKD ON PL.id = SKD.id_plafon

#             WHERE   PL.id_customer = :id
#                     AND PLJ.id_status = 1
#                     AND PLJ.id_hari = :hari
#                     AND (CASE WHEN PLJ.id_minggu = 5 THEN :minggu IN (1,2)
#                               WHEN PLJ.id_minggu = 6 THEN :minggu IN (1,3) 
#                               WHEN PLJ.id_minggu = 7 THEN :minggu IN (1,4) 
#                               WHEN PLJ.id_minggu = 8 THEN :minggu IN (2,3) 
#                               WHEN PLJ.id_minggu = 9 THEN :minggu IN (2,4)
#                               WHEN PLJ.id_minggu = 10 THEN :minggu IN (3,4) 
#                               WHEN PLJ.id_minggu = 11 THEN :minggu IN (1,2,3,4)
#                               ELSE PLJ.id_minggu = :minggu END)
#         """).bindparams(id=id, hari=hari, minggu=minggu)

#         result = conn.execute(query).fetchall()
#         result = set(result) if result or len(list(result)) == 0 else abort(HTTPException)

#         return result



# @app.route('/api/mobile/logCheckInKunjungan', methods=['POST'])
# @token_auth.login_required
# def mobile_15():
#     '''
#         Insert Data CheckIn ke Dalam Table Sales Kunjungan.
#         @param data dari Customer `request.form | form.body`.
#         @result `dict` `Success | Error` Message.
#     '''

#     with db.connect() as conn:
#         id_customer = request.form.get('id_customer')
#         id_user     = request.form.get('id_user') 
        
#         x           = datetime.datetime.now(timezone('Asia/Jakarta'))
#         tanggal     = x.strftime('%Y-%m-%d')
#         waktu_mulai = x.strftime('%H:%M:%S')

#         query  = text("""
#             INSERT INTO sales_kunjungan ( id_customer, id_user, tanggal, waktu_mulai, status) 
#             SELECT :id_customer, :id_user, :tanggal, :waktu_mulai, 1
#             WHERE NOT EXISTS (
#                 SELECT  1
#                 FROM    sales_kunjungan
#                 WHERE   id_customer = :id_customer 
#                         AND id_user = :id_user
#                         AND tanggal = :tanggal
#             )
#         """).bindparams(
#             id_customer = id_customer, 
#             id_user     = id_user, 
#             tanggal     = tanggal, 
#             waktu_mulai = waktu_mulai
#         )

#         result = conn.execute(query)
#         result = set({"messege" : "Data Successfully Added"}) if result or len(list(result)) == 0 else abort(HTTPException)
        
#     return result



# @app.route('/api/mobile/logCheckOutKunjungan', methods=['PUT'])
# @token_auth.login_required
# def mobile_16():
#     '''
#         Insert Data CheckIn ke Dalam Table Sales Kunjungan.
#         @param data dari Customer `request.form | form.body`.
#         @result `dict` `Success | Error` Message.
#     '''

#     with db.connect() as conn:

#         id            = request.args.get('id')
#         waktu_selesai = datetime.datetime.now(timezone('Asia/Jakarta')).strftime('%H:%M:%S')

#         query  = text("""
#             UPDATE sales_kunjungan SET status=2, waktu_selesai=:waktu_selesai WHERE id=:id
#         """).bindparams(id=id, waktu_selesai=waktu_selesai)

#         result = conn.execute(query)
#         result = set({"messege" : "Data Successfully Updated"}) if result or len(list(result)) == 0 else abort(HTTPException)
        
#     return result



# @app.route('/api/mobile/logProsesKunjungan', methods=['POST'])
# @token_auth.login_required
# def mobile_17():
#     '''
#         Insert Data CheckIn ke Dalam Table Sales Kunjungan.
#         @param data dari Customer `request.form | form.body`.
#         @result `dict` `Success | Error` Message.
#     '''

#     with db.connect() as conn:

#         a = request.args.get('id_sales_kunjungan')
#         b = request.args.get('id_plafon')
#         c = request.args.get('id_principal')

#         query  = text("""
#             INSERT INTO sales_kunjungan_detail (id_sales_kunjungan, id_plafon, id_principal) 
#             VALUES (:a, :b, :c)
#         """).bindparams(a=a, b=b, c=c)

#         result = conn.execute(query)
#         result = set({"messege" : "Data Successfully Added"}) if result or len(list(result)) == 0 else abort(HTTPException)
        
#     return result



# @app.route('/api/mobile/updateProsesKunjungan', methods=['PUT'])
# @token_auth.login_required
# def mobile_18():
#     '''
#         Insert Data CheckIn ke Dalam Table Sales Kunjungan.
#         @param data dari Customer `request.form | form.body`.
#         @result `dict` `Success | Error` Message.
#     '''

#     with db.connect() as conn:

#         id     = request.args.get('id_sales_kunjungan_detail')
#         proses = request.args.get('proses')
#         proses = f"is_proses{proses}"

#         query  = text("""
#             UPDATE sales_kunjungan_detail SET :proses=1 WHERE id=:id
#         """).bindparams(id=id, proses=proses)

#         result = conn.execute(query)
#         result = set({"messege" : "Data Successfully Added"}) if result or len(list(result)) == 0 else abort(HTTPException)
        
#     return result

