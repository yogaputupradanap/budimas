from apps.lib.helper import date_now, to_array_string
from datetime import datetime, timedelta
from . import BaseServices
from apps.handler import handle_error, handle_error_rollback
from apps.models import setoran, sales_order
from ..models.setoran_customer import setoran_customer


class Pembayaran(BaseServices):

    @handle_error
    def listFakturBetweenDates(self, id_plafon):
        """
         @brief List faktur between dates. TIDEDD is 30 days from today and TIDEDD is today + 30 days
         @param id_plafon id of planet to list
         @return list of sales order
        """
        current_date = datetime.now().strftime("%Y-%m-%d")
        currentTImeDelta = timedelta(days=30)

        addeddDate = current_date + currentTImeDelta

        from_date = self.req("from") or current_date
        to_date = self.req("to") or addeddDate

        tagihan_jatuh_tempo = (
            self.query()
            .setRawQuery(
            """
                SELECT 
                *
                FROM sales_order 
                JOIN faktur 
                ON 
                faktur.id_sales_order = sales_order.id
                WHERE 
                sales_order.status_order = 1
                AND
                sales_order.id_plafon = :id_plafon
                AND
                sales_order BETWEEN :from_date AND :end_date
            """
            )
            .bindparams(
                {
                    "id_plafon": id_plafon,
                    "from_date": from_date,
                    "end_date": to_date,
                }
            )
            .execute()
            .fetchall()
            .get()
        )

        return tagihan_jatuh_tempo

    @handle_error
    def listTagihanJatuhTempo(self, id_plafon):
        """
         @brief List Tagihan Jatuh tempo for a plafon. This is a method to be used in conjunction with
         @param id_plafon id of the plafon to list
         @return list of dictionaries with keys nama and jenis_faktur as values or None if not
        """
        array_id_plafon = to_array_string(id_plafon)
        
        list_tagihan_jatuh_tempo = (
            self.query()
            .setRawQuery(
            f"""
                SELECT 
                faktur.id_sales_order,
                faktur.no_faktur,
                faktur.total_penjualan ,
                sales_order.status_order,
                faktur.status_faktur,
                faktur.id as id_faktur,
                sales_order.tanggal_jatuh_tempo,
                customer.nama as nama_customer,
                customer.id as id_customer,
                coalesce(faktur.nominal_retur, 0) as nominal_retur,                
                principal.id as id_principal,
                principal.nama as nama_principal
                FROM sales_order
                JOIN faktur
                ON sales_order.id = faktur.id_sales_order
                JOIN plafon
                ON
                plafon.id = sales_order.id_plafon
                JOIN principal
                ON principal.id = plafon.id_principal
                JOIN customer
                ON customer.id = plafon.id_customer
                WHERE 
                sales_order.id_plafon = any (array{array_id_plafon})
                AND
                faktur.jenis_faktur = 'penjualan'
                and
                faktur.status_faktur in (1,2,3,4,5,6)
            """
            )
            .execute()
            .fetchall()
            .get()
        )

        with_faktur_and_setoran = []

        # List of tagihan jatuh tempo.
        for tagihan in list_tagihan_jatuh_tempo:
            faktur = (
                self.query()
                .setRawQuery(
                """
                    SELECT * from faktur WHERE id_sales_order = :id_sales_order
                    AND jenis_faktur = 'penjualan'
                """
                )
                .bindparams({"id_sales_order": tagihan["id_sales_order"]})
                .execute()
                .fetchone()
                .result
            )

            setoran = (
                self.query()
                .setRawQuery(
                """
                    SELECT * FROM setoran WHERE id_sales_order = :id_sales_order ORDER BY tanggal_setoran_diterima ASC
                """
                )
                .bindparams({"id_sales_order": tagihan["id_sales_order"]})
                .execute()
                .fetchall()
                .get()
            )

            tagihan["faktur"] = faktur
            tagihan["setoran"] = setoran

            with_faktur_and_setoran.append(tagihan)

        return with_faktur_and_setoran

    @handle_error
    def updateStatusFaktur(self):
        # Update status_faktur to 1.
        for id_faktur in self.req("id_fakturs"):
            self.query().setRawQuery(
                """
                    UPDATE faktur SET status_faktur = 1 WHERE id = :id  
                """
            ).bindparams({"id": id_faktur}).execute()

        return "success"

    @handle_error_rollback
    def createPayment(self):
        id_sales_order = self.req("notaFaktur")

        add_setoran_customer = setoran_customer(
          id_sales = self.req('id_sales'),
            id_sales_order = id_sales_order,
            jumlah_setoran = self.req("jumlahBayar"),
            tipe_setoran = 1,
            tanggal_input = date_now(),
            is_rekap = 0
        )
        

        self.add(add_setoran_customer).flush()
        
        status = {
            "id_sales_order": id_sales_order,    
            "status": 6,
        }
        
        self.commit()
        return status

    @handle_error
    def getRiwayatSetoranCustomer(self):
        id_sales_order = self.req('id_sales_order')

        if id_sales_order is None:
            raise ValueError("id_sales_order is required")

        list_setoran_customer = (
            self.query().setRawQuery("""
            select 
            sc.*,
            array_agg(s.status_setoran)  as status_setoran,
            array_agg(s.tanggal_setoran_diterima) as tanggal_setoran_diterima,
            array_agg(s.id) as id_setoran
            from setoran_customer sc
            left join setoran s on sc.id = s.id_setoran_customer
            where sc.id_sales_order = :id_sales_order
            group by sc.id, sc.id_sales, sc.id_sales_order, sc.jumlah_setoran, sc.tipe_setoran, sc.tanggal_input
            """).bindparams({"id_sales_order": id_sales_order}).execute().fetchall().get()
        )
        return list_setoran_customer

    @handle_error
    def getRekapPembayaranSales(self):
        id_sales = self.req("id_sales")
        tanggal = date_now()
        list_rekap = (
            self.query()
            .setRawQuery(
                """
                SELECT 
                  sc.*,
                    f.no_faktur
                FROM setoran_customer sc
                left join faktur f on sc.id_sales_order = f.id_sales_order
                where sc.id_sales = :id_sales and sc.tanggal_input = :tanggal and is_rekap = 0
            """
            )
            .bindparams({"id_sales": id_sales, "tanggal": tanggal})
            .execute()
            .fetchall()
            .get()
        )

        return list_rekap
        
    @handle_error
    def __createPayment(self):
        jumlah_setoran = 0
            
        payment = (
            self.query()
            .setRawQuery(
                """
                INSERT INTO setoran 
                (id_sales_order, jumlah_setoran, metode_pembayaran, bukti_transfer, tanggal_setoran_diterima)
                VALUES
                (:id_sales_order, :jumlah_setoran, :metode_pembayaran, :bukti_transfer, :tanggal_setoran_diterima)
                RETURNING *
            """
            )
            .bindparams(
                {
                    "id_sales_order": self.req("notaFaktur"),  # A.K.A id_sales_order
                    "jumlah_setoran": self.req("jumlahBayar"),
                    "metode_pembayaran": self.req("metodePembayaran"),
                    "bukti_transfer": self.req("buktiTransfer"),
                    "tanggal_setoran_diterima": date_now()
                }
            )
            .execute()
            .fetchone()
            .result
        )

        faktur = (
            self.query()
            .setRawQuery("SELECT * FROM faktur WHERE id_sales_order = :id_sales_order")
            .bindparams({"id_sales_order": self.req("notaFaktur")})
            .execute()
            .fetchone()
            .result
        )

        setoran = (
            self.query()
            .setRawQuery(
                """
                SELECT * FROM setoran WHERE id_sales_order = :id_sales_order
            """
            )
            .bindparams({"id_sales_order": self.req("notaFaktur")})
            .execute()
            .fetchall()
            .get()
        )

        for order in setoran:
            jumlah_setoran += order["jumlah_setoran"]

        # Set the status of faktur to 6
        if jumlah_setoran >= faktur["total_penjualan"]:
            (
                self.query()
                .setRawQuery(
                    """
                        UPDATE faktur SET status_faktur = 6 WHERE id_sales_order = :id
                    """
                )
                .bindparams({"id": self.req("notaFaktur")})
                .execute()
            )
            
            payment["current_status"] = 6
        else:
            payment["current_status"] = 1
            
        

        return payment

    @handle_error_rollback
    def submitRekapPembayaranSales(self):
        tanggal = self.req("tanggal")
        nama_sales = self.req("nama_sales")
        buktiTransfer = self.req("buktiTransfer")
        data = self.req("data")

        if not data or len(data) == 0:
            raise ValueError("Data pembayaran tidak boleh kosong")

        # Kumpulkan semua ID setoran_customer untuk update is_rekap
        setoran_customer_ids = []
        total_setoran_created = 0

        # Process setiap data pembayaran
        for item in data:
            id_setoran_customer = item.get("id")
            id_sales_order = item.get("id_sales_order")
            tunai = item.get("tunai", 0)
            non_tunai = item.get("non_tunai", 0)

            # Tambahkan ke list untuk update is_rekap
            if id_setoran_customer:
                setoran_customer_ids.append(id_setoran_customer)

            # Buat setoran untuk tunai jika > 0
            if tunai > 0:
                setoran_tunai = setoran(
                    id_sales_order=id_sales_order,
                    draft_jumlah_setor=tunai,
                    tipe_setoran=1,  # Tunai
                    nama_pj=nama_sales,
                    status_setoran=1,
                    draft_tanggal_input=tanggal,
                    id_setoran_customer=id_setoran_customer,
                    pj_setoran=1

                )
                self.add(setoran_tunai)
                total_setoran_created += 1

            # Buat setoran untuk non_tunai jika > 0
            if non_tunai > 0:
                setoran_non_tunai = setoran(
                    id_sales_order=id_sales_order,
                    draft_jumlah_setor=non_tunai,
                    tipe_setoran=2,  # Non Tunai
                    nama_pj=nama_sales,
                    status_setoran=1,
                    draft_tanggal_input=tanggal,
                    id_setoran_customer=id_setoran_customer,
                    bukti_transfer=buktiTransfer if buktiTransfer else None,
                    pj_setoran=1
                )
                self.add(setoran_non_tunai)
                total_setoran_created += 1

        # Flush untuk mendapatkan ID yang baru dibuat
        self.flush()

        # Update is_rekap = 1 untuk semua setoran_customer yang disubmit
        if setoran_customer_ids:
            setoran_customers_to_update = setoran_customer.query.filter(
                setoran_customer.id.in_(setoran_customer_ids)
            ).all()

            for sc in setoran_customers_to_update:
                sc.is_rekap = 1

        # Commit semua perubahan
        self.commit()

        return {
            "status": "success",
            "message": "Rekap pembayaran berhasil diproses",
            "total_data": len(data),
            "total_setoran_created": total_setoran_created,
            "total_setoran_customer_updated": len(setoran_customer_ids)
        }
