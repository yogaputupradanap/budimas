<script setup>
import Table from "../components/ui/table/Table.vue";
import {detailKonfirmasiOrderColumn} from "../model/tableColumns";
import StatusBar from "../components/ui/StatusBar.vue";
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import {useShipping} from "../store/shipping";
import {computed, inject, nextTick, onMounted, ref, watch} from "vue";
import {
  apiUrl,
  calculateProductDiscounts,
  calculateProductSubtotal,
  fetchWithAuth,
  formatCurrencyAuto,
  getDateNow,
  stringToNumber,
} from "../lib/utils";
import {useRoute, useRouter} from "vue-router";
import Button from "../components/ui/Button.vue";
import {useAlert} from "../store/alert";
import {useKepalaCabang} from "../store/kepalaCabang";
import Modal from "../components/ui/Modal.vue";

const user = useKepalaCabang();
const router = useRouter();
const route = useRoute();
const nav = useRouter();
const shipping = useShipping();
const fakturInfo = ref({});
const detailFaktur = ref([]);
const isRetur = ref(false);
const submitLoading = ref(false);
const modalRef = ref(null);
const selectedProduct = ref({});
const tableKey = ref(0);
const regulerVoucherDebounce = ref(null);

const voucherProdukStatus = ref({
  v2p_active: true,
  v3p_active: true,
});

const voucherRegulerStatus = ref({
  v1r_active: true,
  v2r_active: true,
  v3r_active: true,
});

const initialVoucherProdukState = ref(null);
const hasChanges = ref(false);

const id_faktur =
  shipping?.listDetailFakturShipping?.detailFakturInfo?.id_faktur;
// const id_sales_order = router.params?.id_sales_order;
const alert = useAlert();
const $swal = inject("$swal");
const idCabang = user.kepalaCabangUser.id_cabang;

const setFakturInfo = () => {
  fakturInfo.value = shipping?.listDetailFakturShipping?.detailFakturInfo;
  detailFaktur.value = shipping?.listDetailFakturShipping?.detailFaktur;
  isRetur.value = false;

  const storeRegulerStatus = shipping.voucherStatusStore.regulerStatus;
  voucherRegulerStatus.value = { ...storeRegulerStatus };
};

const id_sales_order = route.params?.id_sales_order; // Gunakan route, bukan router

// 2. Perbaiki fungsi getResource
const getResource = async () => {
  // Gunakan route.query
  await shipping.getListDetailFakturShipping(
    id_sales_order, 
    route.query?.id_order_batch, 
    route.query?.id_sales_orders
  );
  tableKey.value++;
  setFakturInfo();
};


const handleOpenRowModal = (data) => {
  selectedProduct.value = data.value;

  const productStatus = shipping.getVoucherStatusForProduct(
    selectedProduct.value.id_produk
  );

  voucherProdukStatus.value = {
    v2p_active:
      productStatus.v2p_active !== undefined ? productStatus.v2p_active : true,
    v3p_active:
      productStatus.v3p_active !== undefined ? productStatus.v3p_active : true,
  };

  initialVoucherProdukState.value = JSON.stringify(voucherProdukStatus.value);
  hasChanges.value = false;

  nextTick(() => {
    modalRef.value.show();
  });
};

const subtotal = computed(() => {
  let total = 0;
  if (detailFaktur.value && detailFaktur.value.length > 0) {
    detailFaktur.value.forEach((product) => {
      total += calculateProductSubtotal(product);
    });
  }
  return formatCurrencyAuto(total);
});

const diskonNota = computed(() => {
  let totalDiscount = 0;

  if (detailFaktur.value && detailFaktur.value.length > 0) {
    const orderSubtotal = totalOrderSubtotal.value;

    detailFaktur.value.forEach((product) => {
      const voucherStatus = shipping.getVoucherStatusForProduct(
        product.id_produk
      );

      const discountResult = calculateProductDiscounts(
        product,
        voucherStatus,
        orderSubtotal
      );
      totalDiscount += discountResult.totalDiskon;
    });
  }

  return formatCurrencyAuto(totalDiscount);
});

const pajak = computed(() => {
  let totalTax = 0;

  if (detailFaktur.value && detailFaktur.value.length > 0) {
    const orderSubtotal = totalOrderSubtotal.value;

    detailFaktur.value.forEach((product) => {
      const voucherStatus = shipping.getVoucherStatusForProduct(
        product.id_produk
      );

      const discountResult = calculateProductDiscounts(
        product,
        voucherStatus,
        orderSubtotal
      );

      totalTax += discountResult.ppnValue;
    });
  }

  return formatCurrencyAuto(totalTax);
});

