<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import Label from "@/src/components/ui/Label.vue";
import Modal from "@/src/components/ui/Modal.vue";
import { nextTick, onMounted, ref } from "vue";
import { BFormInput } from "bootstrap-vue-next";
import Image from "@/src/components/ui/Image.vue";
import Struk from "@/src/assets/images/struk.png";
import { useAlert } from "@/src/store/alert";
import { useRoute, useRouter } from "vue-router";
import { hutangService } from "@/src/services/hutang";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import { parseCurrency } from "@/src/lib/utils";
import { bayarTagihanPurchasingColumn } from "@/src/model/tableColumns/tagihan-purchasing/bayar-tagihan-purchasing/bayarTagihanPurchasing";
import FIleInput from "@/src/components/ui/formInput/FIleInput.vue";
import Button from "@/src/components/ui/Button.vue";
import { useUser } from "@/src/store/user";

const alert = useAlert();
const route = useRoute();
const router = useRouter();
const modalRef = ref();
const modalValue = ref();
const loadingSubmit = ref(false);
const userStore = useUser();
const tableData = ref([]);
const tableKey = ref(0);
const notaData = ref({});
const loading = ref(false);
const currentDate = ref(new Date().toISOString().split("T")[0]);
const formData = ref({
  keterangan: null,
  picPembayaran: userStore.user.value?.nama || null,
  cabang: userStore.user.value?.nama_cabang || null,
  buktiPembayaran: null,
});

const surat_tagihan = route.params.surat_tagihan;

const openDetail = ({ value }) => {
  modalValue.value = value;

  nextTick(() => {
    modalRef.value.show();
  });
};

const btnBayarIsLunas = () =>
  !notaData.value?.status_bayar || notaData.value.status_bayar === 2;

const submitTagihan = async () => {
  try {
    loadingSubmit.value = true;
    const payload = new FormData();
    payload.append("no_tagihan", surat_tagihan);
    payload.append("tanggal_bayar", currentDate.value);
    payload.append("keterangan", formData.value.keterangan);
    payload.append("pic_pembayaran", formData.value.picPembayaran);
    if (formData.value.buktiPembayaran instanceof File) {
      payload.append("bukti_bayar", formData.value.buktiPembayaran);
    }

    // console.log(
    //   "Sending data:",
    //   JSON.stringify(Object.fromEntries(payload.entries()))
    // );
    const response = await hutangService.postPembayaranTagihan(payload);
    alert.setMessage(response, "success");
    router.back();
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loadingSubmit.value = false;
  }
};

const getDetail = async () => {
  try {
    loading.value = true;
    const table_data = await hutangService.detailHutang(surat_tagihan);
    const nota = await hutangService.detailTagihanNota(surat_tagihan);

    tableData.value = table_data;
    notaData.value = nota[0];
    console.log("notas : ", nota);
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
      :x="40"
    >
      <Card>
        <template #header>Detail Pembayaran Tagihan</template>
        <template #subheader>{{ surat_tagihan }}</template>
        <template #content>
          <div
            class="tw-w-full tw-grid tw-grid-cols-1 lg:tw-grid-cols-6 tw-gap-2"
          >
            <Label class="lg:tw-col-span-2" label="Nama Principal">
              <Skeleton v-if="loading" class="skeleton" />
              <BFormInput
                v-else
                :model-value="notaData?.nama_principal"
                disabled
              />
            </Label>
            <Label class="lg:tw-col-span-2" label="Kode Principal">
              <Skeleton v-if="loading" class="skeleton" />
              <BFormInput
                v-else
                :model-value="notaData?.kode_principal"
                disabled
              />
            </Label>
            <Label class="lg:tw-col-span-2" label="Total Pembayaran">
              <Skeleton v-if="loading" class="skeleton" />
              <BFormInput
                v-else
                :model-value="parseCurrency(notaData?.total_tagihan)"
                disabled
              />
            </Label>
            <Label class="lg:tw-col-span-2" label="Tanggal Pembayaran">
              <BFormInput
                :type="'date'"
                v-model="currentDate"
                required="true"
              />
            </Label>
            <Label class="lg:tw-col-span-2" label="PIC Pembayaran">
              <BFormInput v-model="formData.picPembayaran" disabled />
            </Label>
            <Label class="lg:tw-col-span-2" label="Cabang">
              <BFormInput v-model="formData.cabang" disabled />
            </Label>
            <Label class="lg:tw-col-span-3" label="Keterangan Pembayaran">
              <BFormInput
                placeholder="Masukkan Keterangan"
                v-model="formData.keterangan"
              />
            </Label>
            <Label class="lg:tw-col-span-3" label="Upload Bukti Pembayaran">
              <FIleInput
                class="tw-w-full"
                :model-value="formData.buktiPembayaran"
                @update:model-value="
                  (file) => (formData.buktiPembayaran = file)
                "
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
        <template #header>Rincian Tagihan</template>
        <template #content>
          <Modal
            id="modalRef"
            ref="modalRef"
            centered
            :hide-header="false"
            title="Detail Transfer"
          >
            <Card dense no-header no-subheader no-main-center class="tw-p-4">
              <template #content>
                <FlexBox full no-left-padding flex-col it-center>
                  <Label full label="Bank Asal">
                    <BFormInput model-value="BCA" disabled />
                  </Label>
                  <Label full label="Bank Tujuan">
                    <BFormInput model-value="BCA" disabled />
                  </Label>
                  <Label full label="Bukti Pembayaran :" class="tw-mt-4">
                    <FlexBox full jus-center>
                      <Image
                        :src="Struk"
                        class="tw-w-96 tw-h-auto"
                        object-fit
                        alt="bukti setoran tunai"
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
            :columns="bayarTagihanPurchasingColumn"
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
              :trigger="submitTagihan"
              :loading="loadingSubmit"
              icon="mdi mdi-check"
              :disabled="btnBayarIsLunas()"
              class="tw-bg-green-500 tw-px-4 tw-h-[34px]"
            >
              Submit Pembayaran
            </Button>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
