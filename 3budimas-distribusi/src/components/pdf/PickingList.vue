<script setup>
import { useKepalaCabang } from "@/src/store/kepalaCabang";
import { computed } from "vue";
import budimasImage from "../../assets/images/logo-budimas-black.png";

const props = defineProps({
  pickingList: {
    type: Array,
    default() {
      return [];
    },
  },
  info: {
    type: Object,
    default() {
      return {};
    },
  },
});

const kepalaCabang = useKepalaCabang();

/*
  SAFE ACCESS STORE
*/
const namaKepalaCabang = computed(
  () => kepalaCabang.kepalaCabangUser?.nama || "-"
);

const namaCabang = computed(
  () => kepalaCabang.kepalaCabangUser?.kepalaCabang?.nama_cabang || "-"
);

const capitalizeNamaCabang = computed(() => {
  if (!namaCabang.value || namaCabang.value === "-") return "-";
  return (
    namaCabang.value.substring(0, 1).toUpperCase() +
    namaCabang.value.slice(1).toLowerCase()
  );
});

const noPicking = Date.now();

/*
  GROUPING PRODUCT
*/
const categorizedProduct = computed(() =>
  props.pickingList.reduce((acc, val) => {
    if (acc[val.nama_principal]) {
      acc[val.nama_principal].push(val);
    } else {
      acc[val.nama_principal] = [val];
    }
    return acc;
  }, {})
);

const getCategorizedProductKey = computed(() =>
  Object.keys(categorizedProduct.value)
);
const getJumlahOrder = (val) => Number(val.total_in_pieces || 0);
</script>

<template>
  <div id="picking-list" class="tw-w-full tw-text-[12px] tw-p-4">
    <div class="tw-text-center tw-mb-4">
      <img :src="budimasImage" class="tw-w-[80px] tw-mx-auto" />
      <h1 class="tw-font-bold tw-text-xl">Picking List</h1>
      <p>No Picking: {{ noPicking }}</p>
    </div>

    <div class="tw-mb-4">
      <p>Cabang : {{ capitalizeNamaCabang }}</p>
      <p>Rute : {{ info?.nama_rute }}</p>
      <p>Driver : {{ info?.nama_driver }}</p>
      <p>Armada : {{ info?.nama_armada }}</p>
    </div>

    <div v-for="principal in getCategorizedProductKey" :key="principal">
      <h3 class="tw-font-bold tw-mt-3">{{ principal }}</h3>

      <div
        v-for="item in categorizedProduct[principal]"
        :key="item.produk_id"
        class="tw-flex tw-justify-between tw-border-b tw-py-1"
      >
        <span class="tw-w-52">{{ item.nama_produk }}</span>
        <span class="tw-w-32">{{ item.kode_sku }}</span>
        <span class="tw-w-20">{{ getJumlahOrder(item) }}</span>
      </div>
    </div>

    <div class="tw-mt-16 tw-text-right">
      <p>{{ namaKepalaCabang }}</p>
      <div class="tw-border-b tw-w-40 tw-ml-auto"></div>
      <p>Kepala Cabang</p>
    </div>
  </div>
</template>
