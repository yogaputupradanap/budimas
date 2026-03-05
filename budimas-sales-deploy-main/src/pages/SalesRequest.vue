<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import FlexBox from "../components/ui/FlexBox.vue";
import Card from "../components/ui/Card.vue";
import Button from "../components/ui/Button.vue";
import { useCommonForm } from "@/src/lib/useCommonForm";
import { tambahProdukSchema } from "@/src/model/formSchema";
import SelectInput from "../components/ui/formInput/SelectInput.vue";
import TextField from "../components/ui/formInput/TextField.vue";
import { computed, inject, nextTick, onBeforeMount, onMounted, reactive, ref, watch } from "vue";
import Table from "../components/ui/table/Table.vue";
import Modal from "../components/ui/Modal.vue";
import { listFreeProductsColumns, listOrderColumns, sisaPlafonColumns } from "@/src/model/tableColumns";
import { apiUrl, checkNaN, fetchWithAuth, getCompactTimestamp, parseCurrency, sessionDisk } from "../lib/utils";
import { usePiutang } from "../store/piutang";
import { useKunjungan } from "../store/kunjungan";
import { useSales } from "../store/sales";
import { useSalesRequest } from "../store/salesRequest";
import { useVoucher } from "../store/voucher";
import { usePrincipal } from "../store/principal";
import { useAlert } from "../store/alert";
import { useDashboard } from "../store/dashboard";
import { useRouter } from "vue-router";

// Setup Router dan Stores
const router = useRouter();
const kunjungan = useKunjungan();
const principal = usePrincipal();
const sales = useSales();
const piutang = usePiutang();
const salesRequestStore = useSalesRequest();
const voucher = useVoucher();
const alert = useAlert();
const dashboard = useDashboard();

// Local State
const principalId = ref();
const salesRequest = ref([]);
const filteredSalesRequest = ref([]);
const selectedPrincipalId = ref(null);
const freeProducts = ref([]);
const tableRowIndex = ref(0);
const isEdit = ref(false);
const modal = ref();
const lewatiModal = ref();
const principalProducts = ref([]);
const selectedVoucherByPrincipal = ref({});
const submitLoading = ref(false);
const voucherLoading = ref(false);
const manualSearchTerm = ref("");
const voucherRegulerModal = ref();
const voucherRegulerLoading = ref(false);
const $swal = inject("$swal");
const stokReady = ref(0);
const loadingStokReady = ref(false);

// Tambahkan ref untuk melacak status voucher dan validasi voucher
const invalidVoucherNotifications = ref([]);

// Keys for rerender
const tableKey = ref(0);
const selectKey = ref(0);

// Form State
const { configProps, defineField, handleSubmit, resetForm } =
  useCommonForm(tambahProdukSchema);
const [namaProduk, namaProdukProps] = defineField("namaProduk", configProps);
const [pieces, piecesProps] = defineField("pieces", configProps);
const [box, boxProps] = defineField("box", configProps);
const [karton, kartonProps] = defineField("karton", configProps);
const [kodeVoucher] = defineField("kodeVoucher");

// Local Store
const headerFields = reactive({
  nota_order: ""
});
const tanggalJatuhTempo = ref(null);
const keteranganTidakOrder = ref("");
const availableVouchers = ref({
  voucher1Regular: [],
  voucher2Regular: [],
  voucher3Regular: [],
  voucher2Product: [],
  voucher3Product: []
});

const selectedVouchers = ref({
  voucher2Product: null,
  voucher3Product: null
});

const selectedVoucherReguler = ref({
  voucher1Regular: null,
  voucher2Regular: null,
  voucher3Regular: null
});

/**
 * Pencarian produk berdasarkan term
 */
const searchFiltered = computed(() => {
  if (!manualSearchTerm.value) return filteredSalesRequest.value;

  const term = manualSearchTerm.value.toLowerCase().trim();
  return filteredSalesRequest.value.filter((item) => {
    return (
      // Cari di nama produk
      (item.nama && item.nama.toLowerCase().includes(term)) ||
      // Cari di kode SKU
      (item.kode_sku && item.kode_sku.toLowerCase().includes(term)) ||
      // Cari di harga jual (convert to string first)
      (item.harga_jual && String(item.harga_jual).includes(term)) ||
      // Jika perlu, tambahkan pencarian di kolom lain
      // (item.otherField && item.otherField.toLowerCase().includes(term))
      false
    );
  });
});

/**
 * Menghasilkan nomor order otomatis
 */
const generateOrderNumber = () => {
  const customerCode =
    kunjungan.activeKunjungan.kunjungan.kode_customer ||
    kunjungan.activeKunjungan.kunjungan.customer_id;
  const timestamp = getCompactTimestamp();
  return `OR/${customerCode}/${timestamp}`;
};

/**
 * Membuka modal voucher reguler
 */
const openVoucherRegulerModal = async () => {
  await loadRegularVouchers();
  // Set nilai awal dari voucher reguler yang terpilih di store
  const currentRegularVouchers = voucher.getSelectedRegularVouchers();
  selectedVoucherReguler.value = {
    voucher1Regular: currentRegularVouchers.voucher1Regular?.id || null,
    voucher2Regular: currentRegularVouchers.voucher2Regular?.id || null,
    voucher3Regular: currentRegularVouchers.voucher3Regular?.id || null
  };

  voucherRegulerModal.value.show();
};

/**
 * Tutup modal voucher reguler
 */
const closeVoucherRegulerModal = () => {
  voucherRegulerModal.value.hide();
};

/**
 * Submit voucher reguler dan terapkan ke produk
 */
const submitVoucherReguler = async () => {
  voucherRegulerLoading.value = true;

  try {
    // 1. Ambil objek voucher dari ID yang dipilih
    const selectedVoucherObjects = {
      voucher1Regular: selectedVoucherReguler.value.voucher1Regular
        ? voucher.voucher1RegularList.find(
          (v) => v.id === selectedVoucherReguler.value.voucher1Regular
        )
        : null,
      voucher2Regular: selectedVoucherReguler.value.voucher2Regular
        ? voucher.voucher2RegularList.find(
          (v) => v.id === selectedVoucherReguler.value.voucher2Regular
        )
        : null,
      voucher3Regular: selectedVoucherReguler.value.voucher3Regular
        ? voucher.voucher3RegularList.find(
          (v) => v.id === selectedVoucherReguler.value.voucher3Regular
        )
        : null
    };

    // 2. Simpan voucher reguler yang dipilih ke store
    voucher.setSelectedRegularVouchers(selectedVoucherObjects);

    // 3. Update semua produk dalam salesRequest dengan menggunakan store
    // Terapkan voucher reguler dan dapatkan hasil validasi
    const validationResults =
      salesRequestStore.applyRegularVouchersToAllProducts(
        selectedVoucherObjects
      );

    // 4. Tampilkan notifikasi untuk voucher yang tidak valid
    if (validationResults.hasInvalidVouchers) {
      setTimeout(() => {
        invalidVoucherNotifications.value = validationResults.invalidProducts;

        // Tampilkan pesan voucher yang tidak memenuhi syarat
        let message = "Beberapa voucher tidak dapat diterapkan:\n";
        validationResults.invalidProducts.forEach((product) => {
          product.invalidVouchers.forEach((voucher) => {
            message += `- ${product.productName}: ${voucher.type} - ${voucher.reason}\n`;
          });
        });

        alert.setMessage(message, "warning", 8000);
      }, 500);
    } else {
      // 5. Tampilkan pesan sukses
      const msg =
        selectedVoucherObjects.voucher1Regular ||
        selectedVoucherObjects.voucher2Regular ||
        selectedVoucherObjects.voucher3Regular
          ? "Voucher reguler telah diterapkan ke semua produk"
          : "Semua voucher reguler telah dihapus";

      selectedVoucherByPrincipal.value = {
        ...selectedVoucherByPrincipal.value,
        [selectedPrincipalId.value]: {
          voucher1Regular: selectedVoucherObjects.voucher1Regular,
          voucher2Regular: selectedVoucherObjects.voucher2Regular,
          voucher3Regular: selectedVoucherObjects.voucher3Regular
        }
      };
      alert.setMessage(msg, "success");
    }

    // 6. Sync lokal salesRequest dengan data store
    updateSalesRequestFromStore();

    // 7. Force re-render tabel
    tableKey.value++;
    filterProductsByPrincipal();
  } catch (error) {
    console.error("Error applying regular vouchers:", error);
    alert.setMessage(`Terjadi kesalahan: ${error.message}`, "danger");
  } finally {
    voucherRegulerLoading.value = false;
    closeVoucherRegulerModal();
  }
};

