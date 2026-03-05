<script setup>
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Button from "@/src/components/ui/Button.vue";
import Loader from "@/src/components/ui/Loader.vue";
import Modal from "@/src/components/ui/Modal.vue";
import { onMounted, reactive, ref, computed, watch } from "vue";
import { useVoucher } from "@/src/store/voucher";
import { voucherService } from "@/src/services/vouchers";
import ImageBreak from "@/src/assets/images/image-break.png";
import { parseCurrency } from "@/src/lib/utils";


const vouchers = useVoucher();

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

const loading = ref(false);
const modalDetail = ref();
const isImageError = ref(false);

const voucherList = computed(() => [
  ...vouchers.voucher1RegularList,
  ...vouchers.voucher2RegularList,
  ...vouchers.voucher3RegularList,
]);

const showDetail = (index) => {
  Object.keys(voucherDetail).forEach((key) => {
    voucherDetail[key] = Array.isArray(voucherDetail[key]) ? [] : "";
  });
  
  const selectedVoucher = voucherList.value[index];
  Object.keys(selectedVoucher).forEach((key) => {
    if (key in voucherDetail) {
      voucherDetail[key] = selectedVoucher[key];
    }
  });

  voucherDetail.persentase_diskon_1 = selectedVoucher.persentase_diskon_1 || 0;
  voucherDetail.persentase_diskon_2 = selectedVoucher.persentase_diskon_2 || 0;
  voucherDetail.persentase_diskon_3 = selectedVoucher.persentase_diskon_3 || 0;
  voucherDetail.minimal_total_pembelian = selectedVoucher.minimal_total_pembelian || 0;
  voucherDetail.minimal_subtotal_pembelian = selectedVoucher.minimal_subtotal_pembelian || 0;
  voucherDetail.budget_diskon = selectedVoucher.budget_diskon || "";
  voucherDetail.nominal_diskon = selectedVoucher.nominal_diskon || 0;
  voucherDetail.produk_names = selectedVoucher.produk_names || [];
  voucherDetail.cabang_names = selectedVoucher.cabang_names || [];
  voucherDetail.customer_names = selectedVoucher.customer_names || [];
  voucherDetail.tipe_voucher = selectedVoucher.tipe_voucher || null;
  voucherDetail.minimal_jumlah_produk = selectedVoucher.minimal_jumlah_produk || 0;
  voucherDetail.level_uom = selectedVoucher.level_uom || null;
  modalDetail.value?.show();
};

const getVoucherBgClass = (voucherCode) => {
  const voucherType = voucherCode?.split("-").pop();
  if (voucherType === "1") return "from-blue-600 to-blue-800";
  if (voucherType === "2") return "from-purple-600 to-purple-800";
  if (voucherType === "3") return "from-green-600 to-green-800";
  return "from-indigo-600 to-indigo-800";
};

const loadRegularVouchers = async () => {
  loading.value = true;
  try {
    const [voucher1Regular, voucher2Regular, voucher3Regular] = await Promise.all([
      voucherService.getVoucherV1Regular(),
      voucherService.getVoucherV2Regular(),
      voucherService.getVoucherV3Regular()
    ]);

    vouchers.voucher1RegularList = voucher1Regular || [];
    vouchers.voucher2RegularList = voucher2Regular || [];
    vouchers.voucher3RegularList = voucher3Regular || [];
  } catch (error) {
    console.error("Error loading regular vouchers:", error);
    vouchers.voucher1RegularList = [];
    vouchers.voucher2RegularList = [];
    vouchers.voucher3RegularList = [];
  } finally {
    loading.value = false;
  }
};

const onImageError = (e) => { 
    isImageError.value = true;
    e.target.src = ImageBreak;
    e.target.style.objectFit = "contain"; 
    e.target.style.opacity = "0.3";
};

watch(voucherList, (val) => {
  console.log("Voucher List Updated:", val);
});

onMounted(async () => { await loadRegularVouchers() });

</script>

