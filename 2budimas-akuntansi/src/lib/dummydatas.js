import { reduce } from "./compose";

const GENERATE_DATA_COUNT = 6;

function generateDummmy(columnList) {
  let generateDummyList = [];

  for (let i = 0; i < GENERATE_DATA_COUNT; i++) {
    let newObject = reduce(columnList)((acc, curr, idx) => {
      acc[curr] = `Test ${curr} ${idx}.${i}`;
      return acc;
    });

    generateDummyList.push(newObject);
  }

  return generateDummyList;
}

export const listJurnalDummy = generateDummmy([
  "tanggal",
  "no_akun",
  "nama_akun",
  "keterangan",
  "debit",
  "kredit",
  "id",
]);
export const listSuratTagihanDummy = generateDummmy([
  "surat_tagihan",
  "customer",
  "total_tagihan",
  "jumlah_faktur",
  "tgl_jatuh_tempo",
  "status_kirim",
  "status_bayar",
  "id",
]);

export const suratTagihanPageTwoDummy = generateDummmy([
  "nomor_faktur",
  "total_order",
  "angsuran",
  "sisa_tagihan",
  "tgl_jatuh_tempo",
  "tanggal_order",
  "status_bayar",
]);

export const listSetoranTunaiDummy = generateDummmy([
  "customer",
  "tagihan",
  "setoran",
  "saldo",
  "jumlah_faktur",
  "id_setoran",
]);

export const listSetorTunaiDummy = generateDummmy([
  "id",
  "no_faktur",
  "jatuh_tempo",
  "sales",
  "tagihan",
  "setoran",
]);

export const listTagihanPurchasingDummy = generateDummmy([
  "surat_tagihan",
  "principal",
  "total_tagihan",
  "jumlah_faktur",
  "tanggal_bayar",
  "status_kirim",
  "status_bayar",
]);

export const principalDummy = generateDummmy(["nama", "principal", "id"]);

export const metodePembayaranDummy = generateDummmy(["metode", "id"]);

export const cabangDummy = generateDummmy(["perusahaan", "id"]);

export const periodeawalDummy = generateDummmy(["periode awal", "id"]);
export const periodeakhirDummy = generateDummmy(["periode akhir", "id"]);
export const salesDummy = generateDummmy(["sales", "id"]);
export const customerDummy = generateDummmy(["customer", "id"]);

export const tagihanPurchasingPageTwoDummy = generateDummmy([
  "nomor_faktur",
  "total_order",
  "angsuran",
  "sisa_tagihan",
  "tgl_jatuh_tempo",
  "status_bayar",
]);

export const jurnalDummy = [
  {
    tanggal_setoran: "2024-10-28",
    perusahaan: "PT Maju Sejahtera",
    cabang: "Jakarta",
    id_jurnal: 101,
    detail_jurnal: [
      {
        nama_akun: "Kas",
        jenis_transaksi: "Penerimaan",
        debit: 5000000,
        kredit: null,
      },
      {
        nama_akun: "Penjualan",
        jenis_transaksi: "Pendapatan",
        debit: null,
        kredit: 5000000,
      },
    ],
  },
  {
    tanggal_setoran: "2024-10-27",
    perusahaan: "PT Sukses Makmur",
    cabang: "Bandung",
    id_jurnal: 102,
    detail_jurnal: [
      {
        nama_akun: "Kas",
        jenis_transaksi: "Pengeluaran",
        debit: null,
        kredit: 2000000,
      },
      {
        nama_akun: "Biaya Operasional",
        jenis_transaksi: "Beban",
        debit: 2000000,
        kredit: null,
      },
    ],
  },
  {
    tanggal_setoran: "2024-10-26",
    perusahaan: "PT Abadi Jaya",
    cabang: "Surabaya",
    id_jurnal: 103,
    detail_jurnal: [
      {
        nama_akun: "Piutang Usaha",
        jenis_transaksi: "Penerimaan",
        debit: 3000000,
        kredit: null,
      },
      {
        nama_akun: "Penjualan Kredit",
        jenis_transaksi: "Pendapatan",
        debit: null,
        kredit: 3000000,
      },
    ],
  },
  {
    tanggal_setoran: "2024-10-26",
    perusahaan: "PT Abadi Jaya",
    cabang: "Surabaya",
    id_jurnal: 103,
    detail_jurnal: [
      {
        nama_akun: "Piutang Usaha",
        jenis_transaksi: "Penerimaan",
        debit: 3000000,
        kredit: null,
      },
      {
        nama_akun: "Penjualan Kredit",
        jenis_transaksi: "Pendapatan",
        debit: null,
        kredit: 3000000,
      },
    ],
  },
  {
    tanggal_setoran: "2024-10-26",
    perusahaan: "PT Abadi Jaya",
    cabang: "Surabaya",
    id_jurnal: 103,
    detail_jurnal: [
      {
        nama_akun: "Piutang Usaha",
        jenis_transaksi: "Penerimaan",
        debit: 3000000,
        kredit: null,
      },
      {
        nama_akun: "Penjualan Kredit",
        jenis_transaksi: "Pendapatan",
        debit: null,
        kredit: 3000000,
      },
    ],
  },
];
