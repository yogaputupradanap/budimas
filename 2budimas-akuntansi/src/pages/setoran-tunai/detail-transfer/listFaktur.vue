<script setup>
import { ref, onMounted, computed, nextTick, watch, inject } from "vue";
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
const $swal = inject("$swal");
const modalData = ref({
  nama_customer: "",
  bukti_transfer: "",
});
const isKasirButtonDisabled = ref(true);
const isSimpanButtonDisabled = ref(true);
const isAuditButtonDisabled = ref(true);
const inputDiterimaKasir = ref({});

const validateDiterimaKasir = () => {
  return setoranData.value.data?.every((item) => {
    const diterima = inputDiterimaKasir.value[item.id_setoran] || 0;
    return diterima >= item.setoran;
  });
};

const totalSetoran = computed(() => {
  if (setoranData.value && Array.isArray(setoranData.value.data)) {
    return setoranData.value.data.reduce((acc, item) => {
      return acc + (Number(item.setoran) || 0);
    }, 0);
  }
  return 0;
});

const totalDiterimaKasir = computed(() => {
  // FIX: Tambahkan pengecekan Array.isArray seperti pada totalSetoran
  if (setoranData.value && Array.isArray(setoranData.value.data)) {
    return setoranData.value.data.reduce((sum, item) => {
      return sum + (Number(item.setor_diterima_kasir) || 0);
    }, 0);
  }
  return 0;
});

const checkAllStatus = (statusTarget) => {
  // FIX: Pastikan data adalah array sebelum memanggil .every
  if (setoranData.value && Array.isArray(setoranData.value.data)) {
    return setoranData.value.data.every((item) => item?.status_setoran === statusTarget);
  }
  return false; // Default false jika data belum ada
};

