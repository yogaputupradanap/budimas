<script setup>
import Faktur from "./Faktur.vue";
import { ref, onMounted } from "vue";
import { useShipping } from "@/src/store/shipping";

const props = defineProps({
  list: {
    type: Array,
    default: () => [],
  },
  info: {
    type: Object,
    default: () => ({}),
  }
});

const shipping = useShipping();
const processedFakturList = ref([]);
const isProcessing = ref(true);

// Proses semua faktur untuk ditampilkan
const processFakturData = async () => {
  isProcessing.value = true;
  processedFakturList.value = [];
  
  if (!props.list || props.list.length === 0) {
    isProcessing.value = false;
    return;
  }
  
  // Proses semua faktur secara berurutan
  for (const faktur of props.list) {
    try {
      // Ambil detail faktur
      await shipping.getListDetailFakturShipping(faktur.id_sales_order);
      
      if (shipping.listDetailFakturShipping.detailFaktur && 
          shipping.listDetailFakturShipping.detailFakturInfo) {
        // Tambahkan ke daftar faktur yang akan ditampilkan
        processedFakturList.value.push({
          fakturInfo: shipping.listDetailFakturShipping.detailFakturInfo,
          detailFaktur: shipping.listDetailFakturShipping.detailFaktur,
        });
      }
    } catch (error) {
      console.error(`Error processing faktur ${faktur.id_sales_order}:`, error);
    }
  }
  
  isProcessing.value = false;
};

onMounted(() => {
  processFakturData();
});
</script>

<template>
  <div id="all-faktur">
    <div v-if="isProcessing" class="tw-text-center tw-my-4">
      Memproses faktur...
    </div>
    
    <div v-for="(faktur, index) in processedFakturList" :key="index" class="faktur-container">
      <!-- Render Faktur component for each processed faktur -->
      <Faktur 
        :info="faktur.fakturInfo"
        :list="faktur.detailFaktur"
        :title="'penjualan'" 
        :is-retur="false" />
      
      <!-- Add page break after each faktur except the last one -->
      <div v-if="index < processedFakturList.length - 1" class="page-break"></div>
    </div>
    
    <div v-if="processedFakturList.length === 0 && !isProcessing" class="tw-text-center tw-my-4">
      Tidak ada faktur untuk dicetak
    </div>
  </div>
</template>

<style scoped>
.faktur-container {
  page-break-inside: avoid;
}

.page-break {
  page-break-after: always;
}

@media print {
  .faktur-container {
    page-break-inside: avoid;
  }
  
  .page-break {
    page-break-after: always;
  }
}
</style>