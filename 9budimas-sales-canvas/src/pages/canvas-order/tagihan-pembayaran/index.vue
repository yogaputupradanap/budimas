<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Button from "@/src/components/ui/Button.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import Table from "@/src/components/ui/table/Table.vue";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";
import { ref, onMounted, computed, watch, inject } from "vue";
import { listRiwayatPembayaranColumn } from "@/src/model/tableColumns/canvas-order/pembayaran";
import { salesCanvasService } from "@/src/services/salesCanvas";
import { parseCurrency } from "@/src/lib/utils";
import { useUser } from "@/src/store/user";
import { useRoute } from "vue-router";
import { useOthers } from "@/src/store/others";
import { useSorting } from "@/src/lib/useSorting";
import { usePagination } from "@/src/lib/usePagination";
import { useFiltering } from "@/src/lib/useFiltering";

const route = useRoute();
const userStore = useUser();
const $swal = inject("$swal");

// Initial Data
const initialPembayaranData = ref([]);
const nominalJumlahDibayarkan = ref(0);

// userStore Data
const user = userStore.user.value;
const canvasOrderId = route.params.id_canvas_order;
const principalName = computed(() => user?.principal)

const { endpoints } = salesCanvasService;
const { sorting } = useSorting();
const { pagination } = usePagination();
const { globalFilters } = useFiltering();

const [data, count, loading, totalPage, key] = useFetchPaginate(
  endpoints,
  {
    pagination,
    sorting,
    globalFilters,
    initialSortColumn: "nama_produk",
  }
);

const totalTagihan = computed(() => {
  if (initialPembayaranData.value.length > 0) {
    return initialPembayaranData.value[0].total_tagihan || 0;
  }
});

const customerName = computed(() => {
  if (initialPembayaranData.value.length > 0) {
    return initialPembayaranData.value[0].nama_customer || "-";
  }
});

const fetchTagihanPembayaran = async () => {
  if (!canvasOrderId) return;
  try {
    const res = await salesCanvasService.getListTagihanPembayaran(canvasOrderId);
    initialPembayaranData.value = Array.isArray(res?.pages) 
      ? res.pages : Array.isArray(res) 
      ? res : [];
  } catch (error) {
    console.error("Error fetching tagihan pembayaran:", error);
  }
};

const jumlahKekuranganDibayarkan = computed(() => {
  if (initialPembayaranData.value.length > 0) {
    const totalTagihanValue = initialPembayaranData.value[0].total_tagihan || 0;
    const totalDibayarkan = initialPembayaranData.value.reduce((sum, payment) => {
      return sum + (payment.nominal || 0);
    }, 0);
    return totalTagihanValue - totalDibayarkan;
  }
  return 0;
});

const submitTagihanPembayaran = async () => {
  if (!canvasOrderId || nominalJumlahDibayarkan.value <= 0) return;

  if (nominalJumlahDibayarkan.value > jumlahKekuranganDibayarkan.value) {
    return $swal.warning("Jumlah yang dibayarkan tidak boleh lebih dari kekurangan.");
  }

  try {
    await salesCanvasService.postTagihanPembayaran({
      id_canvas_order: canvasOrderId,
      jumlah_dibayarkan: nominalJumlahDibayarkan.value
    });

    await fetchTagihanPembayaran();
    key.value++;
    nominalJumlahDibayarkan.value = 0;
    $swal.success("Pembayaran Tagihan berhasil dilakukan.");
  } catch (error) {
    console.error("Error submitting tagihan pembayaran:", error);
  }
};

watch(jumlahKekuranganDibayarkan, (newVal) => {
  if (nominalJumlahDibayarkan.value === 0) {
    nominalJumlahDibayarkan.value = newVal;
  }
  else if (nominalJumlahDibayarkan.value > newVal) {
    return $swal.warning("Jumlah yang dibayarkan tidak boleh lebih dari kekurangan.");
  }
});

onMounted(async () => { await fetchTagihanPembayaran() });

</script>

<template>
  <FlexBox full flex-col>
    <SlideRightX
      class="slide-container tw-z-10"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40"
    >
      <Card subheader>
        <template #header>Nota Tagihan</template>
        <template #subheader>CVS-ExampleAutoNumber001</template>
        <template #content>
          <div class="form-grid-card tw-grid-cols-3 tw-items-end">
            <Label label="Principal">
              <BFormInput
                size="md"
                readonly
                placeholder="Principal"
                :model-value="principalName"
                :class="'tw-bg-gray-200'"
              />
            </Label>
             <Label label="Customer">
              <BFormInput
                size="md"
                readonly
                placeholder="Customer"
                :model-value="customerName"
                :class="'tw-bg-gray-200'"
              />
            </Label>
            <Label label="Total Tagihan">
              <BFormInput
                size="md"
                readonly
                placeholder="0"
                :class="'tw-bg-gray-200'"
                :model-value="parseCurrency(totalTagihan)"
              />
            </Label>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
  <FlexBox full flex-col>
    <SlideRightX
      class="slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40"
    >
    <Card no-subheader>
      <template #header>Form Pembayaran</template>
      <template #content>
        <div class="tw-w-full tw-px-8 md:tw-px-28">
          <Label label="Jumlah yang dibayarkan">
            <BFormInput
              type="number"
              size="md"
              placeholder="Nominal Jumlah yang dibayarkan"
              v-model="jumlahKekuranganDibayarkan"
              class="tw-bg-gray-200 tw-w-full"
            />
          </Label>
          <FlexBox
            full jus-center
            class="tw-mt-4 lg:tw-justify-end lg:tw-flex-row tw-flex-wrap-reverse"
          >
            <Button 
              :trigger="submitTagihanPembayaran"
              :disabled="jumlahKekuranganDibayarkan === 0"
              icon="mdi mdi-cash-multiple tw-mr-2"
              class="tw-px-8 tw-py-2 tw-text-sm tw-bg-green-500 hover:tw-bg-green-700"
            >
              Bayarkan
            </Button>
          </FlexBox>
        </div>
      </template>
      </Card>
      <Card no-subheader>
        <template #header>Riwayat Pembayaran</template>
        <template #content>
          <Table
            :key="key"
            :columns="listRiwayatPembayaranColumn"
            :table-data="initialPembayaranData"
            :hideFooter="false"
            :hide-toolbar="true"
          />
      </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
