/**
 * Menghitung diskon untuk Voucher 1 Reguler (V1R)
 * @param {Object} voucher - Data voucher 1 reguler
 * @param {number} totalHarga - Total harga produk
 * @returns {Object} Hasil validasi dan perhitungan diskon
 */
export const calculateVoucher1RegularDiscount = (voucher, totalHarga) => {
  // Jika tidak ada voucher atau totalHarga, return error
  if (!voucher || !totalHarga) {
    return {
      isValid: false,
      value: 0,
      reason: "Voucher atau total harga tidak valid"
    };
  }

  // Hapus validasi minimal subtotal pembelian di sini
  // Validasi akan dilakukan di level aplikasi di salesRequest.js

  // Hitung diskon berdasarkan persentase
  if (voucher.persentase_diskon_1) {
    return {
      isValid: true,
      value: (voucher.persentase_diskon_1 / 100) * totalHarga,
      reason: null
    };
  }

  // Jika ada nilai diskon langsung
  if (voucher.nilai_diskon) {
    return {
      isValid: true,
      value: voucher.nilai_diskon,
      reason: null
    };
  }

  return {
    isValid: true,
    value: 0,
    reason: null
  };
};

/**
 * Menghitung diskon untuk Voucher 2 Reguler (V2R)
 * @param {Object} voucher - Data voucher 2 reguler
 * @param {number} totalHargaSetelahDiskon - Total harga setelah diskon V1R
 * @returns {Object} Hasil validasi dan perhitungan diskon
 */
export const calculateVoucher2RegularDiscount = (
  voucher,
  totalHargaSetelahDiskon
) => {
  // Jika tidak ada voucher atau totalHarga, return error
  if (!voucher || !totalHargaSetelahDiskon) {
    return {
      isValid: false,
      value: 0,
      reason: "Voucher atau total harga tidak valid"
    };
  }

  // Hapus validasi minimal subtotal pembelian di sini
  // Validasi akan dilakukan di level aplikasi di salesRequest.js

  // Hitung diskon berdasarkan persentase
  if (voucher.persentase_diskon_2) {
    return {
      isValid: true,
      value: (voucher.persentase_diskon_2 / 100) * totalHargaSetelahDiskon,
      reason: null
    };
  }

  // Jika ada nilai diskon langsung
  if (voucher.nilai_diskon) {
    return {
      isValid: true,
      value: voucher.nilai_diskon,
      reason: null
    };
  }

  return {
    isValid: true,
    value: 0,
    reason: null
  };
};

/**
 * Menghitung diskon untuk Voucher 3 Reguler (V3R)
 * @param {Object} voucher - Data voucher 3 reguler
 * @param {number} totalHargaSetelahDiskon - Total harga setelah diskon V1R dan V2R
 * @returns {Object} Hasil validasi dan perhitungan diskon
 */
export const calculateVoucher3RegularDiscount = (
  voucher,
  totalHargaSetelahDiskon
) => {
  // Jika tidak ada voucher atau totalHarga, return error
  if (!voucher || !totalHargaSetelahDiskon) {
    return {
      isValid: false,
      value: 0,
      reason: "Voucher atau total harga tidak valid"
    };
  }

  // Hapus validasi minimal subtotal pembelian di sini
  // Validasi akan dilakukan di level aplikasi di salesRequest.js

  // Hitung diskon berdasarkan persentase
  if (voucher.persentase_diskon_3) {
    return {
      isValid: true,
      value: (voucher.persentase_diskon_3 / 100) * totalHargaSetelahDiskon,
      reason: null
    };
  }

  // Jika ada nilai diskon langsung
  if (voucher.nilai_diskon) {
    return {
      isValid: true,
      value: voucher.nilai_diskon,
      reason: null
    };
  }

  return {
    isValid: true,
    value: 0,
    reason: null
  };
};

/**
 * Menghitung diskon untuk Voucher 2 Produk (V2P)
 * @param {Object} voucher - Data voucher 2 produk
 * @param {number} hargaProdukSetelahDiskonRegular - Harga produk setelah diskon reguler
 * @param {Object} product - Data produk
 * @returns {Object} Hasil validasi dan perhitungan diskon
 */
