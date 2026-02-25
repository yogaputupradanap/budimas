<script setup>
import { useRoute } from "vue-router";
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import { listSetoranDetailColumn } from "@/src/model/tableColumns/setoran-tunai/listSetoranDetail";
import { setoranService } from "@/src/services/setoran";
import { usePagination } from "@/src/lib/usePagination";
import { useFiltering } from "@/src/lib/useFiltering";
import { useSorting } from "@/src/lib/useSorting";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import { nextTick, onMounted, ref } from "vue";
import { useAlert } from "@/src/store/alert";
import { parseCurrency } from "@/src/lib/utils";
import Label from "@/src/components/ui/Label.vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import { BFormInput } from "bootstrap-vue-next";
import Image from "@/src/components/ui/Image.vue";
import Struk from "@/src/assets/images/struk.png";
import Modal from "@/src/components/ui/Modal.vue";

const route = useRoute();
const id_sales_order = route.params.id_sales_order;
const id_customer = route.params.id_customer;
const fakturData = ref({});
const loadingData = ref(true);
const alert = useAlert();
const modal = ref();
const modalData = ref([]);

const { endpoints } = setoranService;
const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();
const { onSortingChange, sorting } = useSorting();

const [data, count, loading, totalPage, key] = useFetchPaginate(
  `${endpoints.setoranDetailTunai}/${id_sales_order}?`,
  {
    pagination,
    sorting,
    globalFilters,
    initialSortColumn: "id",
  }
);
const showModalWithData = ({ value, rowIndex, columnId }) => {
  const entries = Object.entries(value).filter(
    ([key]) => key === "nama_sales" || key === "bukti_transfer"
  );

  modalData.value = Object.fromEntries(entries);

  nextTick(() => {
    modal.value.show();
  });
};

const detailFaktur = async () => {
  try {
    const response = await setoranService.detailFakturTunai(
      id_customer,
      id_sales_order
    );
    if (response) {
      fakturData.value = response;
      // console.log(response);
    }
  } catch (error) {
    alert.setMessage(error.message || "An error occurred", "danger");
  } finally {
    loadingData.value = false;
  }
};

onMounted(() => {
  detailFaktur();
});

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
      <Card no-subheader>
        <template #header>Data faktur</template>
        <template #content>
          <div class="form-grid-card">
            <Label label="No Faktur">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                :model-value="fakturData?.no_faktur"
                disabled
              />
            </Label>
            <Label label="Angsuran">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                :model-value="parseCurrency(fakturData?.angsuran)"
                disabled
              />
            </Label>
            <Label label="Status Order">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                :model-value="fakturData?.status_order"
                disabled
              />
            </Label>
            <Label label="Tanggal Tatuh Tempo">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                :model-value="fakturData?.tanggal_jatuh_tempo"
                disabled
              />
            </Label>
            <Label label="Total Order">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                :model-value="parseCurrency(fakturData?.total_order)"
                disabled
              />
            </Label>
          </div>
        </template>
      </Card>
    </SlideRightX>
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
        <template #header>List Detail Setoran Tunai</template>
        <template #content>
          <Modal id="modal" @modal-closed="resetFormModal" ref="modal">
            <Card no-subheader>
              <template #header>Bukti Pembayaran</template>
              <template #content>
                <Label label="Nama PJ" full>
                  <Skeleton v-if="loadingData" class="skeleton" />
                  <BFormInput
                    v-else
                    :model-value="modalData?.nama_sales"
                    disabled
                  />
                </Label>
                <Label full label="Bukti Pembayaran :" class="tw-mt-4">
                  <FlexBox full jus-center>
                    <Image
                      :src="modalData?.bukti_transfer"
                      class="tw-w-96 tw-h-auto"
                      object-fit
                      alt="bukti setoran tunai"
                    />
                    
                  </FlexBox>
                </Label>
              </template>
            </Card>
          </Modal>
          <ServerTable
            table-width="tw-w-[90vw]"
            :columns="listSetoranDetailColumn"
            :key="key"
            :table-data="data"
            :loading="loading"
            :on-pagination-change="onPaginationChange"
            :on-global-filters-change="onColumnFilterChange"
            :on-sorting-change="onSortingChange"
            :pagination="pagination"
            :sorting="sorting"
            :filter="globalFilters"
            :page-count="totalPage"
            :total-data="count"
            @open-row-modal="(val) => showModalWithData(val)"
          />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>