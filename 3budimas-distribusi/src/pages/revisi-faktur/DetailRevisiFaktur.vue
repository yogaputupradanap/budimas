<script setup>
import Table from "@/src/components/ui/table/Table.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import {useShipping} from "@/src/store/shipping";
import {computed, onMounted, ref} from "vue";
import {calculateProductDiscounts, calculateProductSubtotal, formatCurrencyAuto, getDateNow,} from "@/src/lib/utils";
import {useRoute} from "vue-router";
import {detailRevisiFakturCol} from "@/src/model/tableColumns/revisi-faktur/detailRevisiFakturCol";
import StatusBar from "@/src/components/ui/StatusBar.vue";

const router = useRoute();
const shipping = useShipping();
const fakturInfo = ref({});
const detailFaktur = ref([]);
const tableKey = ref(0);

const id_sales_order = router.params?.id_sales_order;

const setFakturInfo = () => {
  fakturInfo.value = shipping?.listDetailFakturShipping?.detailFakturInfo;
  detailFaktur.value = shipping?.listDetailFakturShipping?.detailFaktur;
};

const getResource = async () => {
  await shipping.getListDetailFakturShipping(id_sales_order, router.query?.id_order_batch, router.query?.id_sales_order);
  tableKey.value++;
  setFakturInfo();
};

const subtotal = computed(() => {
  let total = 0;
  if (detailFaktur.value && detailFaktur.value.length > 0) {
    detailFaktur.value.forEach((product) => {
      total += calculateProductSubtotal(product, "delivered");
    });
  }
  return formatCurrencyAuto(total);
});

const totalOrderSubtotal = computed(() => {
  let total = 0;
  if (detailFaktur.value && detailFaktur.value.length > 0) {
    detailFaktur.value.forEach((product) => {
      const kartonToUom1 =
        (product.karton_delivered || 0) * (product.konversi_level3 || 1);
      const boxToUom1 =
        (product.box_delivered || 0) * (product.konversi_level2 || 1);
      const piecesUom1 = product.pieces_delivered || 0;

      const totalPieces = kartonToUom1 + boxToUom1 + piecesUom1;

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
      const voucherStatus = shipping.getVoucherStatusForProduct(
        product.id_produk
      );

      const discountResult = calculateProductDiscounts(
        product,
        voucherStatus,
        orderSubtotal,
        "delivered"
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
        "delivered"
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

onMounted(() => getResource());
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
              :loading="shipping.listDetailFakturShipping.loading"
              label="Tanggal Jatuh Tempo :"
              :value="
                getDateNow(new Date(fakturInfo?.tanggal_jatuh_tempo), false) ||
                ''
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
              :columns="detailRevisiFakturCol" />
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
