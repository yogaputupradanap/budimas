<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import Label from "@/src/components/ui/Label.vue";
import Modal from "@/src/components/ui/Modal.vue";
import { detailTagihanPurchasingColumn } from "@/src/model/tableColumns/tagihan-purchasing/detail-tagihan-purchasing/detailTagihanPurchasing";
import { nextTick, onMounted, ref } from "vue";
import { BFormInput, BFormTextarea } from "bootstrap-vue-next";
import Image from "@/src/components/ui/Image.vue";
import Struk from "@/src/assets/images/struk.png";
import { useAlert } from "@/src/store/alert";
import { useRoute } from "vue-router";
import { hutangService } from "@/src/services/hutang";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import { parseCurrency } from "@/src/lib/utils";
import Button from "@/src/components/ui/Button.vue";
import NoImage from "@/src/assets/images/no-image.svg";

const alert = useAlert();
const route = useRoute();
const modalRef = ref();

const tableData = ref([]);
const tableKey = ref(0);
const notaData = ref({});
const loading = ref(false);

const surat_tagihan = route.params.surat_tagihan;

const handleShowBukti = async () => {
  await nextTick();
  modalRef.value?.show();
  return Promise.resolve();
};

const getDetail = async () => {
  try {
    loading.value = true;
    
    const responseTable = await hutangService.detailHutang(surat_tagihan);
    const responseNota = await hutangService.detailTagihanNota(surat_tagihan);

    console.log("Raw Table Data:", responseTable);
    console.log("Raw Nota Data:", responseNota);

    // 1. Normalisasi Table Data
    // Berdasarkan log Anda: responseTable langsung punya properti .result
    if (responseTable && Array.isArray(responseTable.result)) {
      tableData.value = responseTable.result;
    } else {
      tableData.value = [];
    }

    // 2. Normalisasi Nota Data
    // Pastikan variabel didefinisikan dan digunakan dengan nama yang sama
    const notaSource = responseNota?.result || responseNota?.data || responseNota;
    
    if (Array.isArray(notaSource) && notaSource.length > 0) {
      // Mengambil objek pertama dari array result
      notaData.value = notaSource[0];
    } else if (notaSource && typeof notaSource === 'object' && !Array.isArray(notaSource)) {
      // Jika ternyata API mengembalikan objek langsung
      notaData.value = notaSource;
    } else {
      notaData.value = {};
    }

  } catch (error) {
    console.error("Detail Fetch Error:", error);
    alert.setMessage(error.message || "Gagal memuat detail", "danger");
  } finally {
    loading.value = false;
    tableKey.value++; 
  }
};

console.log(Object.keys(window.notaData || {}));

onMounted(() => getDetail());
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
      <Card>
        <template #header>Surat Tagihan Purchasing</template>
        <template #subheader>{{ surat_tagihan }}</template>
        <template #content>
          <div
            class="tw-w-full tw-grid tw-grid-cols-1 lg:tw-grid-cols-3 tw-gap-2"
          >
            <Label label="Nama Principal">
              <Skeleton v-if="loading" class="skeleton" />
              <BFormInput
                v-else
                :model-value="notaData?.nama_principal"
                disabled
              />
            </Label>
            <Label label="Kode Principal">
              <Skeleton v-if="loading" class="skeleton" />
              <BFormInput
                v-else
                :model-value="notaData?.kode_principal"
                disabled
              />
            </Label>
            <Label label="Total Pembayaran">
              <Skeleton v-if="loading" class="skeleton" />
              <BFormInput
                v-else
                :model-value="parseCurrency(notaData?.total_tagihan)"
                disabled
              />
            </Label>
            <Label label="Tanggal Pembayaran">
              <Skeleton v-if="loading" class="skeleton" />
              <BFormInput
                v-else
                :model-value="notaData?.tanggal_bayar"
                disabled
              />
            </Label>
            <Label label="PIC Pembayaran">
              <Skeleton v-if="loading" class="skeleton" />
              <BFormInput
                v-else
                :model-value="notaData?.pic_pembayaran"
                disabled
              />
            </Label>
            <Label label="Cabang">
              <Skeleton v-if="loading" class="skeleton" />
              <BFormInput
                v-else
                :model-value="notaData?.nama_cabang"
                disabled
              />
            </Label>
            <Label label="Keterangan" full>
              <Skeleton v-if="loading" class="skeleton" />
              <BFormTextarea
                v-else
                :model-value="notaData?.keterangan"
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
        <template #header>List Tagihan</template>
        <template #content>
          <Modal
            id="modalRef"
            ref="modalRef"
            centered
            :hide-header="false"
            :title="`Detail Transfer ${surat_tagihan}`"
          >
            <Card dense no-header no-subheader no-main-center class="tw-p-4">
              <template #content>
                <FlexBox full no-left-padding flex-col it-center>
                  <Label full label="Principal">
                    <BFormInput
                      :model-value="notaData?.nama_principal"
                      disabled
                    />
                  </Label>
                  <Label full label="Total Pembayaran">
                    <BFormInput
                      :model-value="parseCurrency(notaData?.total_tagihan)"
                      disabled
                    />
                  </Label>
                  <Label full label="Bukti Pembayaran :" class="tw-mt-4">
                    <FlexBox full jus-center>
                      <Image
                        :src="notaData?.bukti_bayar 
                              ? `https://storage.googleapis.com/buktitransaksi/${notaData.bukti_bayar}` 
                              : NoImage"
                        class="tw-w-full tw-max-h-[500px]" 
                        object-fit="contain"
                        alt="Bukti Bayar"
                      />
                    </FlexBox>
                  </Label>
                </FlexBox>
              </template>
            </Card>
          </Modal>
          <Table
            :key="tableKey"
            :loading="loading"
            @open-row-modal="(val) => openDetail(val)"
            :columns="detailTagihanPurchasingColumn"
            :table-data="tableData"
          />
          <FlexBox full jus-end class="tw-flex-col tw-items-end tw-gap-5">
            <FlexBox class="tw-gap-5">
              <span class="tw-font-semibold">Total Tagihan:</span>
              <span class="tw-text-gray-600">{{
                parseCurrency(notaData?.total_tagihan)
              }}</span>
            </FlexBox>
            <Button
              icon="mdi mdi-credit-card-check-outline"
              :trigger="handleShowBukti"
              class="tw-bg-blue-500 tw-px-4 tw-h-[34px]"
            >
              Lihat Bukti Pembayaran
            </Button>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
