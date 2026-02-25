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

export const jurnalDummy = generateDummmy([
  "nama",
  "id",
])

export const principalDummy = generateDummmy([
  "nama",
  "principal",
  "id",
])

export const metodePembayaranDummy = generateDummmy([
  "metode",
  "id",
])

export const cabangDummy = generateDummmy([
  "perusahaan",
  "id"
]);

export const periodeawalDummy = generateDummmy([
  "periode awal",
  "id"
]);
export const periodeakhirDummy = generateDummmy([
  "periode akhir",
  "id"
]);
export const salesDummy = generateDummmy([
  "sales",
  "id"
]);
export const customerDummy = generateDummmy([
  "customer",
  "id"
]);

export const tagihanPurchasingPageTwoDummy = generateDummmy([
  'nomor_faktur',
  'total_order',
  'angsuran',
  'sisa_tagihan',
  'tgl_jatuh_tempo',
  'status_bayar'
])
export const listPajakDummy = generateDummmy([
  'nomor_faktur',
  'nomor_faktur_pajak',
  'principal',
  'tanggal',
  'customer',
  'npwp',
  'nilai_faktur'
])
export const listNomorPajakDummy = generateDummmy([
  '',
  'nomor_faktur_pajak',
  'sudah_digunakan',
  'tanggal_digunakan',

])
export const listDetailPajakDummy = generateDummmy([
  'nama_barang',
  'sku',
  'satuan',
  'jumlah',
  'harga_satuan',
  'subtotal'
])
export const listnoPajakDummy = generateDummmy([
  'nomor_faktur_pajak',
])
export const prefixDummy = generateDummmy([
  'id',
  'prefix'
])
export const selectedDummy = generateDummmy([
  'id',
  'angkaselect'
])
