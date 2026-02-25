<script setup>
import {
  ref,
  defineProps,
  defineEmits,
  watch,
  reactive,
  inject,
  computed,
  onMounted,
} from "vue";
import Modal from "./Modal.vue";
import TextField from "./formInput/TextField.vue";
import FlexBox from "./FlexBox.vue";
import Button from "./Button.vue";
import { apiUrl, fetchWithAuth, statusOrderText } from "@/src/lib/utils";
import { useAlert } from "@/src/store/alert";
import SelectInput from "./formInput/SelectInput.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import { useArmada } from "@/src/store/armada";
import { useDriver } from "@/src/store/driver";

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  eventData: {
    type: Object,
    default: () => ({}),
  },
});

const emit = defineEmits(["close", "deleted", "updated"]);
const modalRef = ref(null);
const $swal = inject("$swal");
const alert = useAlert();
const armadaStore = useArmada();
const driverStore = useDriver();
const isEditMode = ref(false);

const formData = reactive({
  tanggalPengiriman: "",
  tanggalPengirimanObj: null,
  rute: "",
  armada: "",
  armadaId: "",
  driver: "",
  driverId: "",
  status_order: "",
});
const originalData = reactive({
  tanggalPengirimanObj: null,
  armadaId: "",
  driverId: "",
});

// Mengambil data armada dan driver saat komponen dimuat
onMounted(async () => {
  await Promise.all([armadaStore.getAllArmada(), driverStore.getAllDriver()]);
});

const handleDelete = async () => {
  const body = props.eventData.extendedProps;
  const method = "POST";
  const url = `${apiUrl}/api/distribusi/delete-jadwal`;

  try {
    const isConfirm = await $swal.confirmDelete(
      "Apakah anda yakin ingin menghapus jadwal ini?"
    );
    if (!isConfirm) return;
    const res = await fetchWithAuth(method, url, body);
    $swal.success(res.message || "Berhasil menghapus jadwal armada");
    emit("deleted");
    modalRef.value?.hide();
  } catch (error) {
    console.error("Error deleting event:", error);
    modalRef.value?.hide();
    $swal.error(error.message || "Gagal menghapus jadwal armada");
  }
};

const hasChanges = computed(() => {
  // Bandingkan tanggal (konversi ke string untuk perbandingan yang konsisten)
  const origDate = originalData.tanggalPengirimanObj
    ? new Date(originalData.tanggalPengirimanObj).toISOString().split("T")[0]
    : null;
  const newDate = formData.tanggalPengirimanObj
    ? new Date(formData.tanggalPengirimanObj).toISOString().split("T")[0]
    : null;

  const dateChanged = origDate !== newDate;
  const armadaChanged = originalData.armadaId !== formData.armadaId;
  const driverChanged = originalData.driverId !== formData.driverId;

  return dateChanged || armadaChanged || driverChanged;
});

const selectedArmadaKubikasi = computed(() => {
  const selectedArmada = armadaStore.armada.list.find(
    (item) => item.id == formData.armadaId
  );
  return parseFloat(selectedArmada?.kubikasi || 0);
});

const estimasiKubikasi = computed(() => {
  return parseFloat(props.eventData?.extendedProps?.estimasi_kubikasi || 0);
});

const isKubikasiValid = computed(() => {
  return estimasiKubikasi.value <= selectedArmadaKubikasi.value;
});

