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
import FlexBox from "@/src/components/ui/FlexBox.vue";
import Button from "@/src/components/ui/Button.vue";
import {calculateKonversi, fetchWithAuth} from "@/src/lib/utils";
import {$swal} from "@/src/components/ui/SweetAlert.vue";
import {useAlert} from "@/src/store/alert";
import {tableListInsertRetur} from "@/src/model/tableColumns/listInsertRetur";

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

const checkIssameWithRequest = (item) => {
  const dataPengajuan = calculateKonversi({
    pieces: item.pieces_retur || 0,
    box: item.box_retur || 0,
    karton: item.karton_retur || 0
  }, item.uom_list)
  const dataRetur = calculateKonversi({
    pieces: (item.pieces_diajukan + item.pieces_good_diajukan) || 0,
    box: (item.box_diajukan + item.box_good_diajukan) || 0,
    karton: (item.karton_diajukan + item.karton_good_diajukan) || 0
  }, item.uom_list)
  return dataPengajuan.pieces !== dataRetur.pieces
};

const handleSubmitRetur = async () => {
  console.log("handleSubmitRetur called", returStore.detailRetur.items);
  returStore.detailRetur.items.forEach(
      (item) => {
        if (checkIssameWithRequest(item)) {
          $swal.error(
              `Jumlah retur untuk ${item.nama_produk} tidak sesuai dengan yang diajukan`,
          );
          throw Error(`Jumlah retur untuk ${item.nama_produk} tidak sesuai dengan yang diajukan`);
        }
      }
  )

  const confirm = await $swal.confirmSubmit(
      "Apakah Anda yakin ingin mengirim data ini?"
  )
  if (!confirm) return;
  try {

    await fetchWithAuth(
        "POST",
        `${process.env.VUE_APP_API_URL}/api/retur/insert-retur-stock/${idRequest}`,
        {
          items: returStore.detailRetur.items
        }
    )
    alert.setMessage("Retur berhasil dikirim", "success");
    router.replace('/retur');
  } catch (error) {
    $swal.error("Gagal mengirim retur", error || "Terjadi kesalahan");
    console.error("Error while cetak KPR:", error);
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
        <template #header>Detail KPR</template>
        <template #content>
          <div class="status-field-container-4-col tw-mb-5">
            <StatusBar
                label="No. KPR"
                :value="returStore.detailRetur.detail.kode_kpr"/>
            <StatusBar label="Customer" :value="returStore.detailRetur.detail.nama"/>
            <StatusBar label="Jumlah Barang" :value="returStore.detailRetur.detail.jumlah_barang"/>
          </div>
        </template>
      </Card>
      <Card :no-subheader="true" class="tw-mb-6">
        <template #header>Form Retur</template>
        <template #content>
          <div class="tw-w-full tw-py-6">
            <Table :key="tableKey" :table-data="returStore.detailRetur.items" :columns="tableListInsertRetur"
                   :loading="returStore.detailRetur.loading"/>
            <FlexBox full jusEnd class="tw-mt-4">
              <Button
                  :loading="loading"
                  class="tw-w-32 tw-mt-6 tw-py-4" :trigger="handleSubmitRetur">
                Submit Retur
              </Button>
            </FlexBox>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