/**
 * Menghitung harga dasar produk (sebelum diskon)
 */
const calculateBasePrice = (product) => {
  const piecesPrice = (product.uom1 || 0) * product.harga_jual;
  const boxPrice =
    (product.uom2 || 0) * product.harga_jual * (product.konversi_2 || 1);
  const kartonPrice =
    (product.uom3 || 0) * product.harga_jual * (product.konversi_3 || 1);

  return piecesPrice + boxPrice + kartonPrice;
};

/**
 * Reset form lewati modal
 */
const resetLewatiTextArea = () => (keteranganTidakOrder.value = "");

/**
 * Memuat voucher untuk produk yang dipilih
 */
const loadVouchersForProduct = async () => {
  if (!namaProduk.value) {
    availableVouchers.value = {
      voucher2Product: [],
      voucher3Product: []
    };
    selectedVouchers.value = {
      voucher2Product: null,
      voucher3Product: null
    };
    return;
  }

  voucherLoading.value = true;
  try {
    const result = await voucher.getAllVouchersForProduct(namaProduk.value);
    availableVouchers.value = {
      voucher2Product: result.voucher2Product || [],
      voucher3Product: result.voucher3Product || []
    };

    // Jika dalam mode edit, ambil voucher yang sudah dipilih sebelumnya
    if (isEdit.value && tableRowIndex.value >= 0) {
      const produk = salesRequest.value[tableRowIndex.value];
      if (produk && produk.voucherSelections) {
        selectedVouchers.value = {
          voucher2Product: produk.voucherSelections.voucher2Product?.id || null,
          voucher3Product: produk.voucherSelections.voucher3Product?.id || null
        };
      }
    } else {
      // Reset selectedVouchers jika ini bukan mode edit
      selectedVouchers.value = {
        voucher2Product: null,
        voucher3Product: null
      };
    }
  } catch (error) {
    console.error("Error loading vouchers:", error);
    alert.setMessage(`Error loading vouchers: ${error}`, "danger");
  } finally {
    voucherLoading.value = false;
  }
};

/**
 * Memuat voucher reguler
 */
const loadRegularVouchers = async () => {
  voucherRegulerLoading.value = true;
  try {
    if (!voucher.voucher1RegularList.length) {
      await voucher.getVoucher1Regular();
    }
    if (!voucher.voucher2RegularList.length) {
      await voucher.getVoucher2Regular();
    }
    if (!voucher.voucher3RegularList.length) {
      await voucher.getVoucher3Regular();
    }

    availableVouchers.value = {
      ...availableVouchers.value,
      voucher1Regular: voucher.voucher1RegularList,
      voucher2Regular: voucher.voucher2RegularList,
      voucher3Regular: voucher.voucher3RegularList
    };
  } catch (error) {
    console.error("Error loading regular vouchers:", error);
    alert.setMessage(`Error loading regular vouchers: ${error}`, "danger");
  } finally {
    voucherRegulerLoading.value = false;
  }
};

/**
 * Menerapkan voucher produk ke produk tertentu
 */
const applyProductVouchersToProduct = async (productId, productVouchers) => {
  if (!productId) return;

  try {
    // Dapatkan hasil penerapan voucher dari store
    const result = await salesRequestStore.applyProductVouchersToProduct(
      productId,
      productVouchers
    );

    if (result.success) {
      // Jika berhasil, periksa jika ada validasi yang perlu ditampilkan
      if (result.validationResults?.hasInvalidVoucher) {
        // Tampilkan pesan untuk voucher yang tidak valid
        let message = "Beberapa voucher tidak dapat diterapkan:\n";

        for (const [voucherType, validation] of Object.entries(
          result.validationResults.voucherValidations
        )) {
          if (!validation.isValid) {
            message += `- ${voucherType}: ${validation.reason}\n`;
          }
        }

        alert.setMessage(message, "warning", 5000);
      }

      // Sync data lokal dengan store
      updateSalesRequestFromStore();

      // Update tampilan tabel
      tableKey.value++;
    } else {
      alert.setMessage(result.error || "Gagal menerapkan voucher", "danger");
    }
  } catch (error) {
    console.error("Error applying product vouchers:", error);
    alert.setMessage(`Terjadi kesalahan: ${error}`, "danger");
  }
};

/**
 * Sinkronkan data salesRequest lokal dengan data dari store
 */
const updateSalesRequestFromStore = () => {
  // Ambil produk dari store dan sync dengan salesRequest lokal
  salesRequest.value = JSON.parse(
    JSON.stringify(salesRequestStore.initialProducts)
  );

  // Filter kembali produk berdasarkan principal yang dipilih
  filterProductsByPrincipal();
};

// Computed Properties
const subTotalBeforeDiscount = computed(() => {
  if (salesRequest.value) {
    return checkNaN(
      salesRequest.value.reduce(
        (total, produk) => total + (produk.totalHarga || 0),
        0
      )
    );
  }
  return 0;
});

const subTotal = computed(() => {
  if (salesRequest.value.length) {
    return checkNaN(
      salesRequest.value.reduce(
        (total, produk) => total + produk.jumlahHarga,
        0
      )
    );
  }
  return 0;
});

const totalDiskon = computed(() => {
  if (!salesRequest.value.length) return 0;

  return checkNaN(
    salesRequest.value.reduce((total, produk) => {
      return total + (produk.totalDiskon || 0);
    }, 0)
  );
});

const subtotalAfterDiscount = computed(() => {
  if (!salesRequest.value.length) return 0;
  return checkNaN(subTotal.value - totalDiskon.value);
});
const pajak = computed(() => {
  if (!salesRequest.value.length) return 0;

  return checkNaN(
    salesRequest.value.reduce((total, produk) => {
      const hasQuantity = produk.uom1 > 0 || produk.uom2 > 0 || produk.uom3 > 0;

      const ppnValue = hasQuantity ? produk.ppnValue || 0 : 0;
      return total + ppnValue;
    }, 0)
  );
});

const total = computed(() => {
  if (salesRequest.value.length) {
    const finalTotal = parseFloat(subTotal.value) + parseFloat(pajak.value);
    return checkNaN(finalTotal);
  }
  return 0;
});

/**
 * Mendapatkan UOM dari API
 */
const getUoms = async ({ id_produk, uom_1, uom_2, uom_3 }) => {
  try {
    const body = {
      products: [{ id_produk, uom_1, uom_2, uom_3 }]
    };

    const uoms = await fetchWithAuth(
      "POST",
      `${apiUrl}/api/produk-uom/get-uoms`,
      body
    );

    return uoms[0];
  } catch (error) {
    const message = `error while getting product uoms : ${error}`;
    alert.setMessage(message, "danger");
  }
};

/**
 * Menerapkan UOM ke nilai
 */
const spreadUoms = async (values) => {
  const { namaProduk, pieces: uom_3, box: uom_2, karton: uom_1 } = values;

  const {
    pieces,
    box,
    carton: karton
  } = await getUoms({
    id_produk: namaProduk,
    uom_1,
    uom_2,
    uom_3
  });

  return {
    ...values,
    pieces,
    box,
    karton
  };
};

