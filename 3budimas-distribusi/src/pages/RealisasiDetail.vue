<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import Table from "../components/ui/table/Table.vue";
import StatusBar from "../components/ui/StatusBar.vue";
import Button from "../components/ui/Button.vue";
import {BFormCheckbox, BFormInput, BFormTextarea} from "bootstrap-vue-next";
import {tableRealisasiDetail} from "../model/tableColumns";
import {useShipping} from "../store/shipping";
import {useRoute, useRouter} from "vue-router";
import {useKepalaCabang} from "../store/kepalaCabang";
import {computed, inject, onMounted, ref, watch} from "vue";
import {useAlert} from "../store/alert";
import {
  apiUrl,
  calculateProductDiscounts,
  calculateProductSubtotal,
  fetchWithAuth,
  formatCurrencyAuto,
} from "../lib/utils";
import Modal from "../components/ui/Modal.vue";
import SelectInput from "../components/ui/formInput/SelectInput.vue";

const shipping = useShipping();
const kepalaCabang = useKepalaCabang();
const router = useRoute();
const tableKey = ref(0);
const fakturInfo = ref({});
const idCabang = kepalaCabang.kepalaCabangUser?.id_cabang || 0;
const localStore = ref([]);
const loadingProduk = ref(true);
const alert = useAlert();
const idSalesOrder = router.params.id_sales_order;
const id_rute = router.params.id_rute;
const keteranganOption = ref([{ text: "Pending" }, { text: "Batal" }]);
const selectedKeterangan = ref("");
const editModalBatal = ref(null);
const keteranganBatal = ref("");
const route = useRouter();
const produkBatal = ref([]);
const idArmada = router.query.id_armada;
const idDriver = router.query.id_driver;
const deliveringDate = router.query.delivering_date;
const $swal = inject("$swal");
const dataFaktur = ref({});
const isPembayaranViaDropper = ref(false);
const jumlahDiterima = ref(0);
const nama_user_base = kepalaCabang.kepalaCabangUser?.kepalaCabang?.nama || "";
const kode_rute = computed(() => fakturInfo.value?.kode || "tidak ada");
const nama_user = computed(() => `${kode_rute.value} - ${nama_user_base}`);

const change = ({ value, rowIndex, columnId }) => {
  localStore.value = localStore.value.map((val, idx) => {
    if (rowIndex === idx) {
      return {
        ...val,
        [columnId]: value,
      };
    }
    return { ...val };
  });
};

// Computed untuk kalkulasi real-time berdasarkan realisasi
const subtotalRealisasi = computed(() => {
  let total = 0;
  if (localStore.value && localStore.value.length > 0) {
    localStore.value.forEach((product) => {
      total += calculateProductSubtotal(product, "realisasi");
    });
  }
  return formatCurrencyAuto(total);
});

const totalOrderSubtotalRealisasi = computed(() => {
  let total = 0;
  if (localStore.value && localStore.value.length > 0) {
    localStore.value.forEach((product) => {
      total += calculateProductSubtotal(product, "realisasi");
    });
  }
  return total;
});

const diskonNotaRealisasi = computed(() => {
  let totalDiscount = 0;

  if (localStore.value && localStore.value.length > 0) {
    const orderSubtotal = totalOrderSubtotalRealisasi.value;

    localStore.value.forEach((product) => {
      const voucherStatus = shipping.getVoucherStatusForProduct(
        product.id_produk
      );

      const discountResult = calculateProductDiscounts(
        product,
        voucherStatus,
        orderSubtotal,
        "realisasi"
      );
      totalDiscount += discountResult.totalDiskon;
    });
  }

  return formatCurrencyAuto(totalDiscount);
});

