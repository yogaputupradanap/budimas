<script setup>
import Table from "../components/ui/table/Table.vue";
import { detailKonfirmasiVoucherColumn } from "../model/tableColumns";
import StatusBar from "../components/ui/StatusBar.vue";

import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import { useShipping } from "../store/shipping";
import { computed, onMounted, ref } from "vue";
import { parseCurrency } from "../lib/utils";
import Faktur from "../components/pdf/Faktur.vue";
import { useRoute } from "vue-router";
import { useAlert } from "../store/alert";
import { useKepalaCabang } from "../store/kepalaCabang";

const user = useKepalaCabang();
const router = useRoute();
const shipping = useShipping();
const submitLoading = ref(false);
const vouchers_2 = ref([]);
const tableKey = ref(0);

const totalDisc = computed(getTotalDisc);
const totalHarga = computed(getTotalHarga);

const { id_produk, id_sales_order } = router.params;
const alert = useAlert();

const removeData = (info) => {
  vouchers_2.value = vouchers_2.value.filter(
    (val) => val.id_draft_voucher_2 !== info.value
  );
  tableKey.value++;
};

const getResource = () => {
  shipping.getSelectedVoucher(id_produk);
  const {
    id_order_detail,
    harga_jual,
    id_sales_order,
    draft_voucher_2_detail,
  } = shipping.selectedProductVoucher.selectedVoucher;

  const vouchers = shipping.selectedProductVoucher.selectedVoucher.vouchers;

  vouchers_2.value = vouchers.map((i) => {
    const id_draft_voucher_2 = draft_voucher_2_detail.find(
      (ii) => ii.kode_voucher === i.kode
    )["id"];

    return {
      ...i,
      id_draft_voucher_2,
      id_sales_order,
      harga_jual,
      id_order_detail,
      id_draft_voucher_2,
    };
  });
};

const submitOrder = async () => {};

function getTotalDisc() {
  return vouchers_2.value.reduce((acc, val) => {
    return acc + val.nilai_diskon;
  }, 0);
}

function getTotalHarga() {
  const { harga_jual } = shipping.selectedProductVoucher.selectedVoucher;
  return harga_jual - totalDisc.value;
}

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
        <template #header>Detail Produk</template>
        <template #content>
          <div class="status-field-container-3-col tw-mb-5">
            <StatusBar
              :loading="shipping.selectedProductVoucher.loading"
              label="Nama Produk :"
              :value="
                shipping.selectedProductVoucher.selectedVoucher?.nama_produk ||
                'unknown'
              " />
            <StatusBar
              :loading="shipping.selectedProductVoucher.loading"
              label="Kode Produk :"
              :value="
                shipping.selectedProductVoucher.selectedVoucher?.kode_sku ||
                'unknown'
              " />
            <StatusBar
              :loading="shipping.selectedProductVoucher.loading"
              label="Harga (satuan pieces) :"
              :value="
                parseCurrency(
                  shipping.selectedProductVoucher.selectedVoucher?.harga_jual
                ) || 'unknown'
              " />
            <StatusBar
              :loading="shipping.selectedProductVoucher.loading"
              label="Harga (setelah diskon) :"
              :value="
                parseCurrency(
                  shipping.selectedProductVoucher.selectedVoucher?.subtotalorder
                ) || 'unknown'
              " />
            <StatusBar
              :loading="shipping.selectedProductVoucher.loading"
              label="UOM 1 (Karton) :"
              :value="
                shipping.selectedProductVoucher.selectedVoucher?.karton_order ||
                0
              " />
            <StatusBar
              :loading="shipping.selectedProductVoucher.loading"
              label="UOM 2 (Box) :"
              :value="
                shipping.selectedProductVoucher.selectedVoucher?.box_order || 0
              " />
            <StatusBar
              :loading="shipping.selectedProductVoucher.loading"
              label="UOM 3 (Pieces) :"
              :value="
                shipping.selectedProductVoucher.selectedVoucher?.pieces_order ||
                0
              " />
          </div>
        </template>
      </Card>
      <Card :no-subheader="true" class="tw-mt-5">
        <template #header>Verifikasi Promo Produk</template>
        <template #content>
          <div class="tw-w-full tw-pb-20 tw-flex tw-flex-col tw-gap-4">
            <Table
              :key="tableKey"
              @remove-row="(val) => removeData(val)"
              classic
              :loading="shipping.selectedProductVoucher.loading"
              :table-data="vouchers_2"
              :columns="detailKonfirmasiVoucherColumn" />
            <div class="tw-flex tw-flex-col tw-items-end tw-mb-5 tw-w-full">
              <table>
                <tr>
                  <td class="tw-font-bold">Total Disc</td>
                  <td class="tw-w-6 tw-text-center">:</td>
                  <td>Rp. {{ parseCurrency(totalDisc) }}</td>
                </tr>
                <tr>
                  <td class="tw-font-bold">Total Harga</td>
                  <td class="tw-w-6 tw-text-center">:</td>
                  <td>Rp. {{ parseCurrency(totalHarga) }}</td>
                </tr>
              </table>
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