/**
 * Filter produk berdasarkan principal
 */
const filterProductsByPrincipal = () => {
  if (!selectedPrincipalId.value || !salesRequest.value.length) {
    filteredSalesRequest.value = salesRequest.value;
    return;
  }

  filteredSalesRequest.value = salesRequest.value.filter(
    (product) => product.id_principal === selectedPrincipalId.value
  );

  tableKey.value++; // Memaksa tabel untuk dirender ulang
};

/**
 * Handle Reset and Add value selected voucher
 */
const handleChangePrincipalEffectOnVoucherReguler = () => {
  selectedVoucherReguler.value = {
    voucher1Regular: null,
    voucher2Regular: null,
    voucher3Regular: null
  };
  voucher.setSelectedRegularVouchers({
    voucher1Regular: selectedVoucherByPrincipal.value[selectedPrincipalId.value]?.voucher1Regular || null,
    voucher2Regular: selectedVoucherByPrincipal.value[selectedPrincipalId.value]?.voucher2Regular || null,
    voucher3Regular: selectedVoucherByPrincipal.value[selectedPrincipalId.value]?.voucher3Regular || null
  });
};

/**
 * Restructure free products
 */
const restructureFreeProduct = () => {
  const newFreeProduct = salesRequest.value
    .map((produk) => {
      const freeProducts = [];

      // Periksa apakah voucherSelections ada sebelum mengakses propertinya
      if (produk.voucherSelections) {
        // Periksa voucher1
        if (
          produk.voucherSelections.voucher1 &&
          produk.voucherSelections.voucher1.free_produk
        ) {
          freeProducts.push(
            ...produk.voucherSelections.voucher1.free_produk.map((free) => ({
              kode_voucher: produk.voucherSelections.voucher1.kode_voucher,
              ...free
            }))
          );
        }

        // Periksa voucher2
        if (
          produk.voucherSelections.voucher2 &&
          produk.voucherSelections.voucher2.free_produk
        ) {
          freeProducts.push(
            ...produk.voucherSelections.voucher2.free_produk.map((free) => ({
              kode_voucher: produk.voucherSelections.voucher2.kode_voucher,
              ...free
            }))
          );
        }

        // Periksa voucher3
        if (
          produk.voucherSelections.voucher3 &&
          produk.voucherSelections.voucher3.free_produk
        ) {
          freeProducts.push(
            ...produk.voucherSelections.voucher3.free_produk.map((free) => ({
              kode_voucher: produk.voucherSelections.voucher3.kode_voucher,
              ...free
            }))
          );
        }
      }

      return freeProducts;
    })
    .filter((products) => products.length !== 0)
    .flat()
    .map((produk, idx) => ({
      no: idx + 1,
      ...produk
    }));

  freeProducts.value = newFreeProduct;
};

/**
 * Handler untuk tambah produk
 */
const tambahProduk = handleSubmit(async (val) => {
  const values = await spreadUoms(val);

  if (salesRequest.value.some((produk) => produk.id === values.namaProduk)) {
    const produk = salesRequest.value.find(
      (produk) => produk.id === values.namaProduk
    );

    tableRowIndex.value = salesRequest.value.findIndex(
      (produk) => produk.id === values.namaProduk
    );

    const valuesAfter = {
      ...values,
      box: produk.uom2 + values.box,
      karton: produk.uom3 + values.karton,
      pieces: produk.uom1 + values.pieces
    };

    editprodukBeforeForm(valuesAfter);
  } else {
    const tableData = prepareProductData(values);

    if (tableData) {
      salesRequest.value.push(tableData);

      // Sync data dengan store
      const storeProductIndex = salesRequestStore.initialProducts.findIndex(
        (p) => p.id === tableData.id
      );

      if (storeProductIndex !== -1) {
        // Update produk di store
        salesRequestStore.initialProducts[storeProductIndex] = JSON.parse(
          JSON.stringify(tableData)
        );
      }
    }
  }

  tableKey.value++;
  closeModal();
  filterProductsByPrincipal();
});

/**
 * Edit produk sebelum form
 */
const editprodukBeforeForm = (values) => {
  const tableData = prepareProductData(values);
  if (tableData) {
    salesRequest.value[tableRowIndex.value] = tableData;

    // Sync dengan store
    const storeProductIndex = salesRequestStore.initialProducts.findIndex(
      (p) => p.id === tableData.id
    );

    if (storeProductIndex !== -1) {
      // Update produk di store
      salesRequestStore.initialProducts[storeProductIndex] = JSON.parse(
        JSON.stringify(tableData)
      );
    }
  }

  tableKey.value++;
  closeModal();
  filterProductsByPrincipal();
};

/**
 * Handler untuk edit produk
 */
const editProduk = handleSubmit(async (values) => {
  // Validasi stok saat submit
  if (isEdit.value && !validateStok()) {
    const produk = salesRequestStore.initialProducts.find(
      (p) => p.id === namaProduk.value
    );
    const totalInput =
      (pieces.value || 0) * 1 +
      (box.value || 0) * (produk.konversi_2 || 1) +
      (karton.value || 0) * (produk.konversi_3 || 1);

    alert.setMessage(
      `Input ${totalInput} pieces melebihi stok ready ${stokReady.value} pieces`,
      "danger"
    );
    return;
  }

  const newValues = await spreadUoms(values);
  editprodukBeforeForm(newValues);
});
/**
 * Hapus produk
 */
const removeProduct = (val) => {
  const productId = val.value.namaProduk;
  const realIndex = salesRequest.value.findIndex(
    (produk) => produk.id === productId
  );

  if (realIndex !== -1) {
    salesRequest.value.splice(realIndex, 1);

    // Reset produk di store ke nilai default
    const storeProductIndex = salesRequestStore.initialProducts.findIndex(
      (p) => p.id === productId
    );

    if (storeProductIndex !== -1) {
      salesRequestStore.initialProducts[storeProductIndex] = {
        ...salesRequestStore.initialProducts[storeProductIndex],
        uom1: 0,
        uom2: 0,
        uom3: 0,
        totalHarga: 0,
        jumlahHarga: 0,
        totalDiskon: 0,
        ppnValue: 0,
        voucherSelections: {
          voucher1Regular: null,
          voucher2Regular: null,
          voucher3Regular: null,
          voucher2Product: null,
          voucher3Product: null
        },
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
        }
      };
    }

    restructureFreeProduct();
    tableKey.value++;
    filterProductsByPrincipal();
  }
};

/**
 * Buka modal tambah
 */
const openTambahModal = () => {
  isEdit.value = false;
  resetForm();
  principalId.value = null;
  // Set default values to 0
  pieces.value = 0;
  box.value = 0;
  karton.value = 0;
  nextTick(() => {
    modal.value.show();
  });
};

/**
 * Reset voucher dan buka modal tambah
 */
const resettingVoucher = async () => {
  openTambahModal();
};

/**
 * Buka modal edit
 */
const openEditModal = async (val) => {
  isEdit.value = true;
  principalId.value = val.value.principalId;
  const productId = val.value.namaProduk;
  tableRowIndex.value = salesRequest.value.findIndex(
    (produk) => produk.id === productId
  );

  namaProduk.value = val.value.namaProduk;
  pieces.value = val.value.pieces;
  box.value = val.value.box;
  karton.value = val.value.karton;

  // Ambil stok ready
  await getStokReady(productId, sales.salesUser.id_cabang);

  await loadVouchersForProduct();

  // Set selected vouchers dari produk yang diedit
  const produk = salesRequest.value[tableRowIndex.value];
  if (produk && produk.voucherSelections) {
    selectedVouchers.value = {
      voucher2Product: produk.voucherSelections.voucher2Product?.id || null,
      voucher3Product: produk.voucherSelections.voucher3Product?.id || null
    };
  } else {
    // Reset jika tidak ada voucher
    selectedVouchers.value = {
      voucher2Product: null,
      voucher3Product: null
    };
  }

  nextTick(() => {
    modal.value.show();
  });
};