const pajakRealisasi = computed(() => {
  let totalTax = 0;

  if (localStore.value && localStore.value.length > 0) {
    const orderSubtotal = totalOrderSubtotalRealisasi.value;

    localStore.value.forEach((product) => {
      const voucherStatus = shipping.getVoucherStatusForProduct(
        product.id_produk
      );

      const discountResult = calculateProductDiscounts(
        product,
        voucherStatus,
        orderSubtotal,
        "realisasi"
      );
      totalTax += discountResult.ppnValue;
    });
  }

  return formatCurrencyAuto(totalTax);
});

const totalPenjualanRealisasi = computed(() => {
  const subtotalNumeric =
    parseFloat(subtotalRealisasi.value.replace(/\./g, "").replace(/,/g, ".")) ||
    0;

  const diskonNumeric =
    parseFloat(
      diskonNotaRealisasi.value.replace(/\./g, "").replace(/,/g, ".")
    ) || 0;

  const pajakNumeric =
    parseFloat(pajakRealisasi.value.replace(/\./g, "").replace(/,/g, ".")) || 0;

  const total = subtotalNumeric - diskonNumeric + pajakNumeric;

  // Sinkronkan jumlah diterima dengan total penjualan secara default
  if (isPembayaranViaDropper.value) {
    jumlahDiterima.value = total;
  }

  return formatCurrencyAuto(total);
});

const onBlurBatalProduk = (val, index) => {
  const btl = localStore.value
    .map((value, idx) => {
      if (idx === index) {
        return {
          id_produk: value.id_produk,
          jumlah_kembali_ke_gudang: parseInt(val.target.value),
        };
      }
    })
    .filter((val) => val !== undefined);

  const prod = produkBatal.value.concat(btl);
  produkBatal.value = prod;
};

const submitPicked = async () => {
  try {
    const filterPicked = localStore.value
      .filter((val) => val.realisasi)
      .map((val) => ({
        realisasi: val.realisasi,
        id_detail_sales: val.id_order_detail,
        id_faktur: dataFaktur.value?.id_faktur || 0,
        id_produk: val.id_produk,
        konversi1: val.konversi_level1,
        konversi2: val.konversi_level2,
        konversi3: val.konversi_level3,
      }));

    if (!filterPicked.length) throw "Semua field jumlah realisasi kosong !!!";

    const isConfirm = await $swal.confirmSubmit();
    if (!isConfirm) return;

    const requestBody = {
      realisasi: filterPicked,
      id_cabang: idCabang,
      id_sales_order: Number(idSalesOrder),
      id_order_batch: router.query?.id_order_batch
        ? Number(router.query.id_order_batch)
        : null,
      nama_user: nama_user.value,
      no_faktur: dataFaktur.value?.no_faktur || "",
    };

    // Tambahkan pembayaran via dropper jika toggle aktif
    if (isPembayaranViaDropper.value) {
      const totalRealisasiNumeric =
        parseFloat(
          totalPenjualanRealisasi.value.replace(/\./g, "").replace(/,/g, ".")
        ) || 0;
      // Fix: jumlahDiterima sudah number, tidak perlu replace
      const jumlahDiterimaNumeric = Number(jumlahDiterima.value) || 0;

      if (jumlahDiterimaNumeric > totalRealisasiNumeric) {
        throw "Jumlah yang diterima tidak boleh lebih besar dari total pembayaran";
      }
      requestBody.pembayaran_via_dropper = jumlahDiterimaNumeric;
      requestBody.jumlah_harus_dibayarkan = totalRealisasiNumeric;
    }

    const res = await fetchWithAuth(
      "POST",
      `${apiUrl}/api/distribusi/submit-realisasi-detail`,
      requestBody
    );

    await shipping.getListFakturShipping(
      idCabang,
      id_rute,
      true,
      idArmada,
      idDriver,
      deliveringDate
    );

    $swal.success(res.message || "Berhasil mengirim realisasi detail");
    route.back();
  } catch (error) {
    $swal.error(error || "Gagal mengirim realisasi detail");
    console.log(error);
  }
};

