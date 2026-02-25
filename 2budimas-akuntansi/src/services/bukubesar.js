import {fetchWithAuth} from "../lib/utils";
import {baseService} from "./baseService";

class BukuBesar extends baseService {
    constructor() {
        super();

        // Kolom default untuk Jurnal Umum
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

        this.joinDTN = ["jurnal_akun", "cabang", "users", "tipe_transaksi", "perusahaan"];

        this.onDTN = [
            "on jurnal.id_akun = jurnal_akun.id",
            "left join cabang on cabang.id = jurnal.id_cabang",
            "left join users on jurnal.id_user = users.id",
            "join tipe_transaksi on jurnal.id_tipe_transaksi = tipe_transaksi.nama",
            "join perusahaan on perusahaan.id = jurnal.id_perusahaan"
        ];

        this.basebukubesarUrl = `/api/akuntansi/get-bukubesar?`;

        this.setServiceName("jurnal");
    }

    async getbukubesar(params = {}) {
        try {
            // Kita gunakan basebukubesarUrl yang mengarah ke /api/akuntansi/get-bukubesar
            const response = await fetchWithAuth("GET", `${this.basebukubesarUrl}?${new URLSearchParams(params)}`);
            return response; 
        } catch (error) {
            this.throwError(error);
        }
    }
}

const bukuBesarService = new BukuBesar();
export {bukuBesarService};