export const calculateVoucher2ProductDiscount = (
  voucher,
  hargaProdukSetelahDiskonRegular,
  product
) => {
  // Validasi awal
  if (!voucher || !hargaProdukSetelahDiskonRegular) {
    return {
      isValid: false,
      value: 0,
      reason: "Voucher atau harga produk tidak valid"
    };
  }

  // Cek apakah voucher berlaku untuk produk ini
  if (voucher.id_produk_asli && voucher.id_produk_asli !== product.id) {
    return {
      isValid: false,
      value: 0,
      reason: "Voucher ini hanya berlaku untuk produk tertentu"
    };
  }

  // Cek syarat minimal subtotal pembelian jika ada
  if (
    voucher.minimal_subtotal_pembelian &&
    hargaProdukSetelahDiskonRegular < voucher.minimal_subtotal_pembelian
  ) {
    return {
      isValid: false,
      value: 0,
      reason: `Total pembelian (${hargaProdukSetelahDiskonRegular}) kurang dari minimal subtotal (${voucher.minimal_subtotal_pembelian})`
    };
  }

  console.log(voucher);
  // Cek syarat minimal jumlah produk dengan konversi
  if (voucher.minimal_jumlah_produk && voucher.level_uom) {
    // Hitung total produk dalam UOM yang sesuai
    let totalJumlahUOM = 0;

    // Konversi semua ke pieces (UOM level 1) terlebih dahulu
    const totalPieces =
      (product.uom1 || 0) +
      (product.uom2 || 0) * (product.konversi_2 || 1) +
      (product.uom3 || 0) * (product.konversi_3 || 1);

    // Konversi ke UOM yang diminta oleh voucher
    switch (voucher.level_uom) {
      case 1: // pieces
        totalJumlahUOM = totalPieces;
        break;
      case 2: // box
        totalJumlahUOM = product.konversi_2
          ? totalPieces / product.konversi_2
          : 0;
        break;
      case 3: // karton
        totalJumlahUOM = product.konversi_3
          ? totalPieces / product.konversi_3
          : 0;
        break;
    }

    if (totalJumlahUOM < voucher.minimal_jumlah_produk) {
      return {
        isValid: false,
        value: 0,
        reason: `Jumlah produk (${totalJumlahUOM.toFixed(
          2
        )}) kurang dari minimal (${
          voucher.minimal_jumlah_produk
        }) untuk level UOM ${voucher.level_uom}`
      };
    }
  }

  // Hitung diskon
  let discount = 0;

  if (voucher.kategori_voucher === 1 && voucher.persentase_diskon_2) {
    // Kategori 1: diskon persentase
    discount =
      (voucher.persentase_diskon_2 / 100) * hargaProdukSetelahDiskonRegular;
  } else if (voucher.kategori_voucher === 2 && voucher.nominal_diskon) {
    // Kategori 2: diskon nominal per satuan
    const totalPieces =
      (product.uom1 || 0) +
      (product.uom2 || 0) * (product.konversi_2 || 1) +
      (product.uom3 || 0) * (product.konversi_3 || 1);

    discount = voucher.nominal_diskon;
  }

  // Batasi dengan budget diskon jika ada
  if (voucher.budget_diskon && discount > voucher.budget_diskon) {
    discount = voucher.budget_diskon;
  }

  return {
    isValid: true,
    value: discount,
    reason: null
  };
};

/**
 * Menghitung diskon untuk Voucher 3 Produk (V3P)
 * @param {Object} voucher - Data voucher 3 produk
 * @param {number} hargaProdukSetelahDiskonV2P - Harga produk setelah diskon V2P
 * @param {Object} product - Data produk
 * @returns {Object} Hasil validasi dan perhitungan diskon
 */
