from datetime import datetime
from . import BaseServices
from apps.handler import handle_error
from ..lib.helper import get_now_datetime, get_current_day_number, get_week_number_cycle


class Customer(BaseServices):

    @handle_error
    def getSalesCustomer(self, id_user):
        """
         @brief Get customer information for sales. This is a wrapper around L { Query } to get the data for a customer and its sales
         @param id_user ID of the user to get the customer for
         @param nama_customer NAMA of the customer to get
         @return A dictionary with the customer information or None if not found ( for example if id_user is None
        """
        query = (
            """
                SELECT customer.nama, customer.kode, customer.id
                FROM plafon
                JOIN customer ON customer.id = plafon.id_customer
                LEFT JOIN sales ON sales.id = plafon.id_sales
                WHERE plafon.id_user = :id_user
				group by customer.nama, customer.kode, customer.id
            """
        )
        
        params = {"id_user": id_user}
        
        return self.query().setRawQuery(query).bindparams(params).execute().fetchall().get()

    @handle_error
    def getHistoryCustomer(self):
        """
         @brief Get sales orders and returbs for a customer. This is used to get history of orders and retur for a customer
         @return list of sales orders and
        """
        id_user = int(self.req("id_user"))
        id_customer = self.req("id_customer")
        from_date = self.req("from_date")
        to_date = self.req("to_date")
        
        def getOrder(tipe):    
            # This function will return a list of plafon sales_order order retur and order plafon sales retur
            query = (
                f"""
                    select sales_order.*, faktur.*, customer.*, principal.nama AS nama_principal from plafon
                    join sales_order on plafon.id = sales_order.id_plafon join customer on customer.id = plafon.id_customer
                    join faktur on faktur.id_sales_order = sales_order.id join principal on plafon.id_principal = principal.id
                    where faktur.jenis_faktur = '{tipe}' and plafon.id_user = :id_user and customer.id = :id_customer and
                    sales_order.tanggal_order between :from_date and :to_date
                """
            )
            
            params = {
                "id_user": id_user,
                "id_customer": id_customer,
                "from_date": str(from_date),
                "to_date": str(to_date)
            }
            
            return self.query().setRawQuery(query).bindparams(params).execute().fetchall().get()
            
        return {
            "sales_order": getOrder('penjualan'),
            "sales_retur": getOrder('retur')
        }
        
    @handle_error
    def getCustomerOrder(self, plafon_id, orderStatus):
        """
         @brief Get customer orders based on plafon_id and order_status. This is used to get the order details for a customer
         @param plafon_id id of the planet that is to be ordered
         @param orderStatus status of the order to be retrieved ( active or cancelled )
         @return list of dictionaries with information about the sales orders for a customer. Each dictionary in the list is keyed by the order id
        """
        orders = []

        sales_orders = (
            self.query()
            .setRawQuery(
                """
                    SELECT *
                    FROM sales_order
                    WHERE id_plafon = :id_plafon
                    AND
                    status_order = :order_status
                """
            )
            .bindparams({"id_plafon": plafon_id, "order_status": orderStatus})
            .execute()
            .fetchall()
            .get()
        )

        # Add products to the list of orders
        for order in sales_orders:
            order_detail = (
                self.query()
                .setRawQuery(
                """
                    SELECT *
                    FROM sales_order_detail
                    WHERE id_sales_order = :id_sales_order
                """
                )
                .bindparams({"id_sales_order": order["id"]})
                .execute()
                .fetchall()
                .get()
            )

            order["products"] = order_detail

            orders.append(order)

        return orders

    @handle_error
    def customerSisaPlafon(self):
        """
        Retrieves the remaining credit (sisa plafon) for customers and calculates their outstanding balance (piutang).

        Returns:
            list: A list of dictionaries containing credit and balance details for each customer.
        """

        plafon_jadwal_list = self.currentPlafonJadwal(self.req("id_user"))

        # Validasi plafon_jadwal_list
        if plafon_jadwal_list:
            for idx, jadwal in enumerate(plafon_jadwal_list):
                if jadwal is None:
                    return {"status": "error", "message": f"jadwal at index {idx} is None"}

                # Cek nilai-nilai dalam jadwal
                if jadwal.get("id_minggu") is None:
                    return {"status": "error", "message": f"id_minggu at index {idx} is None"}
                if jadwal.get("id_hari") is None:
                    return {"status": "error", "message": f"id_hari at index {idx} is None"}
                if jadwal.get("id") is None:
                    return {"status": "error", "message": f"id at index {idx} is None"}
                if jadwal.get("id_plafon") is None:
                    return {"status": "error", "message": f"id_plafon at index {idx} is None"}

        week_combo = {
            5: [1, 2], 6: [1, 3],
            7: [1, 4], 8: [2, 3],
            9: [2, 4], 10: [3, 4]
        }

        # Replace direct datetime usage with helper function
        day_number = get_current_day_number()
        week_number = int(get_week_number_cycle())

        def shouldCreateKunjungan(jadwal, week_number, day_number, week_combo):
            """
             Checks if Kunjungan should be created based on week and day.
            """
            # Validasi nilai sebelum konversi
            id_minggu = jadwal["id_minggu"]
            id_hari = jadwal["id_hari"]

            if id_minggu is None:
                return {"error": "id_minggu is None"}
            if id_hari is None:
                return {"error": "id_hari is None"}

            week = int(id_minggu)
            day = int(id_hari)

            # Use helper function instead of direct datetime import
            now_date = get_now_datetime()
            # id_holidays = holidays.country_holidays('ID')

            # if now_date in id_holidays: return False

            # Returns true if the week is in the combo week.
            if (week == week_number or week == 11) and day == day_number:
                return True
            elif week in week_combo:
                return any(combo_week == week_number and day == day_number for combo_week in week_combo[week])
            return False

        query = """
            SELECT
                principal.id AS id_principal,
                customer.id AS id_customer,
                plafon.id AS id_plafon,
                plafon.id_user AS id_user,
                principal.nama AS nama_principal,
                customer.nama AS nama_customer,
                customer.kode as kode_customer,
                limit_bon, 
                sisa_bon
            FROM plafon
            LEFT JOIN customer ON customer.id = plafon.id_customer
            LEFT JOIN principal ON principal.id = plafon.id_principal 
            WHERE plafon.id_user = :id_user AND plafon.id_customer = :id_customer
        """

        params = {
            "id_user": self.req("id_user"),
            "id_customer": self.req("id_customer"),
        }

        sisa_plafon_records = (
            self.query()
            .setRawQuery(query)
            .bindparams(params)
            .execute()
            .fetchall()
            .get()
        )

        def calculate_credit(plafon):
            limit_bon = plafon.get("limit_bon", 0)
            sisa_bon = plafon.get("sisa_bon", limit_bon)
            remaining_credit = sisa_bon if sisa_bon else limit_bon
            outstanding_balance = int(limit_bon) - int(sisa_bon or limit_bon)

            return {
                **plafon,
                "limit_bon": remaining_credit,
                "piutang": outstanding_balance,
            }

        result = [calculate_credit(plafon) for plafon in sisa_plafon_records]

        id_plafon_kunjungan = []

        for jadwal in plafon_jadwal_list:
            # Create a kunjungan if necessary.
            should_create = shouldCreateKunjungan(jadwal, week_number, day_number, week_combo)

            if should_create is True:
                id_plafon_kunjungan.append(jadwal["id_plafon"])

        # result awal: list of dict (misal hasil dari calculate_credit)
        # id_plafon_kunjungan: list of id_plafon yang valid

        filtered_result = [
            r for r in result
            if r.get("id_plafon") in id_plafon_kunjungan
        ]

        return filtered_result

    def currentPlafonJadwal(self, id_user):
        """
         Get the plafon jadwal of the user. It is possible to have more than one plafon but the user must have at least one of them

         @param id_user - ID of the user.

         @return list of dictionary `
        """
        query = (
            f"""
                select plafon_jadwal.* from plafon_jadwal join plafon
                on plafon.id = plafon_jadwal.id_plafon
                where plafon.id_user = {id_user} 
                and plafon_jadwal.id_status = 1
                and plafon_jadwal.id_hari IS NOT NULL
                and plafon_jadwal.id_minggu IS NOT NULL
            """
        )

        return self.query().setRawQuery(query).execute().fetchall().get()