/**
 * Reset form modal
 */
const resetFormModal = () => {
  resetForm();
  availableVouchers.value = {
    voucher2Product: [],
    voucher3Product: []
  };
  selectedVouchers.value = {
    voucher2Product: null,
    voucher3Product: null
  };
  // Reset stok ready
  stokReady.value = 0;
  loadingStokReady.value = false;
};

/**
 * Tutup modal
 */
const closeModal = () => {
  resetFormModal();
  modal.value.hide();
};

/**
 * Prepare product data dengan voucher selections
 */
const prepareProductData = (values) => {
  // Find product info
  const produk = salesRequestStore.initialProducts.find(
    (product) => product.id === values.namaProduk
  );

  if (!produk) return null;

  // Get selected vouchers from the local state and store
  const regularVouchers = voucher.getSelectedRegularVouchers();

  // Buat objek voucher selections dengan deep clone
  const voucherSelections = {
    // Ambil voucher reguler dari store
    voucher1Regular: regularVouchers.voucher1Regular
      ? JSON.parse(JSON.stringify(regularVouchers.voucher1Regular))
      : null,
    voucher2Regular: regularVouchers.voucher2Regular
      ? JSON.parse(JSON.stringify(regularVouchers.voucher2Regular))
      : null,
    voucher3Regular: regularVouchers.voucher3Regular
      ? JSON.parse(JSON.stringify(regularVouchers.voucher3Regular))
      : null,

    // Ambil voucher produk dari seleksi lokal
    voucher2Product: selectedVouchers.value.voucher2Product
      ? availableVouchers.value.voucher2Product.find(
        (v) => v.id === selectedVouchers.value.voucher2Product
      )
      : null,
    voucher3Product: selectedVouchers.value.voucher3Product
      ? availableVouchers.value.voucher3Product.find(
        (v) => v.id === selectedVouchers.value.voucher3Product
      )
      : null
  };

  // Buat produk dengan nilai UOM
  const productWithUoms = {
    ...produk,
    uom1: values.pieces,
    uom2: values.box,
    uom3: values.karton,
    voucherSelections: JSON.parse(JSON.stringify(voucherSelections))
  };

  // Sync dengan store - menggunakan recalculateProductDiscount di store
  const storeProductIndex = salesRequestStore.initialProducts.findIndex(
    (p) => p.id === values.namaProduk
  );

  if (storeProductIndex !== -1) {
    // Update nilai UOM dan voucher di store
    salesRequestStore.initialProducts[storeProductIndex] = {
      ...salesRequestStore.initialProducts[storeProductIndex],
      uom1: values.pieces,
      uom2: values.box,
      uom3: values.karton,
      voucherSelections: JSON.parse(JSON.stringify(voucherSelections))
    };

    // TAMBAHKAN KODE INI - Hitung subtotal setelah perubahan kuantitas
    const newSubtotal = salesRequestStore.getCurrentSubtotal();

    // Validasi voucher reguler berdasarkan subtotal baru
    let voucherUpdated = false;

    // Validasi voucher 1 reguler
    if (
      regularVouchers.voucher1Regular &&
      regularVouchers.voucher1Regular.minimal_subtotal_pembelian &&
      newSubtotal < regularVouchers.voucher1Regular.minimal_subtotal_pembelian
    ) {
      // Reset voucher yang tidak valid untuk semua produk
      salesRequestStore.initialProducts.forEach((prod) => {
        if (prod.voucherSelections && prod.voucherSelections.voucher1Regular) {
          prod.voucherSelections.voucher1Regular = null;
        }
      });

      // Update produk saat ini juga
      salesRequestStore.initialProducts[
        storeProductIndex
        ].voucherSelections.voucher1Regular = null;

      voucherUpdated = true;
      alert.setMessage(
        `Voucher 1 Reguler dihapus karena subtotal (${newSubtotal}) kurang dari minimal (${regularVouchers.voucher1Regular.minimal_subtotal_pembelian})`,
        "warning",
        3000
      );
    }

    // Validasi voucher 2 reguler - logika yang sama
    if (
      regularVouchers.voucher2Regular &&
      regularVouchers.voucher2Regular.minimal_subtotal_pembelian &&
      newSubtotal < regularVouchers.voucher2Regular.minimal_subtotal_pembelian
    ) {
      salesRequestStore.initialProducts.forEach((prod) => {
        if (prod.voucherSelections && prod.voucherSelections.voucher2Regular) {
          prod.voucherSelections.voucher2Regular = null;
        }
      });

      salesRequestStore.initialProducts[
        storeProductIndex
        ].voucherSelections.voucher2Regular = null;
      voucherUpdated = true;
    }

    // Validasi voucher 3 reguler - logika yang sama
    if (
      regularVouchers.voucher3Regular &&
      regularVouchers.voucher3Regular.minimal_subtotal_pembelian &&
      newSubtotal < regularVouchers.voucher3Regular.minimal_subtotal_pembelian
    ) {
      salesRequestStore.initialProducts.forEach((prod) => {
        if (prod.voucherSelections && prod.voucherSelections.voucher3Regular) {
          prod.voucherSelections.voucher3Regular = null;
        }
      });

      salesRequestStore.initialProducts[
        storeProductIndex
        ].voucherSelections.voucher3Regular = null;
      voucherUpdated = true;
    }

    // Jika ada perubahan voucher, perbarui store
    if (voucherUpdated) {
      // Update selectedRegularVouchers di store untuk menyinkronkan UI
      const updatedRegularVouchers = {
        voucher1Regular:
          regularVouchers.voucher1Regular &&
          newSubtotal >=
          (regularVouchers.voucher1Regular.minimal_subtotal_pembelian || 0)
            ? regularVouchers.voucher1Regular
            : null,
        voucher2Regular:
          regularVouchers.voucher2Regular &&
          newSubtotal >=
          (regularVouchers.voucher2Regular.minimal_subtotal_pembelian || 0)
            ? regularVouchers.voucher2Regular
            : null,
        voucher3Regular:
          regularVouchers.voucher3Regular &&
          newSubtotal >=
          (regularVouchers.voucher3Regular.minimal_subtotal_pembelian || 0)
            ? regularVouchers.voucher3Regular
            : null
      };

      voucher.setSelectedRegularVouchers(updatedRegularVouchers);
    }

    // Recalculate discount di store
    const calculationResult = salesRequestStore.recalculateProductDiscount(
      salesRequestStore.initialProducts[storeProductIndex]
    );

    // Periksa validasi voucher
    if (calculationResult.hasInvalidVoucher) {
      // Reset voucher yang tidak valid di store
      for (const [voucherType, validation] of Object.entries(
        calculationResult.voucherValidations
      )) {
        if (!validation.isValid) {
          salesRequestStore.initialProducts[
            storeProductIndex
            ].voucherSelections[voucherType] = null;

          // Tampilkan pesan voucher tidak valid
          alert.setMessage(
            `${voucherType} tidak memenuhi syarat: ${validation.reason}`,
            "warning",
            5000
          );
        }
      }

      // Hitung ulang setelah reset voucher
      salesRequestStore.recalculateProductDiscount(
        salesRequestStore.initialProducts[storeProductIndex]
      );
    }

    // Ambil data terbaru dari store
    return JSON.parse(
      JSON.stringify(salesRequestStore.initialProducts[storeProductIndex])
    );
  }

  return productWithUoms;
};

/**
 * Mendapatkan semua resources sales request
 */
