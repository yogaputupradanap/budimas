from apps.services import BaseServices
from apps.lib.paginate import Paginate
from flask import request, jsonify
from .BaseAkuntasi import BaseAkuntasi

class Jurnal(BaseAkuntasi):
    def __init__(self):
        super().__init__()
        self.jurnalBaseFromQ = """
            FROM jurnal
            JOIN kode_akun ON jurnal.kode_akun = kode_akun.id
            LEFT JOIN cabang ON cabang.id = jurnal.id_cabang
            LEFT JOIN users ON jurnal.id_user = users.id
            JOIN tipe_transaksi ON jurnal.id_tipe_transaksi = tipe_transaksi.id
            JOIN perusahaan ON perusahaan.id = jurnal.id_perusahaan
        """

    def getJurnal(self):
        conditions = {
            "id_cabang": "jurnal.id_cabang = :id_cabang",
            "id_perusahaan": "jurnal.id_perusahaan = :id_perusahaan",
            "periode_awal": "jurnal.tanggal >= :periode_awal",
            "periode_akhir": "jurnal.tanggal <= :periode_akhir",
        }

        where, bindParams,_ = self.poolRequest(conditions)

        query = f"""
            SELECT 
                Min(jurnal.id_jurnal) as id,
                jurnal.tanggal as tgl_transaksi,
                perusahaan.nama as nama_perusahaan,
                cabang.nama as nama_cabang,
                jurnal.id_jurnal,
                array_agg(
                    json_build_object(
                        'nama_akun', kode_akun.nama,
                        'jenis_transaksi', tipe_transaksi.nama,
                        'debit', COALESCE(jurnal.debit, NULL),
                        'kredit', COALESCE(jurnal.kredit, NULL)
                    )
                ) AS info_jurnal
            {self.jurnalBaseFromQ}
            where {where} jurnal.id_jurnal IS NOT NULL
            GROUP BY jurnal.tanggal, perusahaan.nama, cabang.nama, jurnal.id_jurnal
            ORDER BY jurnal.id_jurnal
        """

        result = Paginate(request, query, bindParams).paginate()
        return result

    def detailJurnal(self, id_jurnal):
        query = f"""
            SELECT 
                Min(jurnal.id_jurnal) as id,
                jurnal.tanggal as tgl_transaksi,
                perusahaan.nama as nama_perusahaan,
                cabang.nama as nama_cabang,
                jurnal.id_jurnal,
                jurnal.keterangan,
                users.nama as user,
                array_agg(
                    json_build_object(
                        'nama_akun', kode_akun.nama,
                        'jenis_transaksi', tipe_transaksi.nama,
                        'keterangan', jurnal.keterangan,
                        'debit', COALESCE(jurnal.debit, NULL),
                        'kredit', COALESCE(jurnal.kredit, NULL)
                    )
                ) AS info_jurnal
            {self.jurnalBaseFromQ}
            WHERE jurnal.id_jurnal ilike '%{id_jurnal}%'
            GROUP BY jurnal.tanggal, perusahaan.nama, cabang.nama, jurnal.id_jurnal, jurnal.keterangan, users.nama
            ORDER BY jurnal.id_jurnal
        """

        result = self.query().setRawQuery(query).execute().fetchall().get()

        return result