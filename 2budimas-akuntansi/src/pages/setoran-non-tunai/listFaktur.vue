<script setup>
import { ref, onMounted, computed, nextTick, inject } from "vue";
import { useRoute, useRouter } from "vue-router";
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import { listFakturNonTunaiColumn } from "@/src/model/tableColumns/setoran-non-tunai/listFaktur";
import { setoranService } from "@/src/services/setoran";
import Table from "@/src/components/ui/table/Table.vue";
import Label from "@/src/components/ui/Label.vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import { useAlert } from "@/src/store/alert";
import { parseCurrency, status } from "@/src/lib/utils";
import Button from "@/src/components/ui/Button.vue";
import { useUser } from "@/src/store/user";
import Modal from "@/src/components/ui/Modal.vue";
import { BFormInput, BFormCheckbox } from "bootstrap-vue-next";
import Image from "@/src/components/ui/Image.vue";
import { watch } from "vue";
import NoImage from "@/src/assets/images/no-image.svg";

const route = useRoute();
const router = useRouter();
const setoranData = ref({});
const loadingData = ref(true);
const alert = useAlert();
const user = useUser();
const key = ref(0);
const $swal = inject("$swal");
const modal1 = ref();
const modalData1 = ref({
  nama_customer: "",
  bukti_transfer: "",
});
const modal2 = ref();
const modalData2 = ref({
  ket_biaya_lainnya: null,
  biaya_lainnya: null,
  id_setoran: null,
  is_max_biaya: false,
});

