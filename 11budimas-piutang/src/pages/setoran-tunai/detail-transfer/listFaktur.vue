<script setup>
import { ref, onMounted, computed, nextTick, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import { listFakturColumn } from "@/src/model/tableColumns/setoran-tunai/listFaktur";
import { setoranService } from "@/src/services/setoran";
import Table from "@/src/components/ui/table/Table.vue";
import Label from "@/src/components/ui/Label.vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import { useAlert } from "@/src/store/alert";
import { parseCurrency, status } from "@/src/lib/utils";
import Button from "@/src/components/ui/Button.vue";
import { useUser } from "@/src/store/user";
import Modal from "@/src/components/ui/Modal.vue";
import { BFormInput } from "bootstrap-vue-next";
import Image from "@/src/components/ui/Image.vue";
import NoImage from "@/src/assets/images/no-image.png";

const route = useRoute();
const router = useRouter();
const setoranData = ref({});
const loadingData = ref(true);
const alert = useAlert();
const user = useUser();
const key = ref(0);
const modal = ref();
const modalData = ref({
  nama_customer: "",
  bukti_transfer: "",
});
const isKasirButtonDisabled = ref(true);
const isAuditButtonDisabled = ref(true);

//
const setoranTunaiGrants = computed(() =>
  user.userAccess.find((val) => val.name === "setoran tunai")
);

const grantAccess = (role) =>
  setoranTunaiGrants.value.grant.some((i) => i === role);

const checkAllStatus = (status) =>
  setoranData.value.data?.every((item) => item?.status_setoran === status);

const detailSetoran = async () => {
  const options = {
    ...route.query,
    tipeSetoran: 1,
  };

  try {
    const response = await setoranService.detailSetoran(options);

    console.log("res", response);
    if (response) {
      setoranData.value = response;
    } else {
      alert.setMessage(`empty fetching setoran result`, "warning");
    }
  } catch (error) {
    alert.setMessage(error.message || "An error occurred", "danger");
  } finally {
    loadingData.value = false;
    key.value++;
  }
};

const showModalWithData = ({ value, rowIndex, columnId }) => {
  modalData.value = {
    nama_customer: value.nama_customer,
    bukti_transfer: value.bukti_transfer,
  };

  nextTick(() => {
    modal.value.show();
  });
};

const resetFormModal = () => {
  modalData.value = {
    nama_customer: "",
    bukti_transfer: "",
  };
};

const submitKonfirmasiSetoran = async () => {
  const id_setoran = setoranData.value.data.map((item) => item.id_setoran);
  const status_setoran = checkAllStatus(status["sales"])
    ? 2
    : checkAllStatus(status["kasir"]) && 3;

  const nama_konfirmasi = user.user.value.nama;

  const body = {
    id_setoran,
    status_setoran,
    nama_konfirmasi,
  };

  try {
    const res = await setoranService.konfirmasiSetoran(body);
    alert.setMessage(res.status, "success");
    router.back();
  } catch (error) {
    alert.setMessage(error, "danger");
  }
};

onMounted(() => {
  detailSetoran();
});

watch(
  setoranData,
  (newValue) => {
    if (newValue.data) {
      // Button kasir enabled jika status sales
      isKasirButtonDisabled.value = !checkAllStatus(status["sales"]);

      // Button audit enabled jika status kasir
      isAuditButtonDisabled.value = !checkAllStatus(status["kasir"]);
    }
  },
  { deep: true }
);
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
        <template #header>Informasi Piutang</template>
        <template #content>
          <div class="form-grid-card">
            <Label label="Nama Sales">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                :model-value="setoranData?.informasi?.nama_sales"
                disabled
              />
            </Label>
            <Label label="Jumlah Customer">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                :model-value="setoranData?.informasi?.jumlah_customer"
                disabled
              />
            </Label>
            <Label label="Total Setoran">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                :model-value="
                  parseCurrency(setoranData?.informasi?.total_setoran)
                "
                disabled
              />
            </Label>
            <Label label="Tanggal Setor">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                :model-value="setoranData?.informasi?.tanggal"
                disabled
              />
            </Label>
            <Label label="Nama Kasir">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                :model-value="setoranData?.informasi?.nama_kasir"
                disabled
              />
            </Label>
            <Label label="Nama Auditor">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                :model-value="setoranData?.informasi?.nama_auditor"
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
        <template #header>List Setoran Customer</template>
        <template #content>
          <Modal id="modal" @modal-closed="resetFormModal" ref="modal">
            <Card no-subheader>
              <template #header>Bukti Pembayaran</template>
              <template #content>
                <Label label="Nama Customer" full>
                  <Skeleton v-if="loadingData" class="skeleton" />
                  <BFormInput
                    v-else
                    :model-value="modalData.nama_customer"
                    disabled
                  />
                </Label>
                <Label full label="Bukti Pembayaran :" class="tw-mt-4">
                  <FlexBox full jus-center>
                    <Image
                      :src="
                        modalData.bukti_transfer
                          ? `https://storage.googleapis.com/buktitransaksi/${modalData.bukti_transfer}`
                          : NoImage
                      "
                      class="tw-w-96 tw-h-auto"
                      object-fit
                      alt="bukti setoran tunai"
                    />
                  </FlexBox>
                </Label>
              </template>
            </Card>
          </Modal>
          <FlexBox full flex-col it-end>
            <Table
              table-width="tw-w-[90vw]"
              :loading="loadingData"
              :columns="listFakturColumn"
              :table-data="setoranData.data"
              :key="key"
              @open-row-modal="(val) => showModalWithData(val)"
            />
            <Button
              v-if="useUser().hasAccess('kasir')"
              :disabled="isKasirButtonDisabled"
              :trigger="submitKonfirmasiSetoran"
              class="tw-px-4 tw-py-2"
              icon="mdi mdi-check-circle"
            >
              konfirmasi kasir
            </Button>
            <Button
              v-if="useUser().hasAccess('audit')"
              :disabled="isAuditButtonDisabled"
              :trigger="submitKonfirmasiSetoran"
              class="tw-px-4 tw-py-2"
              icon="mdi mdi-check-circle"
            >
              konfirmasi audit
            </Button>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