const kirimKeteranganBatal = async () => {
  const id_faktur = dataFaktur.value?.id_faktur || 0;
  const status_faktur =
    selectedKeterangan.value === "Pending"
      ? 1
      : selectedKeterangan.value === "Batal"
      ? 7
      : null;
  const checkField =
    keteranganBatal.value.length &&
    selectedKeterangan.value &&
    produkBatal.value.every((val) => {
      if (val?.hasOwnProperty("jumlah_kembali_ke_gudang")) {
        return val.jumlah_kembali_ke_gudang > 0;
      }
    });

  const body = {
    id_faktur,
    keterangan_batal: keteranganBatal.value,
    status_faktur,
    produk: produkBatal.value,
  };

  try {
    if (!checkField) {
      editModalBatal.value.hide();
      throw "Tidak boleh field ada yang kosong";
    }

    await fetchWithAuth(
      "POST",
      `${apiUrl}/api/distribusi/batal-realisasi`,
      body
    );

    $swal.success("Berhasil menggagalkan faktur");
    route.back();
  } catch (error) {
    $swal.error(error || "Gagal menggagalkan faktur");
    console.log(error);
  }
};

const getResource = async () => {
  fakturInfo.value = shipping.listRuteShipping?.ruteShipping?.find(
    (val) => val.id_rute == router.params.id_rute
  );

  await shipping.getListDetailFakturShipping(idSalesOrder, router.query?.id_order_batch,router.query?.id_sales_order );

  const allFaktur = shipping.listFakturShipping.fakturShipping || [];

  // Ambil data faktur dari detail faktur shipping
  dataFaktur.value = shipping.listDetailFakturShipping?.detailFakturInfo || {};

  // Map data dari list_detail_order ke format yang dibutuhkan tabel
  const detailOrder = shipping.listDetailFakturShipping?.detailFaktur || [];
  localStore.value = detailOrder.map((item) => ({
    ...item,
    // Mapping field untuk kompatibilitas
    nama_produk: item.nama_produk,
    produk_id: item.id_produk,
    id_detail_sales_array: item.id_order_detail,
    jumlah_picked:
      (item.karton_picked || 0) * (item.konversi_level3 || 1) +
      (item.box_picked || 0) * (item.konversi_level2 || 1) +
      (item.pieces_picked || 0),
    // Default realisasi dari shipped
    realisasi:
      (item.karton_shipped || 0) * (item.konversi_level3 || 1) +
      (item.box_shipped || 0) * (item.konversi_level2 || 1) +
      (item.pieces_shipped || 0),
    // Data untuk UnitConversionInput
    total_karton: item.karton_shipped || 0,
    total_box: item.box_shipped || 0,
    total_pieces: item.pieces_shipped || 0,
    konversi1: item.konversi_level1,
    konversi2: item.konversi_level2,
    konversi3: item.konversi_level3,
  }));

  tableKey.value++;
  loadingProduk.value = false;
};
const jadwalkanUlang = async () => {
  try {
    const isConfirm = await $swal.confirmSubmit(
      "Apakah anda yakin ingin menjadwalkan ulang faktur ini ?"
    );
    if (!isConfirm) return;
    const body = {
      id_sales_order: [Number(idSalesOrder)]
    }
    if (router.query?.id_order_batch) {
      body.id_sales_order = router.query?.id_sales_order.split(',').map(id => Number(id));
    }
    const res = await fetchWithAuth(
      "POST",
      `${apiUrl}/api/distribusi/jadwalkan-ulang-faktur`,
      body
    );
    $swal.success(res.message || "Berhasil menjadwalkan ulang faktur");
    route.back();
  } catch (error) {
    $swal.error(error || "Gagal menjadwalkan ulang faktur");
  }
};

