import datetime

from flask import request, current_app

from apps.handler import handle_error, handle_error_rollback, nonServerErrorException
from apps.lib.helper import date_now
from apps.lib.paginate import Paginate
from apps.models import setoran, sales_order, faktur, Plafon, MutasiBank, User, CreditNote
from .BaseAkuntansi import BaseAkuntansi
from ...lib.paginateV2 import PaginateV2


class Setoran(BaseAkuntansi):
    def __init__(self):
        super().__init__()

        self.baseFrom = """
            from setoran
            join sales_order on setoran.id_sales_order = sales_order.id
            join faktur on faktur.id_sales_order = sales_order.id
            join plafon on plafon.id = sales_order.id_plafon
            join customer on customer.id = plafon.id_customer
        """

    @handle_error
    def getListSetoran(self, tipe_setoran):
            tanggal = date_now()
            is_periode_close, next_date = self.check_is_periode_closed()
            if is_periode_close:
                tanggal = next_date.strftime('%Y-%m-%d')
                
            periode_awal = self.req('periode_awal') or tanggal
            periode_akhir = self.req('periode_akhir') or tanggal

            # Define conditions yang bisa dinamis dari request
            conditions = {
                "sales": 'sales.id = :sales',
                'status': 'setoran.status_setoran = :status',
                'id_cabang': 'users.id_cabang = :id_cabang',
            }

            # Kondisi yang selalu ada
            additional_conditions = [
                "setoran.draft_tanggal_input BETWEEN :periode_awal AND :periode_akhir",
                "setoran.tipe_setoran = :tipe_setoran"
            ]

            # Build WHERE clause
            where_clause, bindparams = self.buildWhereClause(conditions, additional_conditions)

            bindparams.update({
                'periode_awal': periode_awal,
                'periode_akhir': periode_akhir,
                'tipe_setoran': tipe_setoran
            })

            query = f"""
                WITH status_tagihan AS (
                    SELECT 
                        setoran.draft_tanggal_input,
                        setoran.nama_pj,
                        SUM(setoran.draft_jumlah_setor) AS setoran_piutang,
                        ARRAY_AGG(setoran.status_setoran) AS status_array,
                        CASE 
                            WHEN setoran.pj_setoran = 1 THEN plafon.id_sales 
                            ELSE NULL 
                        END AS id_sales,
                        setoran.nama_auditor,
                        setoran.nama_kasir,
                        setoran.pj_setoran
                    FROM setoran 
                    JOIN sales_order ON setoran.id_sales_order = sales_order.id
                    JOIN plafon ON sales_order.id_plafon = plafon.id
                    LEFT JOIN sales ON sales.id_user = plafon.id_sales
                    LEFT JOIN users ON users.id = sales.id_user
                    {where_clause}
                    GROUP BY 
                        setoran.draft_tanggal_input, 
                        setoran.nama_pj, 
                        id_sales,
                        setoran.nama_auditor, 
                        setoran.nama_kasir, 
                        setoran.pj_setoran
                )
                SELECT 
                    st.*,
                    CASE 
                        -- Menggunakan ALL pada array agar lebih efisien dibanding ARRAY_FILL
                        WHEN 0 = ALL(st.status_array) THEN 'admin gudang'
                        WHEN 1 = ALL(st.status_array) THEN 'sales'
                        WHEN 2 = ALL(st.status_array) THEN 'kasir'
                        WHEN 3 = ALL(st.status_array) THEN 'audit'
                        ELSE 'mixed status'
                    END AS status_setoran_label
                FROM status_tagihan st
                ORDER BY st.draft_tanggal_input DESC
            """

            return Paginate(request, query, bindparams).paginate()

    @handle_error
    def getDetailListSetoran(self):
        tanggal = self.req('tanggal')
        id_sales = self.req('id_sales')
        nama_pj = self.req('nama_pj')
        pj_setoran = self.req('pj_setoran')

        conditions = {
            "tanggal": "setoran.draft_tanggal_input = :tanggal",
            "tipe_setoran": "setoran.tipe_setoran = :tipe_setoran",
            "status": "setoran.status_setoran = :status",
            "nama_auditor": "setoran.nama_auditor = :nama_auditor",
            "nama_kasir": "setoran.nama_kasir = :nama_kasir",
            "nama_pj": "setoran.nama_pj = :nama_pj",
            "pj_setoran": "setoran.pj_setoran = :pj_setoran",
        }

        # Conditional logic for additional filter
        additional_conditions = []
        if pj_setoran and int(pj_setoran) == 1:
            additional_conditions.append(f"plafon.id_sales = :id_sales")
        elif pj_setoran and int(pj_setoran) == 2:
            additional_conditions.append("1=1")
        else:
            additional_conditions.append(f"plafon.id_sales = :id_sales")

        where_clause, bindparams = self.buildWhereClause(conditions, additional_conditions)

        # Add id_sales to bindparams if needed
        if id_sales and (not pj_setoran or int(pj_setoran) != 2):
            bindparams['id_sales'] = id_sales

        queryInformasi = f"""
            SELECT 
                COUNT(DISTINCT customer.id) as jumlah_customer,
                SUM(setoran.draft_jumlah_setor) as total_setoran,
                setoran.nama_pj,
                setoran.nama_auditor,
                setoran.nama_kasir
            {self.baseFrom}
            {where_clause}
            GROUP BY setoran.nama_pj, setoran.nama_auditor, setoran.nama_kasir
        """

        queryData = f"""
            SELECT 
                setoran.id as id_setoran,
                customer.id as id_customer,
                setoran.draft_tanggal_input as tanggal,
                customer.nama as nama_customer,
                faktur.no_faktur,
                (faktur.total_penjualan - (
                    SELECT COALESCE(SUM(s2.jumlah_setoran), 0)
                    FROM setoran s2
                    WHERE s2.id_sales_order = sales_order.id
                )) as tagihan,
                setoran.draft_jumlah_setor as setoran,
                CASE
                    WHEN ROUND((faktur.total_penjualan - (
                        SELECT COALESCE(SUM(s2.jumlah_setoran), 0)
                        FROM setoran s2
                        WHERE s2.id_sales_order = sales_order.id
                    ) - COALESCE((faktur.nominal_retur), 0))::numeric, 3) = 0
                    THEN 'lunas'
                    ELSE 'belum lunas'
                END as status_pembayaran,
                setoran.status_setoran,
                setoran.bukti_transfer,
                setoran.biaya_lainnya,
                setoran.ket_biaya_lainnya,
                setoran.max_biaya_lainnya,
                setoran.setor_diterima_kasir
            {self.baseFrom}
            {where_clause}
        """

        informasiSetoran = self.query().setRawQuery(queryInformasi).bindparams(bindparams).execute().fetchone().result
        listSetoran = self.query().setRawQuery(queryData).bindparams(bindparams).execute().fetchall().get()

        return {
            "informasi": {**informasiSetoran, "tanggal": tanggal, "id_sales": id_sales},
            "data": listSetoran
        }

    @handle_error_rollback
    def konfirmasiSetoran(self):
        id_setoran = self.req('id_setoran')
        status_setoran = self.req('status_setoran')
        nama_konfirmasi = self.req('nama_konfirmasi')
        diterima_kasir = self.req('diterima_kasir')

        is_sales = False

        token = request.headers.get('Authorization')
        if not token:
            raise nonServerErrorException(401, "Token tidak ditemukan")

        data_mapping_by_id_setoran = {}

        token = token.split(" ")[1] if " " in token else token
        user = (
            self.query().setRawQuery(
                "SELECT nama,id FROM users WHERE tokens = :token",
            )
            .bindparams({
                'token': token
            })
            .execute()
            .fetchone()
            .result
        )

        for id in id_setoran:
            update_setoran = setoran.query.filter(setoran.id == id).first()
            if not update_setoran:
                raise nonServerErrorException('tidak bisa menemukan id setoran yang dimaksud')
            update_setoran.status_setoran = int(status_setoran)
            if int(status_setoran) == 2:

                if update_setoran.id_order_batch:
                    update_faktur = faktur.query.filter(
                        faktur.id_order_batch == update_setoran.id_order_batch,
                    )
                else:
                    update_faktur = faktur.query.filter(faktur.id_sales_order == update_setoran.id_sales_order).first()

                profile = self.__get_data_profile_by_order(id_sales_order=update_faktur.id_sales_order,
                                                           id_order_batch=update_faktur.id_order_batch)

                if update_setoran.pj_setoran == 1:
                    is_sales = True
                else:
                    is_sales = False

                data_mapping_by_id_setoran[id] = {
                    "id_perusahaan": profile.get('id_perusahaan'),
                    "id_cabang": profile.get('id_cabang'),
                    "id_principal": profile.get('id_principal'),
                    "id_faktur": update_faktur.id,
                }

                update_setoran.nama_kasir = nama_konfirmasi
                if diterima_kasir and str(id) in diterima_kasir:
                    update_setoran.setor_diterima_kasir = (update_setoran.setor_diterima_kasir or 0) + float(
                        diterima_kasir[str(id)])
            elif int(status_setoran) == 3:
                update_setoran.nama_auditor = nama_konfirmasi
                update_setoran.tanggal_setoran_diterima = date_now()
                biaya_lainnya = update_setoran.biaya_lainnya or 0
                max_biaya = update_setoran.max_biaya_lainnya or 0
                # Hitung jumlah setoran
                update_setoran.jumlah_setoran = float(
                    update_setoran.draft_jumlah_setor) if biaya_lainnya > max_biaya else float(
                    update_setoran.draft_jumlah_setor) + biaya_lainnya
                # Flush untuk memastikan nilai setoran terupdate
                self.flush()
                # Ambil sales_order untuk mendapat plafon
                current_sales_order = sales_order.query.filter(
                    sales_order.id == update_setoran.id_sales_order
                ).first()
                if current_sales_order:
                    # Update sisa_bon di plafon
                    current_plafon = plafon.query.filter(
                        plafon.id == current_sales_order.id_plafon
                    ).first()
                    if current_plafon:
                        current_plafon.sisa_bon = (current_plafon.sisa_bon or 0) + update_setoran.jumlah_setoran
                    # Ambil faktur yang terkait dengan sales_order
                    current_faktur = faktur.query.filter(
                        faktur.id_sales_order == update_setoran.id_sales_order
                    ).first()
                    if current_faktur:
                        # Hitung total setoran yang sudah dikonfirmasi (termasuk yang sedang diproses)
                        total_setoran_dikonfirmasi = self.db.session.query(
                            self.db.func.coalesce(self.db.func.sum(setoran.jumlah_setoran), 0)
                        ).filter(
                            setoran.id_sales_order == update_setoran.id_sales_order,
                            setoran.status_setoran == 3
                        ).scalar()
                        # Hitung sisa tagihan
                        sisa_tagihan = current_faktur.total_penjualan - total_setoran_dikonfirmasi
                        # Update status faktur jika lunas
                        if sisa_tagihan <= 0:
                            current_faktur.status_faktur = 3
                self.flush()

        if status_setoran == 2:
            payload_pubsub = {
                "created_by": user.get('id'),
                "id_fitur_mal": 13 if is_sales else 14,
                "data": data_mapping_by_id_setoran,
            }

            pubsub = getattr(current_app, 'pubsub', None)

            if pubsub:
                success = pubsub.publish(data=payload_pubsub, topic="create_jurnal")
                if success:
                    current_app.logger.info("success publish pubsub")
                else:
                    current_app.logger.error("failed to publish pubsub")
                    raise nonServerErrorException(code=500, message='Gagal mengirim pesan ke sistem jurnal')
            else:
                current_app.logger.error('pubsub not found')
                raise nonServerErrorException(code=500, message='Gagal mengirim pesan ke sistem jurnal')

        self.commit()
        return {'status': 'konfirmasi sukses'}, 200

    @handle_error_rollback
    def addBiayaLainnya(self):
        id_setoran = self.req('id_setoran')
        biaya_lainnya = self.req('biaya_lainnya')
        ket_biaya_lainnya = self.req('ket_biaya_lainnya')
        is_max_biaya = self.req('is_max_biaya')

        update_setoran = setoran.query.filter(setoran.id == id_setoran).first()

        if not update_setoran:
            raise nonServerErrorException('tidak bisa menemukan id setoran yang dimaksud')

        update_setoran.biaya_lainnya = biaya_lainnya
        update_setoran.ket_biaya_lainnya = ket_biaya_lainnya
        update_setoran.max_biaya_lainnya = 5000 if is_max_biaya else 2900

        self.flush()
        self.commit()

        return {'status': 'biaya lainnya berhasil ditambahkan'}, 200

    @handle_error_rollback
    def simpanKasirSetoran(self):
        id_setoran = self.req('id_setoran')
        nama_kasir = self.req('nama_kasir')
        diterima_kasir = self.req('diterima_kasir')

        if not id_setoran:
            raise nonServerErrorException('id_setoran tidak boleh kosong')
        if not diterima_kasir:
            raise nonServerErrorException('diterima_kasir tidak boleh kosong')

        # Loop untuk setiap id_setoran
        for id in id_setoran:
            update_setoran = setoran.query.filter(setoran.id == id).first()

            if not update_setoran:
                raise nonServerErrorException('tidak bisa menemukan id setoran yang dimaksud')

            if nama_kasir:
                update_setoran.nama_kasir = nama_kasir

            # Update setor_diterima_kasir dengan menambahkan nilai dari payload
            if diterima_kasir and str(id) in diterima_kasir:
                current_value = update_setoran.setor_diterima_kasir or 0
                additional_value = float(diterima_kasir[str(id)])
                update_setoran.setor_diterima_kasir = current_value + additional_value

        self.flush()
        self.commit()

        return {'status': 'setoran berhasil disimpan oleh kasir'}, 200

    @handle_error
    def getListFakturSetoran(self, type):
        """
        Get a list of faktur setoran.
        """
        if type not in ['sales', 'customer']:
            raise nonServerErrorException(400, "Type harus 'sales' atau 'customer'")
        if type == 'customer':
            id_customer = self.req('id_customer')
            data_faktur = (
                self.query().setRawQuery(
                    """
                    WITH data_cte AS (SELECT pp.nama,
                                             f.no_faktur,
                                             f.id            AS id_faktur,
                                             so.tanggal_faktur,
                                             p.id_customer,
                                             f.nominal_retur as total_retur,
                                             p.id_principal,
                                             so.tanggal_jatuh_tempo,
                                             f.total_penjualan,
                                             COALESCE(
                                                     (SELECT SUM(s.jumlah_setoran)
                                                      FROM setoran s
                                                      WHERE s.id_sales_order = so.id
                                                        AND s.status_setoran = 3),
                                                     0
                                             )
                                                             AS setoran --kalo disini itu yg sudah dibayarkan,                        
                                      FROM faktur f
                                               JOIN sales_order so ON so.id = f.id_sales_order
                                               JOIN plafon p ON p.id = so.id_plafon
                                               JOIN customer c ON c.id = p.id_customer
                                               JOIN principal pp ON pp.id = p.id_principal
                                      WHERE f.status_faktur = 2
                                        AND c.id = :id_customer
                                      ORDER BY so.tanggal_jatuh_tempo ASC)
                    SELECT *
                    FROM data_cte
                    """
                )
                .bindparams({"id_customer": id_customer})
                .execute()
                .fetchall()
                .get()
            )

            return {
                "data": data_faktur,
            }
        else:
            id_sales = self.req('id_sales')
            data_faktur = (
                self.query().setRawQuery(
                    """
                    WITH data_cte AS (SELECT pp.nama,
                                             f.no_faktur,
                                             f.id                 AS id_faktur,
                                             so.tanggal_faktur,
                                             p.id_customer,
                                             c.nama               AS nama_customer,
                                             s.draft_jumlah_setor AS jumlah_setoran,
                                             s.id                 AS id_setoran_customer,
                                             f.nominal_retur      as total_retur,
                                             p.id_principal,
                                             so.tanggal_jatuh_tempo,
                                             f.total_penjualan,
                                             COALESCE(
                                                     (SELECT SUM(s.jumlah_setoran)
                                                      FROM setoran s
                                                      WHERE s.id_sales_order = so.id
                                                        AND s.status_setoran = 3),
                                                     0
                                             )
                                                                  AS setoran --kalo disini itu yg sudah dibayarkan,                        

                                      FROM faktur f
                                               JOIN sales_order so ON so.id = f.id_sales_order
                                               JOIN plafon p ON p.id = so.id_plafon
                                               JOIN customer c ON c.id = p.id_customer
                                               JOIN principal pp ON pp.id = p.id_principal
                                               JOIN setoran s ON s.id_sales_order = so.id
                                      WHERE f.status_faktur = 2
                                        AND p.id_sales = :id_sales
                                        AND s.tipe_setoran = 2
                                        AND s.status_setoran = 1
                                        AND s.pj_setoran = 1
                                      ORDER BY so.tanggal_jatuh_tempo ASC)
                    SELECT *
                    FROM data_cte
                    """
                )
                .bindparams({"id_sales": id_sales})
                .execute()
                .fetchall()
                .get()
            )

            return {
                "data": data_faktur,
            }

    @handle_error_rollback
    def insertSetoranKonfirmasiNonTunaiByCustomer(self, id_mutasi):
        """
        Insert a non-cash deposit confirmation.
        """
        id_customer = self.req('id_customer')
        data_fakturs = self.req('data_faktur')
        token = request.headers.get('Authorization')
        if not token:
            raise nonServerErrorException(401, "Token tidak ditemukan")
        token = token.split(" ")[1] if " " in token else token
        user = (
            self.query().setRawQuery(
                "SELECT nama, id FROM users WHERE tokens = :token",
            )
            .bindparams({
                'token': token
            })
            .execute()
            .fetchone()
            .result
        )

        if not user:
            raise nonServerErrorException(401, "Token tidak valid atau user tidak ditemukan")

        if not id_mutasi or not id_customer or not data_fakturs:
            raise nonServerErrorException(400, "ID mutasi, ID customer, dan data faktur tidak boleh kosong")

        data_mutasi, user_mutasi = (self.db.session.query(MutasiBank, users)
                                    .join(users, MutasiBank.id_user == users.id)
                                    .filter(MutasiBank.id_mutasi == int(id_mutasi))
                                    .with_for_update()
                                    .first())

        if not data_mutasi:
            raise nonServerErrorException(404, "Mutasi tidak ditemukan")

        ids_faktur = [faktur['id_faktur'] for faktur in data_fakturs if 'id_faktur' in faktur]
        if not ids_faktur:
            raise nonServerErrorException(400, "Tidak ada faktur yang dipilih untuk setoran")

        real_fakturs = (faktur.query.filter(faktur.id.in_(ids_faktur))
                        .with_for_update()
                        .all())

        if len(real_fakturs) != len(ids_faktur):
            raise nonServerErrorException(400, "Beberapa faktur yang dipilih tidak ditemukan")

        data_mapping_by_id_setoran = {}

        setoran_must_paids = (
            self.query()
            .setRawQuery("""
                         WITH data_cte AS (SELECT pp.nama,
                                                  f.no_faktur,
                                                  f.id  AS                     id_faktur,
                                                  p.id  AS                     id_plafon,
                                                  pp.id AS                     id_principal,
                                                  so.tanggal_faktur,
                                                  p.id_sales,
                                                  so.tanggal_jatuh_tempo,
                                                  COALESCE(f.nominal_retur, 0) total_retur,
                                                  f.total_penjualan,
                                                  COALESCE(
                                                          (SELECT SUM(s.jumlah_setoran)
                                                           FROM setoran s
                                                           WHERE s.id_sales_order = so.id
                                                             AND s.status_setoran = 3),
                                                          0
                                                  )
                                                        AS                     setoran --ini yg harus dibayarkan
                                           FROM faktur f
                                                    JOIN sales_order so ON so.id = f.id_sales_order
                                                    JOIN plafon p ON p.id = so.id_plafon
                                                    JOIN customer c ON c.id = p.id_customer
                                                    JOIN principal pp ON pp.id = p.id_principal
                                           WHERE f.status_faktur = 2
                                             AND c.id = :id_customer
                                             AND f.id IN :id_fakturs

                                           ORDER BY so.tanggal_jatuh_tempo ASC)
                         SELECT *
                         FROM data_cte
                         """)
            .bindparams_v2({
                "id_customer": id_customer,
                "id_fakturs": ids_faktur,

            }, expanding_keys=['id_fakturs']
            )
            .execute()
            .fetchall()
            .get()
        )

        nominal_mutasi = data_mutasi.sisa

        for data_faktur in real_fakturs:
            id_faktur = data_faktur.id

            setoran_must_paid = next(
                (faktur for faktur in setoran_must_paids if faktur['id_faktur'] == id_faktur),
                None
            )

            data_setoran = setoran_must_paid.get('total_penjualan') - setoran_must_paid.get(
                'setoran') - setoran_must_paid.get('total_retur', 0)

            if not data_setoran:
                raise nonServerErrorException(400, f"Faktur {id_faktur} sudah lunas, tidak bisa melakukan setoran")

            id_cn = next(
                (faktur['id_cn'] for faktur in data_fakturs if 'id_cn' in faktur and faktur['id_faktur'] == id_faktur),
                None
            )

            data_plafon_update = (plafon.query
                                  .with_for_update()
                                  .filter(setoran_must_paid.get('id_plafon') == plafon.id)
                                  .first())

            data_faktur_update = faktur.query.with_for_update().filter(faktur.id == id_faktur).first()
            if id_cn:
                credit_note_used = (
                    CreditNote.query
                    .with_for_update()
                    .filter(CreditNote.id_cn == id_cn, CreditNote.id_customer == id_customer, CreditNote.status_cn == 0,
                            CreditNote.id_principal == setoran_must_paid.get('id_principal'))
                    .first()
                )

                if not credit_note_used:
                    raise nonServerErrorException(400, f"Credit Note {id_cn} tidak ditemukan atau sudah digunakan")

                credit_note_used.status_cn = 1  # Update status Credit Note menjadi digunakan
                credit_note_used.id_faktur = id_faktur  # Set ID faktur yang digunakan

                data_setoran -= credit_note_used.total_cn

                if data_setoran <= 0:
                    raise nonServerErrorException(400,
                                                  f"Setoran untuk faktur {id_faktur} tidak boleh negatif setelah menggunakan Credit Note {id_cn}")

                data_plafon_update.sisa_bon = (data_plafon_update.sisa_bon or 0) + credit_note_used.total_cn

                self.add(credit_note_used)

                # Update total_cn pada faktur yang digunakan
                self.flush()

                data_faktur_update.nominal_retur = (data_faktur_update.nominal_retur or 0) + credit_note_used.total_cn

            draft_jumlah_setor = data_setoran

            if nominal_mutasi >= data_setoran:
                # Jika nominal mutasi lebih besar atau sama dengan setoran yang harus dibayar
                # Setoran yang akan dimasukkan adalah data_setoran
                data_faktur_update.status_faktur = 3  # Status faktur lunas
                data_faktur_update.total_dana_diterima = setoran_must_paid.get('setoran') + data_setoran
                data_plafon_update.sisa_bon = (data_plafon_update.sisa_bon or 0) + data_setoran
                draft_jumlah_setor = data_setoran

            else:
                # Jika nominal mutasi kurang dari setoran yang harus dibayar
                # Setoran yang akan dimasukkan adalah nominal_mutasi
                data_plafon_update.sisa_bon = (data_plafon_update.sisa_bon or 0) + nominal_mutasi
                draft_jumlah_setor = nominal_mutasi

            self.add(data_plafon_update)

            if (nominal_mutasi < draft_jumlah_setor) and ((nominal_mutasi * 2) <= draft_jumlah_setor):
                raise nonServerErrorException(400,
                                              f"Nominal mutasi {nominal_mutasi} tidak cukup untuk setoran dalam kelipatan 2x, faktur {id_faktur}")

            # Kurangi nominal mutasi dengan jumlah setoran
            nominal_mutasi -= draft_jumlah_setor

            # Insert setoran
            new_setoran = setoran(
                id_sales_order=data_faktur.id_sales_order,
                draft_tanggal_input=data_mutasi.tanggal_mutasi,
                draft_jumlah_setor=draft_jumlah_setor,
                nama_pj=user_mutasi.nama,
                jumlah_setoran=draft_jumlah_setor,
                tipe_setoran=2,  # Non-tunai
                tanggal_setoran_diterima=date_now(),
                nama_auditor=user['nama'],
                status_setoran=3,  # Sudah dikonfirmasi
                max_biaya_lainnya=2900,  # Biaya lainnya tetap
                pj_setoran=3,  # Non-tunai
            )

            profile = self.__get_data_profile_by_order(id_sales_order=data_faktur.id_sales_order,
                                                       id_order_batch=data_faktur.id_order_batch)

            self.db.session.add(new_setoran)
            self.db.session.flush()

            data_mapping_by_id_setoran[new_setoran.id] = {
                "id_faktur": id_faktur,
                "id_perusahaan": profile.get('id_perusahaan'),
                "id_cabang": profile.get('id_cabang'),
                "id_principal": profile.get('id_principal'),
            }

            # Update faktur commit
            self.db.session.add(data_faktur_update)
            self.db.session.flush()

        # Update mutasi bank
        data_mutasi.id_customer = id_customer

        if nominal_mutasi > 0:
            data_mutasi.sisa = nominal_mutasi
        else:
            # Jika tidak ada sisa, set ke 0
            data_mutasi.status_mutasi = 0
            data_mutasi.sisa = 0

        self.db.session.add(data_mutasi)

        payload_pubsub = {
            "created_by": user.get('id'),
            "id_fitur_mal": 6,
            "data": data_mapping_by_id_setoran,
        }

        pubsub = getattr(current_app, 'pubsub', None)
        if pubsub:
            success = pubsub.publish(data=payload_pubsub, topic="create_jurnal")
            if success:
                current_app.logger.info("success publish pubsub")
            else:
                current_app.logger.error("failed to publish pubsub")
                raise nonServerErrorException(code=500, message='Gagal mengirim pesan ke sistem jurnal')
        else:
            current_app.logger.error('pubsub not found')
            raise nonServerErrorException(code=500, message='Gagal mengirim pesan ke sistem jurnal')

        self.db.session.commit()

        return {
            "message": "Setoran non-tunai berhasil disimpan",
        }

    def __get_data_profile_by_order(self, id_sales_order, id_order_batch=None):
        if id_order_batch:
            query_get_profile = """
                                SELECT pc.id_perusahaan, so.id_cabang, p.id_principal
                                FROM sales_order so
                                         JOIN plafon p ON so.id_plafon = p.id
                                         JOIN principal pc ON pc.id = p.id_principal
                                WHERE so.id_order_batch = :id_order_batch
                                LIMIT 1 \
                                """
            profile = self.query().setRawQuery(query_get_profile).bindparams(
                {"id_order_batch": id_order_batch}).execute().fetchone().result
        else:
            query_get_profile = """
                                SELECT pc.id_perusahaan, so.id_cabang, p.id_principal
                                FROM sales_order so
                                         JOIN plafon p ON so.id_plafon = p.id
                                         JOIN principal pc ON pc.id = p.id_principal
                                WHERE so.id = :id_sales_order
                                LIMIT 1 \
                                """
            profile = self.query().setRawQuery(query_get_profile).bindparams(
                {"id_sales_order": id_sales_order}).execute().fetchone().result
        return profile

    @handle_error_rollback
    def insertSetoranKonfirmasiNonTunaiBySales(self, id_mutasi):
        """
        Insert a non-cash deposit confirmation.
        """
        data_fakturs = self.req('data_faktur')
        id_sales = self.req('id_sales')
        token = request.headers.get('Authorization')
        if not token:
            raise nonServerErrorException(401, "Token tidak ditemukan")
        token = token.split(" ")[1] if " " in token else token
        user = (
            self.query().setRawQuery(
                "SELECT nama, id FROM users WHERE tokens = :token",
            )
            .bindparams({
                'token': token
            })
            .execute()
            .fetchone()
            .result
        )

        if not user:
            raise nonServerErrorException(401, "Token tidak valid atau user tidak ditemukan")

        if not id_mutasi or not id_sales or not data_fakturs:
            raise nonServerErrorException(400, "ID mutasi, ID customer, dan data faktur tidak boleh kosong")

        data_mutasi, user_mutasi = (self.db.session.query(MutasiBank, users)
                                    .join(users, MutasiBank.id_user == users.id)
                                    .filter(MutasiBank.id_mutasi == int(id_mutasi), MutasiBank.status_mutasi == 1)
                                    .with_for_update()
                                    .first())

        if not data_mutasi:
            raise nonServerErrorException(404, "Mutasi tidak ditemukan")

        ids_faktur = list({faktur['id_faktur'] for faktur in data_fakturs if 'id_faktur' in faktur})
        ids_setoran = [faktur['id_setoran_customer'] for faktur in data_fakturs if 'id_setoran_customer' in faktur]
        if not ids_faktur:
            raise nonServerErrorException(400, "Tidak ada faktur yang dipilih untuk setoran")

        real_fakturs = (faktur.query.filter(faktur.id.in_(ids_faktur))
                        .with_for_update()
                        .all())

        real_setorans = (setoran.query
                         .filter(setoran.id.in_(ids_setoran), setoran.tipe_setoran == 2, setoran.status_setoran == 1,
                                 setoran.pj_setoran == 1)
                         .all()
                         )

        if len(real_fakturs) != len(ids_faktur):
            raise nonServerErrorException(400, "Beberapa faktur yang dipilih tidak ditemukan")

        if len(real_setorans) != len(ids_setoran):
            raise nonServerErrorException(400, "Beberapa setoran yang dipilih tidak ditemukan atau tidak valid")

        setoran_must_paids = (
            self.query()
            .setRawQuery("""
                         WITH data_cte AS (SELECT pp.nama,
                                                  f.no_faktur,
                                                  f.id  AS                     id_faktur,
                                                  p.id  AS                     id_plafon,
                                                  pp.id AS                     id_principal,
                                                  so.tanggal_faktur,
                                                  p.id_sales,
                                                  so.tanggal_jatuh_tempo,
                                                  COALESCE(f.nominal_retur, 0) total_retur,
                                                  f.total_penjualan,
                                                  COALESCE(
                                                          (SELECT SUM(s.jumlah_setoran)
                                                           FROM setoran s
                                                           WHERE s.id_sales_order = so.id
                                                             AND s.status_setoran = 3),
                                                          0
                                                  )
                                                        AS                     setoran --ini yg harus dibayarkan
                                           FROM faktur f
                                                    JOIN sales_order so ON so.id = f.id_sales_order
                                                    JOIN plafon p ON p.id = so.id_plafon
                                                    JOIN customer c ON c.id = p.id_customer
                                                    JOIN principal pp ON pp.id = p.id_principal
                                           WHERE f.status_faktur = 2
                                             AND p.id_sales = :id_sales
                                             AND f.id IN :id_fakturs

                                           ORDER BY so.tanggal_jatuh_tempo ASC)
                         SELECT *
                         FROM data_cte
                         """)
            .bindparams_v2({
                "id_sales": id_sales,
                "id_fakturs": ids_faktur,

            }, expanding_keys=['id_fakturs']
            )
            .execute()
            .fetchall()
            .get()
        )

        data_mapping_by_id_setoran = {}

        nominal_mutasi = data_mutasi.sisa

        for odata_setoran in real_setorans:
            id_faktur = next(
                (faktur['id_faktur'] for faktur in data_fakturs if
                 'id_faktur' in faktur and faktur['id_setoran_customer'] == odata_setoran.id),
                None
            )

            setoran_must_paid = next(
                (faktur for faktur in setoran_must_paids if faktur['id_faktur'] == id_faktur),
                None
            )

            data_setoran = setoran_must_paid.get('total_penjualan') - setoran_must_paid.get(
                'setoran') - setoran_must_paid.get('total_retur', 0)

            if not data_setoran:
                raise nonServerErrorException(400, f"Faktur {id_faktur} sudah lunas, tidak bisa melakukan setoran")

            data_faktur_update = faktur.query.with_for_update().filter(faktur.id == id_faktur).first()

            update_setoran = setoran.query.filter(setoran.id == odata_setoran.id).first()

            if data_setoran == update_setoran.draft_jumlah_setor:
                # Jika nominal mutasi lebih besar atau sama dengan setoran yang harus dibayar
                data_faktur_update.status_faktur = 3  # Status faktur lunas
                data_faktur_update.total_dana_diterima = setoran_must_paid.get(
                    'setoran') + update_setoran.draft_jumlah_setor

            plafon_update = (plafon.query
                             .with_for_update()
                             .filter(setoran_must_paid.get('id_plafon') == plafon.id)
                             .first()
                             )

            profile = self.__get_data_profile_by_order(id_sales_order=data_faktur_update.id_sales_order,
                                                       id_order_batch=data_faktur_update.id_order_batch)

            data_mapping_by_id_setoran[update_setoran.id] = {
                "id_faktur": id_faktur,
                "id_perusahaan": profile.get('id_perusahaan'),
                "id_cabang": profile.get('id_cabang'),
                "id_principal": profile.get('id_principal'),
            }

            plafon_update.sisa_bon = (plafon_update.sisa_bon or 0) + update_setoran.draft_jumlah_setor

            self.add(plafon_update)

            update_setoran.jumlah_setoran = update_setoran.draft_jumlah_setor
            update_setoran.tanggal_setoran_diterima = date_now()
            update_setoran.nama_auditor = user['nama']
            update_setoran.status_setoran = 3
            update_setoran.max_biaya_lainnya = 2900

            # Kurangi nominal mutasi dengan jumlah setoran
            nominal_mutasi -= update_setoran.draft_jumlah_setor

            self.db.session.add(update_setoran)

            # Update faktur commit
            self.db.session.add(data_faktur_update)
            self.db.session.flush()

        # Update mutasi bank
        data_mutasi.id_sales = id_sales

        if nominal_mutasi != 0:
            raise nonServerErrorException(400,
                                          f"Nominal mutasi tidak sesuai dengan setoran yang dilakukan, sisa mutasi {nominal_mutasi}")

        data_mutasi.sisa = 0
        data_mutasi.status_mutasi = 0

        self.db.session.add(data_mutasi)

        self.db.session.commit()

        payload_pubsub = {
            "created_by": user.get('id'),
            "id_fitur_mal": 6,
            "data": data_mapping_by_id_setoran,
        }

        pubsub = getattr(current_app, 'pubsub', None)
        if pubsub:
            success = pubsub.publish(data=payload_pubsub, topic="create_jurnal")
            if not success:
                raise nonServerErrorException(500, "Gagal mempublikasikan data ke pubsub")
            else:
                print("Sukses mempublikasikan data ke pubsub")
        else:
            print("Pubsub tidak tersedia di current_app")

        return {
            "message": "Setoran non-tunai berhasil disimpan",
        }

    @handle_error
    def getListKonfirmasiSetoranTunai(self):
        """
        Get a list of confirmed cash deposits.
        """
        periode_awal = self.req('periode_awal')
        periode_akhir = self.req('periode_akhir')

        query = f"""
        select 
            s.nama_pj,
    	    s.draft_tanggal_input,
            sum(s.setor_diterima_kasir) as total_setor_diterima_kasir
            from setoran s
            where s.tipe_setoran = 1
            and s.status_setoran = 2
            and s.pj_setoran in (1,2)
            
        """

        # Conditional logic for additional filter
        bindParams = {}
        if periode_awal and periode_akhir:
            # 2025-08-01
            start_date = datetime.datetime.strptime(periode_awal, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(periode_akhir, '%Y-%m-%d').date()

            bindParams['start_date'] = start_date
            bindParams['end_date'] = end_date

            query += " and s.draft_tanggal_input between :start_date and :end_date "

        else:
            start_date = None
            end_date = None

        query += """group by s.nama_pj, s.draft_tanggal_input""";

        return PaginateV2(request=request, query=query, bindParams=bindParams).paginate()

    @handle_error
    def getDetailKonfirmasiSetoranTunai(self, nama_pj, draft_tanggal_input):
        """
        Get details of a confirmed cash deposit.
        """

        if not nama_pj or not draft_tanggal_input:
            raise nonServerErrorException(400, "Nama penanggung jawab atau tanggal input tidak ditemukan")

        detail_setoran = (
            self.query().setRawQuery(
                """
                SELECT s.nama_pj,
                       s.draft_tanggal_input,
                       SUM(s.setor_diterima_kasir)   as total_setoran,
                       COUNT(DISTINCT p.id_customer) AS jumlah_customer,
                       s.nama_kasir
                FROM setoran s
                         JOIN sales_order so
                              ON so.id = s.id_sales_order
                         JOIN plafon p
                              ON p.id = so.id_plafon
                WHERE s.tipe_setoran = 1
                  AND s.status_setoran = 2
                  AND s.pj_setoran IN (1, 2)
                  AND s.nama_pj = :nama_pj

                  AND s.draft_tanggal_input = :draft_tanggal_input
                GROUP BY s.nama_pj,
                         s.nama_kasir,
                         s.draft_tanggal_input
                ORDER BY s.draft_tanggal_input DESC;
                """,
            )
            .bindparams(
                {
                    'nama_pj': nama_pj,
                    'draft_tanggal_input': draft_tanggal_input
                }
            )
            .execute()
            .fetchone()
            .result
        )

        if not detail_setoran:
            raise nonServerErrorException(404, "Detail setoran tidak ditemukan")

        list_setoran = (
            self.query().setRawQuery(
                """
                with data_cte AS (SELECT s.nama_pj,
                                         s.draft_tanggal_input,
                                         s.setor_diterima_kasir,
                                         s.nama_kasir,
                                         pp.nama                      nama_principal,
                                         c.nama                       nama_customer,
                                         f.no_faktur,
                                         so.tanggal_jatuh_tempo,
                                         f.total_penjualan,
                                         COALESCE(f.nominal_retur, 0) total_retur,
                                         COALESCE(
                                                 (SELECT SUM(s.jumlah_setoran)
                                                  FROM setoran s
                                                  WHERE s.id_sales_order = so.id
                                                    AND s.status_setoran = 3),
                                                 0
                                         )
                                             AS                       setoran
                                  FROM setoran s
                                           JOIN sales_order so
                                                ON so.id = s.id_sales_order
                                           JOIN plafon p
                                                ON p.id = so.id_plafon
                                           JOIN principal pp
                                                ON pp.id = p.id_principal
                                           JOIN customer c
                                                ON c.id = p.id_customer
                                           JOIN faktur f
                                                ON f.id_sales_order = so.id
                                  WHERE s.tipe_setoran = 1
                                    AND s.status_setoran = 2
                                    AND s.pj_setoran IN (1, 2)
                                    AND s.nama_pj = :nama_pj
                                    AND s.draft_tanggal_input = :draft_tanggal_input
                                  ORDER BY s.draft_tanggal_input DESC)
                SELECT *
                from data_cte
                """
            )
            .bindparams(
                {
                    'nama_pj': nama_pj,
                    'draft_tanggal_input': draft_tanggal_input
                }
            )
            .execute()
            .fetchall()
            .get()
        )

        return {
            "status": "success",
            "data": {
                "detail_setoran": detail_setoran,
                "list_setoran": list_setoran
            }
        }

    @handle_error_rollback
    def konfirmasiSetoranTunai(self):
        """
        Confirm cash deposits.
        """
        nama_pj = self.req('nama_pj')
        draft_tanggal_input = self.req('draft_tanggal_input')
        token = request.headers.get('Authorization')
        if not token:
            raise nonServerErrorException(401, "Token tidak ditemukan")

        data_mapping_by_id_setoran = {}

        token = token.split(" ")[1] if " " in token else token
        user = (
            self.query().setRawQuery(
                "SELECT nama,id FROM users WHERE tokens = :token",
            )
            .bindparams({
                'token': token
            })
            .execute()
            .fetchone()
            .result
        )

        data_setorans = (
            self.query().setRawQuery(
                """
                with data_cte AS (SELECT s.nama_pj,
                                         s.id                         id_setoran,
                                         s.draft_tanggal_input,
                                         s.setor_diterima_kasir,
                                         s.nama_kasir,
                                         p.id                         id_plafon,
                                         pp.nama                      nama_principal,
                                         c.nama                       nama_customer,
                                         f.no_faktur,
                                         f.id                         id_faktur,
                                         so.tanggal_jatuh_tempo,
                                         f.total_penjualan,
                                         COALESCE(f.nominal_retur, 0) total_retur,
                                         COALESCE(
                                                 (SELECT SUM(s.jumlah_setoran)
                                                  FROM setoran s
                                                  WHERE s.id_sales_order = so.id
                                                    AND s.status_setoran = 3),
                                                 0
                                         )
                                             AS                       setoran --ini yg harus dibayarkan
                                  FROM setoran s
                                           JOIN sales_order so
                                                ON so.id = s.id_sales_order
                                           JOIN plafon p
                                                ON p.id = so.id_plafon
                                           JOIN principal pp
                                                ON pp.id = p.id_principal
                                           JOIN customer c
                                                ON c.id = p.id_customer
                                           JOIN faktur f
                                                ON f.id_sales_order = so.id
                                  WHERE s.tipe_setoran = 1
                                    AND s.status_setoran = 2
                                    AND s.pj_setoran IN (1, 2)
                                    AND s.nama_pj = :nama_pj
                                    AND s.draft_tanggal_input = :draft_tanggal_input
                                  ORDER BY s.draft_tanggal_input DESC)
                SELECT *
                from data_cte
                """
            )
            .bindparams(
                {
                    'nama_pj': nama_pj,
                    'draft_tanggal_input': draft_tanggal_input
                }
            )
            .execute()
            .fetchall()
            .get()
        )

        for data_setoran in data_setorans:

            update_setoran = setoran.query.filter(
                setoran.id == data_setoran['id_setoran']
            ).first()

            if not update_setoran:
                raise nonServerErrorException(f"Setoran dengan ID {data_setoran.id_setoran} tidak ditemukan")

            update_setoran.jumlah_setoran = update_setoran.draft_jumlah_setor
            update_setoran.tanggal_setoran_diterima = date_now()
            update_setoran.nama_auditor = user['nama']
            update_setoran.status_setoran = 3

            self.add(update_setoran)

            total_tagihan = data_setoran['total_penjualan'] - data_setoran['setoran'] - data_setoran['total_retur']
            update_faktur = (faktur.query
                             .with_for_update()
                             .filter(
                faktur.id == data_setoran['id_faktur']
            ).first())

            if not update_faktur:
                raise nonServerErrorException(f"Faktur dengan ID {data_setoran['id_faktur']} tidak ditemukan")

            if update_setoran.draft_jumlah_setor == total_tagihan:
                update_faktur.status_faktur = 3  # Status faktur lunas
                update_faktur.total_dana_diterima = data_setoran['setoran'] + update_setoran.draft_jumlah_setor - \
                                                    data_setoran['total_retur']

                self.add(update_faktur)

            plafon_update = (plafon.query
                             .with_for_update()
                             .filter(data_setoran['id_plafon'] == plafon.id)
                             .first())

            plafon_update.sisa_bon = (plafon_update.sisa_bon or 0) + update_setoran.draft_jumlah_setor

            profile = self.__get_data_profile_by_order(id_sales_order=update_faktur.id_sales_order,
                                                       id_order_batch=update_faktur.id_order_batch)

            data_mapping_by_id_setoran[update_setoran.id] = {
                "id_faktur": data_setoran['id_faktur'],
                "id_perusahaan": profile.get('id_perusahaan'),
                "id_cabang": profile.get('id_cabang'),
                "id_principal": profile.get('id_principal'),
            }

            self.add(plafon_update)

            self.flush()

        payload_pubsub = {
            "created_by": user.get('id'),
            "id_fitur_mal": 12,
            "data": data_mapping_by_id_setoran,
        }

        pubsub = getattr(current_app, 'pubsub', None)
        if pubsub:
            success = pubsub.publish(data=payload_pubsub, topic="create_jurnal")
            if not success:
                raise nonServerErrorException(500, "Gagal mempublikasikan data ke pubsub")
            else:
                current_app.logger.info("Sukses mempublikasikan data ke pubsub")
        else:
            current_app.logger.error("Pubsub tidak tersedia di current_app")

        self.commit()

        return {
            "status": "success",
            "message": "Setoran tunai berhasil dikonfirmasi",
            "data": data_setorans
        }