const handleUpdate = async () => {
  if (
    !formData.tanggalPengirimanObj ||
    !formData.armadaId ||
    !formData.driverId
  ) {
    $swal.error("Mohon lengkapi semua data");
    return;
  }

  // Validasi kubikasi
  if (!isKubikasiValid.value) {
    $swal.error(
      `Estimasi kubikasi (${estimasiKubikasi.value}) melebihi kapasitas armada (${selectedArmadaKubikasi.value} CBM). Silakan pilih armada dengan kapasitas lebih besar.`
    );
    return;
  }

  // Perbaikan zona waktu untuk tanggal
  const selectedDate = new Date(formData.tanggalPengirimanObj);
  const adjustedDate = new Date(
    selectedDate.getFullYear(),
    selectedDate.getMonth(),
    selectedDate.getDate(),
    12,
    0,
    0
  ); // Set waktu ke 12:00:00 untuk menghindari masalah timezone

  const body = {
    id_proses_picking: props.eventData.extendedProps.id_proses_picking,
    id_driver: formData.driverId,
    id_armada: formData.armadaId,
    tanggal_pengiriman: adjustedDate,
    id_rute: props.eventData.extendedProps.id_rute,
  };

  try {
    const isConfirm = await $swal.confirmSubmit(
      "Apakah anda yakin ingin mengubah jadwal ini?"
    );
    if (!isConfirm) return;
    await fetchWithAuth("POST", `${apiUrl}/api/distribusi/edit-jadwal`, body);
    $swal.success("Jadwal armada berhasil diubah!");
    isEditMode.value = false;
    emit("updated");
    modalRef.value?.hide();
  } catch (error) {
    console.error("Error updating event:", error);
    $swal.error(error.message || "Gagal mengubah jadwal armada");
  }
};

const toggleEditMode = () => {
  isEditMode.value = !isEditMode.value;
};

const cancelEdit = () => {
  isEditMode.value = false;
  // Mengembalikan nilai form data ke nilai asli
  if (props.eventData?.extendedProps) {
    updateFormDataFromProps();
  }
};

const updateFormDataFromProps = () => {
  if (props.eventData?.extendedProps) {
    const eventDate = new Date(props.eventData.start);

    // Update formData
    formData.tanggalPengirimanObj = eventDate;
    formData.tanggalPengiriman = eventDate.toLocaleDateString("id-ID", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    });
    formData.rute = props.eventData.extendedProps.nama_rute || "";
    formData.armada = props.eventData.extendedProps.nama_armada || "";
    formData.armadaId = props.eventData.extendedProps.id_armada || "";
    formData.driver = props.eventData.extendedProps.nama_driver || "";
    formData.driverId = props.eventData.extendedProps.id_driver || "";
    formData.status_order = props.eventData.extendedProps.status_order;

    // Update originalData untuk tracking perubahan
    originalData.tanggalPengirimanObj = eventDate;
    originalData.armadaId = props.eventData.extendedProps.id_armada || "";
    originalData.driverId = props.eventData.extendedProps.id_driver || "";
  }
};

watch(
  () => props.show,
  (newValue) => {
    if (newValue) {
      modalRef.value?.show();
      isEditMode.value = false;
      updateFormDataFromProps();
      console.log("eventData", props.eventData.extendedProps);
    } else {
      modalRef.value?.hide();
    }
  },
  { immediate: true }
);

const statusOrderStr = computed(() => {
  if (!formData.status_order) return "";

  const statuses = formData.status_order.toString().split(",");

  const statusTexts = statuses.map((status) => {
    const trimmedStatus = status.trim();
    return statusOrderText(trimmedStatus);
  });

  // Gabungkan dengan koma dan spasi
  return statusTexts.join(", ");
});

const formattedArmadaOptions = computed(() => {
  return armadaStore.armada.list.map((item) => ({
    ...item,
    namaDisplay: `${item.nama} - [${item.kubikasi || 0} CBM]`,
  }));
});

function handleModalClosed() {
  emit("close");
}
</script>

