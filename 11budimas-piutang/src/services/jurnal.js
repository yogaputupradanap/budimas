import { fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class Jurnal extends baseService {
    constructor() {
        super();

        this.columnDTN = [
            "jurnal.tanggal as tgl_transaksi",
            "jurnal_akun.kode as no_akun",
            "users.nama as nama_akun",
            "tipe_transaksi.nama as jenis_transaksi",
            "jurnal.debit",
            "jurnal.kredit",
            "perusahaan.nama as nama_perusahaan",
            "cabang.nama as nama_cabang"
        ];

        this.joinDTN = [
            "jurnal_akun",
            "cabang",
            "users",
            "tipe_transaksi",
            "perusahaan"
        ];

        this.onDTN = [
            "on jurnal.id_akun = jurnal_akun.id",
            "left join cabang on cabang.id = jurnal.id_cabang",
            "left join users on jurnal.id_user = users.id",
            "join tipe_transaksi on jurnal.id_tipe_transaksi = tipe_transaksi.nama",
            "join perusahaan on perusahaan.id = jurnal.id_perusahaan"
        ];

        this.baseUrl = `/api/akuntansi/get-jurnal`;
        this.detailJurnalUrl = `/api/akuntansi/detail-jurnal`;

        this.setServiceName("jurnal");
    }

    async getJurnal(params = {}) {
        try {
            const result = await fetchWithAuth("GET", `${this.baseUrl}?${new URLSearchParams(params)}`);
            console.log(result);
            return result;
        } catch (error) {
            this.throwError(error);
        }
    }

    async detailJurnal(id_jurnal) {
        try {
            const result = await fetchWithAuth(
                "GET",
                `${this.detailJurnalUrl}/${id_jurnal}`);
            return result;
        } catch (error) {
            this.throwError(error);
        }
    }


}

const jurnalService = new Jurnal();
export { jurnalService };
