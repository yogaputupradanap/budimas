<script setup>
import barcode from "../../assets/images/barcode-pdf-faktur.png";
import {
  getDateNow,
  numberToWords,
  calculateProductDiscounts,
  formatCurrencyAuto,
  calculateProductSubtotal,
} from "@/src/lib/utils";
import { computed } from "vue";
import { useShipping } from "@/src/store/shipping";

const props = defineProps({
  title: {
    type: String,
    default() {
      return "penjualan";
    },
  },
  info: {
    type: Object,
    default() {
      return {};
    },
  },
  list: Array,
  default() {
    return [];
  },
  isRetur: Boolean,
  default() {
    return false;
  },
});

const shipping = useShipping();

// Dapatkan total subtotal pesanan untuk perhitungan diskon
const totalOrderSubtotal = computed(() => {
  let total = 0;
  if (props.list && props.list.length > 0) {
    props.list.forEach((product) => {
      // Konversi semua picked ke level UOM1
      const kartonToUom1 =
        (product.karton_picked || 0) * (product.konversi_level3 || 1);
      const boxToUom1 =
        (product.box_picked || 0) * (product.konversi_level2 || 1);
      const piecesUom1 = product.pieces_picked || 0;

      // Total pieces setelah konversi
      const totalPieces = kartonToUom1 + boxToUom1 + piecesUom1;

      // Hitung subtotal
      total += totalPieces * (product.harga_jual || 0);
    });
  }
  console.log("props.list", props.list);
  return total;
});

const bottomTitle = computed(() => {
  return {
    first: props.isRetur ? "Outlet" : "penjualan",
    second: props.isRetur ? "Saleman" : "Driver",
    third: props.isRetur ? "Spv" : "Checker",
    fourth: props.isRetur ? "Delivery" : "Penerima",
    fifth: "Penerima",
  };
});

// Fungsi untuk mendapatkan status voucher dari produk
function getVoucherStatus(product) {
  try {
    return shipping.getVoucherStatusForProduct(product.id_produk);
  } catch (error) {
    console.error("Error getting voucher status:", error);
    return null;
  }
}

// Fungsi untuk mendapatkan diskon v1r (Voucher Reguler 1)
function getDiskonV1R(product) {
  const voucherStatus = getVoucherStatus(product);
  const { diskon1r } = calculateProductDiscounts(
    product,
    voucherStatus,
    totalOrderSubtotal.value,
    "picked"
  );
  return formatCurrencyAuto(diskon1r) || 0;
}

// Fungsi untuk mendapatkan diskon v2r (Voucher Reguler 2)
function getDiskonV2R(product) {
  const voucherStatus = getVoucherStatus(product);
  const { diskon2r } = calculateProductDiscounts(
    product,
    voucherStatus,
    totalOrderSubtotal.value,
    "picked"
  );
  return formatCurrencyAuto(diskon2r) || 0;
}

// Fungsi untuk mendapatkan diskon v3r (Voucher Reguler 3)
function getDiskonV3R(product) {
  const voucherStatus = getVoucherStatus(product);
  const { diskon3r } = calculateProductDiscounts(
    product,
    voucherStatus,
    totalOrderSubtotal.value,
    "picked"
  );
  return formatCurrencyAuto(diskon3r) || 0;
}

// Fungsi untuk mendapatkan diskon v2p (Voucher Produk 2)
function getDiskonV2P(product) {
  const voucherStatus = getVoucherStatus(product);
  const { diskon2p } = calculateProductDiscounts(
    product,
    voucherStatus,
    totalOrderSubtotal.value,
    "picked"
  );
  return formatCurrencyAuto(diskon2p) || 0;
}

// Fungsi untuk mendapatkan diskon v3p (Voucher Produk 3)
function getDiskonV3P(product) {
  const voucherStatus = getVoucherStatus(product);
  const { diskon3p } = calculateProductDiscounts(
    product,
    voucherStatus,
    totalOrderSubtotal.value,
    "picked"
  );
  return formatCurrencyAuto(diskon3p) || 0;
}

