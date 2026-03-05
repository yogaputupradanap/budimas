from flask import abort
from apps.query import DB
from apps.helper import date_now, time_now

class SalesKunjungan:

    def getListKunjungan(self, kunjunganId):
            """Mengambil daftar kunjungan berdasarkan user_id dan tanggal hari ini."""
            current_date = date_now()

            # Eksekusi query
            response = (
                DB()
                .setRawQuery(
                    """
                    SELECT 
                        sales_kunjungan.*,
                        plafon.id AS id_plafon,
                        customer.nama AS nama_customer, 
                        customer.latitude AS customer_latitude, 
                        customer.longitude AS customer_longitude,
                        customer.kode AS kode_customer,
                        wilayah1.nama AS nama_wilayah_1,
                        wilayah2.nama AS nama_wilayah_2,
                        wilayah3.nama AS nama_wilayah_3,
                        wilayah4.nama AS nama_wilayah_4
                    FROM 
                        sales_kunjungan 
                    JOIN customer 
                        ON sales_kunjungan.customer_id = customer.id
                    LEFT JOIN plafon
                        ON plafon.id_customer = customer.id 
                    JOIN wilayah1
                        ON customer.id_wilayah1 = wilayah1.id
                    JOIN wilayah2
                        ON customer.id_wilayah2 = wilayah2.id
                    JOIN wilayah3
                        ON customer.id_wilayah3 = wilayah3.id
                    JOIN wilayah4
                        ON customer.id_wilayah4 = wilayah4.id
                    WHERE 
                        sales_kunjungan.user_id = :kunjungan_id AND 
                        sales_kunjungan.tanggal = :current_date
                    """
                )
                .bindparams({"kunjungan_id": kunjunganId, "current_date": current_date})
                .execute()
                .fetchall()
                .get()
            )

            # --- PERBAIKAN DI SINI ---
            # Jika response sudah berupa list, langsung kembalikan.
            if isinstance(response, list):
                return response
                
            # Jika response adalah dictionary, ambil key 'result'.
            if isinstance(response, dict):
                return response.get('result', [])
                
            return []

    def checkInOrOutKunjungan(self, kunjunganId, status):
        """Melakukan update status check-in (1) atau check-out (2)."""
        
        # Ambil data kunjungan saat ini untuk validasi
        kunjunganList = self.getListKunjungan(kunjunganId)
        current_time = str(time_now())

        # Validasi: Tidak boleh check-in jika ada kunjungan lain yang masih status 'sedang berkunjung' (1)
        if status == 1:
            if any(map(lambda k: k.get("status") == 1, kunjunganList)):
                return {"status": "error", "message": "Selesaikan kunjungan sebelumnya dulu!"}, 401

        # Tentukan kolom mana yang diupdate berdasarkan status
        time_column = 'waktu_mulai' if status == 1 else 'waktu_selesai'

        DB().setRawQuery(
            f"""
            UPDATE sales_kunjungan 
            SET status = :status, 
                {time_column} = :current_time 
            WHERE id = :kunjunganId                 
            """
        ).bindparams(
            {
                "status": status, 
                "kunjunganId": kunjunganId, 
                "current_time": current_time
            }
        ).execute()

        # Ambil data terbaru setelah update untuk dikembalikan ke frontend
        response_after = (
            DB()
            .setRawQuery(
                """
                SELECT sales_kunjungan.*, customer.nama AS nama_customer, customer.latitude, customer.longitude, plafon.id AS plafon_id
                FROM sales_kunjungan 
                JOIN customer ON sales_kunjungan.customer_id = customer.id
                LEFT JOIN plafon ON customer.id = plafon.id_customer
                WHERE sales_kunjungan.id = :kunjungan_id
                """
            )
            .bindparams({"kunjungan_id": kunjunganId})
            .execute()
            .fetchall()
            .get()
        )

        final_data = response_after.get('result', [])
        if not final_data:
            return {"status": "error", "message": "Data tidak ditemukan"}, 404
            
        return final_data[0]

    def convertPlafonJadwal(self):
        """
        Metode ini dipanggil oleh endpoint 'create-sales-kunjungan'.
        Tambahkan logika konversi jadwal ke sini.
        """
        # Placeholder logika Anda
        return {"status": "success", "message": "Jadwal berhasil dikonversi menjadi kunjungan."}