<template>
  <div class="tw-w-full tw-flex tw-flex-col md:tw-pl-6 tw-pl-0">
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
          <div class="tw-w-full tw-flex tw-justify-between tw-items-center tw-gap-4">
            <div class="tw-grid-row-2">
                <div>
                    <span>List Voucher</span>
                </div>
                <div>
                    <span class="tw-text-xs tw-bg-blue-100 tw-text-blue-700 tw-px-3 tw-py-1 tw-rounded-full">
                        {{ voucherList.length }} Voucher Tersedia
                    </span>
                </div>
            </div>
          </div>
        </template>
        <template #content>
          <div v-if="loading" class="tw-w-full tw-h-[400px] tw-flex tw-justify-center tw-items-center">
            <Loader />
          </div>
          <div v-else-if="voucherList.length === 0" class="tw-w-full tw-h-[400px] tw-flex tw-flex-col tw-justify-center tw-items-center">
            <div class="tw-text-center">
              <div class="tw-bg-gray-100 tw-rounded-full tw-p-4 tw-inline-block">
                <i class="mdi mdi-ticket-confirmation-outline tw-text-5xl tw-text-gray-500"></i>
              </div>
              <p class="tw-mt-4 tw-text-lg tw-font-medium tw-text-gray-700">
                Tidak ada voucher tersedia
              </p>
            </div>
          </div>
          <div v-else class="tw-p-4 tw-pb-6">
            <div class="tw-max-w-5xl tw-mx-auto tw-grid tw-grid-cols-1 md:tw-grid-cols-2 lg:tw-grid-cols-3 tw-gap-6">
              <div
                v-for="(voucher, index) in voucherList"
                :key="voucher.id"
                class="tw-bg-white tw-rounded-xl tw-overflow-hidden tw-shadow-md tw-transition-all tw-duration-300 hover:tw-shadow-xl hover:-tw-translate-y-1 tw-relative"
                >
                <div class="tw-relative tw-w-full tw-h-48 tw-overflow-hidden">
                    <div v-if="voucher.pic_voucher" class="tw-w-full tw-h-full">
                        <BImg
                        :src="`https://storage.googleapis.com/buktitransaksi/${voucher.pic_voucher}`"
                        @error="onImageError"
                        :class="[
                            'tw-w-full tw-h-full tw-object-cover transition-all duration-300',
                            isImageError ? 'tw-object-contain tw-bg-gray-100 tw-p-4' : ''
                        ]"
                        />
                    </div>
                    <div 
                    v-else 
                    class="tw-w-full tw-h-full tw-flex tw-items-center tw-justify-center tw-bg-gray-100"
                    >
                        <span class="tw-text-gray-500 tw-text-sm">
                            No Image Provided
                        </span>
                    </div>
                    <div
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
                      v-else-if="voucher.tipe_voucher === 2 && voucher.is_reguler === 1"
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
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                      <line x1="3" y1="9" x2="21" y2="9"></line>
                      <line x1="9" y1="21" x2="9" y2="9"></line>
                    </svg>
                    <!-- SVG for v3r Vouchers -->
                    <svg
                      v-else-if="voucher.tipe_voucher === 3 && voucher.is_reguler === 1"
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
                      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
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
                      <rect x="3" y="4" width="18" height="16" rx="2" ry="2"></rect>
                      <path d="M12 4v16"></path>
                    </svg>
                  </div>
                </div>
                <div class="tw-p-4">
                  <div class="tw-flex tw-justify-between tw-items-center tw-mb-2 tw-gap-2">
                    <span class="tw-text-xs tw-font-mono tw-bg-gray-100 tw-px-2 tw-py-1 tw-rounded-md tw-text-gray-600">
                      {{ voucher.kode_voucher }}
                    </span>
                    <div class="tw-flex tw-items-center tw-text-gray-500 tw-text-xs">
                      <i class="mdi mdi-calendar tw-mr-1"></i>
                      {{
                        voucher.tanggal_mulai
                          ? `${voucher.tanggal_mulai.split("-").reverse().join("/")} - ${
                              voucher.tanggal_kadaluarsa
                                ? voucher.tanggal_kadaluarsa.split("-").reverse().join("/")
                                : "∞"
                            }`
                          : "Tanggal tidak ditentukan"
                      }}
                    </div>
                  </div>
                  <h3 class="tw-font-bold tw-text-gray-800 tw-mb-3 tw-text-xl tw-line-clamp-2">
                    {{ voucher.nama_voucher }}
                  </h3>
                  <div class="tw-w-full tw-h-px tw-bg-gray-100 tw-my-3"></div>
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
                          <div class="tw-text-xs tw-text-gray-500">Diskon 1</div>
                          <div class="tw-font-bold">{{ voucher.persentase_diskon_1 }}%</div>
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
                          <div class="tw-text-xs tw-text-gray-500">Diskon 2</div>
                          <div class="tw-font-bold">{{ voucher.persentase_diskon_2 }}%</div>
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
                          <div class="tw-text-xs tw-text-gray-500">Diskon 3</div>
                          <div class="tw-font-bold">{{ voucher.persentase_diskon_3 }}%</div>
                        </div>
                      </div>
                      <div
                        v-if="voucher.nominal_diskon"
                        class="tw-bg-green-50 tw-rounded-lg tw-p-2 tw-flex tw-items-center tw-gap-2 tw-w-full">
                        <i class="mdi mdi-cash tw-text-lg tw-text-green-600"></i>
                        <div>
                          <div class="tw-text-xs tw-text-gray-500">Nilai</div>
                          <div class="tw-font-bold">
                            Rp {{ voucher.nominal_diskon }} / UOM 1
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="tw-flex tw-justify-between tw-items-center tw-mt-2">
                    <div class="tw-flex tw-flex-col tw-gap-2">
                      <div
                        v-if="voucher.minimal_subtotal_pembelian"
                        class="tw-flex tw-items-center tw-text-xs tw-text-amber-700 tw-bg-amber-50 tw-px-2 tw-py-1 tw-rounded-md">
                        <i class="mdi mdi-cash-multiple tw-mr-1"></i>
                        Min: Rp {{ voucher.minimal_subtotal_pembelian }}
                      </div>
                      <div
                        v-if="voucher.produk_names && voucher.produk_names.length"
                        class="tw-flex tw-items-center tw-text-xs tw-text-indigo-700 tw-bg-indigo-50 tw-px-2 tw-py-1 tw-rounded-md">
                        <i class="mdi mdi-cube-outline tw-mr-1"></i>
                        {{ voucher.produk_names.length }} Produk
                      </div>
                    </div>
                    <Button
                      :trigger="() => showDetail(index)"
                      size="sm"
                      class="tw-px-4 tw-py-2 tw-self-end"
                    >
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
      <Modal
        id="voucherDetailModal"
        ref="modalDetail"
        title="Detail Voucher"
        size="lg"
      >
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
                          {{ parseCurrency(voucherDetail.nominal_diskon) }} /
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
                      {{ parseCurrency(voucherDetail.minimal_subtotal_pembelian) }}
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
          </template>
        </Card>
      </Modal>
    </SlideRightX>
  </div>
</template>