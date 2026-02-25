from  .  import  BaseModel


class SalesKunjungan(BaseModel) :

    __tablename__  = 'sales_kunjungan'
    customer_id    = BaseModel.foreign('cabang.id')
    user_id        = BaseModel.foreign('user.id')
    tanggal        = BaseModel.date()
    waktu_mulai    = BaseModel.time()
    waktu_selesai  = BaseModel.time()


    def __repr__(self)              :
        return f"data('{self.id}')"
    
    def __init__(self, data=None)   :
        self.set(data)

    def set(self, data=None)        :
        if (data) :
                self.id             = data.get('sales_kunjungan_id')
                self.customer_id    = data.get('customer.id')
                self.user_id        = data.get('user.id')
                self.tanggal        = data.get('tanggal')
                self.waktu_mulai    = data.get('waktu_mulai')
                self.waktu_selesai  = data.get('waktu_selesai')
        return  self


# @app.route('/api/extra/getListKunjungan')
# @token_auth.login_required
# def extra_26():
#     '''
#         Extra "Custom" Resource.\n
#         Mendapatkan Data `Not Existing` {  U  }.

#         @todo    Data dapat digunakan sebagai `Item` pada `Table List`.
#         @return  (json)  Result Data dari Eksekusi Queri atau Error Message.
#     '''
#     return DB(request).setRawQuery("""
                                   
#         WITH  kunjungan  AS  (
                                   
#             SELECT      * 
#             FROM        sales_kunjungan
#             WHERE       id_user  =  :id 
#                 AND     tanggal  =  :tanggal
#             ORDER BY    id DESC 
#             LIMIT       1 
                                   
#         )

#         SELECT      PL   .id_customer,
#                     PLJ  .id_tipe_kunjungan,
#                     CS   .nama                      AS  nama_customer,
#                     CS   .kode                      AS  kode_customer,
#                     COALESCE(SK.id,             0)  AS  id_sales_kunjungan,
#                     COALESCE(SK.status_checkin, 0)  AS  status_checkin,
                    
#                     CASE 
#                         WHEN        PLJ.id_tipe_kunjungan = 1 
#                             THEN    'Terjadwal'
#                         WHEN        PLJ.id_tipe_kunjungan = 2 
#                             THEN    'Tidak Terjadwal'
#                         WHEN        PLJ.id_tipe_kunjungan = 3 
#                             THEN    'Spesial/Pengganti'
#                     END 
#                         AS  tipe_kunjungan

#         FROM        plafon PL
                                   
#         LEFT JOIN   customer CS 
#             ON      CS   .id            = 
#                     PL   .id_customer 
                    
#         LEFT JOIN   plafon_jadwal PLJ 
#             ON      PLJ  .id_plafon     = 
#                     PL   .id
                                   
#         LEFT JOIN   kunjungan SK 
#             ON      SK   .id_customer   = 
#                     PL   .id_customer

#         WHERE       PL   .id_user       =   :id 
#             AND     PLJ  .id_hari       =   :hari
#             AND     PLJ  .id_status     =   1
#             AND     (CASE  
#                         WHEN   PLJ .id_minggu  =  5    THEN   :minggu  IN  (1,2)
#                         WHEN   PLJ .id_minggu  =  6    THEN   :minggu  IN  (1,3) 
#                         WHEN   PLJ .id_minggu  =  7    THEN   :minggu  IN  (1,4) 
#                         WHEN   PLJ .id_minggu  =  8    THEN   :minggu  IN  (2,3) 
#                         WHEN   PLJ .id_minggu  =  9    THEN   :minggu  IN  (2,4)
#                         WHEN   PLJ .id_minggu  =  10   THEN   :minggu  IN  (3,4) 
#                         WHEN   PLJ .id_minggu  =  11   THEN   :minggu  IN  (1,2,3,4)
#                         ELSE   PLJ .id_minggu  =  :minggu 
#                     END)
                    
#         GROUP BY    PL   .id_customer, 
#                     CS   .nama, 
#                     CS   .kode, 
#                     PLJ  .id_tipe_kunjungan,
#                     SK   .id,
# 			        SK   .status_checkin
        
#     """).bindparams({

#         'id'      : request.args.get('id'),
#         'tanggal' : date_now(),
#         'hari'    : dateday_now(),
#         'minggu'  : getPlafonWeek()['minggu'],

#     }).execute().fetchall().get()



# @app.route('/api/extra/getListDetailKunjungan')
# @token_auth.login_required
# def extra_27():
#     '''
#         Extra "Custom" Resource.\n
#         Mendapatkan Data `Not Existing` {  U  }.

#         @todo    Data dapat digunakan sebagai `Item` pada `Table List`.
#         @return  (json)  Result Data dari Eksekusi Queri atau Error Message.
#     '''
#     return DB(request).setRawQuery("""
                                   
#         SELECT 	    PL  .id                               AS  id_plafon, 
#                     PL  .id_principal,
#                     PL  .id_customer,
#                     PL  .id_user,
#                     PR  .nama                             AS  nama_principal,
#                     COALESCE(SKD.id, 0)                   AS  id_sales_kunjungan_detail,
#                     COALESCE(SKD.id_sales_kunjungan, 0)   AS  id_sales_kunjungan,
#                     COALESCE(SKD.status_proses1, 0)       AS  status_proses1,
#                     COALESCE(SKD.status_proses2, 0)       AS  status_proses2,
#                     COALESCE(SKD.status_proses3, 0)       AS  status_proses3,
#                     COALESCE(SKD.status_checkin, 0)       AS  status_checkin
                    
#         FROM        plafon PL
                                   
#         LEFT JOIN   principal PR 
#             ON      PR   .id                    =  
#                     PL   .id_principal
                                   
#         LEFT JOIN   plafon_jadwal PLJ 
#             ON      PLJ  .id_plafon             = 
#                     PL   .id
                                   
#         LEFT JOIN   sales_kunjungan_detail SKD 
#             ON      SKD  .id_plafon             =
#                     PL   .id

#         WHERE       PL   .id_user       =   :id1 
#             AND     PL   .id_customer   =   :id2
#             AND     PLJ  .id_hari       =   :hari
#             AND     PLJ  .id_status     =   1
#             AND     (CASE  
#                         WHEN   PLJ .id_minggu  =  5    THEN   :minggu  IN  (1,2)
#                         WHEN   PLJ .id_minggu  =  6    THEN   :minggu  IN  (1,3) 
#                         WHEN   PLJ .id_minggu  =  7    THEN   :minggu  IN  (1,4) 
#                         WHEN   PLJ .id_minggu  =  8    THEN   :minggu  IN  (2,3) 
#                         WHEN   PLJ .id_minggu  =  9    THEN   :minggu  IN  (2,4)
#                         WHEN   PLJ .id_minggu  =  10   THEN   :minggu  IN  (3,4) 
#                         WHEN   PLJ .id_minggu  =  11   THEN   :minggu  IN  (1,2,3,4)
#                         ELSE   PLJ .id_minggu  =  :minggu 
#                     END)
        
#     """).bindparams({

#         'id1'     : request.args.get('id1'),
#         'id2'     : request.args.get('id2'),
#         'hari'    : dateday_now(),
#         'minggu'  : getPlafonWeek()['minggu'],

#     }).execute().fetchall().get()