const getResources = async () => {
  if (!principal.principalProduct.products.length) {
    await principal.getPrincipalProducts();
  }

  if (!piutang.listPiutang.length) {
    await piutang.getPiutang(
      kunjungan.activeKunjungan.kunjungan.user_id,
      kunjungan.activeKunjungan.kunjungan.customer_id
    );
  }

  if (!salesRequestStore.initialProducts.length) {
    await salesRequestStore.getSalesRequest();
  }

  // Generate nomor nota order otomatis
  headerFields.nota_order = generateOrderNumber();

  // Sync dengan store
  salesRequest.value = JSON.parse(
    JSON.stringify(salesRequestStore.initialProducts)
  );

  if (!selectedPrincipalId.value && principal.principals.length > 0) {
    selectedPrincipalId.value = principal.principals[0].id;
  }

  filterProductsByPrincipal();
  tableKey.value++;
};

/**
 * Mendapatkan produk principal
 */
function getprincipalProducts() {
  if (!isEdit.value) namaProduk.value = 0;
  principalProducts.value = salesRequestStore.initialProducts.filter(
    (product) => product.id_principal === principalId.value
  );
  selectedVoucherReguler.value = {
    voucher1Regular: null,
    voucher2Regular: null,
    voucher3Regular: null
  };
}

/**
 * Skip sales order
 */
const skipSalesOrder = async () => {
  try {
    const body = {
      id_plafon: principal.idPlafons,
      keterangan: keteranganTidakOrder.value
    };
    await fetchWithAuth("POST", `${apiUrl}/api/sales/sales-skip-request`, body);
    alert.setMessage("Berhasil melewati sales order", "success");

    dashboard.setActiveButton("sales request", { value: false });
    router.back();
  } catch (error) {
    alert.setMessage(`Error: ${error}`);
  } finally {
    lewatiModal.value.hide();
  }
};

const round2 = (val) => Number(parseFloat(val || 0).toFixed(2));

/**
 * Submit order
 */
const submitOrder = async () => {
  if (
    Object.keys(headerFields)
      .map((key) => headerFields[key])
      .some((value) => value === "")
  ) {
    const fieldKosong = Object.keys(headerFields)
      .map((key) => {
        if (!headerFields[key]) return key.split("_").join(" ");
        else return null;
      })
      .filter((value) => value !== null);

    alert.setMessage(`Field : ${fieldKosong.join(", ")} Kosong`, "danger");
  } else if (!salesRequest.value.length) {
    alert.setMessage(`List Order Kosong`, "danger");
  } else {
    const currentPrincipalProducts = salesRequest.value;

    const hasProducts = currentPrincipalProducts.some(
      (product) => product.uom1 > 0 || product.uom2 > 0 || product.uom3 > 0
    );

    if (!hasProducts) {
      return alert.setMessage(
        "Tidak ada produk yang diinput dengan jumlah lebih dari 0",
        "danger"
      );
    }

    const removeEmptyUom = currentPrincipalProducts.filter((product) => {
      const entriesProduct = [product.uom1, product.uom2, product.uom3];
      return !entriesProduct.every((val) => val == 0);
    });

    // if (
    //    !removeEmptyUom.every(
    //     (produk) => produk.id_principal === removeEmptyUom[0].id_principal
    //   )
    // ) {
    //   return alert.setMessage(
    //     "Anda memilih lebih dari satu principal, cukup pilih satu principal per faktur",
    //     "danger"
    //   );
    // }

    // Format data produk untuk pengiriman dengan format yang lebih efisien
    const sendProduct = removeEmptyUom.map((produk) => {
      const totalPieces =
        (produk.uom1 || 0) * 1 + // pieces
        (produk.uom2 || 0) * (produk.konversi_2 || 1) + // box to pieces
        (produk.uom3 || 0) * (produk.konversi_3 || 1); // karton to pieces
      // Persiapkan data voucher yang dipilih
      const selectedVoucherDetails = [];

      // Format voucher reguler 1
      if (produk.voucherSelections.voucher1Regular) {
        selectedVoucherDetails.push({
          id: produk.voucherSelections.voucher1Regular.id,
          kode: produk.voucherSelections.voucher1Regular.kode_voucher,
          nilai_diskon:
            produk.voucherSelections.voucher1Regular.nilai_diskon || 0,
          persentase_diskon:
            produk.voucherSelections.voucher1Regular.persentase_diskon_1 || 0,
          tipe: "reguler",
          level: 1
        });
      }

      // Format voucher reguler 2
      if (produk.voucherSelections.voucher2Regular) {
        selectedVoucherDetails.push({
          id: produk.voucherSelections.voucher2Regular.id,
          kode: produk.voucherSelections.voucher2Regular.kode_voucher,
          nilai_diskon:
            produk.voucherSelections.voucher2Regular.nilai_diskon || 0,
          persentase_diskon:
            produk.voucherSelections.voucher2Regular.persentase_diskon_2 || 0,
          tipe: "reguler",
          level: 2
        });
      }

      // Format voucher reguler 3
      if (produk.voucherSelections.voucher3Regular) {
        selectedVoucherDetails.push({
          id: produk.voucherSelections.voucher3Regular.id,
          kode: produk.voucherSelections.voucher3Regular.kode_voucher,
          nilai_diskon:
            produk.voucherSelections.voucher3Regular.nilai_diskon || 0,
          persentase_diskon:
            produk.voucherSelections.voucher3Regular.persentase_diskon_3 || 0,
          tipe: "reguler",
          level: 3
        });
      }

      // Format voucher produk 2
      if (produk.voucherSelections.voucher2Product) {
        selectedVoucherDetails.push({
          id: produk.voucherSelections.voucher2Product.id,
          kode: produk.voucherSelections.voucher2Product.kode_voucher,
          nilai_diskon:
            produk.voucherSelections.voucher2Product.nominal_diskon || 0,
          persentase_diskon:
            produk.voucherSelections.voucher2Product.persentase_diskon_2 || 0,
          tipe: "produk",
          level: 2
        });
      }

      // Format voucher produk 3
      if (produk.voucherSelections.voucher3Product) {
        selectedVoucherDetails.push({
          id: produk.voucherSelections.voucher3Product.id,
          kode: produk.voucherSelections.voucher3Product.kode_voucher,
          nilai_diskon:
            produk.voucherSelections.voucher3Product.nominal_diskon || 0,
          persentase_diskon:
            produk.voucherSelections.voucher3Product.persentase_diskon_3 || 0,
          tipe: "produk",
          level: 3
        });
      }

      // Buat format data voucherSelections yang efisien
      const optimizedVoucherSelections = {};

      // Hanya tambahkan properti jika voucher ada
      if (produk.voucherSelections.voucher1Regular) {
        optimizedVoucherSelections.voucher1Regular = {
          id: produk.voucherSelections.voucher1Regular.id,
          kode_voucher: produk.voucherSelections.voucher1Regular.kode_voucher
        };
      }

      if (produk.voucherSelections.voucher2Regular) {
        optimizedVoucherSelections.voucher2Regular = {
          id: produk.voucherSelections.voucher2Regular.id,
          kode_voucher: produk.voucherSelections.voucher2Regular.kode_voucher
        };
      }

      if (produk.voucherSelections.voucher3Regular) {
        optimizedVoucherSelections.voucher3Regular = {
          id: produk.voucherSelections.voucher3Regular.id,
          kode_voucher: produk.voucherSelections.voucher3Regular.kode_voucher
        };
      }

      if (produk.voucherSelections.voucher2Product) {
        optimizedVoucherSelections.voucher2Product = {
          id: produk.voucherSelections.voucher2Product.id,
          kode_voucher: produk.voucherSelections.voucher2Product.kode_voucher
        };
      }

      if (produk.voucherSelections.voucher3Product) {
        optimizedVoucherSelections.voucher3Product = {
          id: produk.voucherSelections.voucher3Product.id,
          kode_voucher: produk.voucherSelections.voucher3Product.kode_voucher
        };
      }

      // Return object dengan ukuran yang dioptimalkan
      return {
        id_produk: produk.id,
        id_principal: produk.id_principal,
        harga_jual: produk.harga_jual,
        pieces_order: produk.uom1,
        box_order: produk.uom2,
        karton_order: produk.uom3,
        subtotalorder: produk.jumlahHarga,
        totalDiskon: produk.totalDiskon || 0,
        ppn_value: produk.ppnValue || 0,
        ppn_rate: produk.ppnRate || 0,
        totalHarga: produk.totalHarga || 0,
        vouchers: selectedVoucherDetails,
        voucherSelections: optimizedVoucherSelections,
        discountDetails: produk.discountDetails,
        total_pieces: totalPieces
      };
    });

    // Buat request yang dioptimalkan
    const request = {
      id_plafon: principal.idPlafons,
      id_cabang: sales.salesUser.id_cabang,
      no_sales_order: headerFields.nota_order,
      nama_sales: sales.salesUser.nama,
      subtotal_penjualan: round2(subTotal.value),
      subtotal_diskon: round2(totalDiskon.value),
      pajak: round2(pajak.value),
      total_penjualan: round2(total.value),
      products: sendProduct.map(
        ({
           id_produk,
           id_principal,
           harga_jual,
           pieces_order,
           box_order,
           karton_order,
           subtotalorder,
           totalDiskon,
           ppn_value,
           ppn_rate,
           totalHarga,
           vouchers,
           voucherSelections,
           discountDetails,
           total_pieces
         }) => ({
          id_produk,
          id_principal,
          harga_jual: round2(harga_jual),
          pieces_order,
          box_order,
          karton_order,
          subtotalorder: round2(subtotalorder),
          totalDiskon: round2(totalDiskon),
          ppn_value: round2(ppn_value),
          ppn_rate: round2(ppn_rate),
          totalHarga: round2(totalHarga),
          vouchers,
          voucherSelections,
          discountDetails,
          total_pieces
        })
      )
    };

    submitLoading.value = true;
    try {
      const isConfirm = await $swal.confirmSubmit();
      if (!isConfirm) {
        submitLoading.value = false;
        return;
      }

      await fetchWithAuth("POST", `${apiUrl}/api/sales/sales-request`, request);
      await piutang.getPiutang(
        kunjungan.activeKunjungan.kunjungan.user_id,
        kunjungan.activeKunjungan.kunjungan.customer_id
      );

      alert.setMessage(
        `Berhasil request produk dengan no order: ${headerFields.nota_order}`,
        "success"
      );

      await dashboard.getDashboardInfo(
        sessionDisk.getSession("authUser").id_user
      );
      resetAllStores();
      router.back();
    } catch (error) {
      console.log(error);
      alert.setMessage(error, "danger");
      submitLoading.value = false;
    }
  }
};