const totalPenjualan = computed(() => {
  const subtotalNumeric =
    parseFloat(subtotal.value.replace(/\./g, "").replace(/,/g, ".")) || 0;

  const diskonNumeric =
    parseFloat(diskonNota.value.replace(/\./g, "").replace(/,/g, ".")) || 0;

  const pajakNumeric =
    parseFloat(pajak.value.replace(/\./g, "").replace(/,/g, ".")) || 0;

  const total = subtotalNumeric - diskonNumeric + pajakNumeric;

  return formatCurrencyAuto(total);
});

const totalDiskonProduk = computed(() => {
  if (!selectedProduct.value) return formatCurrencyAuto(0);

  const combinedStatus = {
    ...voucherRegulerStatus.value,
    ...voucherProdukStatus.value,
  };

  const { diskon2p, diskon3p } = calculateProductDiscounts(
    selectedProduct.value,
    combinedStatus,
    totalOrderSubtotal.value
  );

  return formatCurrencyAuto(diskon2p + diskon3p);
});

const calculatedDiskon2p = computed(() => {
  if (!selectedProduct.value) return formatCurrencyAuto(0);

  const combinedStatus = {
    ...voucherRegulerStatus.value,
    v2p_active: voucherProdukStatus.value.v2p_active,
    v3p_active: false,
  };

  const { diskon2p } = calculateProductDiscounts(
    selectedProduct.value,
    combinedStatus,
    totalOrderSubtotal.value
  );

  return formatCurrencyAuto(diskon2p);
});

const calculatedDiskon3p = computed(() => {
  if (!selectedProduct.value) return formatCurrencyAuto(0);

  const combinedStatus = {
    ...voucherRegulerStatus.value,
    v2p_active: false,
    v3p_active: voucherProdukStatus.value.v3p_active,
  };

  const { diskon3p } = calculateProductDiscounts(
    selectedProduct.value,
    combinedStatus,
    totalOrderSubtotal.value
  );

  return formatCurrencyAuto(diskon3p);
});

const totalDiskonReguler = computed(() => {
  let totalDiskon = 0;

  if (detailFaktur.value && detailFaktur.value.length > 0) {
    const orderSubtotal = totalOrderSubtotal.value;

    detailFaktur.value.forEach((product) => {
      const regulerStatus = {
        v1r_active: voucherRegulerStatus.value.v1r_active,
        v2r_active: voucherRegulerStatus.value.v2r_active,
        v3r_active: voucherRegulerStatus.value.v3r_active,
        v2p_active: false,
        v3p_active: false,
      };

      const { diskon1r, diskon2r, diskon3r } = calculateProductDiscounts(
        product,
        regulerStatus,
        orderSubtotal
      );
      totalDiskon += diskon1r + diskon2r + diskon3r;
    });
  }

  return formatCurrencyAuto(totalDiskon);
});

const handleRegulerVoucherChange = () => {
  shipping.saveRegulerVoucherStatus(voucherRegulerStatus.value);

  tableKey.value++;

  $swal.success("Status voucher reguler berhasil disimpan");
};