<template>
  <Modal
    ref="modalRef"
    id="armada-event-modal"
    :centered="true"
    @modalClosed="handleModalClosed">
    <div class="tw-p-2">
      <div class="tw-flex tw-justify-between tw-items-center">
        <h3 class="tw-text-xl tw-font-semibold">Detail Jadwal Armada</h3>
        <div class="tw-flex tw-items-center tw-gap-2">
          <span class="tw-text-sm tw-mr-1">Mode Edit</span>
          <label
            class="tw-relative tw-inline-flex tw-items-center tw-cursor-pointer">
            <input
              type="checkbox"
              v-model="isEditMode"
              class="tw-sr-only tw-peer"
              @change="isEditMode ? null : cancelEdit()" />
            <div
              class="tw-w-11 tw-h-6 tw-bg-gray-200 peer-focus:tw-outline-none tw-rounded-full tw-peer peer-checked:after:tw-translate-x-full peer-checked:after:tw-border-white after:tw-content-[''] after:tw-absolute after:tw-top-[2px] after:tw-left-[2px] after:tw-bg-white after:tw-border-gray-300 after:tw-border after:tw-rounded-full after:tw-h-5 after:tw-w-5 after:tw-transition-all peer-checked:tw-bg-blue-500"></div>
          </label>
        </div>
      </div>

      <div v-if="eventData?.extendedProps" class="tw-space-y-3 tw-my-5">
        <!-- Mode View -->
        <div v-if="!isEditMode" class="tw-space-y-4">
          <TextField
            label="Tanggal Pengiriman"
            labelFor="tanggal-pengiriman"
            v-model="formData.tanggalPengiriman"
            disable
            type="text"
            placeholder="Tanggal Pengiriman" />

          <TextField
            label="Rute"
            labelFor="rute"
            v-model="formData.rute"
            disable
            type="text"
            placeholder="Rute" />

          <TextField
            label="Armada"
            labelFor="armada"
            v-model="formData.armada"
            disable
            type="text"
            placeholder="Armada" />

          <TextField
            label="Driver"
            labelFor="driver"
            v-model="formData.driver"
            disable
            type="text"
            placeholder="Driver" />

          <TextField
            label="Status Order"
            labelFor="status_order"
            v-model="statusOrderStr"
            disable
            type="text"
            placeholder="Status Order" />
        </div>

        <!-- Mode Edit -->
        <div v-else class="tw-space-y-4">
          <div>
            <p class="tw-mb-1">Tanggal Pengiriman:</p>
            <VueDatePicker
              v-model="formData.tanggalPengirimanObj"
              :enable-time-picker="false"
              placeholder="mm/dd/yyyy"
              :teleport="true"
              auto-apply
              class="tw-w-full" />
          </div>

          <div>
            <p class="tw-mb-1">Rute:</p>
            <TextField
              v-model="formData.rute"
              disable
              type="text"
              placeholder="Rute" />
          </div>

          <div>
            <p class="tw-mb-1">Armada:</p>
            <SelectInput
              :options="formattedArmadaOptions"
              v-model="formData.armadaId"
              textField="namaDisplay"
              size="sm"
              valueField="id"
              class="tw-w-full tw-h-[40px]" />
            <div
              class="tw-mt-1 tw-text-xs"
              :class="{
                'tw-text-red-500': !isKubikasiValid,
                'tw-text-green-500': isKubikasiValid,
              }">
              Estimasi kubikasi: {{ estimasiKubikasi }} CBM / Kapasitas armada:
              {{ selectedArmadaKubikasi }} CBM
              <span v-if="!isKubikasiValid" class="tw-font-bold">
                (Melebihi kapasitas!)
              </span>
            </div>
          </div>

          <div>
            <p class="tw-mb-1">Driver:</p>
            <SelectInput
              :options="driverStore.driver.list"
              v-model="formData.driverId"
              textField="nama"
              valueField="id"
              size="sm"
              class="tw-w-full tw-h-[40px]" />
          </div>

          <div>
            <p class="tw-mb-1">Status Faktur:</p>
            <TextField
              v-model="statusOrderStr"
              disable
              type="text"
              placeholder="Status Faktur" />
          </div>
        </div>
      </div>

      <FlexBox full jusEnd class="tw-gap-2">
        <!-- Tombol-tombol mode edit -->
        <template v-if="isEditMode">
          <Button
            :trigger="handleUpdate"
            icon="mdi mdi-content-save"
            :disabled="!isKubikasiValid || !hasChanges"
            class="tw-px-4 tw-py-2 tw-bg-green-500 hover:tw-bg-green-600 disabled:tw-bg-green-300">
            Simpan
          </Button>
        </template>

        <!-- Tombol-tombol mode view -->
        <template v-else>
          <Button
            :trigger="handleDelete"
            icon="mdi mdi-delete"
            :disabled="formData.status_order == 3"
            class="tw-px-4 tw-py-2 tw-bg-red-500 hover:tw-bg-red-600 disabled:tw-bg-red-300">
            Hapus jadwal ini
          </Button>
          <Button
            :trigger="handleModalClosed"
            class="tw-bg-gray-200 tw-text-gray-700 tw-px-4 tw-py-2">
            Tutup
          </Button>
        </template>
      </FlexBox>
    </div>
  </Modal>
</template>
