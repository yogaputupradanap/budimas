<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import Label from "@/src/components/ui/Label.vue";
import Modal from "@/src/components/ui/Modal.vue";
import { detailTagihanSalesColumn } from "@/src/model/tableColumns/surat-tagihan-sales/detail-surat-tagihan-sales/detailSuratTagihanSales";
import { nextTick, onMounted, ref } from "vue";
import { BFormInput } from "bootstrap-vue-next";
import Image from "@/src/components/ui/Image.vue";
import Struk from "@/src/assets/images/struk.png";
import { useRoute } from "vue-router";
import { piutangService } from "@/src/services/piutang";
import { useAlert } from "@/src/store/alert";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import { parseCurrency } from "@/src/lib/utils";

const alert = useAlert();
const route = useRoute();
const modalRef = ref();
const modalValue = ref();

const tableData = ref([]);
const tableKey = ref(0);
const notaData = ref({});
const loading = ref(true);

const openDetail = ({ value }) => {
  modalValue.value = value;

  nextTick(() => {
    modalRef.value.show();
  });
};

const getDetail = async () => {
  const nota_tagihan = route.params.nota_tagihan;
  try {
    const table_data = await piutangService.detailPiutang(nota_tagihan);
    const nota = await piutangService.detailTagihanNota(nota_tagihan);

    tableData.value = table_data;
    notaData.value = nota[0];
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loading.value = false;
    tableKey.value++;
  }
};

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
      :x="40">
      <Card>
        <template #header>Surat Tagihan Sales</template>
        <template #subheader>
          <Skeleton
            class="tw-w-52 tw-h-[24px] tw-rounded-xl"
            v-if="loading"></Skeleton>
          <div v-else>
            {{ notaData?.no_tagihan }}
          </div>
        </template>
        <template #content>
          <div class="form-grid-card">
            <Label label="Kode Customer">
              <Skeleton v-if="loading" class="skeleton" />
              <BFormInput
                v-else
                :model-value="notaData?.kode_customer"
                disabled />
            </Label>
            <Label label="Nama Customer">
              <Skeleton v-if="loading" class="skeleton" />
              <BFormInput
                v-else
                :model-value="notaData?.nama_customer"
                disabled />
            </Label>
            <Label label="Kode Principal">
              <Skeleton v-if="loading" class="skeleton" />
              <BFormInput
                v-else
                :model-value="notaData?.kode_principal"
                disabled />
            </Label>
            <Label label="Total Pembayaran">
              <Skeleton v-if="loading" class="skeleton" />
              <BFormInput
                v-else
                :model-value="parseCurrency(notaData?.jumlah_setoran)"
                disabled />
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
      :x="40">
      <Card no-subheader>
        <template #header>List Tagihan</template>
        <template #content>
          <Modal
            id="modalRef"
            ref="modalRef"
            centered
            :hide-header="false"
            title="Detail Transfer">
            <Card dense no-header no-subheader no-main-center class="tw-p-4">
              <template #content>
                <FlexBox full no-left-padding flex-col it-center>
                  <!-- <Label full label="Bank Asal">
                    <BFormInput model-value="BCA" disabled />
                  </Label>
                  <Label full label="Bank Tujuan">
                    <BFormInput model-value="BCA" disabled />
                  </Label> -->
                  <Label full class="tw-mt-4">
                    <FlexBox full jus-center>
                      <Image
                        :src="Struk"
                        class="tw-w-96 tw-h-auto"
                        object-fit
                        alt="bukti setoran tunai" />
                    </FlexBox>
                  </Label>
                </FlexBox>
              </template>
            </Card>
          </Modal>
          <Table
            :loading="loading"
            :key="tableKey"
            @open-row-modal="(val) => openDetail(val)"
            :columns="detailTagihanSalesColumn"
            :table-data="tableData" />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