watch(isPembayaranViaDropper, (newValue) => {
  if (newValue) {
    // Ketika toggle diaktifkan, set jumlah diterima sama dengan total penjualan
    const totalNumeric =
      parseFloat(
        totalPenjualanRealisasi.value.replace(/\./g, "").replace(/,/g, ".")
      ) || 0;
    jumlahDiterima.value = totalNumeric;
  } else {
    // Ketika toggle dinonaktifkan, reset ke 0
    jumlahDiterima.value = 0;
  }
});

onMounted(() => {
  getResource();
});
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px-0">
    <SlideRightX
      class=""
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true">
        <template #header>Daftar Faktur</template>
        <template #content>
          <div class="status-field-container-4-col tw-mb-5">
            <StatusBar
              label="Cabang :"
              :value="
                kepalaCabang.kepalaCabangUser?.kepalaCabang?.nama_cabang || ''
              " />
            <StatusBar label="Rute :" :value="fakturInfo?.nama_rute || ''" />
            <StatusBar
              label="Armada :"
              :value="fakturInfo?.nama_armada || ''" />
            <StatusBar
              label="Driver :"
              :value="fakturInfo?.nama_driver || ''" />
          </div>
          <div class="status-field-container-4-col tw-mb-5">
            <StatusBar
              label="No Faktur :"
              :value="dataFaktur?.no_faktur || ''" />
            <StatusBar
              label="Total Penjualan :"
              :value="formatCurrencyAuto(dataFaktur?.total_penjualan) || ''" />
            <StatusBar
              label="Nama Customer :"
              :value="dataFaktur?.nama_customer || ''" />
          </div>
        </template>
      </Card>
      <Card :no-subheader="true" class="tw-mt-10">
        <template #header>List Faktur</template>
        <template #content>
          <div class="tw-w-full tw-pb-10">
            <Table
              :key="tableKey"
              :loading="loadingProduk"
              :table-data="localStore"
              :columns="tableRealisasiDetail"
              @change="change" />

            <!-- Pembayaran via Dropper Section -->
            <div
              class="tw-w-fit tw-flex tw-mx-3 tw-items-center tw-gap-4 tw-mt-6 tw-mb-4 tw-p-4 tw-border tw-rounded-md"
              :class="
                isPembayaranViaDropper
                  ? 'tw-border-green-400 tw-bg-green-50'
                  : 'tw-border-gray-300 tw-bg-gray-50'
              ">
              <div
                class="tw-flex tw-flex-col tw-items-center tw-border-r-2 tw-pr-4"
                :class="
                  isPembayaranViaDropper
                    ? 'tw-border-green-300'
                    : 'tw-border-slate-300'
                ">
                <BFormCheckbox
                  v-model="isPembayaranViaDropper"
                  switch
                  size="lg"
                  class="tw-scale-125" />
                <span class="tw-text-xs tw-font-medium tw-mt-2">
                  Pembayaran COD
                </span>
              </div>

              <div class="tw-flex tw-gap-4">
                <!-- Pembayaran yang harus dibayar -->
                <div class="tw-flex tw-flex-col">
                  <label
                    class="tw-text-sm tw-font-semibold tw-mb-2 tw-block"
                    :class="
                      isPembayaranViaDropper
                        ? 'tw-text-green-700'
                        : 'tw-text-gray-600'
                    ">
                    Jumlah yang harus dibayar
                  </label>
                  <BFormInput
                    :disabled="true"
                    :value="totalPenjualanRealisasi"
                    class="tw-w-48"
                    :class="
                      isPembayaranViaDropper
                        ? 'tw-bg-green-100 tw-border-green-300 tw-text-green-800'
                        : 'tw-bg-gray-100 tw-border-gray-300 tw-text-gray-500'
                    "
                    placeholder="Rp 0" />
                </div>

                <!-- Jumlah yang diterima -->
                <div class="tw-flex tw-flex-col">
                  <label
                    class="tw-text-sm tw-font-semibold tw-mb-2 tw-block"
                    :class="
                      isPembayaranViaDropper
                        ? 'tw-text-green-700'
                        : 'tw-text-gray-600'
                    ">
                    Jumlah yang diterima
                  </label>
                  <BFormInput
                    v-model="jumlahDiterima"
                    :disabled="!isPembayaranViaDropper"
                    type="number"
                    class="tw-w-48"
                    :class="
                      isPembayaranViaDropper
                        ? 'tw-bg-white tw-border-green-300 tw-text-green-800'
                        : 'tw-bg-gray-100 tw-border-gray-300 tw-text-gray-500'
                    "
                    placeholder="0" />
                </div>
              </div>
            </div>

            <div
              class="tw-w-full tw-flex tw-flex-col md:tw-flex-row md:tw-justify-end tw-gap-2 tw-px-2">
              <Button
                :trigger="jadwalkanUlang"
                icon="mdi mdi-repeat"
                class="md:tw-w-44 tw-h-9">
                Jadwalkan Ulang
              </Button>
              <Button
                :trigger="() => editModalBatal.show()"
                icon="mdi mdi-block-helper"
                class="tw-bg-red-500 md:tw-w-44 tw-h-9">
                Batalkan Faktur
              </Button>
              <Button
                :trigger="submitPicked"
                icon="mdi mdi-check"
                class="tw-bg-green-500 md:tw-w-24 tw-h-9">
                Submit
              </Button>
            </div>
          </div>
        </template>
      </Card>
      <Modal
        id="editModalBatal"
        ref="editModalBatal"
        centered
        @modal-closed="editModalBatal.hide()">
        <Card dense no-subheader no-main-center class="tw-p-4">
          <template #header>
            <span class="tw-text-black">Alasan Batal</span>
          </template>
          <template #content>
            <FlexBox full class="tw-w-full">
              <BForm novalidate class="tw-w-full tw-flex tw-flex-col tw-gap-6">
                <div class="tw-w-full tw-flex tw-flex-col tw-gap-2">
                  <span class="tw-text-sm tw-font-semibold">Pilih Status</span>
                  <SelectInput
                    placeholder="Status"
                    size="md"
                    value-field="text"
                    class="tw-z-50"
                    :options="keteranganOption"
                    v-model="selectedKeterangan" />
                  <BFormTextarea
                    id="textarea"
                    v-model="keteranganBatal"
                    placeholder="Masukkan Alasan"
                    rows="8" />
                  <div
                    class="tw-w-full tw-flex tw-flex-col tw-gap-6 tw-mt-3 tw-border tw-border-gray-300 tw-rounded-md tw-px-4 tw-py-3 tw-shadow-md">
                    <div class="tw-w-[65%] tw-flex tw-flex-col">
                      <span class="tw-text-lg tw-font-bold">Input Jumlah</span>
                      <span class="tw-text-[0.65rem]">
                        Inputkan jumlah produk yang ingin di kembalikan ke
                        gudang
                      </span>
                    </div>
                    <div class="tw-flex tw-flex-col tw-gap-2">
                      <div
                        v-for="(val, index) in localStore"
                        :key="val.produk_id"
                        class="tw-w-full tw-flex tw-flex-col tw-gap-1">
                        <span class="tw-text-xs tw-font-semibold">
                          {{ val.nama_produk }}
                        </span>
                        <BFormInput
                          @blur="(val) => onBlurBatalProduk(val, index)"
                          placeholder="Masukkan jumlah kembali ke gudang"
                          type="number" />
                      </div>
                    </div>
                  </div>
                </div>
                <FlexBox full>
                  <Button
                    :trigger="kirimKeteranganBatal"
                    class="tw-bg-green-500 tw-w-24 tw-h-8">
                    Kirim
                  </Button>
                </FlexBox>
              </BForm>
            </FlexBox>
          </template>
        </Card>
      </Modal>
    </SlideRightX>
  </div>
</template>