/**
 * Mengambil stok ready produk
 */
const getStokReady = async (idProduk, idCabang) => {
  if (!idProduk || !idCabang) {
    stokReady.value = 0;
    return;
  }

  loadingStokReady.value = true;
  try {
    const response = await fetchWithAuth(
      "GET",
      `${apiUrl}/api/produk/stok-ready?id_produk=${idProduk}&id_cabang=${idCabang}`
    );

    stokReady.value = response[0]?.jumlah_ready || 0;
  } catch (error) {
    console.error("Error fetching stok ready:", error);
    stokReady.value = 0;
    alert.setMessage(`Error loading stok ready: ${error}`, "warning");
  } finally {
    loadingStokReady.value = false;
  }
};

/**
 * Validasi stok ready
 */
const validateStok = () => {
  if (!isEdit.value || !namaProduk.value) return true;

  const produk = salesRequestStore.initialProducts.find(
    (p) => p.id === namaProduk.value
  );
  if (!produk) return true;

  const totalPieces =
    (pieces.value || 0) * 1 +
    (box.value || 0) * (produk.konversi_2 || 1) +
    (karton.value || 0) * (produk.konversi_3 || 1);

  return totalPieces <= stokReady.value;
};

/**
 * Format currency
 */
const checkCurrencyMinus = (value) => {
  return value < 1 ? 0 : parseCurrency(value);
};

// Watch
watch(selectedPrincipalId, () => {
  filterProductsByPrincipal();
  handleChangePrincipalEffectOnVoucherReguler();
});

watch(principalId, () => getprincipalProducts());

watch(namaProduk, () => {
  if (namaProduk.value) {
    // Reset selectedVouchers terlebih dahulu
    selectedVouchers.value = {
      voucher2Product: null,
      voucher3Product: null
    };

    // Kemudian load voucher yang tersedia untuk produk baru
    loadVouchersForProduct();
  } else {
    // Jika produk tidak dipilih, reset juga
    availableVouchers.value = {
      voucher2Product: [],
      voucher3Product: []
    };
    selectedVouchers.value = {
      voucher2Product: null,
      voucher3Product: null
    };
  }
});

watch(kunjungan.activeKunjungan.kunjungan, () => {
  piutang.$reset();
  voucher.$reset();
  salesRequestStore.clearInitialProducts();

  getResources();
});

watch(
  [salesRequest, filteredSalesRequest],
  () => {
    // Recalculate totals saat salesRequest berubah
    tableKey.value++;
  },
  { deep: true }
);

watch(
  () => voucher.getSelectedRegularVouchers(),
  () => {
    // Saat voucher reguler berubah di store, sync dengan data lokal
    updateSalesRequestFromStore();
    tableKey.value++;
  },
  { deep: true }
);

onMounted(() => {
  getResources();
});

watch(kunjungan.activeKunjungan.kunjungan, () => {
  piutang.$reset();
  voucher.$reset();
  salesRequestStore.clearInitialProducts();

  getResources();
});

const resetAllStores = () => {
  salesRequestStore.clearInitialProducts();
  voucher.$reset();

  salesRequest.value = [];
  filteredSalesRequest.value = [];
  availableVouchers.value = {
    voucher1Regular: [],
    voucher2Regular: [],
    voucher3Regular: [],
    voucher2Product: [],
    voucher3Product: []
  };
  selectedVouchers.value = {
    voucher2Product: null,
    voucher3Product: null
  };
  selectedVoucherReguler.value = {
    voucher1Regular: null,
    voucher2Regular: null,
    voucher3Regular: null
  };
  freeProducts.value = [];
  invalidVoucherNotifications.value = [];

  headerFields.nota_order = generateOrderNumber();

  getResources();
};

onBeforeMount(() => {
  resetAllStores();
});
</script>

