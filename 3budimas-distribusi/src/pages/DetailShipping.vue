<script setup>
import Table from "../components/ui/table/Table.vue";
import {dataColumnsDetailShipping} from "../model/tableColumns";
import StatusBar from "../components/ui/StatusBar.vue";
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import {useShipping} from "../store/shipping";
import {computed, inject, nextTick, onMounted, ref} from "vue";
import {
  apiUrl,
  calculateProductDiscounts,
  calculateProductSubtotal,
  downloadPdf,
  fetchWithAuth,
  formatCurrencyAuto,
  getDateNow,
} from "../lib/utils";
import Faktur from "../components/pdf/Faktur.vue";
import {useRoute, useRouter} from "vue-router";
import {useAlert} from "../store/alert";
import {useKepalaCabang} from "../store/kepalaCabang";
import {downloadPdf2} from "../lib/faktur";

const user = useKepalaCabang();
const router = useRoute();
const shipping = useShipping();
const fakturInfo = ref({});
const detailFaktur = ref([]);
const pdfTitle = ref("");
const isRetur = ref(false);
const tableKey = ref(0);
const route = useRouter();

const id_faktur =
  shipping?.listDetailFakturShipping?.detailFakturInfo?.id_faktur;
const id_sales_order = router.params?.id_sales_order;
const alert = useAlert();
const idCabang = user?.kepalaCabangUser?.id_cabang;
const idRute = router.params?.id_rute;
const $swal = inject("$swal");
const idArmada = router.query.id_armada;
const idDriver = router.query.id_driver;
const deliveringDate = router.query.delivering_date;
const namaShipping = user?.kepalaCabangUser?.nama;

const setFakturInfo = () => {
  fakturInfo.value = shipping?.listDetailFakturShipping?.detailFakturInfo;
  detailFaktur.value = shipping?.listDetailFakturShipping?.detailFaktur;
  isRetur.value = false;
};

const updateStatusFaktur = async () => {
  try {
    const isConfirm = await $swal.confirmSubmit();
    if (!isConfirm) return false;

    await fetchWithAuth(
      "PUT",
      `${apiUrl}/api/distribusi/submit-shipping?id_sales_order=${id_sales_order}&nama=${namaShipping}&id_cabang=${idCabang}`
    );

    $swal.success("Berhasil mengupdate status faktur");
    await shipping.getListFakturShipping(
      idCabang,
      idRute,
      false,
      idArmada,
      idDriver,
      deliveringDate
    );
    route.back();
    return true;
  } catch (error) {
    console.log(error);
    return false;
  }
};

const donwloadFakturPdf = async (title) => {
  const isA4 = detailFaktur.value.length > 8;
  setFakturInfo();
  pdfTitle.value = title;

  // Memastikan objek fakturInfo memiliki semua property yang dibutuhkan
  if (!fakturInfo.value.total_penjualan) {
    // Tambahkan data yang mungkin diperlukan oleh Faktur.vue
    fakturInfo.value = {
      ...fakturInfo.value,
      subtotal_penjualan: parseFloat(
        subtotal.value.replace(/\./g, "").replace(/,/g, ".")
      ),
      subtotal_diskon: parseFloat(
        diskonNota.value.replace(/\./g, "").replace(/,/g, ".")
      ),
      pajak: parseFloat(pajak.value.replace(/\./g, "").replace(/,/g, ".")),
      total_penjualan: parseFloat(
        totalPenjualan.value.replace(/\./g, "").replace(/,/g, ".")
      ),
    };
  }

  // Pastikan setiap item di detailFaktur memiliki property yang diperlukan
  if (detailFaktur.value && detailFaktur.value.length > 0) {
    detailFaktur.value = detailFaktur.value.map((item) => {
      // Pastikan vouchers ada dan merupakan array
      if (!item.vouchers) {
        item.vouchers = [];
      }

      // Pastikan draft_voucher_detail ada dan merupakan array
      if (!item.draft_voucher_detail) {
        item.draft_voucher_detail = [];
      }

      // Hitung subtotalorder jika tidak ada
      if (!item.subtotalorder) {
        // Konversi semua picked ke level UOM1
        const kartonToUom1 =
          (item.karton_picked || 0) * (item.konversi_level3 || 1);
        const boxToUom1 = (item.box_picked || 0) * (item.konversi_level2 || 1);
        const piecesUom1 = item.pieces_picked || 0;

        // Total pieces setelah konversi
        const totalPieces = kartonToUom1 + boxToUom1 + piecesUom1;

        // Hitung subtotal
        item.subtotalorder = totalPieces * (item.harga_jual || 0);
      }

      return item;
    });
  }

  if (title === "retur") {
    try {
      const retur = await fetchWithAuth(
        "GET",
        `${apiUrl}/api/distribusi/get-detail-faktur-retur/${id_sales_order}`
      );

      if (!Object.keys(retur.detail_faktur).length) {
        throw "Tidak ada faktur retur";
      }

      fakturInfo.value = retur.detail_faktur;
    } catch (error) {
      $swal.error(error);
      return;
    } finally {
      isRetur.value = true;
    }
  }

  nextTick(() => {
    downloadPdf(
      "faktur",
      `faktur ${title} ${getDateNow()}`,
      isA4 ? "portrait" : "portrait",
      isA4 ? "letter" : "letter"
    );
  });
};