const submitOrder = async () => {
  const orderSubtotal = totalOrderSubtotal.value;

  const voucherProducts = detailFaktur.value.map((product) => {
    const voucherStatus = shipping.getVoucherStatusForProduct(
      product.id_produk
    );

    const discountResult = calculateProductDiscounts(
      product,
      voucherStatus,
      orderSubtotal
    );

    const productVouchers = [];

    if (product.v1r_nama && voucherStatus.v1r_active) {
      productVouchers.push({
        kode: product.v1r_kode,
        nama: product.v1r_nama,
        diskon: parseFloat(discountResult.diskon1r.toFixed(2)),
        active: true,
        id_dv: product.v1r_id_dv,
      });
    } else if (product.v1r_nama && !voucherStatus.v1r_active) {
      productVouchers.push({
        kode: product.v1r_kode,
        nama: product.v1r_nama,
        diskon: 0,
        active: false,
        id_dv: product.v1r_id_dv,
      });
    }

    if (product.v2r_nama && voucherStatus.v2r_active) {
      productVouchers.push({
        kode: product.v2r_kode,
        nama: product.v2r_nama,
        diskon: parseFloat(discountResult.diskon2r.toFixed(2)),
        active: true,
        id_dv: product.v2r_id_dv,
      });
    } else if (product.v2r_nama && !voucherStatus.v2r_active) {
      productVouchers.push({
        kode: product.v2r_kode,
        nama: product.v2r_nama,
        diskon: 0,
        active: false,
        id_dv: product.v2r_id_dv,
      });
    }

    if (product.v3r_nama && voucherStatus.v3r_active) {
      productVouchers.push({
        kode: product.v3r_kode,
        nama: product.v3r_nama,
        diskon: parseFloat(discountResult.diskon3r.toFixed(2)),
        active: true,
        id_dv: product.v3r_id_dv,
      });
    } else if (product.v3r_nama && !voucherStatus.v3r_active) {
      productVouchers.push({
        kode: product.v3r_kode,
        nama: product.v3r_nama,
        diskon: 0,
        active: false,
        id_dv: product.v3r_id_dv,
      });
    }

    if (product.v2p_nama && voucherStatus.v2p_active) {
      productVouchers.push({
        kode: product.v2p_kode,
        nama: product.v2p_nama,
        diskon: parseFloat(discountResult.diskon2p.toFixed(2)),
        active: true,
        id_dv: product.v2p_id_dv,
      });
    } else if (product.v2p_nama && !voucherStatus.v2p_active) {
      productVouchers.push({
        kode: product.v2p_kode,
        nama: product.v2p_nama,
        diskon: 0,
        active: false,
        id_dv: product.v2p_id_dv,
      });
    }

    if (product.v3p_nama && voucherStatus.v3p_active) {
      productVouchers.push({
        kode: product.v3p_kode,
        nama: product.v3p_nama,
        diskon: parseFloat(discountResult.diskon3p.toFixed(2)),
        active: true,
        id_dv: product.v3p_id_dv,
      });
    } else if (product.v3p_nama && !voucherStatus.v3p_active) {
      productVouchers.push({
        kode: product.v3p_kode,
        nama: product.v3p_nama,
        diskon: 0,
        active: false,
        id_dv: product.v3p_id_dv,
      });
    }

    const voucher_status = {};

    if (product.v1r_nama !== null) {
      voucher_status.v1r_active = voucherStatus.v1r_active || false;
    }

    if (product.v2r_nama !== null) {
      voucher_status.v2r_active = voucherStatus.v2r_active || false;
    }

    if (product.v3r_nama !== null) {
      voucher_status.v3r_active = voucherStatus.v3r_active || false;
    }

    if (product.v2p_nama !== null) {
      voucher_status.v2p_active = voucherStatus.v2p_active || false;
    }

    if (product.v3p_nama !== null) {
      voucher_status.v3p_active = voucherStatus.v3p_active || false;
    }

    const calculatedSubtotal = calculateProductSubtotal(product);

    return {
      id_produk: product.id_produk,
      konversi_level1: product.konversi_level1,
      konversi_level2: product.konversi_level2,
      konversi_level3: product.konversi_level3,
      karton_order: product.karton_order,
      box_order: product.box_order,
      pieces_order: product.pieces_order,
      id_sales_order_detail: product.id_order_detail,
      puom1_packing_lebar: product.puom1_packing_lebar,
      puom1_packing_panjang: product.puom1_packing_panjang,
      puom1_packing_tinggi: product.puom1_packing_tinggi,
      puom2_packing_lebar: product.puom2_packing_lebar,
      puom2_packing_panjang: product.puom2_packing_panjang,
      puom2_packing_tinggi: product.puom2_packing_tinggi,
      puom3_packing_lebar: product.puom3_packing_lebar,
      puom3_packing_panjang: product.puom3_packing_panjang,
      puom3_packing_tinggi: product.puom3_packing_tinggi,
      subtotalorder: calculatedSubtotal,
      vouchers: productVouchers,
      voucher_status: voucher_status,
    };
  });

  const vouchers = {
    voucher_product: voucherProducts,
    total_order_subtotal: orderSubtotal,
  };

  try {
    const isConfirmed = await $swal.confirmSubmit(
      "Apakah Anda yakin ingin mengkonfirmasi order ini?"
    );
    if (!isConfirmed) return;
    const response = await fetchWithAuth(
      "PATCH",
      `${apiUrl}/api/distribusi/konfirmasi-order`,
      {
        id_sales_order,
        id_cabang: idCabang,
        total_penjualan: stringToNumber(totalPenjualan.value),
        subtotal_diskon: stringToNumber(diskonNota.value),
        // Menghitung DPP: (Subtotal - Diskon)
        dpp: stringToNumber(subtotal.value) - stringToNumber(diskonNota.value),
        pajak: stringToNumber(pajak.value),
        products: detailFaktur.value,
        // Gunakan optional chaining untuk query router
        id_order_batch: route.query?.id_order_batch || null, 
        vouchers,
      }
    );

    $swal.success(
      `Order dengan No Order [${fakturInfo.value.no_order}] berhasil dikonfirmasi!`
    );
    router.replace("/konfirmasi");
  } catch (error) {
    $swal.error(
      error.message || "Gagal mengkonfirmasi order. Silakan coba lagi."
    );
  }
};
const totalOrderSubtotal = computed(() => {
  let total = 0;
  if (detailFaktur.value && detailFaktur.value.length > 0) {
    detailFaktur.value.forEach((product) => {
      total += calculateProductSubtotal(product);
    });
  }
  return total;
});