export const calculateVoucher3ProductDiscount = (
  voucher,
  hargaProdukSetelahDiskonV2P,
  product
) => {
  // Validasi awal
  if (!voucher || !hargaProdukSetelahDiskonV2P) {
    return {
      isValid: false,
      value: 0,
      reason: "Voucher atau harga produk tidak valid"
    };
  }

  // Cek apakah voucher berlaku untuk produk ini
  if (voucher.id_produk_asli && voucher.id_produk_asli !== product.id) {
    return {
      isValid: false,
      value: 0,
      reason: "Voucher ini hanya berlaku untuk produk tertentu"
    };
  }

  // Cek syarat minimal subtotal pembelian jika ada
  if (
    voucher.minimal_subtotal_pembelian &&
    hargaProdukSetelahDiskonV2P < voucher.minimal_subtotal_pembelian
  ) {
    return {
      isValid: false,
      value: 0,
      reason: `Total pembelian (${hargaProdukSetelahDiskonV2P}) kurang dari minimal subtotal (${voucher.minimal_subtotal_pembelian})`
    };
  }

  // Cek syarat minimal jumlah produk dengan konversi
  if (voucher.minimal_jumlah_produk && voucher.level_uom) {
    // Hitung total produk dalam UOM yang sesuai
    let totalJumlahUOM = 0;

    // Konversi semua ke pieces (UOM level 1) terlebih dahulu
    const totalPieces =
      (product.uom1 || 0) +
      (product.uom2 || 0) * (product.konversi_2 || 1) +
      (product.uom3 || 0) * (product.konversi_3 || 1);

    // Konversi ke UOM yang diminta oleh voucher
    switch (voucher.level_uom) {
      case 1: // pieces
        totalJumlahUOM = totalPieces;
        break;
      case 2: // box
        totalJumlahUOM = product.konversi_2
          ? totalPieces / product.konversi_2
          : 0;
        break;
      case 3: // karton
        totalJumlahUOM = product.konversi_3
          ? totalPieces / product.konversi_3
          : 0;
        break;
    }

    if (totalJumlahUOM < voucher.minimal_jumlah_produk) {
      return {
        isValid: false,
        value: 0,
        reason: `Jumlah produk (${totalJumlahUOM.toFixed(
          2
        )}) kurang dari minimal (${
          voucher.minimal_jumlah_produk
        }) untuk level UOM ${voucher.level_uom}`
      };
    }
  }

  let discount = 0;

  // Kategori 1: diskon persentase
  if (voucher.kategori_voucher === 1 && voucher.persentase_diskon_3) {
    discount =
      (voucher.persentase_diskon_3 / 100) * hargaProdukSetelahDiskonV2P;
  }
  // Kategori 2: diskon nominal per satuan
  else if (voucher.kategori_voucher === 2 && voucher.nominal_diskon) {
    // Hitung total pieces dari semua UOM
    let totalPieces =
      (product.uom1 || 0) +
      (product.uom2 || 0) * (product.konversi_2 || 1) +
      (product.uom3 || 0) * (product.konversi_3 || 1);

    discount = voucher.nominal_diskon;
  }

  // Periksa limit budget diskon jika ada
  if (voucher.budget_diskon && discount > voucher.budget_diskon) {
    discount = voucher.budget_diskon;
  }

  return {
    isValid: true,
    value: discount,
    reason: null
  };
};

/**
 * Menghitung total diskon dari semua voucher yang dipilih untuk satu produk
 * @param {Object} voucherSelections - Objek yang berisi voucher1Regular, voucher2Regular, voucher3Regular, voucher2Product, voucher3Product
 * @param {number} totalHarga - Total harga produk sebelum diskon
 * @param {Object} product - Data produk yang dipesan
 * @returns {Object} Objek berisi nilai diskon, hasil validasi voucher, dan pesan validasi
 */
