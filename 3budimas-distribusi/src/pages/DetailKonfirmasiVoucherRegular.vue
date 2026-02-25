<script setup>
import Table from "../components/ui/table/Table.vue";
import { detailKonfirmasiVoucherRegularColumn } from "../model/tableColumns";
import StatusBar from "../components/ui/StatusBar.vue";

import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import { computed, onMounted, ref } from "vue";
import { apiUrl, fetchWithAuth, parseCurrency } from "../lib/utils";
import Faktur from "../components/pdf/Faktur.vue";
import { useRoute } from "vue-router";
import { useAlert } from "../store/alert";
import { format } from "date-fns";

const router = useRoute();
const datas = ref([]);
const tableData = ref([]);
const loading = ref(false);
const tableKey = ref(0);

const totalDisc = computed(getTotalDisc);
const totalHarga = computed(getTotalHarga);

const { id_sales_order } = router.params;
const alert = useAlert();

const removeData = (info) => {
  tableData.value = tableData.value.filter((val) => val.id !== info.value);
  tableKey.value++;
};

const getTableData = () => {
  const { subtotal_penjualan, id_sales_order } = datas.value.detail_faktur;
  const { voucher_1, draft_voucher_detail } = datas.value.list_detail_order[0];

  tableData.value = voucher_1.map((i) => ({
    ...i,
    draft_voucher_detail,
    subtotal_penjualan,
    id_sales_order,
  }));

  tableKey.value++;
};

const getResource = async () => {
  try {
    loading.value = true;
    const res = await fetchWithAuth(
      "GET",
      `${apiUrl}/api/distribusi/get-detail-faktur/${id_sales_order}`
    );

    datas.value = res;
    getTableData();
  } catch (error) {
    alert.setMessage(error, "error");
  } finally {
    loading.value = false;
  }
};

function getTotalDisc() {
  if (datas.value.list_detail_order) {
    return datas.value?.list_detail_order[0]?.voucher_1.reduce((acc, val) => {
      return acc + val.nilai_diskon;
    }, 0);
  }
}

function getTotalHarga() {
  if (datas.value.detail_faktur) {
    const { subtotal_penjualan, subtotal_diskon } = datas.value?.detail_faktur;
    const total = subtotal_penjualan + subtotal_diskon;

    return total - totalDisc.value || 0;
  }
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
        <template #header>Detail Order Transaksi</template>
        <template #content>
          <div class="status-field-container-3-col tw-mb-5">
            <StatusBar
              :loading="loading"
              label="Nota Order :"
              :value="datas?.detail_faktur?.no_faktur || 'unknown'" />
            <StatusBar
              :loading="loading"
              label="Kode Principal :"
              :value="datas?.detail_faktur?.kode_principal || 'unknown'" />
            <StatusBar
              :loading="loading"
              label="Nama Principal :"
              :value="datas?.detail_faktur?.nama_principal || 'unknown'" />
            <StatusBar
              :loading="loading"
              label="Kode Customer :"
              :value="datas?.detail_faktur?.kode_customer || 'unknown'" />
            <StatusBar
              :loading="loading"
              label="Nama Customer :"
              :value="datas?.detail_faktur?.nama_customer || 0" />
            <StatusBar
              :loading="loading"
              label="Tanggal Order :"
              :value="
                format(
                  new Date(datas?.detail_faktur?.tanggal_order || null),
                  'dd-MM-yyyy'
                ) || ''
              " />
          </div>
        </template>
      </Card>
      <Card :no-subheader="true" class="tw-mt-5">
        <template #header>Verifikasi Promo</template>
        <template #content>
          <div class="tw-w-full tw-pb-20 tw-flex tw-flex-col tw-gap-4">
            <Table
              :key="tableKey"
              @remove-row="(val) => removeData(val)"
              classic
              :loading="loading"
              :table-data="tableData"
              :columns="detailKonfirmasiVoucherRegularColumn" />
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
