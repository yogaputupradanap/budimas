<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";

import Table from "../components/ui/table/Table.vue";
import {useKepalaCabang} from "../store/kepalaCabang";
import {onMounted, ref} from "vue";
import {useListRute} from "@/src/store/listRute";
import {useRetur} from "@/src/store/retur";
import {useRoute, useRouter} from "vue-router";
import StatusBar from "@/src/components/ui/StatusBar.vue";
import {tableListPengajuanRetur} from "@/src/model/tableColumns/listPengajuanRetur";
import FlexBox from "@/src/components/ui/FlexBox.vue";
import Button from "@/src/components/ui/Button.vue";
import {useAlert} from "@/src/store/alert";
import {$swal} from "@/src/components/ui/SweetAlert.vue";
import generateReturPenjualanPDF from "@/src/lib/retur";
import {fetchWithAuth} from "@/src/lib/utils";

const route = useRoute()
const router = useRouter();
const kepalaCabang = useKepalaCabang();
const alert = useAlert();
const returStore = useRetur()
const ruteStore = useListRute()
const tableKey = ref(0);
const selectedRute = ref(null);
const idRequest = route.params.id_request;
const loading = ref(false);

const handleCetakKpr = async () => {
  const confirm = await $swal.confirmSubmit(
      "Apakah Anda yakin ingin mencetak KPR untuk pengajuan ini?",
  )
  if (!confirm) return;
  try {
    const clause = {
      id_request: `='${idRequest}'`,
    }
    const updatedData = await fetchWithAuth(
        "PATCH",
        `${process.env.VUE_APP_API_URL}/api/retur/cetak-kpr/${idRequest}`,
        {
          status_request: 1,
          kode_kpr: returStore.detailRetur.detail.kode_kpr,
        }
    )
    const dataMapping = returStore.detailRetur.items.map((item, index) =>
        [
          index + 1,
          item.kode_sku,
          item.nama_produk,
          `${item.pieces_retur} PC`,
          `${item.box_retur} BOX`,
          `${item.karton_retur} CT`,
          item.alasan_retur
        ]
    );
    generateReturPenjualanPDF(
        {
          data: dataMapping,
          info: returStore.detailRetur.detail,
        }
    )
    alert.setMessage("KPR berhasil dicetak", "success");
    router.replace('/retur/list-pengajuan');
  } catch (error) {
    console.error("Error while cetak KPR:", error);
    alert.setMessage("Gagal mencetak KPR " + error.message, "error");
  }
};

onMounted(
    async () => {
      returStore.detailRetur.detail = {
        header: {},
        detail: [],
      }
      await returStore.getDetailRetur(idRequest)
      tableKey.value++;
    }
)

</script>

<template>
  <div class="tw-flex tw-flex-col tw-w-full tw-gap-4 lg:tw-px-4 tw-px-0">
    <SlideRightX class="" :duration-enter="0.6" :duration-leave="0.6" :delay-out="0.1" :delay-in="0.1" :initial-x="-40"
                 :x="40">
      <Card :no-subheader="true" class="tw-mb-6 ">
        <template #header>Detail Pengajuan Retur</template>
        <template #content>
          <div class="status-field-container-4-col tw-mb-5">
            <StatusBar
                label="No. KPR"
                :value="returStore.detailRetur.detail.kode_kpr"/>
            <StatusBar label="Customer" :value="returStore.detailRetur.detail.nama"/>
            <StatusBar label="Rute" :value="returStore.detailRetur.detail.nama_rute"/>
            <StatusBar label="Jumlah Barang" :value="returStore.detailRetur.detail.jumlah_barang"/>
          </div>
        </template>
      </Card>
      <Card :no-subheader="true" class="tw-mb-6">
        <template #header>List Pengajuan Retur</template>
        <template #content>
          <div class="tw-w-full tw-py-6">
            <Table :key="tableKey" :table-data="returStore.detailRetur.items" :columns="tableListPengajuanRetur"
                   :loading="returStore.detailRetur.loading"/>
            <FlexBox full jusEnd class="tw-mt-4">
              <Button
                  :loading="loading"
                  class="tw-w-32 tw-mt-6 tw-py-4" :trigger="handleCetakKpr">
                Cetak KPR
              </Button>
            </FlexBox>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
