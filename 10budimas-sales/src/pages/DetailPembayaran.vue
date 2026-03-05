<script setup>
import Card from "../components/ui/Card.vue";
import FlexBox from "../components/ui/FlexBox.vue";
import SlideRightX from "../components/animation/SlideRightX.vue";
import TextField from "../components/ui/formInput/TextField.vue";
import { useCommonForm } from "../lib/useCommonForm";
import { pembayaranSchema } from "../model/formSchema";
import { usePembayaran } from "../store/pembayaran";
import { apiUrl, fetchWithAuth, parseCurrency, parseNumberFromCurrency } from "../lib/utils";
import Button from "../components/ui/Button.vue";
import { inject, onMounted, ref } from "vue";
import { useAlert } from "../store/alert";
import { useRoute } from "vue-router";
import { useSales } from "../store/sales";
import Table from "../components/ui/table/Table.vue";
import { ListDetailPembayaranColumn } from "../model/tableColumns";

const sales = useSales();
const pembayaranStore = usePembayaran();
const alert = useAlert();
const route = useRoute();
const { handleSubmit, configProps, defineField } =
  useCommonForm(pembayaranSchema);
const localStore = ref({});
const riwayatPembayaran = ref([]);
const loading = ref(false);

const [jumlahBayar, jumlahBayarProps] = defineField("jumlahBayar", configProps);

const $swal = inject("$swal");

const onSubmit = handleSubmit(async (values) => {
  try {
    const jumlahBayarNum = parseNumberFromCurrency(values.jumlahBayar, {
      precision: true
    });

    if (jumlahBayarNum <= (localStore.value.total_penjualan - (localStore.value.jumlah_bayar || 0) - (localStore.value.nominal_retur || 0))) {
      const isConfirm = await $swal.confirmSubmit();
      if (!isConfirm) {
        return;
      }

      await fetchWithAuth("POST", `${apiUrl}/api/finance/create-payment`, {
        ...values,
        jumlahBayar: jumlahBayarNum,
        notaFaktur: localStore.value.id_sales_order,
        id_sales: sales.salesUser.sales.id
      });

      alert.setMessage(
        `Berhasil melakukan pembayaran sebesar : \n Rp. ${parseCurrency(
          jumlahBayarNum
        )} pada faktur ${localStore.value.no_faktur}`,
        "success"
      );
      await getRiwayatPembayaran();
    } else {
      alert.setMessage(
        "Jumlah bayar melebihi jumlah tagihan faktur",
        "warning"
      );
    }
  } catch (error) {
    alert.setMessage(error, "danger");
  }
});

const getDetailPembayaran = () => {
  const detailPembayaran = pembayaranStore.listPembayaran.find(
    (val) => val.id_sales_order == route.params.id_sales_order
  );

  localStore.value = detailPembayaran;

  const sisa_pembayaran =
    detailPembayaran?.total_penjualan - (detailPembayaran?.jumlah_bayar || 0) - (detailPembayaran?.nominal_retur || 0);
  jumlahBayar.value = parseCurrency(sisa_pembayaran);
};

const getRiwayatPembayaran = async () => {
  try {
    loading.value = true;
    const res = await fetchWithAuth(
      "GET",
      `${apiUrl}/api/finance/riwayat-setoran-customer?id_sales_order=${route.params.id_sales_order}`
    );

    riwayatPembayaran.value = res.data || res;
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  getDetailPembayaran();
  getRiwayatPembayaran();
});
</script>

<template>
  <FlexBox full flex-col class="lg:tw-pl-4 tw-pl-2">
    <SlideRightX
      class="tw-w-full"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card dense>
        <template #header>Nota Tagihan</template>
        <template #subheader>
          <span class="tw-text-black tw-font-semibold">
            {{ localStore?.no_faktur }}
          </span>
        </template>
        <template #content>
          <div class="tw-grid tw-grid-cols-1 xl:tw-grid-cols-4 tw-gap-4">
            <FlexBox flex-col gap="small">
              <span class="tw-font-semibold">Nama Principal</span>
              <BFormInput
                class="tw-truncate"
                plaintext
                :title="localStore?.nama_principal"
                :model-value="localStore?.nama_principal" />
            </FlexBox>
            <FlexBox flex-col gap="small">
              <span class="tw-font-semibold">Nama Customer</span>
              <BFormInput
                class="tw-truncate"
                plaintext
                :title="localStore?.nama_customer"
                :model-value="localStore?.nama_customer" />
            </FlexBox>
            <FlexBox flex-col gap="small">
              <span class="tw-font-semibold">Jatuh Tempo</span>
              <BFormInput
                plaintext
                :model-value="localStore?.tanggal_jatuh_tempo" />
            </FlexBox>
            <FlexBox flex-col gap="small">
              <span class="tw-font-semibold">Total Pembayaran</span>
              <BFormInput
                plaintext
                :model-value="`Rp. ${parseCurrency(
                  localStore?.jumlah_bayar
                )}`" />
            </FlexBox>
          </div>
        </template>
      </Card>
    </SlideRightX>
    <FlexBox full jus-between class="tw-flex-col lg:tw-flex-row">
      <SlideRightX
        class="tw-w-full"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.3"
        :delay-out="0.3"
        :initial-x="-40"
        :x="40">
        <Card dense no-subheader>
          <template #header>Form Pembayaran</template>
          <template #content>
            <FlexBox full class="tw-pb-6">
              <BForm
                novalidate
                class="tw-w-full tw-flex tw-flex-col tw-gap-6 tw-px-0 xl:tw-px-20">
                <TextField
                  placeholder="Masukkan Jumlah Yang Dibayar"
                  type="currency"
                  label-for="input-2"
                  label="Jumlah Yang Dibayarkan"
                  group-id="input-group-2"
                  v-model="jumlahBayar"
                  :precision="true"
                  :config-props="jumlahBayarProps" />
                <FlexBox full jus-end class="tw-mt-8">
                  <Button
                    :trigger="onSubmit"
                    class="tw-bg-green-500 tw-border-none tw-w-28 tw-h-8">
                    Submit
                  </Button>
                </FlexBox>
              </BForm>
            </FlexBox>
          </template>
        </Card>
      </SlideRightX>
    </FlexBox>
    <FlexBox full jus-between class="tw-flex-col lg:tw-flex-row">
      <SlideRightX
        class="tw-w-full"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.3"
        :delay-out="0.3"
        :initial-x="-40"
        :x="40">
        <Card dense no-subheader>
          <template #header>Riwayat Pembayaran</template>
          <template #content>
            <FlexBox full class="tw-pb-6">
              <Table
                :loading="loading"
                :columns="ListDetailPembayaranColumn"
                :table-data="riwayatPembayaran" />
            </FlexBox>
          </template>
        </Card>
      </SlideRightX>
    </FlexBox>
  </FlexBox>
</template>
