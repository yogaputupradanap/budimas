<!-- eslint-disable vue/multi-word-component-names -->
<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import { onMounted, reactive, ref, computed } from "vue";
import { useModal } from "bootstrap-vue-next";
import Loader from "../components/ui/Loader.vue";
import { useVoucher } from "../store/voucher";
import { parseCurrency } from "../lib/utils";
import { usePrincipal } from "../store/principal";
import Button from "../components/ui/Button.vue";
import { useAlert } from "../store/alert";
import { useKunjungan } from "../store/kunjungan";
import { useSales } from "../store/sales";

const { show, hide } = useModal("detail-voucher");
const vouchers = useVoucher();
const principal = usePrincipal();
const alert = useAlert();
const kunjungan = useKunjungan();
const sales = useSales();
const voucherCategory = ref("");
const voucherDetail = reactive({
  nama_voucher: "",
  persentase_diskon_1: 0,
  persentase_diskon_2: 0,
  persentase_diskon_3: 0,
  minimal_total_pembelian: 0,
  minimal_subtotal_pembelian: 0,
  budget_diskon: "",
  tanggal_mulai: "",
  tanggal_kadaluarsa: "",
  promo: "",
  syarat_ketentuan: "",
  kode_voucher: "",
  is_reguler: null,
  produk_names: [],
  cabang_names: [],
  customer_names: [],
  nominal_diskon: 0,
  tipe_voucher: null,
  minimal_jumlah_produk: 0,
  level_uom: null,
});

// Filter
const selectedPrincipalId = ref(null);
const filterLoading = ref(false);
const filteredVouchers = ref([]);
const selectedVoucherType = ref(null);

const voucherTypes = [
  { value: "v1r", text: "Voucher Reguler 1" },
  { value: "v2r", text: "Voucher Reguler 2" },
  { value: "v3r", text: "Voucher Reguler 3" },
  { value: "v2p", text: "Voucher Produk 2" },
  { value: "v3p", text: "Voucher Produk 3" },
];

const showDetail = (index) => {
  // Reset detail terlebih dahulu
  Object.keys(voucherDetail).forEach((key) => {
    voucherDetail[key] = Array.isArray(voucherDetail[key]) ? [] : "";
  });

  // Set nilai-nilai dari voucher yang dipilih
  const selectedVoucher = filteredVouchers.value[index];
  const voucherType = selectedVoucher["kode_voucher"].split("-");
  voucherCategory.value = voucherType[voucherType.length - 1];

  // Copy semua properti voucher ke voucherDetail
  Object.keys(selectedVoucher).forEach((key) => {
    if (key in voucherDetail) {
      voucherDetail[key] = selectedVoucher[key];
    }
  });

  // Pastikan properti yang mungkin tidak ada di voucher tertentu tetap ada dengan nilai default
  voucherDetail.persentase_diskon_1 = selectedVoucher.persentase_diskon_1 || 0;
  voucherDetail.persentase_diskon_2 = selectedVoucher.persentase_diskon_2 || 0;
  voucherDetail.persentase_diskon_3 = selectedVoucher.persentase_diskon_3 || 0;
  voucherDetail.minimal_total_pembelian =
    selectedVoucher.minimal_total_pembelian || 0;
  voucherDetail.minimal_subtotal_pembelian =
    selectedVoucher.minimal_subtotal_pembelian || 0;
  voucherDetail.budget_diskon = selectedVoucher.budget_diskon || "";
  voucherDetail.nominal_diskon = selectedVoucher.nominal_diskon || 0;
  voucherDetail.produk_names = selectedVoucher.produk_names || [];
  voucherDetail.cabang_names = selectedVoucher.cabang_names || [];
  voucherDetail.customer_names = selectedVoucher.customer_names || [];
  voucherDetail.tipe_voucher = selectedVoucher.tipe_voucher || null;
  voucherDetail.minimal_jumlah_produk =
    selectedVoucher.minimal_jumlah_produk || 0;
  voucherDetail.level_uom = selectedVoucher.level_uom || null;

  show();
};