const submitAndPrintFaktur = async (title) => {
  try {
    const isUpdated = await updateStatusFaktur();

    if (isUpdated) {
      await donwloadFakturPdf(title);
    }
  } catch (error) {
    console.log(error);
    $swal.error(
      "Terjadi kesalahan saat submit dan cetak faktur. Silakan coba lagi."
    );
  }
};

const downloadRetur = async () => await donwloadFakturPdf("retur");

const getResource = async () => {
  await shipping.getListRuteShipping(idCabang);
  await shipping.getListFakturShipping(
    idCabang,
    idRute,
    false,
    idArmada,
    idDriver,
    deliveringDate
  );
  const id_order_batch = router.query.id_order_batch;
  const id_sales_orders = router.query.id_sales_orders;
    await shipping.getListDetailFakturShipping(id_sales_order, id_order_batch, id_sales_orders);


  tableKey.value++;
  setFakturInfo();
};

// Computed properties untuk perhitungan rincian pembayaran dengan format yang benar

const subtotal = computed(() => {
  let total = 0;
  if (detailFaktur.value && detailFaktur.value.length > 0) {
    detailFaktur.value.forEach((product) => {
      total += calculateProductSubtotal(product, "picked");
    });
  }
  return formatCurrencyAuto(total);
});

const totalOrderSubtotal = computed(() => {
  let total = 0;
  if (detailFaktur.value && detailFaktur.value.length > 0) {
    detailFaktur.value.forEach((product) => {
      // Konversi semua picked ke level UOM1
      const kartonToUom1 =
        (product.karton_picked || 0) * (product.konversi_level3 || 1);
      const boxToUom1 =
        (product.box_picked || 0) * (product.konversi_level2 || 1);
      const piecesUom1 = product.pieces_picked || 0;

      // Total pieces setelah konversi
      const totalPieces = kartonToUom1 + boxToUom1 + piecesUom1;

      // Hitung subtotal (total pieces x harga jual per piece)
      total += totalPieces * (product.harga_jual || 0);
    });
  }
  return total;
});

const diskonNota = computed(() => {
  let totalDiscount = 0;

  if (detailFaktur.value && detailFaktur.value.length > 0) {
    const orderSubtotal = totalOrderSubtotal.value;

    detailFaktur.value.forEach((product) => {
      // Dapatkan status voucher untuk produk ini
      const voucherStatus = shipping.getVoucherStatusForProduct(
        product.id_produk
      );

      // Hitung diskon dengan fungsi yang sama seperti di halaman konfirmasi
      const discountResult = calculateProductDiscounts(
        product,
        voucherStatus,
        orderSubtotal,
        "picked"
      );
      totalDiscount += discountResult.totalDiskon;
    });
  }

  return formatCurrencyAuto(totalDiscount);
});