export const calculateTotalDiscount = (
  voucherSelections,
  totalHarga,
  product
) => {
  // Object untuk menyimpan hasil perhitungan
  const result = {
    voucherResults: {},
    discountDetails: {
      diskon1Regular: 0,
      diskon2Regular: 0,
      diskon3Regular: 0,
      diskon2Product: 0,
      diskon3Product: 0
    },
    voucherValidations: {
      voucher1Regular: { isValid: true, reason: null },
      voucher2Regular: { isValid: true, reason: null },
      voucher3Regular: { isValid: true, reason: null },
      voucher2Product: { isValid: true, reason: null },
      voucher3Product: { isValid: true, reason: null }
    },
    totalDiskon: 0,
    hargaSetelahDiskon: totalHarga,
    hasInvalidVoucher: false
  };

  // Step 1: Hitung diskon Voucher 1 Regular
  if (voucherSelections.voucher1Regular) {
    const v1rResult = calculateVoucher1RegularDiscount(
      voucherSelections.voucher1Regular,
      totalHarga
    );
    result.voucherResults.voucher1Regular = v1rResult;
    result.voucherValidations.voucher1Regular = {
      isValid: v1rResult.isValid,
      reason: v1rResult.reason
    };

    if (v1rResult.isValid) {
      result.discountDetails.diskon1Regular = v1rResult.value;
    } else {
      result.hasInvalidVoucher = true;
    }
  }

  // Hitung harga setelah diskon V1R
  const hargaSetelahV1R = totalHarga - result.discountDetails.diskon1Regular;

  // Step 2: Hitung diskon Voucher 2 Regular
  if (voucherSelections.voucher2Regular) {
    const v2rResult = calculateVoucher2RegularDiscount(
      voucherSelections.voucher2Regular,
      hargaSetelahV1R
    );
    result.voucherResults.voucher2Regular = v2rResult;
    result.voucherValidations.voucher2Regular = {
      isValid: v2rResult.isValid,
      reason: v2rResult.reason
    };

    if (v2rResult.isValid) {
      result.discountDetails.diskon2Regular = v2rResult.value;
    } else {
      result.hasInvalidVoucher = true;
    }
  }

  // Hitung harga setelah diskon V2R
  const hargaSetelahV2R =
    hargaSetelahV1R - result.discountDetails.diskon2Regular;

  // Step 3: Hitung diskon Voucher 3 Regular
  if (voucherSelections.voucher3Regular) {
    const v3rResult = calculateVoucher3RegularDiscount(
      voucherSelections.voucher3Regular,
      hargaSetelahV2R
    );
    result.voucherResults.voucher3Regular = v3rResult;
    result.voucherValidations.voucher3Regular = {
      isValid: v3rResult.isValid,
      reason: v3rResult.reason
    };

    if (v3rResult.isValid) {
      result.discountDetails.diskon3Regular = v3rResult.value;
    } else {
      result.hasInvalidVoucher = true;
    }
  }

  // Hitung harga setelah diskon V3R
  const hargaSetelahV3R =
    hargaSetelahV2R - result.discountDetails.diskon3Regular;

  // Step 4: Hitung diskon Voucher 2 Product
  if (voucherSelections.voucher2Product) {
    const v2pResult = calculateVoucher2ProductDiscount(
      voucherSelections.voucher2Product,
      hargaSetelahV3R,
      product
    );
    result.voucherResults.voucher2Product = v2pResult;
    result.voucherValidations.voucher2Product = {
      isValid: v2pResult.isValid,
      reason: v2pResult.reason
    };

    if (v2pResult.isValid) {
      result.discountDetails.diskon2Product = v2pResult.value;
    } else {
      result.hasInvalidVoucher = true;
    }
  }

  // Hitung harga setelah diskon V2P
  const hargaSetelahV2P =
    hargaSetelahV3R - result.discountDetails.diskon2Product;

  // Step 5: Hitung diskon Voucher 3 Product
  if (voucherSelections.voucher3Product) {
    const v3pResult = calculateVoucher3ProductDiscount(
      voucherSelections.voucher3Product,
      hargaSetelahV2P,
      product
    );
    result.voucherResults.voucher3Product = v3pResult;
    result.voucherValidations.voucher3Product = {
      isValid: v3pResult.isValid,
      reason: v3pResult.reason
    };

    if (v3pResult.isValid) {
      result.discountDetails.diskon3Product = v3pResult.value;
    } else {
      result.hasInvalidVoucher = true;
    }
  }

  // Hitung total diskon dan harga akhir
  result.totalDiskon =
    result.discountDetails.diskon1Regular +
    result.discountDetails.diskon2Regular +
    result.discountDetails.diskon3Regular +
    result.discountDetails.diskon2Product +
    result.discountDetails.diskon3Product;

  result.hargaSetelahDiskon = totalHarga - result.totalDiskon;

  return result;
};