const filterVouchers = async () => {
  // Cek apakah principal sudah dipilih
  if (!selectedPrincipalId.value) {
    alert.setMessage("Silakan pilih Principal terlebih dahulu", "warning");
    return;
  }
  // Cek apakah jenis voucher sudah dipilih
  if (!selectedVoucherType.value) {
    alert.setMessage("Silakan pilih Jenis Voucher terlebih dahulu", "warning");
    return;
  }

  filterLoading.value = true;

  try {
    switch (selectedVoucherType.value) {
      case "v1r":
        if (!vouchers.voucher1RegularList.length) {
          await vouchers.getVoucher1Regular();
        }
        filteredVouchers.value = vouchers.voucher1RegularList.filter(
          (v) => v.id_principal == selectedPrincipalId.value
        );
        break;

      case "v2r":
        if (!vouchers.voucher2RegularList.length) {
          await vouchers.getVoucher2Regular();
        }
        filteredVouchers.value = vouchers.voucher2RegularList.filter(
          (v) => v.id_principal == selectedPrincipalId.value
        );
        break;

      case "v3r":
        if (!vouchers.voucher3RegularList.length) {
          await vouchers.getVoucher3Regular();
        }
        filteredVouchers.value = vouchers.voucher3RegularList.filter(
          (v) => v.id_principal == selectedPrincipalId.value
        );
        break;

      case "v2p":
        const v2p = await vouchers.getVoucher2ProductAll();
        filteredVouchers.value = v2p.filter((v) => {
          const principalMatch = v.id_principal == selectedPrincipalId.value;

          const cabangMatch =
            !v.cabang_ids ||
            v.cabang_ids.length === 0 ||
            (sales.salesUser?.id_cabang &&
              v.cabang_ids.includes(sales.salesUser.id_cabang));

          return principalMatch && cabangMatch;
        });
        break;

      case "v3p":
        const v3p = await vouchers.getVoucher3ProductAll();
        filteredVouchers.value = v3p.filter((v) => {
          const principalMatch = v.id_principal == selectedPrincipalId.value;

          const customerMatch =
            !v.customer_ids ||
            v.customer_ids.length === 0 ||
            (kunjungan.activeKunjungan?.kunjungan?.customer_id &&
              v.customer_ids.includes(
                kunjungan.activeKunjungan.kunjungan.customer_id
              ));

          const cabangMatch =
            !v.cabang_ids ||
            v.cabang_ids.length === 0 ||
            (sales.salesUser?.id_cabang &&
              v.cabang_ids.includes(sales.salesUser.id_cabang));

          return principalMatch && customerMatch && cabangMatch;
        });
        break;
    }
  } catch (error) {
    console.error("Error filtering vouchers:", error);
    filteredVouchers.value = [];
  } finally {
    filterLoading.value = false;
  }
};

// Mendapatkan warna latar belakang berdasarkan tipe voucher
const getVoucherBgClass = (voucherCode) => {
  const voucherType = voucherCode.split("-").pop();
  if (voucherType === "1") return "from-blue-600 to-blue-800";
  if (voucherType === "2") return "from-purple-600 to-purple-800";
  if (voucherType === "3") return "from-green-600 to-green-800";
  return "from-indigo-600 to-indigo-800";
};

const openImage = (imageUrl) => {
  window.open(
    `https://storage.googleapis.com/buktitransaksi/${imageUrl}`,
    "_blank"
  );
};

onMounted(async () => {
  if (!principal.principals.length) {
    await principal.getPrincipals();
  }
});
</script>