const tolakOrder = async () => {
  try {
    const isConfirmed = await $swal.confirmTolak("Apakah Anda yakin...");
    if (!isConfirmed) return;
    
    await fetchWithAuth("PATCH", `${apiUrl}/api/distribusi/tolak-order`, {
      id_sales_order,
      id_order_batch: route.query?.id_order_batch || null, // Gunakan route
    });
    
    $swal.success(`Order [${fakturInfo.value.no_order}] berhasil ditolak!`);
    router.replace("/konfirmasi"); // Gunakan router untuk navigasi
  } catch (error) {
    $swal.error(error || "Gagal menolak order.");
  }
};

const handleCancel = () => {
  modalRef.value.hide();
};

const handleSave = () => {
  initialVoucherProdukState.value = JSON.stringify(voucherProdukStatus.value);
  hasChanges.value = false;

  shipping.saveProductVoucherStatus(
    selectedProduct.value.id_produk,
    voucherProdukStatus.value
  );

  $swal.success("Voucher produk berhasil disimpan");

  tableKey.value++;

  modalRef.value.hide();
};

watch(
  voucherProdukStatus,
  (newValue) => {
    const currentState = JSON.stringify(newValue);
    hasChanges.value = currentState !== initialVoucherProdukState.value;
  },
  { deep: true }
);

watch(
  voucherRegulerStatus,
  (newValue) => {
    if (regulerVoucherDebounce.value) {
      clearTimeout(regulerVoucherDebounce.value);
    }

    regulerVoucherDebounce.value = setTimeout(() => {
      shipping.saveRegulerVoucherStatus(newValue);
      tableKey.value++;
    }, 100);
  },
  { deep: true }
);

watch(
  () => shipping.voucherStatusStore,
  () => {
    tableKey.value++;
  },
  { deep: true }
);