// Fungsi untuk mendapatkan total diskon
function getTotalDiskon(product) {
  const voucherStatus = getVoucherStatus(product);
  const { totalDiskon } = calculateProductDiscounts(
    product,
    voucherStatus,
    totalOrderSubtotal.value,
    "picked"
  );
  return formatCurrencyAuto(totalDiskon);
}

const computedTotal = computed(() => {
  let subtotalValue = 0;
  let totalDiskonValue = 0;
  let totalPpnValue = 0;

  if (props.list && props.list.length > 0) {
    let totalOrderSubtotal = 0;
    props.list.forEach((product) => {
      const kartonToUom1 =
        (product.karton_picked || 0) * (product.konversi_level3 || 1);
      const boxToUom1 =
        (product.box_picked || 0) * (product.konversi_level2 || 1);
      const piecesUom1 = product.pieces_picked || 0;
      const totalPieces = kartonToUom1 + boxToUom1 + piecesUom1;
      totalOrderSubtotal += totalPieces * (product.harga_jual || 0);
    });

    props.list.forEach((product) => {
      subtotalValue += calculateProductSubtotal(product, "picked");

      const voucherStatus = getVoucherStatus(product);

      const discountResult = calculateProductDiscounts(
        product,
        voucherStatus,
        totalOrderSubtotal,
        "picked"
      );

      totalDiskonValue += discountResult.totalDiskon;
      totalPpnValue += discountResult.ppnValue;
    });
  }

  const totalValue = subtotalValue - totalDiskonValue + totalPpnValue;

  return {
    subtotal: subtotalValue,
    diskon: totalDiskonValue,
    pajak: totalPpnValue,
    total: totalValue,
  };
});
</script>