const isKasirButtonDisabled = ref(true);
const isAuditButtonDisabled = ref(true);

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
    tipeSetoran: 2,
  };

  try {
    const response = await setoranService.detailSetoran(options);

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

const showModalWithData1 = ({ value, rowIndex, columnId }) => {
  modalData1.value = {
    nama_customer: value.nama_customer,
    bukti_transfer: value.bukti_transfer,
  };

  nextTick(() => {
    modal1.value.show();
  });
};

const showModalWithData2 = ({ value, rowIndex, columnId }) => {
  modalData2.value = {
    ket_biaya_lainnya: value.ket_biaya_lainnya || null,
    biaya_lainnya: value.biaya_lainnya?.toString() || null,
    id_setoran: value.id_setoran,
    is_max_biaya: parseInt(value.max_biaya_lainnya) === 5000,
  };

  nextTick(() => {
    modal2.value.show();
  });
};

const showModal = ({ funcId, ...params }) => {
  if (funcId === "lihat-bukti-setor") {
    showModalWithData1({ ...params });
  } else if (funcId === "tambah-biaya-lainnya") {
    showModalWithData2({ ...params });
  }
};

const resetFormModal1 = () => {
  modalData1.value = {
    nama_customer: "",
    bukti_transfer: "",
  };
};

const resetFormModal2 = () => {
  modalData2.value = {
    ket_biaya_lainnya: null,
    biaya_lainnya: null,
    id_setoran: null,
    is_max_biaya: false,
  };
};

const submitKonfirmasiSetoran = async () => {
  const id_setoran = setoranData.value.data.map((item) => item.id_setoran);
  const status_setoran = 3;

  const nama_konfirmasi = user.user.value.nama;

  const body = {
    id_setoran,
    status_setoran,
    nama_konfirmasi,
  };

  try {
    const isConfirm = await $swal.confirmSubmit();
    if (!isConfirm) return;
    const res = await setoranService.konfirmasiSetoran(body);
    alert.setMessage(res.status, "success");
    router.back();
  } catch (error) {
    alert.setMessage(error, "danger");
  }
};

const submitBiayaLainnya = async () => {
  // Cek apakah ini operasi hapus (ketika semua field dikosongkan)
  const isDeleting =
    !modalData2.value.ket_biaya_lainnya && !modalData2.value.biaya_lainnya;

  const body = {
    id_setoran: modalData2.value.id_setoran,
    biaya_lainnya: isDeleting ? null : parseInt(modalData2.value.biaya_lainnya),
    ket_biaya_lainnya: isDeleting ? null : modalData2.value.ket_biaya_lainnya,
    is_max_biaya: modalData2.value.is_max_biaya,
  };

  try {
    const response = await setoranService.addBiayaLainnya(body);

    // Custom message berdasarkan operasi
    if (isDeleting) {
      alert.setMessage("Biaya lainnya berhasil dihapus", "success");
    } else {
      // Cek apakah ini edit (ada data lama) atau tambah baru
      const existingData = setoranData.value.data?.find(
        (item) => item.id_setoran === modalData2.value.id_setoran
      );
      const isEditing =
        existingData?.biaya_lainnya || existingData?.ket_biaya_lainnya;

      alert.setMessage(
        isEditing
          ? "Biaya lainnya berhasil diubah"
          : "Biaya lainnya berhasil ditambahkan",
        "success"
      );
    }

    modal2.value.hide();
    await detailSetoran();
  } catch (error) {
    alert.setMessage(error.message || "An error occurred", "danger");
  }
};

onMounted(() => {
  detailSetoran();
});

watch(
  setoranData,
  (newValue) => {
    if (newValue.data) {
      isAuditButtonDisabled.value = !checkAllStatus(status["sales"]);
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
      :x="40">
      <Card no-subheader>
        <template #header>Informasi Piutang</template>
        <template #content>
          <div class="form-grid-card">
            <Label label="Nama PJ">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                :model-value="setoranData?.informasi?.nama_pj"
                disabled />
            </Label>
            <Label label="Jumlah Customer">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                :model-value="setoranData?.informasi?.jumlah_customer"
                disabled />
            </Label>
            <Label label="Total Setoran">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                :model-value="
                  parseCurrency(setoranData?.informasi?.total_setoran)
                "
                disabled />
            </Label>
            <Label label="Tanggal Setor">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                :model-value="setoranData?.informasi?.tanggal"
                disabled />
            </Label>
            <Label label="Nama Kasir">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                :model-value="setoranData?.informasi?.nama_kasir"
                disabled />
            </Label>
            <Label label="Nama Auditor">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                :model-value="setoranData?.informasi?.nama_auditor"
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
        <template #header>List Setoran Customer</template>
        <template #content>
          <Modal id="modal1" @modal-closed="resetFormModal1" ref="modal1">
            <Card no-subheader>
              <template #header>Bukti Pembayaran</template>
              <template #content>
                <Label label="Nama Customer" full>
                  <Skeleton v-if="loadingData" class="skeleton" />
                  <BFormInput
                    v-else
                    :model-value="modalData1.nama_customer"
                    disabled />
                </Label>
                <Label full label="Bukti Pembayaran :" class="tw-mt-4">
                  <FlexBox full jus-center>
                    <Image
                      :src="
                        modalData1.bukti_transfer
                          ? `https://storage.googleapis.com/buktitransaksi/${modalData1.bukti_transfer}`
                          : Struk
                      "
                      class="tw-w-96 tw-h-auto"
                      object-fit
                      alt="bukti setoran tunai" />
                  </FlexBox>
                </Label>
              </template>
            </Card>
          </Modal>
          <Modal id="modal2" @modal-closed="resetFormModal2" ref="modal2">
            <Card no-subheader>
              <template #header>Form Biaya Lainnya</template>
              <template #content>
                <form class="tw-w-full">
                  <Label label="Keterangan Biaya:" full>
                    <BFormInput
                      v-model="modalData2.ket_biaya_lainnya"
                      placeholder="Masukkan keterangan biaya"
                      required
                      :disabled="
                        setoranData.data?.find(
                          (item) => item.id_setoran === modalData2.id_setoran
                        )?.status_setoran === 3
                      " />
                  </Label>
                  <Label label="Jumlah Biaya:" full class="tw-mt-4">
                    <BFormInput
                      v-model="modalData2.biaya_lainnya"
                      type="number"
                      placeholder="Masukkan jumlah biaya"
                      required
                      :disabled="
                        setoranData.data?.find(
                          (item) => item.id_setoran === modalData2.id_setoran
                        )?.status_setoran === 3
                      " />
                  </Label>
                  <Label full class="tw-mt-4">
                    <BFormCheckbox
                      id="checkbox-1"
                      v-model="modalData2.is_max_biaya"
                      name="checkbox-1"
                      :value="true"
                      :unchecked-value="false"
                      :disabled="
                        setoranData.data?.find(
                          (item) => item.id_setoran === modalData2.id_setoran
                        )?.status_setoran === 3
                      ">
                      Max Rp 5.000
                    </BFormCheckbox>
                  </Label>
                  <FlexBox jus-end>
                    <Button
                      v-if="
                        setoranData.data?.find(
                          (item) => item.id_setoran === modalData2.id_setoran
                        )?.status_setoran !== 3
                      "
                      type="button"
                      :trigger="submitBiayaLainnya"
                      class="tw-mt-4 tw-bg-green-500 tw-py-2 tw-px-4"
                      icon="mdi mdi-check-circle">
                      Submit
                    </Button>
                  </FlexBox>
                </form>
              </template>
            </Card>
          </Modal>
          <FlexBox full flex-col it-end>
            <Table
              table-width="tw-w-[90vw]"
              :loading="loadingData"
              :columns="listFakturNonTunaiColumn"
              :table-data="setoranData.data"
              :key="key"
              @open-row-modal="(val) => showModal(val)" />
            <Button
              v-if="useUser().hasAccess('audit')"
              :disabled="isAuditButtonDisabled"
              :trigger="submitKonfirmasiSetoran"
              class="tw-px-4 tw-py-2"
              icon="mdi mdi-check-circle">
              konfirmasi audit
            </Button>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
