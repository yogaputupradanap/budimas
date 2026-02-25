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
                users.tokens AS token, users.id AS id_user,
                sales.id AS id_sales,
                users.nama AS nama_user,
                users.email AS user_email,
                users.password
                FROM 
                users JOIN sales ON users.id = sales.id_user 
                WHERE 
                users.email=:email
            """
            )
            .bindparams({"email": email})
            .execute()
            .fetchone()
            .result
        )

        if not len(getInfo):
            raise nonServerErrorException('Email salah atau tidak ada', 403)
        
        if not bcrypt.checkpw(password.encode('utf-8'), getInfo["password"].encode('utf-8')):
            raise nonServerErrorException('Password salah', 403)

        return getInfo

    @handle_error
    def salesInfo(self, userid, tahun=None, bulan=None):
        isRange = tahun and bulan
        current_date, _, _ = str(datetime.now()), None, None
        last_update = str(datetime.now())

        data_dict, param2 = {"userid": userid}, {"userid": userid}
        
        if isRange:
            data_dict["from_date"] = f"{tahun}-{bulan}-01"
            last_day = monthrange(int(tahun), int(bulan))[1]
            data_dict["to_date"] = f"{tahun}-{bulan}-{last_day}"
        else:
            data_dict["tanggal_order"], param2["current_date"] = current_date, current_date
        # total order
        baseQuery = f"""
              FROM plafon 
              JOIN sales_order ON sales_order.id_plafon = plafon.id 
                """
       
        clause = {
            "userid": "plafon.id_user = :userid",
        }
        tanggal_order_clause = "sales_order.tanggal_order BETWEEN :from_date AND :to_date" if isRange else "sales_order.tanggal_order = :tanggal_order"

        where, _ = GetWhereBindParams(data_dict, clause)
        where_clause =  f""" WHERE {tanggal_order_clause} AND """ + where if where else ""
        queryTotalOrder = f"""
                SELECT count(sales_order.id)
                {baseQuery}
                {where_clause}
            """
        print("Query Total Order: ", queryTotalOrder)
        print("Params Total Order: ", data_dict)
        totalOrder = (
            self.query()
            .setRawQuery(
                queryTotalOrder
            )
            .bindparams(data_dict)
            .execute()
            .fetchall()
            .get()
        )

        queryCustomerOrder = f"""
                SELECT COUNT(DISTINCT plafon.id_customer) 
                {baseQuery}
                {where_clause}
            """
        
        print("Query Total Customer Order: ", queryCustomerOrder)
        print("Params Total Customer Order: ", data_dict)
        # total customer order
        totalCustomerOrder = (
            self.query()
            .setRawQuery(
                queryCustomerOrder
            )
            .bindparams(data_dict)
            .execute()
            .fetchall()
            .get()
        )

        # mendapatkan list customer yang sudah dikunjungi
        # data_dict_belumKunjungan = {**data_dict}
        
        extra_clause = self.GetSchedule()
        tanggal_kunjungan_clause = "sales_kunjungan.tanggal BETWEEN :from_date AND :to_date" if isRange else "sales_kunjungan.tanggal = :tanggal_order"
        
        where_belumKunjungan, _ = GetWhereBindParams(data_dict, clause)
        where_belumKunjungan_clause = f""" WHERE {tanggal_kunjungan_clause} AND """ + (where_belumKunjungan if where_belumKunjungan else "") + f" AND ({extra_clause})"

        queryKunjungan = f"""
                select count(distinct plafon.id_customer) 
                from plafon
                join sales_kunjungan on sales_kunjungan.id_plafon = plafon.id
                join plafon_jadwal on plafon_jadwal.id = sales_kunjungan.id_plafon_jadwal
                {where_belumKunjungan_clause}
                  """
        
        belumKunjungan = (
            self.query()
            .setRawQuery(queryKunjungan)
            .bindparams(data_dict)
            .execute()
            .fetchone()
            .result
        )["count"]

        print("belum kunjungan: ", belumKunjungan)
        print("kueri belum kunjungan: ", queryKunjungan)

        status_kunjungan = [1, 2]  # sudah berkunjung
        clause_sudahKunjungan = {
            "userid": "plafon.id_user = :userid",
            "status_kunjungan": "sales_kunjungan.status in :status_kunjungan",
        }

        data_dict_sudahKunjungan = {**data_dict, "status_kunjungan": status_kunjungan}
      
        where_sudahKunjungan, _ = GetWhereBindParams(data_dict_sudahKunjungan, clause_sudahKunjungan)
        where_sudahKunjungan_clause = f""" WHERE {tanggal_kunjungan_clause} AND """ + (where_sudahKunjungan if where_sudahKunjungan else "") + f" AND ({extra_clause})"

        queryKunjungan = f"""
                select count(distinct plafon.id_customer)
                from plafon
                join sales_kunjungan on sales_kunjungan.id_plafon = plafon.id 
                join plafon_jadwal on plafon_jadwal.id = sales_kunjungan.id_plafon_jadwal
                {where_sudahKunjungan_clause}
                  """
        print("kueri sudah kunjungan: ", queryKunjungan)
        print("klause sudah kunjungan: ", clause_sudahKunjungan)
        
        sudahKunjungan = (
              self.query()
              .setRawQuery(queryKunjungan)
              .bindparams_v2(data_dict_sudahKunjungan, ['status_kunjungan'])
              .execute()
              .fetchone()
              .result
        )["count"]
        
        print("sudah berkunjung: ", sudahKunjungan)

        # mendapatkan totol order dalam rupiah
        queryTotalTransaksi = f"""
                    select SUM(sales_order_detail.subtotalorder)
                    {baseQuery}
                    join sales_order_detail on sales_order_detail.id_sales_order = sales_order.id
                    {where_clause}
                """
        print("Query Total Transaksi: ", queryTotalTransaksi)
        print("Params Total Transaksi: ", data_dict)
        totalTransaksi = (
            self.query().setRawQuery(
                queryTotalTransaksi
            )
            .bindparams(data_dict)
            .execute()
            .fetchone()
            .result
        )["sum"]

        queryTotalPencapaian = f"""
                    select sum(setoran_customer.jumlah_setoran)
                    {baseQuery}
                    join setoran_customer on setoran_customer.id_sales_order = sales_order.id
                    {where_clause}
                    """

        totalPencapaian = (
            self.query().setRawQuery(
                queryTotalPencapaian
            )
            .bindparams(data_dict)
            .execute()
            .fetchone()
            .result
        )["sum"]

        totalCallPlan = 0
        if isRange:
            where_kunjungan_clause = f""" WHERE {tanggal_kunjungan_clause} AND """ + (where_belumKunjungan if where_belumKunjungan else "")
            queryTotalCallPlan = f"""
                        select count(distinct plafon.id_customer) 
                        from plafon
                        join sales_kunjungan on sales_kunjungan.id_plafon = plafon.id
                        join plafon_jadwal on plafon_jadwal.id = sales_kunjungan.id_plafon_jadwal
                        {where_kunjungan_clause}
                       """
            totalCallPlan = (
                self.query()
                .setRawQuery(queryTotalCallPlan)
                .bindparams(data_dict)
                .execute()
                .fetchone()
                .result
            )['count']
            # totalCallPlan = belumKunjungan

        return {
            "totalOrder": totalOrder[0]["count"],
            "totalCustomerOrder": totalCustomerOrder[0]["count"],
            "belumKunjungan": belumKunjungan or 0,
            "sudahBerkunjung": sudahKunjungan or 0,
            "updateTerakhir": str(last_update),
            "totalTransaksi": totalTransaksi if totalTransaksi else 0,
            "totalCallPlan": totalCallPlan,
            "totalPencapaian": totalPencapaian if totalPencapaian else 0,
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
        sales = (
            self.query()
            .setRawQuery(
            """
                SELECT 
                sales.*,
                jabatan.nama AS nama_jabatan,
                cabang.nama AS nama_cabang
                FROM sales 
                JOIN users 
                ON sales.id_user = users.id
                JOIN jabatan
                ON jabatan.id = users.id_jabatan 
                JOIN cabang
                ON cabang.id = users.id_cabang
                WHERE sales.id = :id_sales
            """
            )
            .bindparams({"id_sales": id_sales})
            .execute()
            .fetchall()
            .get()
        )

        user = User().getUser(sales[0]["id_user"], "sales", sales[0])
        return user
    
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
        
        charts_data = (
            self.query()
            .setRawQuery(query)
            .bindparams(params)
            .execute()
            .fetchall()
            .get()
        )
        
        # Process results
        result_dict = defaultdict(lambda: {"omset": 0})
        
        for val in charts_data:
            tanggal = val["tanggal_order"]
            omset = val["omset"]
            result_dict[tanggal]["tanggal"] = tanggal
            result_dict[tanggal]["omset"] += omset
        result = list(result_dict.values())
        print("Omset result: ", result)
        return result