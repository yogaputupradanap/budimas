<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Table from "../components/ui/table/Table.vue";
import { StockOpnameColumns } from "../model/tableColumns";
import Card from "../components/ui/Card.vue";
import SelectInput from "../components/ui/formInput/SelectInput.vue";
import { onMounted, ref, watch } from "vue";
import FlexBox from "../components/ui/FlexBox.vue";
import { usePrincipal } from "../store/principal";
import { useKunjungan } from "../store/kunjungan";
import Button from "../components/ui/Button.vue";
import { apiUrl, fetchWithAuth } from "../lib/utils";
import { useSales } from "../store/sales";
import { useAlert } from "../store/alert";
import { useDashboard } from "../store/dashboard";

const dashboardStore = useDashboard();
const principalStore = usePrincipal();
const kunjungan = useKunjungan();
const sales = useSales();
const alert = useAlert();
const principal = ref(principalStore?.principals[0]?.id);
const localPrincipalProduct = ref([]);

const stockOpname = async () => {
  const opname = {
    id_sales: sales.salesUser.sales.id,
    id_principal: principal.value,
    id_customer: kunjungan.activeKunjungan.kunjungan.customer_id,
    products: localPrincipalProduct.value.map((product) => ({
      id_produk: product.id,
      pieces: product?.pieces || 0,
      box: product?.box || 0,
      karton: product?.karton || 0,
    })),
  };

  try {
    await fetchWithAuth("POST", `${apiUrl}/api/sales/stock-opname`, opname);

    alert.setMessage(`Berhasil stock opname`, "success");
  } catch (error) {
    alert.setMessage(error, "warning");
  }

  resetLocalPrincipal();
};

const change = ({ value, rowIndex, columnId }) => {
  localPrincipalProduct.value = localPrincipalProduct.value.map(
    (product, idx) => {
      if (rowIndex === idx) {
        return {
          ...product,
          [columnId]: value,
        };
      }

      return { ...product };
    }
  );
};

const resetLocalPrincipal = () => {
  localPrincipalProduct.value = principalStore.stockOpnameProducts
    .filter((product) => product.id_principal === principal.value)
    .map((product, idx) => ({ no: idx + 1, ...product }));

  principalStore.principalProduct.tableKey++;
};

const fetchPrincipalProducts = async () => {
  if (!principalStore.principalProduct.products.length)
    await principalStore.getPrincipalProducts();
  console.log("stock opname product : ", principalStore.stockOpnameProducts);

  resetLocalPrincipal();
};

onMounted(() => {
  fetchPrincipalProducts();
});

watch(principal, () => resetLocalPrincipal());
</script>

<template>
  <FlexBox full flex-col class="lg:tw-pl-6 tw-pl-2">
    <SlideRightX
      class="tw-z-10 tw-w-full"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card no-header no-subheader class="tw-p-6">
        <template #content>
          <FlexBox
            full
            it-center
            class="tw-w-full tw-flex-wrap md:tw-flex-nowrap">
            <span class="tw-text-xl tw-font-bold">Pilih Principal :</span>
            <div class="tw-w-auto tw-min-w-[200px]">
              <SelectInput
                text-field="nama"
                value-field="id"
                :options="principalStore.principals"
                v-model="principal"
                size="sm" />
            </div>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="tw-w-full"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card no-subheader>
        <template #header>Daftar Barang</template>
        <template #content>
          <FlexBox full flex-col class="tw-pb-10">
            <Table
              :key="principalStore.principalProduct.tableKey"
              :columns="StockOpnameColumns"
              :table-data="localPrincipalProduct"
              classic
              @change="change"
              :loading="principalStore.principalProduct.loading" />
            <FlexBox full jus-end>
              <Button
                :trigger="stockOpname"
                class="tw-bg-green-500 tw-text-white tw-w-28 tw-border-none">
                Submit
              </Button>
            </FlexBox>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