const pajak = computed(() => {
  let totalTax = 0;

  if (detailFaktur.value && detailFaktur.value.length > 0) {
    detailFaktur.value.forEach((product) => {
      const voucherStatus = shipping.getVoucherStatusForProduct(
        product.id_produk
      );

      const discountResult = calculateProductDiscounts(
        product,
        voucherStatus,
        totalOrderSubtotal.value,
        "picked"
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

const downloadFakturPdf2 = async (title) => {
  try {
    setFakturInfo();

    if (title === "retur") {
      try {
        const retur = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/distribusi/get-detail-faktur-retur/${id_sales_order}`
        );

        if (!Object.keys(retur.detail_faktur).length) {
          throw "Tidak ada faktur retur";
        }

        fakturInfo.value = retur.detail_faktur;
        const isRetur = true;
        await downloadPdf2(
          fakturInfo.value,
          detailFaktur.value,
          `faktur ${title} ${getDateNow()}`,
          isRetur
        );
      } catch (error) {
        $swal.error(error);
      }
    } else {
      // Faktur penjualan biasa
      const isRetur = false;
      await downloadPdf2(
        fakturInfo.value,
        detailFaktur.value,
        `faktur ${title} ${getDateNow()}`,
        isRetur
      );
    }
  } catch (error) {
    console.error("Error generating PDF:", error);
    $swal.error("Terjadi kesalahan saat mencetak faktur");
  }
};

onMounted(() => getResource());
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px-0">
    <Faktur
      v-show="false"
      :info="fakturInfo"
      :list="detailFaktur"
      :is-retur="isRetur"
      :title="pdfTitle" />
    <SlideRightX
      class=""
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true">
        <template #header>Detail Shipping Transaksi</template>
        <template #content>
          <div class="status-field-container-4-col tw-mb-5">
            <StatusBar
              :loading="shipping.listDetailFakturShipping.loading"
              label="Nomor Faktur :"
              :value="fakturInfo?.nomor_faktur || ''" />
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
            <StatusBar
              v-if="fakturInfo?.tempo_label"
              :loading="shipping.listDetailFakturShipping.loading"
              label="Terms :"
              :value="fakturInfo?.tempo_label || ''" />
          </div>
        </template>
      </Card>
      <Card :no-subheader="true" class="tw-mt-5">
        <template #header>Detail Produk Shipping</template>
        <template #content>
          <div class="tw-w-full">
            <Table
              :key="tableKey"
              classic
              :loading="shipping.listDetailFakturShipping.loading"
              :table-data="shipping.listDetailFakturShipping.detailFaktur || []"
              :columns="dataColumnsDetailShipping" />
          </div>
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
            <div class="tw-flex tw-flex-row tw-mt-3">
              <!-- <Button
                :trigger="downloadRetur"
                class="tw-bg-[#0d6efd] tw-text-white tw-mr-2"
                disabled
                variant="primary">
                <i class="mdi mdi-printer"></i>
                &nbsp;
                <p>Cetak Surat Retur</p>
              </Button> -->

              <!-- Tombol Submit Faktur -->
              <!-- <Button
                :trigger="updateStatusFaktur"
                class="tw-bg-[#198754] tw-text-white tw-px-4 tw-py-2 tw-rounded-lg tw-flex tw-items-center tw-mr-2">
                <i class="mdi mdi-check-circle"></i>
                &nbsp;
                <p>Submit Faktur</p>
              </Button> -->

              <!-- Tombol Cetak Faktur (tanpa submit) -->
              <!-- <Button
                :trigger="() => downloadFakturPdf2('penjualan')"
                :disabled="shipping.listDetailFakturShipping.loading"
                class="tw-bg-[#0d6efd] tw-text-white tw-px-4 tw-py-2 tw-rounded-lg tw-flex tw-items-center">
                <i class="mdi mdi-printer"></i>
                &nbsp;
                <p>Cetak Faktur (PDF)</p>
              </Button> -->

              <!-- Tombol Submit & Cetak -->
              <!-- <Button
                :trigger="() => submitAndPrintFaktur('penjualan')"
                :disabled="shipping.listDetailFakturShipping.loading"
                class="tw-bg-[#6c757d] tw-text-white tw-px-4 tw-py-2 tw-rounded-lg tw-flex tw-items-center tw-ml-2">
                <i class="mdi mdi-content-save-outline"></i>
                &nbsp;
                <p>Submit & Cetak</p>
              </Button> -->
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>

<style scoped>
.status-field-container-4-col {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
}
</style>