<template>
  <FlexBox full flex-col class="lg:tw-pl-6 tw-pl-2">
    <!-- Header Form -->
    <SlideRightX
      class="tw-w-full tw-z-20"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card dense no-subheader class="tw-pb-10">
        <template #header>Form Sales Request Order</template>
        <template #content>
          <FlexBox flex-col>
            <FlexBox it-center class="px-4 tw-flex-col lg:tw-flex-row">
              <FlexBox flex-col gap="small">
                <span class="tw-font-semibold">Sales</span>
                <BFormInput
                  class="lg:tw-w-[270px] tw-w-full"
                  disabled
                  :model-value="sales.salesUser.nama" />
              </FlexBox>
              <FlexBox flex-col gap="small">
                <span class="tw-font-semibold">Customer</span>
                <BFormInput
                  class="lg:tw-w-[270px] tw-w-full"
                  :title="kunjungan.activeKunjungan.kunjungan.nama_customer"
                  disabled
                  :model-value="
                    kunjungan.activeKunjungan.kunjungan.nama_customer
                  " />
              </FlexBox>
              <FlexBox flex-col gap="small">
                <span class="tw-font-semibold">Nota Order</span>
                <BFormInput
                  v-model="headerFields.nota_order"
                  class="lg:tw-w-[270px] tw-w-full"
                  readonly
                  title="Nomor nota order otomatis dibuat dengan format OR/{kode_customer}/timestamp" />
              </FlexBox>
            </FlexBox>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>

    <!-- Info Sisa Plafon dan Piutang -->
    <SlideRightX
      class="tw-w-full"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card no-subheader class="tw-pb-8">
        <template #header>Info Sisa Plafon dan Piutang</template>
        <template #content>
          <div class="tw-w-full lg:tw-w-[60%]">
            <Table
              classic
              :key="piutang.tableKey"
              :loading="piutang.loading"
              :columns="sisaPlafonColumns"
              :table-data="piutang.listPiutang"
              hide-footer
              hide-toolbar />
          </div>
        </template>
      </Card>
    </SlideRightX>

    <!-- Action Buttons -->
    <SlideRightX
      class="tw-w-full"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.3"
      :delay-out="0.3"
      :initial-x="-40"
      :x="40">
      <FlexBox full jus-end>
        <!-- <Button
          :trigger="resettingVoucher"
          class="tw-bg-blue-600 tw-border-none tw-w-40 tw-h-10">
          <i class="mdi mdi-plus tw-text-sm md:tw-text-lg tw-mr-1"></i>
          <span class="tw-text-xs md:tw-text-sm">Tambah Produk</span>
        </Button> -->
        <BButton
          @click="lewatiModal.show()"
          class="tw-bg-red-500 tw-border-none tw-px-6 tw-h-10">
          <i class="mdi mdi-block-helper tw-text-sm md:tw-text-lg tw-mr-2"></i>
          <span class="tw-text-xs md:tw-text-sm">Lewati Sales Request</span>
        </BButton>
      </FlexBox>
    </SlideRightX>

    <!-- List Order -->
    <SlideRightX
      class="tw-w-full"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.4"
      :delay-out="0.4"
      :initial-x="-40"
      :x="40">
      <Card dense no-subheader class="tw-pb-10">
        <template #header>List Order</template>
        <template #content>
          <FlexBox full gap="small" it-center class="tw-px-4">
            <FlexBox flex-col gap="small" class="tw-w-full md:tw-w-1/3">
              <span class="tw-font-semibold">Pilih Principal</span>
              <SelectInput
                :search="true"
                placeholder="Pilih Principal"
                :style="[{ height: '45px' }]"
                :options="principal.principals"
                v-model="selectedPrincipalId"
                text-field="nama"
                value-field="id" />
            </FlexBox>
          </FlexBox>

          <FlexBox full jus-end class="tw-flex-col lg:tw-flex-row tw-px-4">
            <!-- modal untuk tambah atau edit -->
            <Modal id="modal" @modal-closed="resetFormModal" ref="modal">
              <Card dense no-subheader no-main-center class="tw-p-4">
                <template #header>
                  <span class="tw-text-black">
                    {{ isEdit ? "Edit" : "Tambah" }} Produk
                  </span>
                </template>
                <template #content>
                  <FlexBox full>
                    <BForm
                      novalidate
                      class="tw-w-full tw-flex tw-flex-col tw-gap-6">
                      <FlexBox full flex-col gap="small">
                        <span class="tw-font-semibold">Principal</span>
                        <SelectInput
                          :disabled="isEdit"
                          :search="true"
                          placeholder="Pilih Principal"
                          :style="[{ height: '45px' }]"
                          :options="principal.principals"
                          v-model="principalId"
                          text-field="nama"
                          value-field="id" />
                      </FlexBox>
                      <BFormGroup
                        id="input-group-1"
                        label="Nama Produk:"
                        label-for="input-1"
                        v-bind="namaProdukProps">
                        <SelectInput
                          :disabled="isEdit"
                          placeholder="Pilih Produk"
                          text-field="nama"
                          :search="true"
                          value-field="id"
                          size="md"
                          :options="principalProducts"
                          v-model="namaProduk" />
                      </BFormGroup>

                      <BFormGroup
                        v-if="isEdit"
                        id="stok-ready-group"
                        label="Stok Ready:"
                        label-for="stok-ready-input">
                        <BInputGroup>
                          <BFormInput
                            id="stok-ready-input"
                            :value="
                              loadingStokReady
                                ? 'Loading...'
                                : `${stokReady} pieces`
                            "
                            disabled
                            readonly
                            class="tw-bg-gray-100"
                            placeholder="Stok ready akan dimuat..." />
                          <BInputGroupText>
                            <i
                              v-if="loadingStokReady"
                              class="mdi mdi-loading mdi-spin"></i>
                            <i v-else class="mdi mdi-package-variant"></i>
                          </BInputGroupText>
                        </BInputGroup>
                      </BFormGroup>

                      <TextField
                        group-id="input-group-2"
                        label-for="input-2"
                        :config-props="piecesProps"
                        v-model="pieces"
                        type="number"
                        label="Jml UOM 1 / Pieces"
                        placeholder="Masukkan Jumlah dalam Pieces" />
                      <TextField
                        group-id="input-group-3"
                        label-for="input-3"
                        :config-props="boxProps"
                        v-model="box"
                        type="number"
                        label="Jml UOM 2 / Box"
                        placeholder="Masukkan Jumlah dalam box" />
                      <TextField
                        group-id="input-group-4"
                        label-for="input-4"
                        :config-props="kartonProps"
                        v-model="karton"
                        type="number"
                        label="Jml UOM 3 / Karton"
                        placeholder="Masukkan Jumlah dalam Karton" />

                      <!-- Voucher 2 Select -->
                      <BFormGroup
                        id="voucher2-product-group"
                        label="Voucher 2 Produk:"
                        label-for="voucher2-product-select">
                        <SelectInput
                          id="voucher2-product-select"
                          placeholder="Pilih Voucher 2 Produk"
                          text-field="nama_voucher"
                          :clearable="true"
                          :search="true"
                          value-field="id"
                          size="md"
                          :options="availableVouchers.voucher2Product"
                          v-model="selectedVouchers.voucher2Product"
                          :loading="voucherLoading" />
                      </BFormGroup>

                      <!-- Voucher 3 Produk Select -->
                      <BFormGroup
                        id="voucher3-product-group"
                        label="Voucher 3 Produk:"
                        label-for="voucher3-product-select">
                        <SelectInput
                          id="voucher3-product-select"
                          placeholder="Pilih Voucher 3 Produk"
                          text-field="nama_voucher"
                          :search="true"
                          :clearable="true"
                          value-field="id"
                          size="md"
                          :options="availableVouchers.voucher3Product"
                          v-model="selectedVouchers.voucher3Product"
                          :loading="voucherLoading" />
                      </BFormGroup>

                      <FlexBox full jus-end>
                        <BButton
                          @click="closeModal"
                          class="tw-bg-red-600 tw-border-none">
                          Cancel
                        </BButton>
                        <BButton
                          @click="isEdit ? editProduk() : tambahProduk()"
                          type="submit"
                          class="tw-bg-green-500 tw-border-none">
                          {{ isEdit ? "Update" : "Submit" }}
                        </BButton>
                      </FlexBox>
                    </BForm>
                  </FlexBox>
                </template>
              </Card>
            </Modal>
            <Modal id="voucher-reguler-modal" ref="voucherRegulerModal">
              <Card dense no-subheader no-main-center class="tw-p-4">
                <template #header>
                  <span class="tw-text-black">Pilih Voucher Reguler</span>
                </template>
                <template #content>
                  <FlexBox full>
                    <BForm
                      novalidate
                      class="tw-w-full tw-flex tw-flex-col tw-gap-6">
                      <!-- Voucher Reguler 1 Select -->
                      <BFormGroup
                        id="voucher-reguler1-group"
                        label="Voucher Reguler 1:"
                        label-for="voucher-reguler1-select">
                        <SelectInput
                          id="voucher-reguler1-select"
                          placeholder="Pilih Voucher Reguler 1"
                          text-field="nama_voucher"
                          :clearable="true"
                          :search="true"
                          value-field="id"
                          size="md"
                          :options="
                            selectedPrincipalId
                              ? voucher.voucher1RegularList.filter(
                                  (v) => v.id_principal === selectedPrincipalId
                                )
                              : []
                          "
                          v-model="selectedVoucherReguler.voucher1Regular"
                          :loading="voucherRegulerLoading" />
                      </BFormGroup>

                      <!-- Voucher Reguler 2 Select -->
                      <BFormGroup
                        id="voucher-reguler2-group"
                        label="Voucher Reguler 2:"
                        label-for="voucher-reguler2-select">
                        <SelectInput
                          id="voucher-reguler2-select"
                          placeholder="Pilih Voucher Reguler 2"
                          text-field="nama_voucher"
                          :clearable="true"
                          :search="true"
                          value-field="id"
                          size="md"
                          :options="
                            selectedPrincipalId
                              ? voucher.voucher2RegularList.filter(
                                  (v) => v.id_principal === selectedPrincipalId
                                )
                              : []
                          "
                          v-model="selectedVoucherReguler.voucher2Regular"
                          :loading="voucherRegulerLoading" />
                      </BFormGroup>

                      <!-- Voucher Reguler 3 Select -->
                      <BFormGroup
                        id="voucher-reguler3-group"
                        label="Voucher Reguler 3:"
                        label-for="voucher-reguler3-select">
                        <SelectInput
                          id="voucher-reguler3-select"
                          placeholder="Pilih Voucher Reguler 3"
                          text-field="nama_voucher"
                          :search="true"
                          :clearable="true"
                          value-field="id"
                          size="md"
                          :options="
                            selectedPrincipalId
                              ? voucher.voucher3RegularList.filter(
                                  (v) => v.id_principal === selectedPrincipalId
                                )
                              : []
                          "
                          v-model="selectedVoucherReguler.voucher3Regular"
                          :loading="voucherRegulerLoading" />
                      </BFormGroup>

                      <FlexBox full jus-end>
                        <BButton
                          @click="closeVoucherRegulerModal"
                          class="tw-bg-red-600 tw-border-none">
                          Cancel
                        </BButton>
                        <BButton
                          @click="submitVoucherReguler"
                          type="submit"
                          class="tw-bg-green-500 tw-border-none">
                          Terapkan
                        </BButton>
                      </FlexBox>
                    </BForm>
                  </FlexBox>
                </template>
              </Card>
            </Modal>

            <Modal
              id="lewati-modal"
              @modal-closed="resetLewatiTextArea"
              ref="lewatiModal">
              <Card no-subheader no-main-center class="tw-pb-5">
                <template #header>
                  <span class="tw-text-xl tw-text-black">
                    Keterangan / Alasan Tidak Order
                  </span>
                </template>
                <template #content>
                  <FlexBox full flex-col it-end gap="extra large">
                    <BFormTextarea
                      id="textarea"
                      v-model="keteranganTidakOrder"
                      placeholder="Masukkan Alasan"
                      rows="8" />
                    <FlexBox>
                      <BButton
                        class="tw-bg-red-500 tw-w-20 tw-h-8"
                        @click="lewatiModal.hide()">
                        Cancel
                      </BButton>
                      <Button
                        class="tw-bg-green-500 tw-px-4 tw-h-8"
                        :trigger="skipSalesOrder">
                        Submit
                      </Button>
                    </FlexBox>
                  </FlexBox>
                </template>
              </Card>
            </Modal>
          </FlexBox>

          <FlexBox full jusEnd class="md:tw-mb-[-2.75rem] tw-px-4">
            <BFormInput
              v-model="manualSearchTerm"
              placeholder="Cari produk..."
              class="tw-w-full md:tw-w-64" />
          </FlexBox>
          <Table
            table-width="tw-w-[100vw]"
            :loading="salesRequestStore.loading"
            :key="tableKey"
            :columns="listOrderColumns"
            :table-data="searchFiltered"
            classic
            :hideSearch="true"
            :hideToolbar="false"
            @open-row-modal="(val) => openEditModal(val)"
            @remove-row="(val) => removeProduct(val)" />
          <FlexBox full class="tw-ps-4">
            <Button :trigger="openVoucherRegulerModal" class="tw-bg-purple-600">
              <i
                class="mdi mdi-ticket-percent tw-text-sm md:tw-text-lg tw-mr-1"></i>
              <span class="tw-text-xs md:tw-text-sm">Voucher Reguler</span>
            </Button>
          </FlexBox>

          <FlexBox gap="small" flex-col full class="tw-px-4 tw-mt-6">
            <div
              class="tw-w-full md:tw-w-96 tw-ml-auto tw-bg-gray-50 tw-rounded-lg tw-p-4 tw-shadow-sm">
              <h3
                class="tw-font-semibold tw-text-gray-700 tw-mb-3 tw-text-base">
                Rincian Pembayaran
              </h3>

              <div class="tw-flex tw-justify-between tw-py-2">
                <span class="tw-text-gray-600">Sub Total (Sebelum Diskon)</span>
                <span class="tw-font-medium">
                  Rp. {{ checkCurrencyMinus(subTotalBeforeDiscount) }}
                </span>
              </div>

              <div
                class="tw-flex tw-justify-between tw-py-2 tw-border-b tw-border-gray-400">
                <span class="tw-text-gray-600">Total Diskon</span>
                <span class="tw-font-medium tw-text-red-500">
                  - Rp. {{ checkCurrencyMinus(totalDiskon) }}
                </span>
              </div>

              <div class="tw-flex tw-justify-between tw-py-2">
                <span class="tw-text-gray-600">Sub Total</span>
                <span class="tw-font-medium">
                  Rp. {{ checkCurrencyMinus(subTotal) }}
                </span>
              </div>

              <div
                class="tw-flex tw-justify-between tw-py-2 tw-border-b tw-border-gray-400">
                <span class="tw-text-gray-600">PPN</span>
                <span class="tw-font-medium">
                  + Rp. {{ checkCurrencyMinus(pajak) }}
                </span>
              </div>

              <div
                class="tw-flex tw-justify-between tw-py-3 tw-mt-2 tw-bg-blue-50 tw-rounded-md tw-px-3">
                <span class="tw-font-bold tw-text-gray-800">Total</span>
                <span class="tw-font-bold tw-text-lg tw-text-blue-700">
                  Rp. {{ checkCurrencyMinus(total) }}
                </span>
              </div>
            </div>

            <FlexBox full jus-end class="tw-mt-4">
              <Button
                v-if="!freeProducts.length"
                :trigger="submitOrder"
                :loading="submitLoading"
                class="tw-bg-green-500 hover:tw-bg-green-600 tw-border-none tw-w-40 tw-h-10 tw-text-white tw-rounded-md tw-font-medium">
                <i class="mdi mdi-check tw-mr-2"></i>
                Submit Order
              </Button>
            </FlexBox>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>

    <!-- Free Products Section -->
    <Card v-if="freeProducts.length" no-subheader class="tw-pb-8">
      <template #header>List Free Produk</template>
      <template #content>
        <FlexBox full flex-col it-end>
          <Table
            :key="tableKey"
            :columns="listFreeProductsColumns"
            :table-data="freeProducts"
            hide-footer
            hide-toolbar />
          <FlexBox full>
            <span class="tw-text-sm tw-text-blue-500">
              {{ `* Tergantung ketersediaan stock produk` }}
            </span>
          </FlexBox>
          <Button :trigger="submitOrder" class="tw-bg-green-500 tw-w-28 tw-h-9">
            <i class="mdi mdi-check tw-mr-2"></i>
            Submit
          </Button>
        </FlexBox>
      </template>
    </Card>
  </FlexBox>
</template>