const detailSetoran = async () => {
  loadingData.value = true;
  const options = { ...route.query, tipeSetoran: 1 };

  try {
    const response = await setoranService.detailSetoran(options);
    // console.log("Raw Response:", response);

    if (response && response.data) {
      // CARA MENAMPILKAN/MENGAMBIL RESULT:
      // Karena di log Anda strukturnya response.data.result
      const actualData = Array.isArray(response.data.result) 
        ? response.data.result 
        : [];

      // Simpan ke setoranData.value.data agar Tabel bisa membaca
      setoranData.value = {
        informasi: response.informasi || {},
        data: actualData // Kita ratakan (flatten) ke properti .data
      };

      // Sekarang forEach akan berjalan lancar
      actualData.forEach((item) => {
        if (item.id_setoran) {
          const sisa = Number(item.setoran) - (Number(item.setor_diterima_kasir) || 0);
          inputDiterimaKasir.value[item.id_setoran] = sisa > 0 ? sisa : 0;
        }
      });

      // console.log("Data Result Berhasil Dimuat:", actualData);
    }
  } catch (error) {
    console.error("Error pada detailSetoran:", error);
    alert.setMessage(error.message, "danger");
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
  if (useUser().hasAccess("kasir")) {
    const hasInvalidInput = setoranData.value.data?.some((item) => {
      const selisih = item.setoran - (item.setor_diterima_kasir || 0);
      const inputValue = inputDiterimaKasir.value[item.id_setoran] || 0;
      return inputValue > selisih;
    });

    if (hasInvalidInput) {
      alert.setMessage(
        "Input tidak boleh lebih dari sisa yang belum diterima",
        "danger"
      );
      return;
    }
  }

  // Validasi untuk audit: cek langsung dari database
  if (useUser().hasAccess("audit")) {
    const isValid = setoranData.value.data?.every((item) => {
      const currentDiterima = item.setor_diterima_kasir || 0;
      return currentDiterima >= item.setoran;
    });

    if (!isValid) {
      alert.setMessage(
        "Tidak bisa konfirmasi audit: masih ada yang belum diterima kasir sepenuhnya",
        "danger"
      );
      return;
    }
  }

  const id_setoran = setoranData.value.data.map((item) => item.id_setoran);
  let status_setoran;
  if (useUser().hasAccess("kasir")) {
    status_setoran = 2;
  } else if (useUser().hasAccess("audit")) {
    status_setoran = 3;
  }

  const body = {
    id_setoran,
    status_setoran,
    nama_konfirmasi: user.user.value.nama,
    diterima_kasir: inputDiterimaKasir.value,
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

const submitSimpanSetoran = async () => {
  // Validasi untuk kasir: cek input tidak boleh lebih dari selisih
  const hasInvalidInput = setoranData.value.data?.some((item) => {
    const selisih = item.setoran - (item.setor_diterima_kasir || 0);
    const inputValue = inputDiterimaKasir.value[item.id_setoran] || 0;
    return inputValue > selisih;
  });

  if (hasInvalidInput) {
    alert.setMessage(
      "Input tidak boleh lebih dari sisa yang belum diterima",
      "danger"
    );
    return;
  }

  const id_setoran = setoranData.value.data.map((item) => item.id_setoran);

  const body = {
    id_setoran,
    nama_kasir: user.user.value.nama,
    diterima_kasir: inputDiterimaKasir.value,
  };

  try {
    const isConfirm = await $swal.confirmSubmit();
    if (!isConfirm) return;
    const res = await setoranService.simpanKasirSetoran(body);
    alert.setMessage(res.status, "success");
    router.back();
  } catch (error) {
    alert.setMessage(error, "danger");
  }
};

onMounted(() => {
  detailSetoran();
  window.inputDiterimaKasir = inputDiterimaKasir.value;
  window.userStore = useUser();
  window.triggerValidation = () => {
    if (checkAllStatus(status["kasir"])) {
      isAuditButtonDisabled.value = !validateDiterimaKasir();
    }
  };
});

watch(
  setoranData,
  (newValue) => {
    // 1. Validasi awal: pastikan newValue dan newValue.data adalah Array
    if (newValue && Array.isArray(newValue.data)) {
      
      // 2. Gunakan forEach dengan aman
      newValue.data.forEach((item) => {
        if (item && item.id_setoran) {
          const selisih = item.setoran - (item.setor_diterima_kasir || 0);
          inputDiterimaKasir.value[item.id_setoran] = selisih > 0 ? selisih : 0;
        }
      });

      window.inputDiterimaKasir = inputDiterimaKasir.value;

      // 3. Logika pengecekan selisih
      const hasSelisih = newValue.data.some((item) => {
        const selisih = item.setoran - (item.setor_diterima_kasir || 0);
        return selisih > 0;
      });

      // 4. Logika tombol konfirmasi kasir
      const allStatus1or0 = newValue.data.every(
        (item) => item.status_setoran === 1 || item.status_setoran === 0
      );
      
      isKasirButtonDisabled.value = !allStatus1or0 || hasSelisih;
      isSimpanButtonDisabled.value = !hasSelisih;
      
      // 5. Gunakan optional chaining untuk safety pada status["kasir"]
      isAuditButtonDisabled.value = !checkAllStatus(status?.["kasir"]);

    } else {
      // 6. Fallback jika data kosong atau bukan array
      isKasirButtonDisabled.value = true;
      isSimpanButtonDisabled.value = true;
      isAuditButtonDisabled.value = true;
    }
  },
  { deep: true }
);

watch(
  inputDiterimaKasir,
  () => {
    window.inputDiterimaKasir = inputDiterimaKasir.value;

    // Update state tombol secara realtime berdasarkan inputan user
    if (setoranData.value.data) {
      const hasSelisih = setoranData.value.data.some((item) => {
        const currentDiterima = item.setor_diterima_kasir || 0;
        const inputValue = inputDiterimaKasir.value[item.id_setoran] || 0;
        const totalDiterima = currentDiterima + inputValue;
        const selisih = item.setoran - totalDiterima;
        return selisih > 0;
      });

      // Logika tombol konfirmasi kasir: disabled jika ada selisih
      const allStatus1or0 = setoranData.value.data.every(
        (item) => item.status_setoran === 1 || item.status_setoran === 0
      );
      isKasirButtonDisabled.value = !allStatus1or0 || hasSelisih;

      // Logika tombol simpan: enabled jika ada selisih (berlawanan dengan konfirmasi)
      isSimpanButtonDisabled.value = !hasSelisih;

      // Update tombol audit juga
      isAuditButtonDisabled.value = !checkAllStatus(2) || hasSelisih;
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
          <Modal id="modal" @modal-closed="resetFormModal" ref="modal">
            <Card no-subheader>
              <template #header>Bukti Pembayaran</template>
              <template #content>
                <Label label="Nama Customer" full>
                  <Skeleton v-if="loadingData" class="skeleton" />
                  <BFormInput
                    v-else
                    :model-value="modalData.nama_customer"
                    disabled />
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
                      alt="bukti setoran tunai" />
                  </FlexBox>
                </Label>
              </template>
            </Card>
          </Modal>
          <FlexBox full flex-col it-end>
          <!-- <pre class="tw-te xt-xs">{{ setoranData.data }}</pre>  -->
          
            <Table
              table-width="tw-w-[90vw]"
              :loading="loadingData"
              :columns="listFakturColumn"
              :table-data="setoranData.data"
              :meta="{
                      updateRow: (data, index, column, action) => {
                        if (action === 'openRowModal') showModalWithData(data)
                      }
                    }"
              :key="key"
              @open-row-modal="(val) => showModalWithData(val)" />

            <!-- Summary totals -->
            <FlexBox full class="tw-px-4">
              <Label label="Total Setoran">
                <Skeleton v-if="loadingData" class="skeleton" />
                <BFormInput
                  v-else
                  :model-value="parseCurrency(totalSetoran)"
                  disabled />
              </Label>
              <Label label="Total Diterima Kasir">
                <Skeleton v-if="loadingData" class="skeleton" />
                <BFormInput
                  v-else
                  :model-value="parseCurrency(totalDiterimaKasir)"
                  disabled />
              </Label>
            </FlexBox>

            <div v-if="useUser().hasAccess('kasir')" class="tw-flex tw-gap-2">
              <Button
                :disabled="isSimpanButtonDisabled"
                :trigger="submitSimpanSetoran"
                class="tw-px-4 tw-py-2"
                icon="mdi mdi-content-save">
                Simpan
              </Button>
              <Button
                :disabled="isKasirButtonDisabled"
                :trigger="submitKonfirmasiSetoran"
                class="tw-px-4 tw-py-2"
                icon="mdi mdi-check-circle">
                konfirmasi kasir
              </Button>
            </div>
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
