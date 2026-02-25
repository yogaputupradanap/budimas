from flask import request, current_app

from apps.handler import handle_error, handle_error_rollback, nonServerErrorException
from apps.lib.helper import date_now, datetime_now
from apps.lib.paginate import Paginate
from apps.models.pengeluaran_kasir import pengeluaran_kasir
from .BaseAkuntansi import BaseAkuntansi


class Kasir(BaseAkuntansi):
    def __init__(self):
        super().__init__()

    @handle_error
    def getListPengeluaranKasir(self):
        tanggal = date_now()
        tanggal_pengajuan = self.req('tanggal_pengajuan') or tanggal
        id_jabatan = self.req('id_jabatan')

        if id_jabatan not in ['16', '2']:  # Assuming 16 is the ID for Kasir
            id_user = self.req('id_user')
            additional_conditions = [
                "DATE(pk.tanggal_pengajuan) = :tanggal_pengajuan",
                "pk.id_user = :id_user"
            ]
        else:
            id_user = None
            additional_conditions = [
                "DATE(pk.tanggal_pengajuan) = :tanggal_pengajuan"
            ]

        conditions = {
            "id_cabang": "pk.id_cabang = :id_cabang",
            "status_pengeluaran": "pk.status_pengeluaran = :status_pengeluaran",
        }

        where_clause, bindparams = self.buildWhereClause(conditions, additional_conditions)
        bindparams['tanggal_pengajuan'] = tanggal_pengajuan
        if id_user is not None:
            bindparams['id_user'] = id_user

        query = f"""
            SELECT 
                pk.id,
                pk.id_cabang,
                pk.id_user,
                pk.no_pengeluaran,
                pk.keterangan_pengeluaran,
                pk.pic,
                TO_CHAR(pk.tanggal_pengajuan, 'YYYY-MM-DD HH24:MI:SS') AS tanggal_pengajuan,
                TO_CHAR(pk.tanggal_acc, 'YYYY-MM-DD HH24:MI:SS') AS tanggal_acc,
                TO_CHAR(pk.tanggal_diberikan, 'YYYY-MM-DD HH24:MI:SS') AS tanggal_diberikan,
                pk.jumlah_pengeluaran,
                pk.status_pengeluaran,
                pk.jumlah_acc,
                u.nama AS nama_kasir,
                c.nama AS nama_cabang,
                p.id as id_perusahaan,
                p.kode as kode_perusahaan,
                p.nama as nama_perusahaan
            FROM pengeluaran_kasir pk
            JOIN users u ON pk.id_user = u.id
            JOIN cabang c ON pk.id_cabang = c.id
            LEFT JOIN perusahaan p ON pk.id_perusahaan = p.id
            {where_clause}
            ORDER BY pk.tanggal_pengajuan DESC
        """

        return Paginate(request, query, bindparams).paginate()

    @handle_error_rollback
    def addPengeluaranKasir(self):
        # Get request data
        id_user = self.req('id_user')
        id_cabang = self.req('id_cabang')
        keterangan_pengeluaran = self.req('keterangan_pengeluaran')
        pic = self.req('pic')
        jumlah_pengeluaran = self.req('jumlah_pengeluaran')
        # kode_cabang = self.req('kode_cabang')
        id_perusahaan = self.req('id_perusahaan')

        res_perusahaan = self.query().setRawQuery(
        "SELECT kode FROM perusahaan WHERE id = :id_perusahaan"
        ).bindparams({'id_perusahaan': id_perusahaan}).execute().fetchone().result
        
        kode_perusahaan = res_perusahaan.get('kode') if res_perusahaan else None

        # 3. Ambil Kode Cabang OTOMATIS dari database
        res_cabang = self.query().setRawQuery(
            "SELECT kode FROM cabang WHERE id = :id_cabang"
        ).bindparams({'id_cabang': id_cabang}).execute().fetchone().result
        
        kode_cabang = res_cabang.get('kode') if res_cabang else None

        # Validation - check required fields
        if not id_user:
            raise nonServerErrorException(500, 'ID User wajib diisi atau refresh halaman terlebih dahulu')

        if not id_cabang:
            raise nonServerErrorException(500, 'ID Cabang wajib diisi atau refresh halaman terlebih dahulu')

        if not pic:
            raise nonServerErrorException(500, 'PIC wajib diisi')

        if not jumlah_pengeluaran:
            raise nonServerErrorException(500, 'Jumlah pengeluaran wajib diisi')

        if not kode_perusahaan:
            raise nonServerErrorException(500, 'Kode perusahaan wajib diisi')

        if not kode_cabang:
            raise nonServerErrorException(500, 'Kode cabang wajib diisi')

        if not id_perusahaan:
            raise nonServerErrorException(500, 'ID Perusahaan wajib diisi')

        # Generate no_pengeluaran
        current_year_month = datetime_now()[:7].replace('-', '')  # Format: YYYYMM
        prefix = f"OUT/{kode_perusahaan}{kode_cabang}/{current_year_month}-"

        # Get the latest counter for this month
        query_counter = f"""
            SELECT COUNT(*) as counter 
            FROM pengeluaran_kasir 
            WHERE no_pengeluaran LIKE :prefix
        """

        counter_result = self.query().setRawQuery(query_counter).bindparams({
            'prefix': f"{prefix}%"
        }).execute().fetchone().result

        counter = (counter_result['counter'] or 0) + 1
        counter_str = str(counter).zfill(4)

        no_pengeluaran = f"{prefix}{counter_str}"

        # Create new pengeluaran_kasir record
        new_pengeluaran = pengeluaran_kasir(
            no_pengeluaran=no_pengeluaran,
            id_user=int(id_user),
            id_cabang=int(id_cabang),
            keterangan_pengeluaran=keterangan_pengeluaran,
            pic=pic,
            tanggal_pengajuan=datetime_now(),
            # tanggal_acc=None,
            tanggal_diberikan=None,
            jumlah_pengeluaran=float(jumlah_pengeluaran),
            status_pengeluaran=1,
            id_perusahaan=int(id_perusahaan),
            jumlah_acc=float(jumlah_pengeluaran),  # Set jumlah_acc same as jumlah_pengeluaran initially
            tanggal_acc=datetime_now()
        )

        self.add(new_pengeluaran)
        self.flush()

        payload_pubsub = {
            'id_fitur_mal': 15,
            'id_perusahaan': int(id_perusahaan),
            'id_cabang': int(id_cabang),
            'id_pengeluaran': new_pengeluaran.id,
            'created_by': int(id_user),
        }

        pubsub = getattr(current_app, 'pubsub', None)
        if pubsub:
            success = pubsub.publish(data=payload_pubsub, topic='log_activity')
            if not success:
                current_app.logger.error(
                    f'Failed to publish to pubsub topic log_activity with payload: {payload_pubsub}')
                raise nonServerErrorException(500, 'Gagal mempublikasikan pesan ke PubSub')

            current_app.logger.info(f'Published to pubsub topic log_activity with payload: {payload_pubsub}')
        else:
            current_app.logger.error('PubSub client is not configured in the current_app context.')

        # Add to database
        self.flush()
        self.commit()

        return {'message': f'Pengeluaran kasir berhasil ditambahkan dengan no : {no_pengeluaran}',
                'status': 'success'}, 200

    @handle_error
    def getKonfirmasiPengeluaranKasir(self, id=None):
        id_pengeluaran = self.req('id_pengeluaran') or id

        if not id_pengeluaran:
            raise nonServerErrorException('ID Pengeluaran wajib diisi')

        query = """
                SELECT pk.id,
                       pk.no_pengeluaran,
                       pk.id_cabang,
                       pk.id_user,
                       pk.keterangan_pengeluaran,
                       pk.pic,
                       TO_CHAR(pk.tanggal_pengajuan, 'YYYY-MM-DD HH24:MI:SS') AS tanggal_pengajuan,
                       TO_CHAR(pk.tanggal_acc, 'YYYY-MM-DD HH24:MI:SS')       AS tanggal_acc,
                       TO_CHAR(pk.tanggal_diberikan, 'YYYY-MM-DD HH24:MI:SS') AS tanggal_diberikan,
                       pk.jumlah_pengeluaran,
                       pk.jumlah_acc,
                       pk.status_pengeluaran,
                       u.nama                                                 AS nama_kasir,
                       c.nama                                                 AS nama_cabang,
                       pk.status_pengeluaran,
                       p.id                                                   as id_perusahaan,
                       p.kode                                                 as kode_perusahaan,
                       p.nama                                                 as nama_perusahaan
                FROM pengeluaran_kasir pk
                         JOIN users u ON pk.id_user = u.id
                         JOIN cabang c ON pk.id_cabang = c.id
                         JOIN perusahaan p ON pk.id_perusahaan = p.id
                WHERE pk.id = :id_pengeluaran \
                """

        result = self.query().setRawQuery(query).bindparams({
            'id_pengeluaran': id_pengeluaran
        }).execute().fetchone().result

        if not result:
            raise nonServerErrorException('Data pengeluaran kasir tidak ditemukan')

        return result

    @handle_error_rollback
    def konfirmasiPengeluaranKasir(self):
        id_pengeluaran = self.req('id_pengeluaran')
        status_pengeluaran = 3

        token = request.headers.get('Authorization').replace('Bearer ', '')
        user = self.query().setRawQuery(
            "SELECT id FROM users WHERE tokens = :token"
        ).bindparams({'token': token}).execute().fetchone().result

        if not id_pengeluaran:
            raise nonServerErrorException(500, 'ID Pengeluaran wajib diisi')

        # Find the pengeluaran kasir record
        update_pengeluaran = pengeluaran_kasir.query.filter(
            pengeluaran_kasir.id == id_pengeluaran
        ).first()

        if not update_pengeluaran:
            raise nonServerErrorException(500, 'Data pengeluaran kasir tidak ditemukan')

        # Validasi status harus 1 sebelum bisa diubah ke 3
        if update_pengeluaran.status_pengeluaran != 1:
            raise nonServerErrorException(500, 'Status pengeluaran harus sudah di-setujui sebelum bisa dikonfirmasi')

        # Update status
        update_pengeluaran.status_pengeluaran = int(status_pengeluaran)
        update_pengeluaran.tanggal_diberikan = datetime_now()

        payload_pubsub = {
            'id_fitur_mal': 11,
            'id_perusahaan': update_pengeluaran.id_perusahaan,
            'id_cabang': update_pengeluaran.id_cabang,
            'id_pengeluaran': id_pengeluaran,
            'created_by': user.get('id'),
        }

        pubsub = getattr(current_app, 'pubsub', None)
        if pubsub:
            success = pubsub.publish(data=payload_pubsub, topic='create_jurnal')
            if not success:
                current_app.logger.error(
                    f'Failed to publish to pubsub topic create_jurnal with payload: {payload_pubsub}')
                raise nonServerErrorException(500, 'Gagal mempublikasikan pesan ke PubSub')

            current_app.logger.info(f'Published to pubsub topic create_jurnal with payload: {payload_pubsub}')
        else:
            current_app.logger.error('PubSub client is not configured in the current_app context.')

        self.flush()
        self.commit()
        data_update = self.getKonfirmasiPengeluaranKasir(id=id_pengeluaran)

        return {'message': 'Pengeluaran kasir berhasil dikonfirmasi', 'data': data_update}, 200

    @handle_error
    def listLaporanKasir(self):
        tanggal = date_now()
        periode_awal = self.req('periode_awal') or tanggal
        periode_akhir = self.req('periode_akhir') or tanggal

        conditions = {
            "id_cabang": "laporan.id_cabang = :id_cabang",
        }

        additional_conditions = [
            "laporan.tanggal BETWEEN :periode_awal AND :periode_akhir"
        ]

        where_clause, bindparams = self.buildWhereClause(conditions, additional_conditions)
        bindparams.update({
            'periode_awal': periode_awal,
            'periode_akhir': periode_akhir
        })

        query = f"""
            WITH pemasukan AS (
                SELECT 
                    s.draft_tanggal_input AS tanggal,
                    u.id_cabang,
                    SUM(s.setor_diterima_kasir) AS total_pemasukan
                FROM setoran s
                JOIN sales_order so ON s.id_sales_order = so.id
                JOIN plafon p ON so.id_plafon = p.id
                JOIN sales sa ON p.id_sales = sa.id
                JOIN users u ON sa.id_user = u.id
                WHERE s.tipe_setoran = 1 
                    AND s.status_setoran IN (2, 3)
                    AND s.draft_tanggal_input BETWEEN :periode_awal AND :periode_akhir
                GROUP BY s.draft_tanggal_input, u.id_cabang
            ),
            pengeluaran AS (
                SELECT 
                    DATE(pk.tanggal_diberikan) AS tanggal,
                    pk.id_cabang,
                    SUM(pk.jumlah_pengeluaran) AS total_pengeluaran
                FROM pengeluaran_kasir pk
                WHERE pk.status_pengeluaran = 3
                    AND DATE(pk.tanggal_diberikan) BETWEEN :periode_awal AND :periode_akhir
                GROUP BY DATE(pk.tanggal_diberikan), pk.id_cabang
            ),
            laporan AS (
                SELECT 
                    COALESCE(pemasukan.tanggal, pengeluaran.tanggal) AS tanggal,
                    COALESCE(pemasukan.id_cabang, pengeluaran.id_cabang) AS id_cabang,
                    COALESCE(pemasukan.total_pemasukan, 0) AS total_pemasukan,
                    COALESCE(pengeluaran.total_pengeluaran, 0) AS total_pengeluaran,
                    (COALESCE(pemasukan.total_pemasukan, 0) - COALESCE(pengeluaran.total_pengeluaran, 0)) AS saldo_akhir
                FROM pemasukan
                FULL OUTER JOIN pengeluaran ON pemasukan.tanggal = pengeluaran.tanggal 
                    AND pemasukan.id_cabang = pengeluaran.id_cabang
            )
            SELECT 
                ROW_NUMBER() OVER (ORDER BY laporan.tanggal DESC) AS id,
                laporan.tanggal,
                laporan.total_pemasukan,
                laporan.total_pengeluaran,
                laporan.saldo_akhir,
                c.nama AS nama_cabang
            FROM laporan
            LEFT JOIN cabang c ON laporan.id_cabang = c.id
            {where_clause}
            ORDER BY laporan.tanggal DESC
        """

        return Paginate(request, query, bindparams).paginate()

    @handle_error
    def getDetailLaporanKasir(self):
        tanggal = self.req('tanggal')
        jenis = self.req('jenis')  # optional filter: 'pemasukan' atau 'pengeluaran'
        id_cabang = self.req('id_cabang')

        if not tanggal:
            raise nonServerErrorException(500, 'Tanggal wajib diisi')

        if not id_cabang:
            raise nonServerErrorException(500, 'ID Cabang wajib diisi')

        # Query untuk detail laporan
        detail_conditions = []
        detail_params = {
            'tanggal': tanggal,
            'id_cabang': id_cabang
        }

        # Build UNION query untuk pemasukan dan pengeluaran
        pemasukan_query = """
                          SELECT s.draft_tanggal_input  AS tanggal,
                                 'pemasukan'            AS jenis,
                                 s.setor_diterima_kasir AS nominal,
                                 s.nama_pj              AS pic
                          FROM setoran s
                                   JOIN sales_order so ON s.id_sales_order = so.id
                                   JOIN plafon p ON so.id_plafon = p.id
                                   JOIN sales sa ON p.id_sales = sa.id
                                   JOIN users u ON sa.id_user = u.id
                          WHERE s.tipe_setoran = 1
                            AND s.status_setoran IN (2, 3)
                            AND s.draft_tanggal_input = :tanggal
                            AND u.id_cabang = :id_cabang \
                          """

        pengeluaran_query = """
                            SELECT pk.tanggal_diberikan  AS tanggal,
                                   'pengeluaran'         AS jenis,
                                   pk.jumlah_pengeluaran AS nominal,
                                   pk.pic                AS pic
                            FROM pengeluaran_kasir pk
                            WHERE pk.status_pengeluaran = 3
                              AND DATE(pk.tanggal_diberikan) = :tanggal
                              AND pk.id_cabang = :id_cabang \
                            """

        # Jika ada filter jenis
        if jenis == 'pemasukan':
            detail_query = pemasukan_query
        elif jenis == 'pengeluaran':
            detail_query = pengeluaran_query
        else:
            detail_query = f"""
                {pemasukan_query}
                UNION ALL
                {pengeluaran_query}
            """

        detail_query += " ORDER BY jenis, nominal DESC"

        detail_result = self.query().setRawQuery(detail_query).bindparams(detail_params).execute().fetchall().result

        if detail_result:
            detail_result = [dict(row) for row in detail_result]

        info_query = """
                     WITH pemasukan AS (SELECT COALESCE(SUM(s.setor_diterima_kasir), 0) AS total_pemasukan
                                        FROM setoran s
                                                 JOIN sales_order so ON s.id_sales_order = so.id
                                                 JOIN plafon p ON so.id_plafon = p.id
                                                 JOIN sales sa ON p.id_sales = sa.id
                                                 JOIN users u ON sa.id_user = u.id
                                        WHERE s.tipe_setoran = 1
                                          AND s.status_setoran IN (2, 3)
                                          AND s.draft_tanggal_input = :tanggal
                                          AND u.id_cabang = :id_cabang),
                          pengeluaran AS (SELECT COALESCE(SUM(pk.jumlah_pengeluaran), 0) AS total_pengeluaran
                                          FROM pengeluaran_kasir pk
                                          WHERE pk.status_pengeluaran = 3
                                            AND DATE(pk.tanggal_diberikan) = :tanggal
                                            AND pk.id_cabang = :id_cabang)
                     SELECT pemasukan.total_pemasukan,
                            pengeluaran.total_pengeluaran,
                            (pemasukan.total_pemasukan - pengeluaran.total_pengeluaran) AS sisa_saldo
                     FROM pemasukan,
                          pengeluaran \
                     """

        info_result = self.query().setRawQuery(info_query).bindparams(detail_params).execute().fetchone().result

        if info_result:
            info_result = dict(info_result)

        return {
            'detailLaporan': detail_result or [],
            'laporanInfo': info_result or {
                'total_pemasukan': 0,
                'total_pengeluaran': 0,
                'sisa_saldo': 0
            }
        }
