<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";

import Table from "../components/ui/table/Table.vue";
import {useKepalaCabang} from "../store/kepalaCabang";
import {onMounted, ref} from "vue";
import SelectInputV2 from "@/src/components/ui/formInput/SelectInputV2.vue";
import Button from "@/src/components/ui/Button.vue";
import FlexBox from "@/src/components/ui/FlexBox.vue";
import {tableListPengajuan} from "@/src/model/tableColumns/listPengajuan";
import {useListRute} from "@/src/store/listRute";
import {useRetur} from "@/src/store/retur";

const kepalaCabang = useKepalaCabang();
const returStore = useRetur()
const ruteStore = useListRute()
const tableKey = ref(0);
const selectedRute = ref(null);

const handleCari = async () => {
  if (!selectedRute.value) return;
  await returStore.getListPengajuan(selectedRute.value);
  tableKey.value++;
};

onMounted(
    async () => {
      returStore.listPengajuan.listPengajuan = [];
    }
)

</script>

<template>
  <div class="tw-flex tw-flex-col tw-w-full tw-gap-4 lg:tw-px-4 tw-px-0">
    <SlideRightX class="" :duration-enter="0.6" :duration-leave="0.6" :delay-out="0.1" :delay-in="0.1" :initial-x="-40"
                 :x="40">
      <Card :no-subheader="true" class="tw-mb-6 ">
        <template #header>Cari Pengajuan</template>
        <template #content>
          <div class="tw-grid tw-grid-cols-1 lg:tw-grid-cols-2 tw-mb-8 tw-w-full tw-gap-2">
            <BFormGroup
                class="tw-w-1/2"
                id="input-group-6"
                label="Rute"
                label-for="input-6"
            >
              <SelectInputV2
                  v-model="selectedRute"
                  :options="ruteStore.arraySOD"
                  placeholder="Pilih Rute"
                  text-field="nama_rute"
                  value-field="id"
                  virtual-scroll="true"
              />
            </BFormGroup>
            <FlexBox full jusEnd class="tw-mb-4">
              <Button
                  class="tw-w-32 tw-mt-6"
                  icon="mdi mdi-magnify"
                  :trigger="handleCari"
              >
                Cari
              </Button>
            </FlexBox>
          </div>
        </template>
      </Card>
      <Card :no-subheader="true" class="tw-mb-6">
        <template #header>List Pengajuan</template>
        <template #content>
          <div class="tw-w-full tw-py-6">

            <Table :key="tableKey" :table-data="returStore.listPengajuan.listPengajuan" :columns="tableListPengajuan"
                   :loading="returStore.listPengajuan.loading"/>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
