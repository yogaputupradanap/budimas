import { useUser } from "@/src/store/user";

/**
 * Prepare data structure for PDF report
 * @param {Object} row - Main stock opname data
 * @param {Array} productData - Stock opname detail data
 * @returns {Object} Structured data for PDF
 */
export const prepareReportData = (row, productData) => {
    const userStore = useUser();
    const userData = {
        nama: userStore.user.value.nama,
        nama_perusahaan: userStore.user.value.nama_perusahaan,
        nama_cabang: userStore.user.value.nama_cabang
    };

    return {
        user: userData,
        stockOpnameDetail: [{
            tanggal_so: row.tanggal_so,
            kode_so: row.kode_so,
            nama_principal: row.nama_principal,
            produks: productData.map(formatProductData)
        }]
    };
};

/**
 * Format product data for PDF display
 * @param {Object} prod - Raw product data
 * @returns {Object} Formatted product data
 */
export const formatProductData = (prod) => ({
    sku: prod.sku,
    nama_produk: prod.nama_produk,
    stock: prod.stok,
    uom3: prod.uom_3,
    uom2: prod.uom_2,
    uom1: prod.uom_1,
    selisih: prod.stok - prod.stok_sistem,
    stock_system: prod.stok_sistem,
    harga: prod.harga,
    subtotal: prod.subtotal,
    subtotal_selisih: prod.subtotal_selisih,
    keterangan: prod.ket_produk,
});