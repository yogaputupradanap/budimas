from datetime import datetime, timedelta

import holidays

from .User import User
from calendar import monthrange
from . import BaseServices
from apps.handler import handle_error, nonServerErrorException
from collections import defaultdict
import bcrypt
from apps.lib.helper import GetWhereBindParams
from apps.services.BaseSales import BaseSales
from apps.services.User import UserService

from ..lib.helper import get_day_number_for_date, get_week_number_for_date, is_holiday, get_current_day_number, \
    get_week_number_cycle, get_now_datetime


class Sales(BaseSales):
    @handle_error
    def get_token_by_credential(self):
        email = self.req("email")
        password = self.req("password")

        getInfo = (
            self.query()
            .setRawQuery(
            """
                SELECT 
                users.tokens AS token, 
                users.id AS id_user,
                sales.id AS id_sales,
                users.nama AS nama_user,
                users.email AS user_email,
                users.password
                FROM 
                users 
                JOIN sales ON users.id = sales.id_user 
                WHERE users.email = :email
            """
            )
            .bindparams({"email": email})
            .execute()
            .fetchone()
            .result
        )

        # ✅ FIX 1
        if not getInfo:
            raise nonServerErrorException('Email salah atau tidak ada', 403)

        # ✅ FIX 2
        if not bcrypt.checkpw(
            password.encode('utf-8'),
            getInfo["password"].encode('utf-8')
        ):
            raise nonServerErrorException('Password salah', 403)

        return getInfo

    @handle_error
    def salesInfo(self, userid, tahun=None, bulan=None):
        isRange = tahun and bulan
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        last_update = now.strftime("%Y-%m-%d %H:%M:%S")

        # Fungsi pembantu untuk menangani response List atau Dict
        def safe_extract(response, key, default=0):
            if isinstance(response, list): 
                return response[0].get(key, default) if response else default
            if isinstance(response, dict): 
                res = response.get('result')
                if isinstance(res, list):
                    return res[0].get(key, default) if res else default
                if isinstance(res, dict):
                    return res.get(key, default)
            return default

        data_dict = {"userid": userid}
        
        if isRange:
            data_dict["from_date"] = f"{tahun}-{bulan}-01"
            last_day = monthrange(int(tahun), int(bulan))[1]
            data_dict["to_date"] = f"{tahun}-{bulan}-{last_day}"
        else:
            data_dict["tanggal_order"] = current_date

        # 1. Base query & Clauses
        baseQuery = " FROM plafon JOIN sales_order ON sales_order.id_plafon = plafon.id "
        clause = {"userid": "plafon.id_user = :userid"}
        tanggal_order_clause = "sales_order.tanggal_order BETWEEN :from_date AND :to_date" if isRange else "sales_order.tanggal_order = :tanggal_order"

        where, _ = GetWhereBindParams(data_dict, clause)
        where_clause = f" WHERE {tanggal_order_clause} AND {where}" if where else f" WHERE {tanggal_order_clause}"

        # 2. Eksekusi Query - Total Order
        queryTotalOrder = f"SELECT count(sales_order.id) as count {baseQuery} {where_clause}"
        resTotalOrder = self.query().setRawQuery(queryTotalOrder).bindparams(data_dict).execute().fetchall().get()
        totalOrderCount = safe_extract(resTotalOrder, 'count')

        # 3. Eksekusi Query - Total Customer Order
        queryCustomerOrder = f"SELECT COUNT(DISTINCT plafon.id_customer) as count {baseQuery} {where_clause}"
        resCustomerOrder = self.query().setRawQuery(queryCustomerOrder).bindparams(data_dict).execute().fetchall().get()
        totalCustomerOrderCount = safe_extract(resCustomerOrder, 'count')

        # 4. Kunjungan setup
        extra_clause = self.GetSchedule()
        tanggal_kunjungan_clause = "sales_kunjungan.tanggal BETWEEN :from_date AND :to_date" if isRange else "sales_kunjungan.tanggal = :tanggal_order"
        
        # 5. Belum Kunjungan
        where_belumKunjungan_clause = f" WHERE {tanggal_kunjungan_clause} AND {where} AND ({extra_clause})"
        queryKunjungan = f"""
                SELECT count(distinct plafon.id_customer) as count
                FROM plafon
                JOIN sales_kunjungan ON sales_kunjungan.id_plafon = plafon.id
                JOIN plafon_jadwal ON plafon_jadwal.id = sales_kunjungan.id_plafon_jadwal
                {where_belumKunjungan_clause}
        """
        resBelum = self.query().setRawQuery(queryKunjungan).bindparams(data_dict).execute().fetchone().get()
        belumKunjungan = safe_extract(resBelum, 'count')

        # 6. Sudah Kunjungan
        data_dict_sudah = {**data_dict, "status_1": 1, "status_2": 2}
        querySudahKunjungan = f"""
                SELECT count(distinct plafon.id_customer) as count
                FROM plafon
                JOIN sales_kunjungan ON sales_kunjungan.id_plafon = plafon.id 
                JOIN plafon_jadwal ON plafon_jadwal.id = sales_kunjungan.id_plafon_jadwal
                WHERE {tanggal_kunjungan_clause} AND {where} 
                AND sales_kunjungan.status IN (:status_1, :status_2)
                AND ({extra_clause})
        """
        resSudah = self.query().setRawQuery(querySudahKunjungan).bindparams(data_dict_sudah).execute().fetchone().get()
        sudahKunjungan = safe_extract(resSudah, 'count')

        # 7. Total Transaksi (Rupiah)
        queryTotalTransaksi = f"""
                SELECT SUM(sales_order_detail.subtotalorder) as sum
                {baseQuery}
                JOIN sales_order_detail ON sales_order_detail.id_sales_order = sales_order.id
                {where_clause}
        """
        resTransaksi = self.query().setRawQuery(queryTotalTransaksi).bindparams(data_dict).execute().fetchone().get()
        totalTransaksiVal = safe_extract(resTransaksi, 'sum')

        # 8. Total Pencapaian (Setoran)
        queryTotalPencapaian = f"""
                SELECT sum(setoran_customer.jumlah_setoran) as sum
                {baseQuery}
                JOIN setoran_customer ON setoran_customer.id_sales_order = sales_order.id
                {where_clause}
        """
        resPencapaian = self.query().setRawQuery(queryTotalPencapaian).bindparams(data_dict).execute().fetchone().get()
        totalPencapaianVal = safe_extract(resPencapaian, 'sum')

        # 9. Total Call Plan (Jika isRange)
        totalCallPlanVal = 0
        if isRange:
            where_kunj_clause = f" WHERE {tanggal_kunjungan_clause} AND {where}"
            queryTotalCallPlan = f"""
                        SELECT count(distinct plafon.id_customer) as count
                        FROM plafon
                        JOIN sales_kunjungan ON sales_kunjungan.id_plafon = plafon.id
                        JOIN plafon_jadwal ON plafon_jadwal.id = sales_kunjungan.id_plafon_jadwal
                        {where_kunj_clause}
            """
            resCP = self.query().setRawQuery(queryTotalCallPlan).bindparams(data_dict).execute().fetchone().get()
            totalCallPlanVal = safe_extract(resCP, 'count')

        return {
            "totalOrder": totalOrderCount,
            "totalCustomerOrder": totalCustomerOrderCount,
            "belumKunjungan": belumKunjungan,
            "sudahBerkunjung": sudahKunjungan,
            "updateTerakhir": last_update,
            "totalTransaksi": totalTransaksiVal,
            "totalCallPlan": totalCallPlanVal,
            "totalPencapaian": totalPencapaianVal,
        }

    def calculate_call_plan(self, userid, tahun, bulan):
        """
        Menghitung jadwal call plan untuk sales berdasarkan jadwal yang ada di plafon_jadwal
        """
        tahun = int(tahun)
        bulan = int(bulan)

        # Dapatkan semua jadwal dari plafon_jadwal untuk user tertentu
        jadwal_query = self.query().setRawQuery(
            """
            SELECT 
                pj.id, pj.id_plafon, pj.id_tipe_kunjungan, pj.id_hari, pj.id_minggu, p.id_customer,
                c.nama as customer_name
            FROM plafon_jadwal pj 
            LEFT JOIN plafon p ON pj.id_plafon = p.id
            LEFT JOIN customer c ON p.id_customer = c.id
            WHERE p.id_user = :userid
            """
        ).bindparams({"userid": userid}).execute().fetchall().get()

        if not jadwal_query:
            return 0

        # Kombinasi minggu
        week_combo = {
            5: [1, 2], 6: [1, 3], 7: [1, 4],
            8: [2, 3], 9: [2, 4], 10: [3, 4]
        }

        total_call_plan = 0
        last_day = monthrange(tahun, bulan)[1]

        # Simulasi untuk setiap hari dalam bulan
        for day in range(1, last_day + 1):
            current_date = datetime(tahun, bulan, day)

            # Skip hari libur
            # if is_holiday(current_date):
            #     continue

            # Dapatkan nomor hari dan minggu
            day_number = get_day_number_for_date(current_date)
            week_number = get_week_number_for_date(current_date)

            # Proses jadwal untuk hari ini
            for jadwal in jadwal_query:
                week = int(jadwal["id_minggu"])
                day = int(jadwal["id_hari"])

                if (week == week_number or week == 11) and day == day_number:
                    total_call_plan += 1
                elif week in week_combo:
                    if any(combo_week == week_number and day == day_number for combo_week in week_combo[week]):
                        total_call_plan += 1

        return total_call_plan

    @handle_error
    def getSaleses(self):
        saleses = (
            self.query()
            .setRawQuery(
            """
                SELECT * FROM sales JOIN users ON sales.id_user = users.id
            """
            )
            .execute()
            .fetchall()
            .get()
        )

        return saleses
    
    @handle_error
    def getSales(self, id_sales):
        # Ambil output dari DB
        response = (
            self.query()
            .setRawQuery("""
                SELECT sales.*, jabatan.nama AS nama_jabatan, cabang.nama AS nama_cabang
                FROM sales 
                JOIN users ON sales.id_user = users.id
                JOIN jabatan ON jabatan.id = users.id_jabatan 
                JOIN cabang ON cabang.id = users.id_cabang
                WHERE sales.id = :id_sales
            """)
            .bindparams({"id_sales": id_sales})
            .execute()
            .fetchall()
            .get()
        )

        # 1. Ambil list dari dalam key 'result'
        data_list = response.get('result', [])

        # 2. Cek apakah datanya ada sebelum akses indeks [0]
        if not data_list:
            return {"status": "error", "message": "Sales tidak ditemukan"}, 404

        sales_data = data_list[0]

        # 3. Panggil UserService (pastikan sudah di-import)
        # from apps.services.User import UserService
        return UserService().getUser(sales_data["id_user"], "sales", sales_data)
    
    @handle_error
    def history(self, id_plafon, jenis_faktur):
        return (
            self.query()
            .setRawQuery(
                """
                    SELECT * FROM sales_order 
                    JOIN faktur 
                    ON 
                    sales_order.id = faktur.id_sales_order 
                    WHERE 
                    id_plafon = :id_plafon
                    AND
                    jenis_faktur = :jenis_faktur
                """
            )
            .bindparams(
                {
                    "id_plafon": id_plafon, 
                    "jenis_faktur": jenis_faktur
                }
            )
            .execute()
            .fetchall()
            .get()
        )
    
    @handle_error
    def getOmset(self):
        # Input validation and parsing
        user_id = self.req('user_id')
        if not user_id:
            raise ValueError("user_id is required")

        tahun = self.req('tahun')
        bulan = self.req('bulan')
        if not (tahun and bulan):
            raise ValueError("tahun and bulan are required")
        
        tahun, bulan = int(tahun), int(bulan)
        tanggal = int(self.req('tanggal') or monthrange(tahun, bulan)[1])
        
        jenis_faktur = self.req('jenis_faktur') or 'penjualan'
        status_faktur = self.req('status_faktur')
        
        # Date formatting
        from_date = f"{tahun:04d}-{bulan:02d}-01"
        to_date = f"{tahun:04d}-{bulan:02d}-{tanggal:02d}"
        
        # Status condition
        status_condition = "faktur.status_faktur = :status_faktur" if status_faktur else "faktur.status_faktur in (0, 1, 2, 3, 4, 5)"
        
        # Query parameters
        params = {
            "user_id": user_id,
            "from_date": from_date,
            "to_date": to_date,
            "jenis_faktur": jenis_faktur,
        }
        if status_faktur:
            params["status_faktur"] = status_faktur
        
        # Query execution
        query = f"""
            SELECT faktur.total_penjualan AS omset, sales_order.tanggal_order AS tanggal_order
            FROM plafon
            JOIN users ON users.id = plafon.id_user
            JOIN sales_order ON sales_order.id_plafon = plafon.id
            JOIN faktur ON faktur.id_sales_order = sales_order.id
            WHERE plafon.id_user = :user_id
            AND faktur.jenis_faktur = :jenis_faktur
            AND {status_condition}
            AND sales_order.tanggal_order BETWEEN :from_date AND :to_date
        """
        
        # Query execution
        response = (
            self.query()
            .setRawQuery(query)
            .bindparams(params)
            .execute()
            .fetchall()
            .get()
        )
        
        # --- PERBAIKAN DI SINI ---
        # Ambil list data dari dalam key 'result'
        charts_data = response.get('result', [])
        
        # Process results
        result_dict = defaultdict(lambda: {"omset": 0})
        
        # Sekarang looping ini aman karena charts_data sudah berbentuk LIST
        for val in charts_data:
            tanggal = str(val["tanggal_order"]) # Pastikan jadi string untuk key dict
            omset = val["omset"] or 0 # Antisipasi jika omset None
            
            result_dict[tanggal]["tanggal"] = tanggal
            result_dict[tanggal]["omset"] += omset
            
        result = list(result_dict.values())
        return result