<template>
  <div
    id="faktur"
    class="tw-w-full tw-h-full tw-flex tw-flex-col tw-items-center tw-text-xs portrait-faktur courier-font tw-tracking-tighter">
    <div class="tw-w-full tw-flex tw-flex-col tw-px-2">
      <div
        class="tw-w-full tw-flex tw-justify-between tw-p-4 tw-pb-4 tw-border-b tw-border-black">
        <div
          class="tw-max-w-[250px] tw-flex tw-flex-col tw-gap-1 tw-text-[13px]">
          <span class="tw-font-bold">PT. BUDIMAS MAKMUR MULIA</span>
          <div
            class="tw-pb-4 tw-border-b tw-border-black tw-border-dashed tw-leading-3">
            <span>Jl. Serut RT 04/XII Mojosongo Solo</span>
            <br />
            <span>Telp. / Fax. (0271) 856064</span>
            <br />
            <span>Email : budimas.solo@yahoo.com</span>
          </div>
          <span>Tanggal : {{ getDateNow() }}</span>
        </div>
        <div
          class="tw-w-[250px] tw-flex tw-flex-col tw-justify-between tw-items-center">
          <span
            class="tw-w-1/2 tw-h-8 tw-font-bold tw-text-center tw-text-[13px] tw-border-2 tw-border-black">
            {{ props.info.kode_rute }}#{{ props.info.kode_principal }}
          </span>
          <span
            class="tw-text-[13px] tw-font-semibold tw-border-b tw-border-black tw-pb-2 tw-uppercase">
            faktur {{ isRetur ? "retur" : "penjualan" }}
          </span>
          <span class="tw-text-[13px]">
            No. {{ isRetur ? "Retur" : "Faktur" }} :
            <br />
            {{ props.info.nomor_faktur }}
          </span>
        </div>
        <div
          class="tw-max-w-[250px] tw-flex tw-flex-col tw-text-[13px] tw-gap-1">
          <div
            class="tw-w-full tw-flex tw-flex-col tw-border-b tw-border-black tw-border-dashed tw-pb-4 tw-leading-3">
            <span>
              Kepada Yth.
              <br />
              {{ props.info.nama_customer }} ({{ props.info.kode_customer }})
              <br />
              {{ props.info.alamat_customer }}
              <br />
              Telp : {{ props.info.telepon_customer }}
            </span>
          </div>
          <span v-if="!isRetur">
            Jatuh Tempo :
            {{ getDateNow(new Date(props.info.tanggal_jatuh_tempo)) }}
          </span>
          <span v-if="isRetur">
            Tanggal Pengajuan :
            {{ getDateNow(new Date(props.info.tanggal_retur_pengajuan)) }}
          </span>
        </div>
      </div>
      <div class="tw-w-full tw-text-[11px] tw-tracking-tighter">
        <div class="tw-font-bold tw-flex tw-px-2">
          <div class="tw-w-20 tw-text-start tw-py-1">Kode</div>
          <div class="tw-w-36 tw-text-start tw-py-1">Nama</div>
          <div class="tw-w-20 fullw tw-py-1">
            <div>
              <div>Jumlah UOM</div>
              <div class="tw-flex tw-justify-around">
                <span>1</span>
                <span>2</span>
                <span>3</span>
              </div>
            </div>
          </div>
          <div class="tw-w-20 tw-text-start tw-py-1 tw-pl-2">Harga Satuan</div>
          <div class="tw-w-52 tw-py-1">
            <div>
              <div>Diskon</div>
              <div class="tw-flex tw-justify-around">
                <span>D1R</span>
                <span>D2R</span>
                <span>D3R</span>
                <span>D2K</span>
                <span>D3K</span>
              </div>
            </div>
          </div>
          <div v-if="isRetur" class="tw-w-24 tw-text-start tw-py-1">
            Alasan retur
          </div>
          <div class="tw-w-20 tw-text-end tw-py-1">Total Disc</div>
          <div class="tw-w-20 tw-text-end tw-py-1">Sub Total</div>
        </div>

        <div class="tw-w-full tw-h-[1px] tw-bg-black tw-mt-2"></div>

        <div class="tw-px-2">
          <div v-for="item in props.list" :key="item" class="tw-flex">
            <div class="tw-py-1 tw-text-start tw-w-20">{{ item.kode_sku }}</div>
            <div class="tw-py-1 tw-text-start tw-w-36">
              {{ item.nama_produk }}
            </div>
            <div class="tw-py-1 tw-text-center tw-w-[26px]">
              {{ item[isRetur ? "pieces_retur" : "pieces_picked"] || 0 }}
            </div>
            <div class="tw-py-1 tw-text-center tw-w-[26px]">
              {{ item[isRetur ? "box_retur" : "box_picked"] || 0 }}
            </div>
            <div class="tw-py-1 tw-text-center tw-w-[26px]">
              {{ item[isRetur ? "karton_retur" : "karton_picked"] || 0 }}
            </div>
            <div class="tw-py-1 tw-text-start tw-pl-2 tw-w-20">
              {{ formatCurrencyAuto(item.harga_jual) }}
            </div>
            <div class="tw-py-1 tw-text-center tw-w-[42px]">
              {{
                getDiskonV1R(item) == 0 || getDiskonV1R(item) == null
                  ? 0
                  : item.v1r_persen
              }}
            </div>
            <div class="tw-py-1 tw-text-center tw-w-[42px]">
              {{
                getDiskonV2R(item) == 0 || getDiskonV2R(item) == null
                  ? 0
                  : item.v2r_persen
              }}
            </div>
            <div class="tw-py-1 tw-text-center tw-w-[42px]">
              {{
                getDiskonV3R(item) == 0 || getDiskonV3R(item) == null
                  ? 0
                  : item.v3r_persen
              }}
            </div>
            <div class="tw-py-1 tw-text-center tw-w-[42px]">
              {{
                getDiskonV2P(item) == 0 || getDiskonV2P(item) == null
                  ? 0
                  : item.v2p_nominal_diskon
                  ? item.v2p_nominal_diskon + "/" + item.puom1_kode
                  : item.v2p_persen
              }}
            </div>
            <div class="tw-py-1 tw-text-center tw-w-[42px]">
              {{
                getDiskonV3P(item) == 0 || getDiskonV3P(item) == null
                  ? 0
                  : item.v3p_nominal_diskon
                  ? item.v3p_nominal_diskon + "/" + item.puom1_kode
                  : item.v3p_persen
              }}
            </div>
            <div v-if="isRetur" class="tw-py-1 tw-text-start tw-w-24">
              {{ item.keterangan_retur || "-" }}
            </div>
            <div class="tw-py-1 tw-text-end tw-w-20">
              {{ getTotalDiskon(item) }}
            </div>
            <div class="tw-py-1 tw-text-end tw-w-20">
              {{
                (() => {
                  const kartonToUom1 =
                    (item.karton_picked || 0) * (item.konversi_level3 || 1);
                  const boxToUom1 =
                    (item.box_picked || 0) * (item.konversi_level2 || 1);
                  const piecesUom1 = item.pieces_picked || 0;
                  const totalPieces = kartonToUom1 + boxToUom1 + piecesUom1;
                  const subtotal = totalPieces * (item.harga_jual || 0);
                  return formatCurrencyAuto(subtotal);
                })()
              }}
            </div>
          </div>
        </div>

        <div class="tw-w-full tw-h-[1px] tw-bg-black tw-mt-2"></div>
      </div>
      <div
        v-if="!isRetur"
        class="tw-w-full tw-flex tw-justify-between tw-px-2 tw-pb-4">
        <div class="tw-w-[72%] tw-text-[7px] tw-relative">
          <div class="tw-flex tw-flex-col tw-pt-0 tw-absolute -tw-top-1">
            <span class="tw-h-2">
              • Pembayaran dengan Cek/BG dianggap lunas setelah diuangkan
            </span>
            <span class="tw-h-2">
              • Barang diterima dengan baik dan benar, maksimal komplain 2X24
              jam
            </span>
            <span class="tw-h-2">• Copy bukan untuk penghasilan</span>
            <span class="tw-h-2">• Penjualan KREDIT</span>
            <span class="tw-h-2">
              • Pembayaran melalui BG/Tranfer ditunjukan ke PT. Budimas Makmur
              Mulia Dengan Nomor Rek: 783036499 Bank BCA Cabang Veteran
            </span>
          </div>
        </div>
        <div
          class="tw-w-[28%] tw-h-12 tw-flex tw-justify-end tw-pr-2 tw-text-[11px] tw-relative">
          <div class="tw-flex tw-w-full tw-flex-col tw-absolute -tw-top-[6px]">
            <div class="tw-flex">
              <span class="tw-w-[80px]">Subtotal</span>
              <span class="tw-w-[4px] tw-flex tw-justify-center">:</span>
              <span class="tw-w-full tw-text-right">
                {{ formatCurrencyAuto(computedTotal.subtotal) }}
              </span>
            </div>
            <div class="tw-flex">
              <span class="tw-w-[80px]">Discount Final</span>
              <span class="tw-w-[4px] tw-flex tw-justify-center">:</span>
              <span class="tw-w-full tw-text-right">
                - {{ formatCurrencyAuto(computedTotal.diskon) }}
              </span>
            </div>
            <div class="tw-flex">
              <span class="tw-w-[80px]">PPN</span>
              <span class="tw-w-[4px] tw-flex tw-justify-center">:</span>
              <span class="tw-w-full tw-text-right">
                + {{ formatCurrencyAuto(computedTotal.pajak) }}
              </span>
            </div>
          </div>
        </div>
      </div>
      <div class="tw-w-full tw-h-[1px] tw-bg-black tw-mt-2"></div>
      <div
        class="tw-w-full tw-flex tw-justify-between tw-items-center tw-p-2 tw-text-[8px] tw-mb-2">
        <div class="tw-w-[72%] tw-capitalize tw-relative">
          <span class="tw-absolute -tw-top-3">
            {{ `(${numberToWords(formatCurrencyAuto(computedTotal.total))})` }}
          </span>
        </div>
        <div
          class="tw-w-[28%] tw-flex tw-justify-end tw-pr-2 tw-text-[13px] tw-relative">
          <div class="tw-flex tw-w-full tw-absolute -tw-top-3 tw-font-bold">
            <span class="tw-w-[80px]">Total</span>
            <span class="tw-w-[4px] tw-flex tw-justify-center">:</span>
            <span class="tw-w-full tw-text-right">
              Rp {{ formatCurrencyAuto(computedTotal.total) }}
            </span>
          </div>
        </div>
      </div>
      <div class="tw-w-full tw-flex tw-text-[8px]">
        <div class="tw-w-[500px] tw-h-[90px] tw-flex tw-flex-col tw-px-2">
          <div
            class="tw-w-[75%] tw-h-full tw-flex tw-flex-col tw-justify-between tw-pb-3 tw-leading-3">
            <span class="tw-max-w-48">
              Jam : {{ getDateNow(new Date(), true, true) }}/{{
                props.info.status_order_str
              }}/{{ props.info.nama_fakturist || "admin fakturist" }}
            </span>
            <span>Sales : {{ props.info.nama_sales }}</span>
            <span>{{ props.info.no_order }}</span>
          </div>
          <div class="tw-w-[35%] tw-flex tw-justify-start tw-items-center">
            <img :src="barcode" class="tw-w-10" />
          </div>
          <span class="tw-text-[6px]">
            *Faktur ini sah dan diproses oleh komputer
          </span>
        </div>
        <div
          class="tw-w-full tw-flex tw-flex-col tw-items-center tw-gap-2 tw-pr-2 tw-pb-4 tw-text-[12px]">
          <span>Hormat Kami,</span>
          <div class="tw-w-full tw-flex tw-justify-between tw-gap-4">
            <div class="tw-w-full tw-flex tw-flex-col tw-items-center">
              <span>{{ bottomTitle.first }}</span>
              <div class="tw-w-full tw-h-12 tw-border-b tw-border-black"></div>
              <span v-if="!isRetur">{{ props.info.nama_sales }}</span>
            </div>
            <div class="tw-w-full tw-flex tw-flex-col tw-items-center">
              <span>{{ bottomTitle.second }}</span>
              <div class="tw-w-full tw-h-12 tw-border-b tw-border-black"></div>
              <span v-if="!isRetur">{{ props.info.nama_driver }}</span>
            </div>
            <div class="tw-w-full tw-flex tw-flex-col tw-items-center">
              <span>{{ bottomTitle.third }}</span>
              <div class="tw-w-full tw-h-12 tw-border-b tw-border-black"></div>
              <span></span>
            </div>
            <div class="tw-w-full tw-flex tw-flex-col tw-items-center">
              <span>{{ bottomTitle.fourth }}</span>
              <div class="tw-w-full tw-h-12 tw-border-b tw-border-black"></div>
              <span></span>
            </div>
            <div
              v-if="isRetur"
              class="tw-w-full tw-flex tw-flex-col tw-items-center">
              <span>{{ bottomTitle.fifth }}</span>
              <div class="tw-w-full tw-h-12 tw-border-b tw-border-black"></div>
              <span></span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.portrait-faktur {
  width: 8.5in;
  height: 11in;
}

.courier-font,
.courier-font * {
  font-family: "Courier New", monospace !important;
}

.portrait-faktur {
  width: 8.5in;
  height: 11in;
}

/* Perbaikan untuk kolom UOM dan Diskon */
.tw-w-32 > div,
.tw-w-52 > div {
  width: 100%;
  text-align: center;
}

.tw-w-32 > div > div,
.tw-w-52 > div > div {
  display: flex;
  justify-content: space-around;
  width: 100%;
}

.tw-w-32 > div > div > span,
.tw-w-52 > div > div > span {
  flex: 1;
  text-align: center;
}

@media print {
  .portrait-faktur {
    width: 8.5in !important;
    height: 11in !important;
  }

  .courier-font,
  .courier-font * {
    font-family: "Courier New", monospace !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
}
</style>
