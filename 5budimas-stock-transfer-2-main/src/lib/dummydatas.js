import { reduce } from "./compose"

const GENERATE_DATA_COUNT = 20

function generateDummmy(columnList) {
    let generateDummyList = []

    for(let i = 0; i < GENERATE_DATA_COUNT; i++) {
        let newObject = reduce(columnList)((acc, curr, idx) => {
            acc[curr] = `Test ${curr} ${idx}.${i}`
            return acc
        })

        generateDummyList.push(newObject)
    }

    return generateDummyList
}

const listStockColumn = ["id", "nama_produk", "sku", "satuan", "principal", "jumlah"]
const listProdukColumn = ["nama_produk", "uom1", "uom2", "uom3"]
const listCabangColumn = ["id", "cabang"]
const listPrincipal = ["id", "principal"]
const listProduk = ["id", "produk"]
const listPengajuantransfer = ['nota', 'tanggal', 'cabang_awal', 'cabang_tujuan', 'jumlah']
const detailPengajuanTransfer = ["nama_produk", "nama_principal", "uom1", "uom2", "uom3"]
const listPengirimanStockTransfer = ["nota_stock_transfer", "nama_produk", "nama_cabang_awal", "nama_cabang_tujuan", "jumlah_picked"]
const detailPengirimanStockTransfer = ["sku", "nama_produk", "nama_principal", "uom1", "uom2", "uom3"]
const listStatusPengiriman = ["nota", "nama_principal", "cabang_awal", "cabang_tujuan", "jumlah_produk", "status"]
const detailPenerimaanBarang = ["nama_produk", "satuan", 'jumlah_order', 'uom1', 'uom2', 'uom3']
const listEskalasi = ["nota", "tanggal", "tanggal_penerimaan", "cabang_awal", "cabang_tujuan", "status"]

export const listStockDummyDatas = generateDummmy(listStockColumn)
export const listProductDummy = generateDummmy(listProdukColumn)
export const listCabangDummy = generateDummmy(listCabangColumn)
export const listPrincipalDummy = generateDummmy(listPrincipal)
export const listProdukSelectDummy = generateDummmy(listProduk)
export const listPengajuantransferDummy = generateDummmy(listPengajuantransfer)
export const detailPengajuanTransferDummy = generateDummmy(detailPengajuanTransfer)
export const listPengirimanStockTransferDummy = generateDummmy(listPengirimanStockTransfer)
export const detailPengirimanStockTransferDummy = generateDummmy(detailPengirimanStockTransfer)
export const listStatusPengirimanDummy = generateDummmy(listStatusPengiriman)
export const detailPenerimaanBarangDummy = generateDummmy(detailPenerimaanBarang)
export const listEskalasiDummy = generateDummmy(listEskalasi)