onMounted(() => getResource());
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px-0">
    <Modal id="modal" ref="modalRef">
      <div class="tw-p-4">
        <h3
          class="tw-text-lg tw-font-semibold tw-mb-5 tw-text-center tw-border-b tw-pb-3">
          Voucher Produk untuk {{ selectedProduct.nama_produk }}
        </h3>

        <div class="tw-space-y-5 tw-mb-6">
          <div
            v-if="selectedProduct.v2p_nama"
            class="tw-bg-gradient-to-r tw-from-green-50 tw-to-emerald-50 tw-border tw-border-green-200 tw-rounded-lg tw-shadow-md tw-p-5 tw-transition-all tw-duration-200 hover:tw-shadow-lg"
            :class="{
              'tw-opacity-70': !voucherProdukStatus.v2p_active,
              'tw-border-green-400': voucherProdukStatus.v2p_active,
            }">
            <div class="tw-flex tw-justify-between tw-items-start">
              <div class="tw-flex-1">
                <div class="tw-flex tw-items-center tw-mb-2">
                  <i
                    class="mdi mdi-ticket-percent tw-text-xl tw-text-green-600 tw-mr-2"></i>
                  <h4 class="tw-font-semibold tw-text-green-800">
                    {{ selectedProduct.v2p_nama }}
                    <span
                      class="tw-ml-1 tw-text-xs tw-bg-green-200 tw-text-green-700 tw-py-0.5 tw-px-1.5 tw-rounded">
                      {{
                        selectedProduct.v2p_kategori_voucher === 1
                          ? `(${selectedProduct.v2p_persen}%)`
                          : `(${formatCurrencyAuto(
                              selectedProduct.v2p_nominal_diskon
                            )}/${selectedProduct.puom1_nama})`
                      }}
                    </span>
                  </h4>
                </div>
                <div class="tw-flex tw-flex-col tw-gap-1">
                  <p class="tw-text-red-600 tw-font-medium tw-text-lg">
                    Diskon: Rp.
                    {{ calculatedDiskon2p }}
                  </p>
                  <p
                    class="tw-text-xs tw-text-gray-500 tw-bg-white tw-inline-block tw-px-2 tw-py-1 tw-rounded">
                    Kode: {{ selectedProduct.v2p_kode }}
                  </p>
                </div>
              </div>
              <div class="tw-flex tw-items-center">
                <div
                  class="tw-relative tw-inline-block tw-w-10 tw-h-6 tw-transition tw-duration-200 tw-ease-in-out">
                  <input
                    type="checkbox"
                    id="voucher2p"
                    v-model="voucherProdukStatus.v2p_active"
                    class="tw-opacity-0 tw-w-0 tw-h-0" />
                  <label
                    for="voucher2p"
                    class="tw-toggle-label tw-absolute tw-cursor-pointer tw-top-0 tw-left-0 tw-right-0 tw-bottom-0 tw-bg-gray-300 tw-rounded-full"
                    :class="
                      voucherProdukStatus.v2p_active
                        ? 'tw-bg-green-500'
                        : 'tw-bg-gray-300'
                    ">
                    <span
                      class="tw-toggle-dot tw-absolute tw-left-1 tw-bottom-1 tw-bg-white tw-w-4 tw-h-4 tw-rounded-full tw-transition-transform tw-duration-200 tw-ease-in-out"
                      :class="
                        voucherProdukStatus.v2p_active
                          ? 'tw-transform tw-translate-x-4'
                          : ''
                      "></span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <div
            v-if="selectedProduct.v3p_nama"
            class="tw-bg-gradient-to-r tw-from-purple-50 tw-to-violet-50 tw-border tw-border-purple-200 tw-rounded-lg tw-shadow-md tw-p-5 tw-transition-all tw-duration-200 hover:tw-shadow-lg"
            :class="{
              'tw-opacity-70': !voucherProdukStatus.v3p_active,
              'tw-border-purple-400': voucherProdukStatus.v3p_active,
            }">
            <div class="tw-flex tw-justify-between tw-items-start">
              <div class="tw-flex-1">
                <div class="tw-flex tw-items-center tw-mb-2">
                  <i
                    class="mdi mdi-ticket-percent tw-text-xl tw-text-purple-600 tw-mr-2"></i>
                  <h4 class="tw-font-semibold tw-text-purple-800">
                    {{ selectedProduct.v3p_nama }}
                    <span
                      class="tw-ml-1 tw-text-xs tw-bg-purple-200 tw-text-purple-700 tw-py-0.5 tw-px-1.5 tw-rounded">
                      {{
                        selectedProduct.v3p_kategori_voucher === 1
                          ? `(${selectedProduct.v3p_persen}%)`
                          : `(${formatCurrencyAuto(
                              selectedProduct.v3p_nominal_diskon
                            )}/${selectedProduct.puom1_nama})`
                      }}
                    </span>
                  </h4>
                </div>
                <div class="tw-flex tw-flex-col tw-gap-1">
                  <p class="tw-text-red-600 tw-font-medium tw-text-lg">
                    Diskon: Rp.
                    {{ calculatedDiskon3p }}
                  </p>
                  <p
                    class="tw-text-xs tw-text-gray-500 tw-bg-white tw-inline-block tw-px-2 tw-py-1 tw-rounded">
                    Kode: {{ selectedProduct.v3p_kode }}
                  </p>
                </div>
              </div>
              <div class="tw-flex tw-items-center">
                <div
                  class="tw-relative tw-inline-block tw-w-10 tw-h-6 tw-transition tw-duration-200 tw-ease-in-out">
                  <input
                    type="checkbox"
                    id="voucher3p"
                    v-model="voucherProdukStatus.v3p_active"
                    class="tw-opacity-0 tw-w-0 tw-h-0" />
                  <label
                    for="voucher3p"
                    class="tw-toggle-label tw-absolute tw-cursor-pointer tw-top-0 tw-left-0 tw-right-0 tw-bottom-0 tw-bg-gray-300 tw-rounded-full"
                    :class="
                      voucherProdukStatus.v3p_active
                        ? 'tw-bg-purple-500'
                        : 'tw-bg-gray-300'
                    ">
                    <span
                      class="tw-toggle-dot tw-absolute tw-left-1 tw-bottom-1 tw-bg-white tw-w-4 tw-h-4 tw-rounded-full tw-transition-transform tw-duration-200 tw-ease-in-out"
                      :class="
                        voucherProdukStatus.v3p_active
                          ? 'tw-transform tw-translate-x-4'
                          : ''
                      "></span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="tw-border-t tw-border-gray-200 tw-pt-4 tw-mt-6">
          <div class="tw-bg-gray-50 tw-rounded-lg tw-p-3 tw-mb-4">
            <p
              class="tw-text-sm tw-text-gray-700 tw-flex tw-justify-between tw-items-center">
              <span>Total diskon produk:</span>
              <span class="tw-font-medium tw-text-red-600 tw-text-lg">
                Rp. {{ totalDiskonProduk }}
              </span>
            </p>
          </div>

          <div class="tw-flex tw-justify-end tw-gap-2">
            <Button
              class="tw-px-5 tw-py-2 tw-bg-gray-500 hover:tw-bg-gray-600"
              :trigger="handleCancel">
              Batal
            </Button>
            <Button
              class="tw-px-5 tw-py-2 tw-bg-blue-500 hover:tw-bg-blue-600"
              :disabled="!hasChanges"
              :trigger="handleSave">
              <i class="mdi mdi-content-save tw-mr-1"></i>
              Simpan
            </Button>
          </div>
        </div>
      </div>
    </Modal>
    <SlideRightX
      class=""
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true">
        <template #header>Detail Order Transaksi</template>
        <template #content>
          <div class="status-field-container-3-col tw-mb-5">
            <StatusBar
              :loading="shipping.listDetailFakturShipping.loading"
              label="No Order :"
              :value="fakturInfo?.no_order || ''" />
            <StatusBar
              :loading="shipping.listDetailFakturShipping.loading"
              label="Customer :"
              :value="fakturInfo?.nama_customer || ''" />
            <StatusBar
              :loading="shipping.listDetailFakturShipping.loading"
              label="Tanggal Order :"
              :value="
                getDateNow(new Date(fakturInfo?.tanggal_order), false) || ''
              " />
            <!-- <StatusBar
              :loading="shipping.listDetailFakturShipping.loading"
              label="Tanggal Jatuh Tempo :"
              :value="
                getDateNow(new Date(fakturInfo?.tanggal_jatuh_tempo), false) ||
                ''
              " /> -->
          </div>
        </template>
      </Card>
      <Card :no-subheader="true" class="tw-mt-5">
        <template #header>List Order</template>
        <template #content>
         <div class="tw-w-full">
            <span v-if="shipping.listDetailFakturShipping.detailFaktur.length > 0">
              {{ shipping.listDetailFakturShipping.detailFaktur[0].nama_produk }}
            </span>

            <Table
              :key="tableKey"
              classic
              :loading="shipping?.listDetailFakturShipping?.loading"
              :table-data="shipping?.listDetailFakturShipping?.detailFaktur || []"
              :columns="detailKonfirmasiOrderColumn"
              @open-row-modal="handleOpenRowModal" 
            />
          </div>
          <Card :no-subheader="true" class="tw-mt-5">
            <template #header>
              <div class="tw-flex tw-items-center">
                <i
                  class="mdi mdi-ticket-percent tw-text-xl tw-text-blue-600 tw-mr-2"></i>
                <span>Voucher Reguler</span>
              </div>
            </template>
            <template #content>
              <div class="tw-w-full">
                <div
                  class="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 lg:tw-grid-cols-3 tw-gap-4 tw-mb-6">
                  <div
                    v-if="detailFaktur[0]?.v1r_nama"
                    class="tw-bg-gradient-to-r tw-from-blue-50 tw-to-indigo-50 tw-border tw-border-blue-200 tw-rounded-lg tw-shadow-md tw-p-5 tw-transition-all tw-duration-200 hover:tw-shadow-lg"
                    :class="{
                      'tw-opacity-70': !voucherRegulerStatus.v1r_active,
                      'tw-border-blue-400 tw-shadow-blue-100':
                        voucherRegulerStatus.v1r_active,
                    }">
                    <div class="tw-flex tw-justify-between tw-items-start">
                      <div class="tw-flex-1">
                        <div class="tw-flex tw-items-center tw-mb-2">
                          <div
                            class="tw-rounded-full tw-bg-blue-100 tw-p-1.5 tw-mr-2">
                            <i
                              class="mdi mdi-ticket-percent tw-text-xl tw-text-blue-600"></i>
                          </div>
                          <h4 class="tw-font-semibold tw-text-blue-800">
                            {{ detailFaktur[0].v1r_nama }}
                          </h4>
                        </div>
                        <span
                          class="tw-inline-block tw-mb-2 tw-text-sm tw-bg-blue-100 tw-text-blue-700 tw-py-1 tw-px-2 tw-rounded-md">
                          Diskon {{ detailFaktur[0].v1r_persen }}%
                        </span>
                        <div class="tw-flex tw-flex-col tw-gap-1 tw-mt-3">
                          <p
                            class="tw-text-xs tw-text-gray-500 tw-bg-white tw-inline-block tw-px-2 tw-py-1 tw-rounded tw-border tw-border-gray-100">
                            <i class="mdi mdi-barcode tw-mr-1"></i>
                            Kode: {{ detailFaktur[0].v1r_kode }}
                          </p>
                          <p class="tw-text-xs tw-text-gray-700 tw-mt-1">
                            <i class="mdi mdi-currency-usd tw-mr-1"></i>
                            Min. Subtotal:
                            <span class="tw-font-medium">
                              Rp.
                              {{
                                formatCurrencyAuto(
                                  detailFaktur[0].v1r_minimal_subtotal_pembelian
                                )
                              }}
                            </span>
                          </p>
                        </div>
                      </div>
                      <div class="tw-flex tw-items-center">
                        <div
                          class="tw-relative tw-inline-block tw-w-12 tw-h-6 tw-transition tw-duration-200 tw-ease-in-out">
                          <input
                            type="checkbox"
                            id="voucher1r"
                            v-model="voucherRegulerStatus.v1r_active"
                            class="tw-opacity-0 tw-w-0 tw-h-0" />
                          <label
                            for="voucher1r"
                            class="tw-toggle-label tw-absolute tw-cursor-pointer tw-top-0 tw-left-0 tw-right-0 tw-bottom-0 tw-rounded-full tw-transition-all tw-duration-300"
                            :class="
                              voucherRegulerStatus.v1r_active
                                ? 'tw-bg-blue-500'
                                : 'tw-bg-gray-300'
                            ">
                            <span
                              class="tw-toggle-dot tw-absolute tw-left-1 tw-bottom-1 tw-bg-white tw-w-4 tw-h-4 tw-rounded-full tw-transition-transform tw-duration-300 tw-ease-in-out tw-shadow-sm"
                              :class="
                                voucherRegulerStatus.v1r_active
                                  ? 'tw-transform tw-translate-x-6'
                                  : ''
                              "></span>
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div
                    v-if="detailFaktur[0]?.v2r_nama"
                    class="tw-bg-gradient-to-r tw-from-teal-50 tw-to-emerald-50 tw-border tw-border-teal-200 tw-rounded-lg tw-shadow-md tw-p-5 tw-transition-all tw-duration-200 hover:tw-shadow-lg"
                    :class="{
                      'tw-opacity-70': !voucherRegulerStatus.v2r_active,
                      'tw-border-teal-400 tw-shadow-teal-100':
                        voucherRegulerStatus.v2r_active,
                    }">
                    <div class="tw-flex tw-justify-between tw-items-start">
                      <div class="tw-flex-1">
                        <div class="tw-flex tw-items-center tw-mb-2">
                          <div
                            class="tw-rounded-full tw-bg-teal-100 tw-p-1.5 tw-mr-2">
                            <i
                              class="mdi mdi-ticket-percent tw-text-xl tw-text-teal-600"></i>
                          </div>
                          <h4 class="tw-font-semibold tw-text-teal-800">
                            {{ detailFaktur[0].v2r_nama }}
                          </h4>
                        </div>
                        <span
                          class="tw-inline-block tw-mb-2 tw-text-sm tw-bg-teal-100 tw-text-teal-700 tw-py-1 tw-px-2 tw-rounded-md">
                          Diskon {{ detailFaktur[0].v2r_persen }}%
                        </span>
                        <div class="tw-flex tw-flex-col tw-gap-1 tw-mt-3">
                          <p
                            class="tw-text-xs tw-text-gray-500 tw-bg-white tw-inline-block tw-px-2 tw-py-1 tw-rounded tw-border tw-border-gray-100">
                            <i class="mdi mdi-barcode tw-mr-1"></i>
                            Kode: {{ detailFaktur[0].v2r_kode }}
                          </p>
                          <p class="tw-text-xs tw-text-gray-700 tw-mt-1">
                            <i class="mdi mdi-currency-usd tw-mr-1"></i>
                            Min. Subtotal:
                            <span class="tw-font-medium">
                              Rp.
                              {{
                                formatCurrencyAuto(
                                  detailFaktur[0].v2r_minimal_subtotal_pembelian
                                )
                              }}
                            </span>
                          </p>
                        </div>
                      </div>
                      <div class="tw-flex tw-items-center">
                        <div
                          class="tw-relative tw-inline-block tw-w-12 tw-h-6 tw-transition tw-duration-200 tw-ease-in-out">
                          <input
                            type="checkbox"
                            id="voucher2r"
                            v-model="voucherRegulerStatus.v2r_active"
                            class="tw-opacity-0 tw-w-0 tw-h-0" />
                          <label
                            for="voucher2r"
                            class="tw-toggle-label tw-absolute tw-cursor-pointer tw-top-0 tw-left-0 tw-right-0 tw-bottom-0 tw-rounded-full tw-transition-all tw-duration-300"
                            :class="
                              voucherRegulerStatus.v2r_active
                                ? 'tw-bg-teal-500'
                                : 'tw-bg-gray-300'
                            ">
                            <span
                              class="tw-toggle-dot tw-absolute tw-left-1 tw-bottom-1 tw-bg-white tw-w-4 tw-h-4 tw-rounded-full tw-transition-transform tw-duration-300 tw-ease-in-out tw-shadow-sm"
                              :class="
                                voucherRegulerStatus.v2r_active
                                  ? 'tw-transform tw-translate-x-6'
                                  : ''
                              "></span>
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div
                    v-if="detailFaktur[0]?.v3r_nama"
                    class="tw-bg-gradient-to-r tw-from-yellow-50 tw-to-amber-50 tw-border tw-border-yellow-200 tw-rounded-lg tw-shadow-md tw-p-5 tw-transition-all tw-duration-200 hover:tw-shadow-lg"
                    :class="{
                      'tw-opacity-70': !voucherRegulerStatus.v3r_active,
                      'tw-border-yellow-400 tw-shadow-yellow-100':
                        voucherRegulerStatus.v3r_active,
                    }">
                    <div class="tw-flex tw-justify-between tw-items-start">
                      <div class="tw-flex-1">
                        <div class="tw-flex tw-items-center tw-mb-2">
                          <div
                            class="tw-rounded-full tw-bg-yellow-100 tw-p-1.5 tw-mr-2">
                            <i
                              class="mdi mdi-ticket-percent tw-text-xl tw-text-yellow-600"></i>
                          </div>
                          <h4 class="tw-font-semibold tw-text-yellow-800">
                            {{ detailFaktur[0].v3r_nama }}
                          </h4>
                        </div>
                        <span
                          class="tw-inline-block tw-mb-2 tw-text-sm tw-bg-yellow-100 tw-text-yellow-700 tw-py-1 tw-px-2 tw-rounded-md">
                          Diskon {{ detailFaktur[0].v3r_persen }}%
                        </span>
                        <div class="tw-flex tw-flex-col tw-gap-1 tw-mt-3">
                          <p
                            class="tw-text-xs tw-text-gray-500 tw-bg-white tw-inline-block tw-px-2 tw-py-1 tw-rounded tw-border tw-border-gray-100">
                            <i class="mdi mdi-barcode tw-mr-1"></i>
                            Kode: {{ detailFaktur[0].v3r_kode }}
                          </p>
                          <p class="tw-text-xs tw-text-gray-700 tw-mt-1">
                            <i class="mdi mdi-currency-usd tw-mr-1"></i>
                            Min. Subtotal:
                            <span class="tw-font-medium">
                              Rp.
                              {{
                                formatCurrencyAuto(
                                  detailFaktur[0].v3r_minimal_subtotal_pembelian
                                )
                              }}
                            </span>
                          </p>
                        </div>
                      </div>
                      <div class="tw-flex tw-items-center">
                        <div
                          class="tw-relative tw-inline-block tw-w-12 tw-h-6 tw-transition tw-duration-200 tw-ease-in-out">
                          <input
                            type="checkbox"
                            id="voucher3r"
                            v-model="voucherRegulerStatus.v3r_active"
                            class="tw-opacity-0 tw-w-0 tw-h-0" />
                          <label
                            for="voucher3r"
                            class="tw-toggle-label tw-absolute tw-cursor-pointer tw-top-0 tw-left-0 tw-right-0 tw-bottom-0 tw-rounded-full tw-transition-all tw-duration-300"
                            :class="
                              voucherRegulerStatus.v3r_active
                                ? 'tw-bg-yellow-500'
                                : 'tw-bg-gray-300'
                            ">
                            <span
                              class="tw-toggle-dot tw-absolute tw-left-1 tw-bottom-1 tw-bg-white tw-w-4 tw-h-4 tw-rounded-full tw-transition-transform tw-duration-300 tw-ease-in-out tw-shadow-sm"
                              :class="
                                voucherRegulerStatus.v3r_active
                                  ? 'tw-transform tw-translate-x-6'
                                  : ''
                              "></span>
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </Card>
          <div class="tw-flex tw-flex-col tw-items-end tw-mb-5 tw-w-full">
            <div
              class="tw-w-full md:tw-w-80 tw-ml-auto tw-bg-gray-50 tw-rounded-lg tw-p-4 tw-shadow-sm">
              <h3
                class="tw-font-semibold tw-text-gray-700 tw-mb-3 tw-text-base">
                Rincian Pembayaran
              </h3>
              <div class="tw-space-y-3">
                <div class="tw-flex tw-justify-between tw-items-center tw-py-2">
                  <span class="tw-text-gray-600">SubTotal</span>
                  <span class="tw-font-medium">Rp. {{ subtotal }}</span>
                </div>

                <div class="tw-flex tw-justify-between tw-items-center tw-py-2">
                  <span class="tw-text-gray-600">Diskon Nota</span>
                  <span class="tw-font-medium tw-text-red-500">
                    - Rp. {{ diskonNota }}
                  </span>
                </div>

                <div
                  class="tw-flex tw-justify-between tw-items-center tw-py-2 tw-border-b tw-border-gray-400">
                  <span class="tw-text-gray-600">PPN</span>
                  <span class="tw-font-medium">+ Rp. {{ pajak }}</span>
                </div>

                <div
                  class="tw-flex tw-justify-between tw-items-center tw-py-3 tw-mt-1 tw-bg-blue-50 tw-rounded-md tw-px-3">
                  <span class="tw-font-bold tw-text-gray-800">Total</span>
                  <span class="tw-font-bold tw-text-lg tw-text-blue-700">
                    Rp. {{ totalPenjualan }}
                  </span>
                </div>
              </div>
            </div>
            <div class="tw-flex tw-flex-row tw-gap-2 tw-mt-3">
              <Button
                :trigger="tolakOrder"
                class="tw-px-4 tw-py-2 tw-bg-red-500"
                icon="mdi mdi-close">
                Tolak
              </Button>
              <Button
                :trigger="submitOrder"
                class="tw-px-4 tw-py-2"
                icon="mdi mdi-check">
                Submit
              </Button>
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
