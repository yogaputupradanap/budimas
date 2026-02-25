from . import BaseServices
from apps.handler import handle_error, nonServerErrorException, handle_error_rollback
from ..lib.helper import date_now, time_now, date_now_stamp, time_now_stamp, datetime_now
from ..lib.paginate import Paginate
from ..lib.paginateV2 import PaginateV2
from ..lib.utils import calculate_konversi
from ..models import Plafon, Principal, Perusahaan, ReturRequest, ReturRequestDetail, LogInventory, Stok, CreditNoteDetail, CreditNote
from flask import request


class Retur(BaseServices):

    @handle_error
    def get_list_pengajuan(self):
        """
        Get all retur data.
        """
        id_rute = self.req('id_rute')

        retur = (
            self.query()
            .setRawQuery(
                """
                SELECT
                    r.tanggal_request,
                    c.nama,
                    r.id_request,
                    rute.nama_rute,
                    COUNT(rrd.id_request_detail) AS jumlah_barang
                FROM retur_request r
                         JOIN customer c ON r.id_customer = c.id
                         LEFT JOIN retur_request_detail rrd ON rrd.id_request = r.id_request
                         JOIN rute ON rute.id = c.id_rute
                WHERE c.id_rute = :id_rute AND r.status_request = '0'
                GROUP BY r.id_request, c.id, rute.nama_rute
                """
            )
            .bindparams({"id_rute": id_rute})
            .execute()
            .fetchall()
            .get()  # atau hilangkan .get() jika tidak ada method-nya
        )

        if not retur:
            raise nonServerErrorException("Tidak ada retur yang ditemukan", 404)

        return retur

    @handle_error
    def get_retur_detail(self, id_request):
        """
        Get detail of a specific retur request.
        """
        header_retur_detail = (
            self.query()
            .setRawQuery(
                """
                SELECT
                    r.tanggal_request,
                    c.nama,
                    c.kode,
                    c.alamat,
                    r.id_request,
                    so.id_plafon,
                    rute.nama_rute,
                    pr.nama nama_perusahaan,
                    pr.alamat alamat_perusahaan,
                    COUNT(rrd.id_request_detail) AS jumlah_barang
                FROM retur_request r
                         JOIN customer c ON r.id_customer = c.id
                         JOIN retur_request_detail rrd ON rrd.id_request = r.id_request
                         JOIN sales_order so ON so.id = r.id_sales_order
                         JOIN plafon p ON p.id = so.id_plafon
                         JOIN principal pc ON pc.id = p.id_principal
                         JOIN perusahaan pr ON pr.id = pc.id_perusahaan
                         JOIN rute ON rute.id = c.id_rute
                WHERE r.id_request = :id_request
                GROUP BY r.id_request, c.id, rute.nama_rute, so.id_plafon, pc.id, pr.id,
                         p.id
                """
            )
            .bindparams({"id_request": id_request})
            .execute()
            .fetchone()
            .result
        )

        if not header_retur_detail:
            raise nonServerErrorException("Detail retur tidak ditemukan", 404)

        detail_retur = (
            self.query()
            .setRawQuery(
                """
                SELECT
                    rrd.alasan_retur,
                    rrd.karton_diajukan,
                    rrd.box_diajukan,
                    rrd.id_produk,
                    rrd.pieces_diajukan,
                    rrd.pieces_retur,
                    rrd.box_retur,
                    rrd.karton_retur,
                    rrd.box_good_diajukan,
                    rrd.karton_good_diajukan,
                    rrd.pieces_good_diajukan,                    
                    p.kode_sku,
                    p.nama AS nama_produk,
                    -- GROUP TO JSON DATA PRODUCT UOM
                    json_agg(DISTINCT jsonb_build_object(
                'id', pu.id,
                'level', pu.level,
		        'faktor_konversi', pu.faktor_konversi
                 )) AS uom_list
                FROM retur_request_detail rrd
                         JOIN produk p ON p.id = rrd.id_produk
                         JOIN produk_uom pu ON pu.id_produk = p.id
                WHERE rrd.id_request = :id_request
                GROUP BY rrd.alasan_retur, rrd.karton_diajukan, rrd.box_diajukan,
                         rrd.pieces_diajukan, p.id , rrd.id_produk,
                         rrd.pieces_retur, rrd.box_retur, rrd.karton_retur, rrd.box_good_diajukan,
                         rrd.karton_good_diajukan, rrd.pieces_good_diajukan
                ;

                """
            )
            .bindparams({"id_request": id_request})
            .execute()
            .fetchall()
            .get()  # atau hilangkan .get() jika tidak ada method-nya
        )

        if not detail_retur:
            raise nonServerErrorException("Detail retur tidak ditemukan", 404)

        id_plafon = header_retur_detail['id_plafon']
        data_plafon = (
            self.db.session.query(plafon,
                                  principal,
                                  perusahaan.kode.label('kode_perusahan'))
            .join(principal, plafon.id_principal == principal.id)
            .join(perusahaan, principal.id_perusahaan == perusahaan.id)
            .filter(plafon.id == id_plafon)
            .first()
        )

        if not data_plafon:
            raise nonServerErrorException("Data plafon tidak ditemukan", 404)

        principal_data = data_plafon[1]
        kode_perusahan = data_plafon[2]
        prefix_kode_kpr = f"KPR/{kode_perusahan}-{principal_data.kode}"

        last_kode_request = (
            ReturRequest.query.filter(
                ReturRequest.kode_kpr.startswith(prefix_kode_kpr)
            ).with_for_update().order_by(ReturRequest.kode_kpr.desc()).first()
        )
        if last_kode_request:
            last_number = int(last_kode_request.kode_kpr.split('/')[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        counter_str = f"{new_number:04d}"

        kode_kpr = f"{prefix_kode_kpr}/{counter_str}"

        header_retur_detail['kode_kpr'] = kode_kpr
        tanggal_request = header_retur_detail['tanggal_request']

        header_retur_detail['tanggal_request'] = tanggal_request.strftime("%d/%m/%Y")

        return {
            "header": header_retur_detail,
            "detail": detail_retur
        }

    @handle_error_rollback
    def cetak_kpr(self, id_request):
        """
        Cetak KPR untuk retur request.
        """
        kode_kpr = self.req('kode_kpr')

        if not kode_kpr:
            raise nonServerErrorException("Kode KPR tidak boleh kosong", 400)

        # Update kode_kpr pada retur_request
        retur_request = ReturRequest.query.filter_by(id_request=int(id_request)).first()
        if not retur_request:
            raise nonServerErrorException("Retur request tidak ditemukan", 404)
        retur_request.kode_kpr = kode_kpr
        retur_request.status_request = 1
        self.add(retur_request).flush()
        self.commit()

        return {"message": "KPR berhasil dicetak", "id_request": id_request}

    @handle_error
    def get_retur_list(self):
        """
        Get list of retur requests.
        """
        bind_params = {"id_cabang": self.req('id_cabang')}
        id_customer = self.req('id_customer')

        where_clause = "WHERE r.id_cabang = :id_cabang AND rr.status_request > '0'"

        if id_customer:
            where_clause += " AND rr.id_customer = :id_customer"
            bind_params['id_customer'] = id_customer


        query = f"""
        SELECT 
        rr.kode_kpr, 
        c.nama nama_customer,
        rr.tanggal_request,
        rr.id_request,
        rr.status_request,
        COUNT(rrd.id_request_detail) jumlah_barang
        from retur_request rr
        JOIN retur_request_detail rrd
        ON rr.id_request = rrd.id_request
        JOIN customer c 
        ON c.id = rr.id_customer
        JOIN rute r
        ON r.id = c.id_rute 
        {where_clause}
        GROUP BY rr.id_request, c.nama 
        """

        return PaginateV2(request=request,query=query,bindParams=bind_params).paginate()

    @handle_error_rollback
    def insert_retur_stock(self, id_request):
        """
        Insert retur stock for a specific request.
        """
        retur_request = (ReturRequest.query.filter_by(id_request=int(id_request))
                        .with_for_update()
                         .first())
        headers = request.headers.get('Authorization')

        token = headers.split(' ')[1] if headers else None

        is_periode_closed, next_date = self.check_is_periode_closed()

        product = self.req('items')

        if not retur_request:
            raise nonServerErrorException("Retur request tidak ditemukan", 404)

        if not product:
            raise nonServerErrorException("Produk tidak boleh kosong", 400)

        # Update status request to '2' (retur stock)
        retur_request.status_request = 2

        datas_retur_request_detail = (
            self.query().setRawQuery(
                """
                SELECT
                    rrd.id_request_detail,
                    rrd.id_produk,
                    rrd.karton_retur AS karton_diajukan,
                    rrd.box_retur AS box_diajukan,
                    rrd.pieces_retur AS pieces_diajukan,
                    p.ppn,
                    rrd.id_sales_order_detail,
                    -- GROUP TO JSON DATA PRODUCT UOM
                    json_agg(
                            DISTINCT jsonb_build_object(
                            'id', produk_uom.id,
                            'level', produk_uom.level,
                            'faktor_konversi', produk_uom.faktor_konversi
                                     )
                    ) AS uom_list
                FROM retur_request_detail rrd
                         JOIN produk p ON p.id = rrd.id_produk
                         JOIN produk_uom ON produk_uom.id_produk = rrd.id_produk
                WHERE rrd.id_request = :id_request
                GROUP BY  rrd.id_request_detail,
                          p.ppn
                """
            )
        .bindparams({"id_request": id_request})
        .execute()
        .fetchall()
            .get()
        )
        if not datas_retur_request_detail:
            raise nonServerErrorException("Tidak ada detail retur yang ditemukan", 404)

        # Check user
        user =(
            self.query().setRawQuery(
            """
            SELECT id, id_cabang FROM users WHERE tokens = :token
            """
        )
        .bindparams({"token": token})
        .execute()
        .fetchone()
            .result
        )

        # Check if have voucher

        voucher_used = (
            self.query().setRawQuery(
                """
                select dv.id_sales_order_detail,
                    dv.tipe_voucher,
                       CASE
                           WHEN dv.tipe_voucher = 1
                               THEN v1.persentase_diskon_1
                           WHEN dv.tipe_voucher = 2
                               THEN v2.persentase_diskon_2
                           WHEN dv.tipe_voucher = 3
                               THEN v3.persentase_diskon_3
                           ELSE NULL
                           END AS persentase_diskon
                from retur_request rr
                         join draft_voucher dv
                              on dv.id_sales_order = rr.id_sales_order
                         left join voucher_1 v1
                                   on v1.id = dv.id_voucher
                         left join voucher_2 v2
                                   on v2.id = dv.id_voucher
                         left join voucher_3 v3
                                   on v3.id = dv.id_voucher
                where dv.status_promo = '2'
                and rr.id_request = :id_request
                ORDER BY dv.tipe_voucher DESC
                """
            )
            .bindparams({"id_request": id_request})
            .execute()
            .fetchall()
            .get()
        )

        # data for log
        data_plafon = (
            self.query().setRawQuery(
                """
                select pp.id_perusahaan, so.id_cabang, p.kode from retur_request rr
                                                               JOIN sales_order so
                                                                    ON so.id = rr.id_sales_order
                                                               JOIN plafon p
                                                                    ON p.id = so.id_plafon
                                                               JOIN principal pp
                                                                    ON pp.id = p.id_principal
                    WHERE rr.id_request = :id_request
                """
            )
            .bindparams({"id_request":id_request})
            .execute()
            .fetchone()
            .result
        )

        subtotal_retur_request_retur = 0
        total_diskon_retur_request_retur = 0
        total_dpp_retur_request_retur = 0
        total_ppn_retur_request_retur = 0
        total_retur_request_retur = 0

        # Generate Credit Note

        date_stamp = date_now_stamp()

        if is_periode_closed:
            date_stamp = date_now_stamp(add_days=1)

        prefix_no_cn = f"CN/{date_stamp}/{data_plafon['kode']}"

        last_cn = (
            CreditNote.query
            .filter(CreditNote.kode_cn.startswith(prefix_no_cn))
            .with_for_update()
            .order_by(CreditNote.kode_cn.desc())
            .first()
        )
        if last_cn:
            last_number = int(last_cn.kode_cn.split('/')[-1].split('-')[-1])
            next_number = last_number + 1
        else:
            next_number = 1

        kode_cn = f"{prefix_no_cn}-{next_number:04d}"

        tanggal = datetime_now()
        if is_periode_closed:
            tanggal = datetime_now(add_days=1)

        insert_credit_note = CreditNote(
            kode_cn=kode_cn,
            id_customer=retur_request.id_customer,
            id_principal=retur_request.id_principal,
            tanggal=tanggal,
            status_cn=0,  # Status CN 0 berarti belum dipakai
            id_retur_request=retur_request.id_request,
        )

        self.add(insert_credit_note)
        self.flush()

        tanggal_date = date_now()
        if is_periode_closed:
            tanggal_date = next_date.strftime('%Y-%m-%d')

        # Update retur_request
        for item in product:
            data_retur_request_detail = (
                next((detail for detail in datas_retur_request_detail if detail['id_produk'] == item.get('id_produk')), None)
            )

            data_voucher_used = sorted(
                [
                    voucher for voucher in voucher_used
                    if voucher['id_sales_order_detail'] == data_retur_request_detail.get('id_sales_order_detail')
                ],
                key=lambda v: v['tipe_voucher'],  # ascending
                reverse=True  # jadi 3, 2, 1
            )

            if not data_retur_request_detail:
                raise nonServerErrorException("Detail retur tidak ditemukan untuk produk ID: {}".format(item.get('id_produk')), 404)

            data_retur = calculate_konversi(
                value={
                    "karton": data_retur_request_detail.get('karton_diajukan', 0),
                    "box": data_retur_request_detail.get('box_diajukan', 0),
                    "pieces": data_retur_request_detail.get('pieces_diajukan', 0)
                },
                data_konversi=data_retur_request_detail['uom_list']
            )

            data_received_bad = calculate_konversi(
                value={
                    "karton": item.get('karton_diajukan', 0) ,
                    "box": item.get('box_diajukan', 0) ,
                    "pieces": item.get('pieces_diajukan', 0)
                },
                data_konversi=data_retur_request_detail['uom_list']
            )

            data_received_good = calculate_konversi(
                value={
                    "karton": item.get('karton_good_diajukan', 0),
                    "box": item.get('box_good_diajukan', 0),
                    "pieces": item.get('pieces_good_diajukan', 0)
                },
                data_konversi=data_retur_request_detail['uom_list']
            )

            if data_retur['pieces'] != (data_received_bad['pieces'] + data_received_good['pieces']):
                raise nonServerErrorException(
                    "Jumlah retur yang diterima tidak sesuai dengan jumlah yang diajukan",
                    400
                )

            id_produk = item.get('id_produk')
            karton_bad = item.get('karton_diajukan', 0)
            box_bad = item.get('box_diajukan', 0)
            pieces_bad = item.get('pieces_diajukan', 0)
            karton_good = item.get('karton_good_diajukan', 0)
            box_good = item.get('box_good_diajukan', 0)
            pieces_good = item.get('pieces_good_diajukan', 0)

            if not id_produk:
                raise nonServerErrorException("ID Produk dan jumlah retur harus diisi", 400)

            # update retur_request_detail
            retur_detail = (
                self.db.session.query(ReturRequestDetail)
                .filter_by(id_request=int(id_request), id_produk=id_produk)
                .with_for_update()
                .first()
            )
            if not retur_detail:
                raise nonServerErrorException("Detail retur tidak ditemukan", 404)

            subtotal_retur = (
                data_retur['pieces'] * retur_detail.harga_satuan
            )

            diskon_retur = 0
            if len(data_voucher_used) > 0:
                for voucher in data_voucher_used:
                    if voucher['persentase_diskon'] is not None:
                        diskon_retur += (
                            subtotal_retur *( voucher['persentase_diskon'] /100)
                        )

            dpp_retur = subtotal_retur - diskon_retur
            ppn_retur = dpp_retur * (data_retur_request_detail['ppn'] / 100)
            total_retur = dpp_retur + ppn_retur

            retur_detail.karton_diajukan = karton_bad
            retur_detail.box_diajukan = box_bad
            retur_detail.pieces_diajukan = pieces_bad
            retur_detail.karton_good_diajukan = karton_good
            retur_detail.box_good_diajukan = box_good
            retur_detail.pieces_good_diajukan = pieces_good
            retur_detail.subtotal_retur = subtotal_retur
            retur_detail.diskon_retur = diskon_retur
            retur_detail.dpp_retur = dpp_retur
            retur_detail.ppn_retur = ppn_retur
            retur_detail.total_retur = total_retur

            # Update totals for retur_request
            subtotal_retur_request_retur += subtotal_retur
            total_diskon_retur_request_retur += diskon_retur
            total_dpp_retur_request_retur += dpp_retur
            total_ppn_retur_request_retur += ppn_retur
            total_retur_request_retur += total_retur

            data_stock = (
                stok.query
                .filter_by(
                    cabang_id=data_plafon['id_cabang'],
                    produk_id=id_produk
                )
                .with_for_update()
                .first()
            )

            if not data_stock:
                raise nonServerErrorException("Stok tidak ditemukan untuk produk ID: {}".format(id_produk), 404)

            id_uom_level_1 = next((uom['id'] for uom in data_retur_request_detail['uom_list'] if uom['level'] == 1), None)

            log_inventory_stock_good = None
            log_inventory_stock_bad = None

            # INFO if ada received bad stock
            if data_received_bad['pieces'] > 0:
                log_inventory_stock_bad = LogInventory(
                    id_transaksi=id_request,
                    id_cabang=user['id_cabang'],
                    id_perusahaan=data_plafon['id_perusahaan'],
                    id_transaksi_tipe=3,
                    id_produk=item.get('id_produk'),
                    id_user=user['id'],
                    stok_awal=data_stock.jumlah_bad,
                    stok_peralihan=data_received_bad['pieces'],
                    stok_akhir=data_stock.jumlah_bad + data_received_bad['pieces'],
                    harga=retur_detail.harga_satuan,
                    tanggal=tanggal_date,
                    valuasi=0,
                    waktu=time_now(),
                    keterangan="Retur Pembelian",
                    produk_uom_id=id_uom_level_1,
                )

            # INFO if ada received good stock
            if data_received_good['pieces'] > 0:
                log_inventory_stock_good = LogInventory(
                    id_transaksi=id_request,
                    id_cabang=user['id_cabang'],
                    id_perusahaan=data_plafon['id_perusahaan'],
                    id_transaksi_tipe=3,
                    id_produk=item.get('id_produk'),
                    id_user=user['id'],
                    stok_awal=data_stock.jumlah_ready,  # pakai ready
                    stok_peralihan=data_received_good['pieces'],
                    stok_akhir=data_stock.jumlah_ready + data_received_good['pieces'],
                    harga=retur_detail.harga_satuan,
                    tanggal=tanggal_date,
                    valuasi=0,
                    waktu=time_now(),
                    keterangan="Retur Pembelian",
                    produk_uom_id=id_uom_level_1,
                )

            # ✅ Tambahkan ke session hanya jika tidak None
            if log_inventory_stock_good:
                self.add(log_inventory_stock_good)
            if log_inventory_stock_bad:
                self.add(log_inventory_stock_bad)

            # Update stok
            data_stock.jumlah_bad += data_received_bad['pieces']

            data_stock.jumlah_ready += data_received_good['pieces']
            data_stock.jumlah_good +=  data_received_good['pieces']
            data_stock.tanggal_update = tanggal_date
            data_stock.waktu_update = time_now()

            insert_credit_note_detail = CreditNoteDetail(
                id_cn=insert_credit_note.id_cn,
                id_retur_request_detail=retur_detail.id_request_detail,
                nominal_cn=total_retur,
                tanggal=tanggal,
            )

            self.add(data_stock)
            self.add(insert_credit_note_detail)
            self.add(retur_detail)
            self.flush()

        retur_request.subtotal_retur = subtotal_retur_request_retur
        retur_request.total_diskon_retur = total_diskon_retur_request_retur
        retur_request.total_dpp_retur = total_dpp_retur_request_retur
        retur_request.total_ppn_retur = total_ppn_retur_request_retur
        retur_request.total_retur = total_retur_request_retur
        retur_request.tanggal_retur = tanggal_date

        insert_credit_note.total_cn = total_retur_request_retur

        self.add(retur_request).flush()

        self.add(insert_credit_note).flush()

        self.commit()

        return {"message": "Retur stock berhasil diinsert", "id_request": id_request}