<template>
  <div class="tw-w-full tw-flex tw-flex-col md:tw-pl-6 tw-pl-0">
    <!-- Section Filter -->
    <SlideRightX
      class="tw-w-full"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card no-subheader>
        <template #header>Filter Voucher</template>
        <template #content>
          <div class="tw-p-4">
            <div class="tw-grid tw-grid-cols-1 md:tw-grid-cols-3 tw-gap-4">
              <!-- Filter Principal -->
              <div>
                <label
                  class="tw-block tw-text-sm tw-font-medium tw-mb-2 tw-text-gray-700">
                  <i class="mdi mdi-domain tw-mr-1"></i>
                  Principal
                </label>
                <BFormSelect
                  v-model="selectedPrincipalId"
                  :options="[
                    { value: null, text: 'Pilih Principal', disabled: true },
                    ...principal.principals.map((p) => ({
                      value: p.id,
                      text: p.nama,
                    })),
                  ]"
                  class="tw-w-full tw-rounded tw-shadow-sm" />
              </div>

              <!-- Filter Jenis Voucher -->
              <div>
                <label
                  class="tw-block tw-text-sm tw-font-medium tw-mb-2 tw-text-gray-700">
                  <i class="mdi mdi-tag-multiple tw-mr-1"></i>
                  Jenis Voucher
                </label>
                <BFormSelect
                  v-model="selectedVoucherType"
                  :options="[
                    {
                      value: null,
                      text: 'Pilih Jenis Voucher',
                      disabled: true,
                    },
                    ...voucherTypes,
                  ]"
                  class="tw-w-full tw-rounded tw-shadow-sm" />
              </div>

              <!-- Button Filter -->
              <div class="tw-flex tw-items-end">
                <BButton
                  @click="filterVouchers"
                  variant="primary"
                  class="tw-bg-blue-600 hover:tw-bg-blue-700 tw-border-none tw-px-6 tw-py-2 tw-w-full tw-shadow-md"
                  :disabled="filterLoading">
                  <BSpinner
                    small
                    v-if="filterLoading"
                    class="tw-mr-2"></BSpinner>
                  <i class="mdi mdi-filter-variant tw-mr-2" v-else></i>
                  Filter Voucher
                </BButton>
              </div>
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>

    <!-- Section Voucher List -->
    <SlideRightX
      class="tw-w-full tw-mt-6"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card no-subheader>
        <template #header>
          <div
            class="tw-w-full tw-flex tw-justify-between tw-items-center tw-gap-4">
            <span>Daftar Voucher</span>
            <span
              class="tw-text-sm tw-bg-blue-100 tw-text-blue-700 tw-px-3 tw-py-1 tw-rounded-full">
              {{ filteredVouchers.length }} Voucher Tersedia
            </span>
          </div>
        </template>
        <template #content>
          <!-- Loading State -->
          <div
            v-if="filterLoading"
            class="tw-w-full tw-h-[400px] tw-flex tw-justify-center tw-items-center">
            <Loader />
          </div>

          <!-- Empty State -->
          <div
            v-else-if="filteredVouchers.length === 0"
            class="tw-w-full tw-h-[400px] tw-flex tw-flex-col tw-justify-center tw-items-center">
            <div class="tw-text-center">
              <div
                class="tw-bg-gray-100 tw-rounded-full tw-p-4 tw-inline-block">
                <i
                  class="mdi mdi-ticket-confirmation-outline tw-text-5xl tw-text-gray-500"></i>
              </div>
              <p class="tw-mt-4 tw-text-lg tw-font-medium tw-text-gray-700">
                {{
                  selectedPrincipalId
                    ? "Tidak ada voucher tersedia"
                    : "Silakan pilih Principal dan filter untuk melihat voucher"
                }}
              </p>
              <p class="tw-text-gray-500">
                {{
                  selectedPrincipalId
                    ? "Silakan coba filter dengan kriteria yang berbeda"
                    : "Gunakan filter di atas untuk menampilkan voucher"
                }}
              </p>
            </div>
          </div>

          <!-- Voucher List -->
          <div v-else class="tw-p-4 tw-pb-6">
            <div
              class="tw-max-w-5xl tw-mx-auto tw-grid tw-grid-cols-1 md:tw-grid-cols-2 lg:tw-grid-cols-3 tw-gap-6">
              <!-- Voucher Card -->
              <div
                v-for="(voucher, index) in filteredVouchers"
                :key="voucher.id"
                class="tw-bg-white tw-rounded-xl tw-overflow-hidden tw-shadow-md tw-transition-all tw-duration-300 hover:tw-shadow-xl hover:-tw-translate-y-1 tw-relative">
                <!-- Image Section -->
                <div class="tw-relative tw-w-full tw-h-48 tw-overflow-hidden">
                  <!-- Voucher Image or SVG Placeholder -->
                  <div v-if="voucher.pic_voucher" class="tw-w-full tw-h-full">
                    <BImg
                      :src="`https://storage.googleapis.com/buktitransaksi/${voucher.pic_voucher}`"
                      class="tw-w-full tw-h-full tw-object-cover" />
                  </div>
                  <!-- SVG Placeholder if no image -->
                  <div
                    v-else
                    :class="[
                      'tw-w-full tw-h-full tw-flex tw-justify-center tw-items-center tw-bg-gradient-to-br',
                      getVoucherBgClass(voucher.kode_voucher),
                    ]">
                    <!-- SVG for v1r Vouchers -->
                    <svg
                      v-if="voucher.tipe_voucher === 1"
                      xmlns="http://www.w3.org/2000/svg"
                      width="120"
                      height="120"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="1"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      class="tw-text-white tw-opacity-30">
                      <circle cx="12" cy="12" r="10"></circle>
                      <path d="M12 8v8"></path>
                      <path d="M8 12h8"></path>
                    </svg>

                    <!-- SVG for v2r Vouchers -->
                    <svg
                      v-else-if="
                        voucher.tipe_voucher === 2 && voucher.is_reguler === 1
                      "
                      xmlns="http://www.w3.org/2000/svg"
                      width="120"
                      height="120"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="1"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      class="tw-text-white tw-opacity-30">
                      <rect
                        x="3"
                        y="3"
                        width="18"
                        height="18"
                        rx="2"
                        ry="2"></rect>
                      <line x1="3" y1="9" x2="21" y2="9"></line>
                      <line x1="9" y1="21" x2="9" y2="9"></line>
                    </svg>

                    <!-- SVG for v3r Vouchers -->
                    <svg
                      v-else-if="
                        voucher.tipe_voucher === 3 && voucher.is_reguler === 1
                      "
                      xmlns="http://www.w3.org/2000/svg"
                      width="120"
                      height="120"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="1"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      class="tw-text-white tw-opacity-30">
                      <polygon
                        points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                    </svg>

                    <!-- SVG for v2p Vouchers -->
                    <svg
                      v-else-if="
                        voucher.tipe_voucher === 2 && voucher.is_reguler !== 1
                      "
                      xmlns="http://www.w3.org/2000/svg"
                      width="120"
                      height="120"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="1"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      class="tw-text-white tw-opacity-30">
                      <path
                        d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                      <polyline points="3.29 7 12 12 20.71 7"></polyline>
                      <line x1="12" y1="22" x2="12" y2="12"></line>
                    </svg>

                    <!-- SVG for v3p Vouchers -->
                    <svg
                      v-else-if="
                        voucher.tipe_voucher === 3 && voucher.is_reguler !== 1
                      "
                      xmlns="http://www.w3.org/2000/svg"
                      width="120"
                      height="120"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="1"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      class="tw-text-white tw-opacity-30">
                      <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                    </svg>

                    <!-- Default SVG for other cases -->
                    <svg
                      v-else
                      xmlns="http://www.w3.org/2000/svg"
                      width="120"
                      height="120"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="1"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      class="tw-text-white tw-opacity-30">
                      <path d="M3 10h18M6 14h12M10 18h4M8 6h8"></path>
                      <rect
                        x="3"
                        y="4"
                        width="18"
                        height="16"
                        rx="2"
                        ry="2"></rect>
                      <path d="M12 4v16"></path>
                    </svg>
                  </div>
                  <!-- Hover Overlay -->
                  <div
                    class="tw-absolute tw-inset-0 tw-bg-black tw-bg-opacity-0 hover:tw-bg-opacity-60 tw-transition-all tw-duration-300 tw-flex tw-justify-center tw-items-center tw-gap-2 tw-opacity-0 hover:tw-opacity-100">
                    <Button
                      v-if="voucher.pic_voucher"
                      class="tw-bg-white tw-text-gray-800 tw-px-4 tw-py-2"
                      :trigger="() => openImage(voucher.pic_voucher)">
                      <i class="mdi mdi-image-search tw-mr-1"></i>
                      Lihat Gambar
                    </Button>
                  </div>
                </div>

                <!-- Image Modal -->
                <BModal
                  :id="`view-image-${voucher.id}`"
                  centered
                  hide-footer
                  title="Voucher Image">
                  <div class="tw-w-full">
                    <BImg
                      v-if="voucher.pic_voucher"
                      :src="`https://storage.googleapis.com/buktitransaksi/${voucher.pic_voucher}`"
                      class="tw-w-full tw-rounded-md"
                      fluid />
                  </div>
                </BModal>

                <!-- Content Section -->
                <div class="tw-p-4">
                  <!-- Kode Voucher -->
                  <div
                    class="tw-flex tw-justify-between tw-items-center tw-mb-2 tw-gap-2">
                    <span
                      class="tw-text-xs tw-font-mono tw-bg-gray-100 tw-px-2 tw-py-1 tw-rounded-md tw-text-gray-600">
                      {{ voucher.kode_voucher }}
                    </span>
                    <div
                      class="tw-flex tw-items-center tw-text-gray-500 tw-text-xs">
                      <i class="mdi mdi-calendar tw-mr-1"></i>
                      {{
                        voucher.tanggal_mulai
                          ? `${voucher.tanggal_mulai
                              .split("-")
                              .reverse()
                              .join("/")} - ${
                              voucher.tanggal_kadaluarsa
                                ? voucher.tanggal_kadaluarsa
                                    .split("-")
                                    .reverse()
                                    .join("/")
                                : "∞"
                            }`
                          : "Tanggal tidak ditentukan"
                      }}
                    </div>
                  </div>

                  <!-- Voucher Name -->
                  <h3
                    class="tw-font-bold tw-text-gray-800 tw-mb-3 tw-text-xl tw-line-clamp-2">
                    {{ voucher.nama_voucher }}
                  </h3>

                  <!-- Divider -->
                  <div class="tw-w-full tw-h-px tw-bg-gray-100 tw-my-3"></div>

                  <!-- Discount Info -->
                  <div class="tw-mb-4">
                    <div class="tw-flex tw-gap-2">
                      <div
                        v-if="voucher.persentase_diskon_1"
                        :class="[
                          'tw-rounded-lg tw-p-2 tw-flex tw-items-center tw-gap-2 tw-w-full',
                          voucher.kode_voucher.split('-').pop() === '1'
                            ? 'tw-bg-blue-50'
                            : voucher.kode_voucher.split('-').pop() === '2'
                            ? 'tw-bg-purple-50'
                            : 'tw-bg-green-50',
                        ]">
                        <i
                          :class="[
                            'mdi mdi-percent-circle-outline tw-text-lg',
                            voucher.kode_voucher.split('-').pop() === '1'
                              ? 'tw-text-blue-600'
                              : voucher.kode_voucher.split('-').pop() === '2'
                              ? 'tw-text-purple-600'
                              : 'tw-text-green-600',
                          ]"></i>
                        <div>
                          <div class="tw-text-xs tw-text-gray-500">
                            Diskon 1
                          </div>
                          <div class="tw-font-bold">
                            {{ voucher.persentase_diskon_1 }}%
                          </div>
                        </div>
                      </div>

                      <div
                        v-if="voucher.persentase_diskon_2"
                        :class="[
                          'tw-rounded-lg tw-p-2 tw-flex tw-items-center tw-gap-2 tw-w-full',
                          voucher.kode_voucher.split('-').pop() === '1'
                            ? 'tw-bg-blue-50'
                            : voucher.kode_voucher.split('-').pop() === '2'
                            ? 'tw-bg-purple-50'
                            : 'tw-bg-green-50',
                        ]">
                        <i
                          :class="[
                            'mdi mdi-percent-circle-outline tw-text-lg',
                            voucher.kode_voucher.split('-').pop() === '1'
                              ? 'tw-text-blue-600'
                              : voucher.kode_voucher.split('-').pop() === '2'
                              ? 'tw-text-purple-600'
                              : 'tw-text-green-600',
                          ]"></i>
                        <div>
                          <div class="tw-text-xs tw-text-gray-500">
                            Diskon 2
                          </div>
                          <div class="tw-font-bold">
                            {{ voucher.persentase_diskon_2 }}%
                          </div>
                        </div>
                      </div>

                      <div
                        v-if="voucher.persentase_diskon_3"
                        :class="[
                          'tw-rounded-lg tw-p-2 tw-flex tw-items-center tw-gap-2 tw-w-full',
                          voucher.kode_voucher.split('-').pop() === '1'
                            ? 'tw-bg-blue-50'
                            : voucher.kode_voucher.split('-').pop() === '2'
                            ? 'tw-bg-purple-50'
                            : 'tw-bg-green-50',
                        ]">
                        <i
                          :class="[
                            'mdi mdi-percent-circle-outline tw-text-lg',
                            voucher.kode_voucher.split('-').pop() === '1'
                              ? 'tw-text-blue-600'
                              : voucher.kode_voucher.split('-').pop() === '2'
                              ? 'tw-text-purple-600'
                              : 'tw-text-green-600',
                          ]"></i>
                        <div>
                          <div class="tw-text-xs tw-text-gray-500">
                            Diskon 3
                          </div>
                          <div class="tw-font-bold">
                            {{ voucher.persentase_diskon_3 }}%
                          </div>
                        </div>
                      </div>

                      <div
                        v-if="voucher.nominal_diskon"
                        class="tw-bg-green-50 tw-rounded-lg tw-p-2 tw-flex tw-items-center tw-gap-2 tw-w-full">
                        <i
                          class="mdi mdi-cash tw-text-lg tw-text-green-600"></i>
                        <div>
                          <div class="tw-text-xs tw-text-gray-500">Nilai</div>
                          <div class="tw-font-bold">
                            Rp {{ parseCurrency(voucher.nominal_diskon) }} / UOM
                            1
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Footer -->
                  <div
                    class="tw-flex tw-justify-between tw-items-center tw-mt-2">
                    <div class="tw-flex tw-flex-col tw-gap-2">
                      <div
                        v-if="voucher.minimal_subtotal_pembelian"
                        class="tw-flex tw-items-center tw-text-xs tw-text-amber-700 tw-bg-amber-50 tw-px-2 tw-py-1 tw-rounded-md">
                        <i class="mdi mdi-cash-multiple tw-mr-1"></i>
                        Min: Rp
                        {{ parseCurrency(voucher.minimal_subtotal_pembelian) }}
                      </div>
                      <div
                        v-if="
                          voucher.produk_names && voucher.produk_names.length
                        "
                        class="tw-flex tw-items-center tw-text-xs tw-text-indigo-700 tw-bg-indigo-50 tw-px-2 tw-py-1 tw-rounded-md">
                        <i class="mdi mdi-cube-outline tw-mr-1"></i>
                        {{ voucher.produk_names.length }} Produk
                      </div>
                    </div>

                    <Button
                      :trigger="() => showDetail(index)"
                      size="sm"
                      class="tw-px-4 tw-py-2 tw-self-end">
                      <i class="mdi mdi-information-outline tw-mr-1"></i>
                      Detail
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <!-- Modal Detail Voucher -->
      <BModal
        centered
        id="detail-voucher"
        hide-footer
        hide-header
        size="lg"
        content-class="tw-rounded-xl tw-overflow-hidden">
        <Card no-subheader no-main-center>
          <template #header>
            <div class="tw-flex tw-justify-between tw-items-center tw-gap-3">
              <div class="tw-flex tw-items-center tw-gap-2">
                <i
                  :class="[
                    'mdi mdi-ticket-confirmation tw-text-2xl',
                    voucherDetail.tipe_voucher === 1
                      ? 'tw-text-blue-600'
                      : voucherDetail.tipe_voucher === 2
                      ? 'tw-text-purple-600'
                      : 'tw-text-green-600',
                  ]"></i>
                <span class="tw-text-black tw-font-bold tw-text-lg">
                  Detail Voucher
                </span>
              </div>
              <span
                :class="[
                  'tw-px-3 tw-py-1 tw-rounded-full tw-text-xs tw-font-semibold',
                  voucherDetail.tipe_voucher === 1
                    ? 'tw-bg-blue-100 tw-text-blue-800'
                    : voucherDetail.tipe_voucher === 2
                    ? 'tw-bg-purple-100 tw-text-purple-800'
                    : 'tw-bg-green-100 tw-text-green-800',
                ]">
                {{ voucherDetail.kode_voucher }}
              </span>
            </div>
          </template>
          <template #content>
            <div
              class="tw-max-h-[70vh] tw-w-full tw-overflow-y-auto tw-pr-2 tw-custom-scrollbar">
              <div class="tw-flex tw-flex-col tw-gap-5">
                <!-- Header Info Card -->
                <div
                  class="tw-bg-white tw-p-4 tw-rounded-xl tw-border tw-border-gray-200 tw-shadow-sm tw-mb-6">
                  <h5 class="tw-font-semibold tw-mb-3 tw-flex tw-items-center">
                    <i
                      :class="[
                        'mdi mdi-ticket-confirmation tw-mr-2',
                        voucherDetail.tipe_voucher === 1
                          ? 'tw-text-blue-600'
                          : voucherDetail.tipe_voucher === 2
                          ? 'tw-text-purple-600'
                          : 'tw-text-green-600',
                      ]"></i>
                    Informasi Voucher
                  </h5>

                  <div class="tw-bg-gray-50 tw-p-4 tw-rounded-lg">
                    <!-- Kode Voucher -->
                    <div class="tw-flex tw-items-center tw-gap-2 tw-mb-3">
                      <div
                        class="tw-bg-gray-200 tw-px-3 tw-py-1 tw-rounded-full">
                        <span class="tw-text-xs tw-font-mono tw-text-gray-700">
                          {{ voucherDetail.kode_voucher }}
                        </span>
                      </div>
                    </div>

                    <!-- Nama Voucher -->
                    <h2
                      class="tw-font-bold tw-text-xl tw-mb-3 tw-text-gray-800">
                      {{ voucherDetail.nama_voucher }}
                    </h2>

                    <!-- Tanggal -->
                    <div
                      class="tw-flex tw-items-center tw-text-gray-600 tw-bg-white tw-px-3 tw-py-2 tw-rounded-lg tw-shadow-sm tw-w-fit">
                      <i
                        class="mdi mdi-calendar-range tw-mr-2 tw-text-amber-500"></i>
                      <span>
                        {{
                          voucherDetail.tanggal_mulai ||
                          "Tanggal mulai tidak ditentukan"
                        }}
                        -
                        {{ voucherDetail.tanggal_kadaluarsa || "Selamanya" }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Informasi Diskon -->
                <div
                  :class="[
                    'tw-p-5 tw-rounded-xl tw-border tw-shadow-sm',
                    voucherDetail.tipe_voucher === 1
                      ? 'tw-bg-blue-50 tw-border-blue-200'
                      : voucherDetail.tipe_voucher === 2
                      ? 'tw-bg-purple-50 tw-border-purple-200'
                      : 'tw-bg-green-50 tw-border-green-200',
                  ]">
                  <h4
                    class="tw-font-bold tw-mb-4 tw-text-lg tw-flex tw-items-center">
                    <i
                      :class="[
                        'mdi mdi-percent-circle tw-mr-2 tw-text-2xl',
                        voucherDetail.tipe_voucher === 1
                          ? 'tw-text-blue-600'
                          : voucherDetail.tipe_voucher === 2
                          ? 'tw-text-purple-600'
                          : 'tw-text-green-600',
                      ]"></i>
                    Informasi Diskon
                  </h4>

                  <div
                    class="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-gap-4">
                    <div
                      v-if="voucherDetail.persentase_diskon_1 > 0"
                      class="tw-flex tw-items-center tw-gap-2 tw-bg-white tw-rounded-lg tw-p-3 tw-shadow-sm">
                      <i
                        :class="[
                          'mdi mdi-percent-circle tw-text-xl',
                          voucherDetail.tipe_voucher === 1
                            ? 'tw-text-blue-600'
                            : voucherDetail.tipe_voucher === 2
                            ? 'tw-text-purple-600'
                            : 'tw-text-green-600',
                        ]"></i>
                      <div>
                        <div class="tw-text-sm tw-text-gray-600">Diskon 1</div>
                        <div class="tw-font-bold tw-text-lg">
                          {{ voucherDetail.persentase_diskon_1 }}%
                        </div>
                      </div>
                    </div>

                    <div
                      v-if="voucherDetail.persentase_diskon_2 > 0"
                      class="tw-flex tw-items-center tw-gap-2 tw-bg-white tw-rounded-lg tw-p-3 tw-shadow-sm">
                      <i
                        :class="[
                          'mdi mdi-percent-circle tw-text-xl',
                          voucherDetail.tipe_voucher === 1
                            ? 'tw-text-blue-600'
                            : voucherDetail.tipe_voucher === 2
                            ? 'tw-text-purple-600'
                            : 'tw-text-green-600',
                        ]"></i>
                      <div>
                        <div class="tw-text-sm tw-text-gray-600">Diskon 2</div>
                        <div class="tw-font-bold tw-text-lg">
                          {{ voucherDetail.persentase_diskon_2 }}%
                        </div>
                      </div>
                    </div>

                    <div
                      v-if="voucherDetail.persentase_diskon_3 > 0"
                      class="tw-flex tw-items-center tw-gap-2 tw-bg-white tw-rounded-lg tw-p-3 tw-shadow-sm">
                      <i
                        :class="[
                          'mdi mdi-percent-circle tw-text-xl',
                          voucherDetail.tipe_voucher === 1
                            ? 'tw-text-blue-600'
                            : voucherDetail.tipe_voucher === 2
                            ? 'tw-text-purple-600'
                            : 'tw-text-green-600',
                        ]"></i>
                      <div>
                        <div class="tw-text-sm tw-text-gray-600">Diskon 3</div>
                        <div class="tw-font-bold tw-text-lg">
                          {{ voucherDetail.persentase_diskon_3 }}%
                        </div>
                      </div>
                    </div>

                    <div
                      v-if="voucherDetail.nominal_diskon > 0"
                      class="tw-flex tw-items-center tw-gap-2 tw-bg-white tw-rounded-lg tw-p-3 tw-shadow-sm">
                      <i class="mdi mdi-cash tw-text-xl tw-text-green-600"></i>
                      <div>
                        <div class="tw-text-sm tw-text-gray-600">
                          Nilai Diskon
                        </div>
                        <div class="tw-font-bold tw-text-lg">
                          Rp {{ parseCurrency(voucherDetail.nominal_diskon) }} /
                          UOM 1
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Persyaratan -->
                <div class="tw-flex tw-flex-col tw-gap-4">
                  <div
                    v-if="voucherDetail.minimal_subtotal_pembelian > 0"
                    class="tw-bg-white tw-p-4 tw-rounded-xl tw-border tw-border-gray-200 tw-shadow-sm">
                    <h5
                      class="tw-font-semibold tw-mb-2 tw-flex tw-items-center">
                      <i
                        class="mdi mdi-cash-multiple tw-mr-2 tw-text-amber-500"></i>
                      Minimal Subtotal
                    </h5>
                    <div class="tw-text-xl tw-font-bold tw-text-green-600">
                      Rp
                      {{
                        parseCurrency(voucherDetail.minimal_subtotal_pembelian)
                      }}
                    </div>
                  </div>

                  <div
                    v-if="
                      voucherDetail.minimal_jumlah_produk &&
                      voucherDetail.tipe_voucher === 2 &&
                      voucherDetail.is_reguler !== 1
                    "
                    class="tw-bg-white tw-p-4 tw-rounded-xl tw-border tw-border-gray-200 tw-shadow-sm">
                    <h5
                      class="tw-font-semibold tw-mb-2 tw-flex tw-items-center">
                      <i
                        class="mdi mdi-package-variant-closed tw-mr-2 tw-text-amber-500"></i>
                      Minimal Jumlah Produk
                    </h5>
                    <div class="tw-flex tw-items-center">
                      <div class="tw-text-xl tw-font-bold tw-text-green-600">
                        {{ voucherDetail.minimal_jumlah_produk }}
                      </div>
                      <div
                        class="tw-text-gray-500 tw-ml-2 tw-text-sm"
                        v-if="voucherDetail.level_uom">
                        (Level UOM: {{ voucherDetail.level_uom }})
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Syarat Ketentuan -->
                <div
                  class="tw-bg-white tw-p-4 tw-rounded-xl tw-border tw-border-gray-200 tw-shadow-sm">
                  <h5 class="tw-font-semibold tw-mb-3 tw-flex tw-items-center">
                    <i
                      class="mdi mdi-text-box-check-outline tw-mr-2 tw-text-blue-600"></i>
                    Syarat dan Ketentuan
                  </h5>
                  <p
                    class="tw-bg-gray-50 tw-p-3 tw-rounded-lg tw-text-gray-800">
                    {{
                      voucherDetail.syarat_ketentuan ||
                      "Tidak ada syarat dan ketentuan khusus"
                    }}
                  </p>
                </div>

                <!-- List Produk yang Dapat Menggunakan Voucher -->
                <div
                  v-if="
                    voucherDetail.produk_names &&
                    voucherDetail.produk_names.length > 0
                  "
                  class="tw-bg-white tw-p-4 tw-rounded-xl tw-border tw-border-gray-200 tw-shadow-sm">
                  <h5 class="tw-font-semibold tw-mb-3 tw-flex tw-items-center">
                    <i
                      class="mdi mdi-cube-outline tw-mr-2 tw-text-purple-600"></i>
                    Produk yang Dapat Menggunakan Voucher
                    <span
                      class="tw-ml-2 tw-bg-purple-100 tw-text-purple-800 tw-px-2 tw-py-0.5 tw-rounded-full tw-text-xs">
                      {{ voucherDetail.produk_names.length }}
                    </span>
                  </h5>
                  <div
                    class="tw-max-h-40 tw-overflow-y-auto tw-bg-gray-50 tw-p-3 tw-rounded-lg">
                    <div
                      v-for="(produk, idx) in voucherDetail.produk_names"
                      :key="idx"
                      class="tw-flex tw-items-center tw-mb-2 tw-bg-white tw-p-2 tw-rounded-md tw-shadow-sm">
                      <i
                        class="mdi mdi-package-variant-closed tw-text-gray-500 tw-mr-2"></i>
                      <span>{{ produk }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Footer Actions -->
            <div class="tw-flex tw-justify-end tw-w-full tw-mt-5">
              <Button :trigger="hide" class="tw-bg-red-500 tw-py-2 tw-px-4">
                <i class="mdi mdi-close tw-mr-1"></i>
                Tutup
              </Button>
            </div>
          </template>
        </Card>
      </BModal>
    </SlideRightX>
  </div>
</template>

<style scoped>
.tw-custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent;
}
.tw-custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.tw-custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.tw-custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 20px;
}
</style>
