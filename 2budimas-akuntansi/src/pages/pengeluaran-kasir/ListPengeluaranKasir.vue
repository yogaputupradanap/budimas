<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import { listPengeluaranKasirColumn } from "@/src/model/tableColumns/pengeluaran-kasir/listPengeluaranKasirColumn";
import { setoranService } from "@/src/services/setoran";
import { usePagination } from "@/src/lib/usePagination";
import { useFiltering } from "@/src/lib/useFiltering";
import { useSorting } from "@/src/lib/useSorting";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import { computed, inject, onMounted, ref, watch } from "vue";
import Label from "@/src/components/ui/Label.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import Button from "@/src/components/ui/Button.vue";
import { useTableSearch } from "@/src/lib/useTableSearch";
import { useOthers } from "@/src/store/others";
import { useUser } from "@/src/store/user";
import {
  fetchWithAuth,
  formatCurrencyAuto,
  getTodayDate,
  statusPengeluaranList,
} from "@/src/lib/utils";
import Modal from "@/src/components/ui/Modal.vue";
import TextField from "@/src/components/ui/formInput/TextField.vue";
import { useAlert } from "@/src/store/alert";
import { cetakStrukPengeluaranKasir } from "@/src/model/pdf/strukPengeluaranKasir";

const others = useOthers();
const user = useUser();
const tanggalPengajuan = ref(getTodayDate());
const statusPengeluaran = ref();
const perusahaan = ref();
const id_user = ref(user?.user?.value?.id || null);
const alert = useAlert();
const $swal = inject("$swal");
const nama_kasir = ref(user?.user?.value?.nama_user || "");

// Modal and form state
const addPengeluaranModal = ref();
const konfirmasiPengeluaranModal = ref();
const formLoading = ref(false);
const konfirmasiLoading = ref(false);
const formData = ref({
  no_pengeluaran: "",
  jumlah_pengeluaran: "",
  keterangan_pengeluaran: "",
  pic: user?.user?.value?.nama_user || "",
});

const konfirmasiData = ref({
  id: null,
  no_pengeluaran: "",
  jumlah_pengeluaran: "",
  jumlah_acc: "",
  keterangan_pengeluaran: "",
  pic: "",
  nama_cabang: "",
  nama_kasir: "",
  status_pengeluaran: null,
  tanggal_pengajuan: "",
  tanggal_acc: "",
});

// Reset form data
const resetForm = () => {
  formData.value = {
    jumlah_pengeluaran: "",
    keterangan_pengeluaran: "",
    pic: user?.user?.value?.nama_user || "",
  };
};

// Show modal and reset form
const showAddModal = () => {
  resetForm();
  addPengeluaranModal.value.show();
};

// Submit pengeluaran
const submitPengeluaran = async () => {
  try {
    // 1. Perbaiki Fungsi Konfirmasi
    const result = await $swal.fire({
      title: 'Simpan Pengeluaran',
      text: "Pastikan data yang Anda masukkan sudah benar.",
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: 'Ya, Simpan',
      cancelButtonText: 'Batal'
    });

    if (!result.isConfirmed) return;
    
    formLoading.value = true;

    // 2. Siapkan Payload
    const payload = {
      ...formData.value,
      id_cabang: user?.user?.value?.id_cabang,
      id_user: user?.user?.value?.id_user, // Gunakan ID dari user store jika id_user.value kosong
      id_perusahaan: perusahaan.value || null,
      // kode_cabang: user?.user?.value?.kode_cabang,
    };
    console.log("Cek Payload Sebelum Kirim:", payload);

    // 3. Kirim ke API
    const response = await fetchWithAuth(
      "POST",
      setoranService.endpoints.addPengeluaran,
      payload
    );

    // 4. Handle Success
    alert.setMessage(response.message || "Data berhasil disimpan", "success");
    
    if (addPengeluaranModal.value) {
      addPengeluaranModal.value.hide();
    }

    // Reset Form (Opsional tapi disarankan)
    formData.value = {
      no_pengeluaran: "",
      jumlah_pengeluaran: "",
      keterangan_pengeluaran: "",
      pic: user?.user?.value?.nama || "",
    };

    // Refresh Tabel
    pagination.value = { ...pagination.value };

  } catch (error) {
    // 5. Perbaiki Alert Error agar tidak crash
    const errorMsg = error.response?.data?.message || error.message || "Terjadi kesalahan sistem";
    alert.setMessage(errorMsg, "danger");
    console.error(error);
  } finally {
    formLoading.value = false;
  }
};



const showKonfirmasiModal = async (id) => {
  try {
    const response = await fetchWithAuth(
      "GET",
      `${setoranService.endpoints.getKonfirmasiPengeluaran}?id_pengeluaran=${id}`
    );

    konfirmasiData.value = {
      id: response.id,
      no_pengeluaran: response.no_pengeluaran,
      jumlah_pengeluaran: response.jumlah_pengeluaran,
      jumlah_acc: response.jumlah_acc,
      keterangan_pengeluaran: response.keterangan_pengeluaran,
      pic: response.pic,
      nama_cabang: response.nama_cabang,
      nama_kasir: response.nama_kasir,
      status_pengeluaran: response.status_pengeluaran,
      tanggal_pengajuan: response.tanggal_pengajuan,
      tanggal_acc: response.tanggal_acc,
    };

    konfirmasiPengeluaranModal.value.show();
  } catch (error) {
    console.error("Error in showKonfirmasiModal:", error);
    alert.setMessage(error, "danger");
  }
};

// Submit konfirmasi pengeluaran
const submitKonfirmasi = async () => {
  try {
    // GANTI baris ini: const isConfirm = await $swal.confirmSubmit();
    // MENJADI standar SweetAlert2:
    const result = await $swal.fire({
      title: 'Konfirmasi',
      text: "Apakah Anda yakin ingin mengonfirmasi pengeluaran ini?",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Ya, Konfirmasi!',
      cancelButtonText: 'Batal'
    });

    // Cek apakah user menekan tombol 'Ya'
    if (!result.isConfirmed) return;

    konfirmasiLoading.value = true;

    const payload = {
      id_pengeluaran: konfirmasiData.value.id,
    };

    const response = await fetchWithAuth(
      "POST",
      setoranService.endpoints.konfirmasiPengeluaran,
      payload
    );

    alert.setMessage(response.message || "Berhasil!", "success");
    
    if (konfirmasiPengeluaranModal.value) {
        konfirmasiPengeluaranModal.value.hide();
    }

    // Cetak struk setelah konfirmasi berhasil
    cetakStrukPengeluaranKasir(response.data, nama_kasir.value || "");

    pagination.value = { ...pagination.value };
  } catch (error) {
    // Tangkap pesan error dari API jika ada
    const msg = error.response?.data?.message || error.message || error;
    alert.setMessage(msg, "danger");
    console.error(error);
  } finally {
    konfirmasiLoading.value = false;
  }
};

const handleCustomAction = (data) => {
  // Destructuring harus sesuai dengan object yang dikirim
  const { value: id, columnId } = data;

  if (columnId === "konfirmasi") {
    showKonfirmasiModal(id);
  }
};

// Initialize form on component mount
onMounted(() => {
  resetForm();
});

const { endpoints } = setoranService;
const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();
const { onSortingChange, sorting } = useSorting();
const paginate = useFetchPaginate(
  `${endpoints.listPengeluaran}`,
  {
    pagination,
    sorting,
    globalFilters,
    initialSortColumn: "tanggal_pengajuan",
    additionalParams: {
      id_cabang: user?.user?.value?.id_cabang,
      id_user: user?.user?.value?.id_user, // Gunakan id_user sesuai Proxy Object Anda
      id_jabatan: user?.user?.value?.id_jabatan,
    },
  }
);

// Mapping manual untuk memastikan reaktivitas tetap terjaga
const data = paginate[0];      // Ini adalah ref(data)
const count = paginate[1];     // Ini adalah ref(count)
const loading = paginate[2];   // Ini adalah ref(loading)
const totalPage = paginate[3]; // Ini adalah ref(totalPage)
const key = paginate[4];       // Ini adalah ref(key)

const displayData = computed(() => {
  // Jika sedang mode pencarian dan ada hasil di clientData
  if (clientData.pages && clientData.pages.length > 0) {
    return clientData.pages;
  }
  // Jika tidak, gunakan data default dari server pagination
  return data.value?.result || [];
});

// Atau modifikasi tombol Cari Data di template agar tidak merusak mode server
const handleSearch = async () => {
  await searchQuery(); // Jalankan fungsi cari bawaan
  isServerTable.value = true; // Paksa kembali ke mode server
};
  

// all methods and properties that needed for table filtering
const fieldPool = [tanggalPengajuan, statusPengeluaran];
const queryEntries = computed(() => [
  ["tanggal_pengajuan=", tanggalPengajuan.value],
  ["status_pengeluaran=", statusPengeluaran.value],
  ["id_cabang=", user?.user?.value?.id_cabang],
  ["id_user=", user?.user?.value?.id],
  ["id_jabatan=", user?.user?.value?.id_jabatan],
]);

const options = {
  initialColumnName: "tanggal_pengajuan",
  checkFieldFilterFunc: (val) => val[1] === undefined || val[1] === null,
  filterFunction: (val) => val[1] !== undefined && val[1] !== null,
  asArgument: true,
};

const formattedJumlahPengeluaran = computed(() =>
  formatCurrencyAuto(konfirmasiData.value.jumlah_pengeluaran)
);

const formattedJumlahAcc = computed(() =>
  formatCurrencyAuto(konfirmasiData.value.jumlah_acc)
);

const filteredColumns = computed(() => {
  const jabatanId = Number(user?.user?.value?.id_jabatan);
  let cols = [...listPengeluaranKasirColumn];

  if (jabatanId !== 16) {
    cols = cols.filter(col => col.id !== "actions");
  } else {
    cols = cols.filter(col => col.id !== "tanggal_diberikan");
  }
  
  return cols.length > 0 ? cols : listPengeluaranKasirColumn;
});

const [
  clientData,
  button,
  searchLoading,
  isServerTable,
  clientKey,
  searchQuery,
] = useTableSearch(endpoints.listPengeluaran, fieldPool, queryEntries, options);

const reset = () => {
  fieldPool.forEach((val) => (val.value = null));
  tanggalPengajuan.value = getTodayDate();
  isServerTable.value = true;
};

  // Paksa isServerTable selalu true setiap kali searchQuery dijalankan
  watch(isServerTable, (val) => {
    if (val === false) {
      isServerTable.value = true;
    }
  });

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
        <template #header>Filter Pengeluaran Kasir</template>
        <template #content>
          <FlexBox full flexCol itEnd class="md:tw-flex-row">
            <FlexBox full>
              <Label label="Tanggal Pengajuan">
                <VueDatePicker
                  v-model="tanggalPengajuan"
                  model-type="yyyy-MM-dd"
                  format="yyyy-MM-dd"
                  :clearable="false"
                  :enable-time-picker="false"
                  placeholder="yyyy-MM-dd"
                  auto-apply />
              </Label>
              <Label label="Status Pengeluaran">
                <SelectInput
                  v-model="statusPengeluaran"
                  placeholder="Pilih Status"
                  size="md"
                  :search="true"
                  :options="statusPengeluaranList"
                  text-field="name"
                  value-field="value" />
              </Label>
            </FlexBox>
            <FlexBox full jusEnd>
              <Button
                :trigger="reset"
                icon="mdi mdi-reload"
                class="tw-h-[38px] tw-w-full xl:tw-w-32 tw-bg-red-500">
                Reset
              </Button>
              <Button
                :loading="searchLoading"
                :trigger="handleSearch"  
                :icon="button.icon"
                class="tw-h-[38px] tw-w-full xl:tw-w-32">
                Cari Data
              </Button>
            </FlexBox>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card no-subheader>
        <template #header>
          <div class="tw-flex tw-justify-between tw-items-center">
            <span>List Pengeluaran Kasir</span>
          </div>
        </template>
        
        <template #content>
          <FlexBox full jusEnd class="tw-px-4">
            <Button
              :trigger="showAddModal"
              icon="mdi mdi-plus"
              class="tw-py-2 tw-px-4">
              Add Pengeluaran
            </Button>
          </FlexBox>
          <ServerTable
            v-if="isServerTable"
            :columns="filteredColumns"
            :key="key"
            :table-data="clientData?.pages?.length > 0 ? clientData.pages : (data?.result || [])"
            :loading="loading || searchLoading"
            :on-pagination-change="onPaginationChange"
            :on-global-filters-change="onColumnFilterChange"
            :on-sorting-change="onSortingChange"
            :pagination="pagination"
            :sorting="sorting"
            :filter="globalFilters || ''" 
            :page-count="totalPage"
            :total-data="count || 0"
            @customAction="handleCustomAction" />

          <Table
            v-else
            :key="clientKey"
            :columns="filteredColumns"
            :table-data="clientData.pages || []"
            @customAction="handleCustomAction" />
        </template>
      </Card>
    </SlideRightX>

    <!-- Add Pengeluaran Modal -->
    <Modal ref="addPengeluaranModal" id="addPengeluaranModal" :centered="true">
      <SlideRightX
        :duration-enter="0.3"
        :duration-leave="0.3"
        :delay-in="0.1"
        :delay-out="0.1"
        :initial-x="-20"
        :x="20">
        <Card no-subheader>
          <template #header>
            <div class="tw-flex tw-justify-between tw-items-center">
              <span>Pengajuan Pengeluaran</span>
            </div>
          </template>
          <template #content>
            <div class="tw-space-y-4 tw-w-full">
              <Label label="Jumlah Pengeluaran">
                <TextField
                  class="tw-w-full"
                  v-model="formData.jumlah_pengeluaran"
                  type="number"
                  placeholder="Masukkan jumlah pengeluaran"
                  size="md" />
              </Label>

              <Label label="Keterangan Pengeluaran">
                <TextField
                  class="tw-w-full"
                  v-model="formData.keterangan_pengeluaran"
                  placeholder="Masukkan keterangan pengeluaran" />
              </Label>

              <Label label="Perusahaan">
                <SelectInput
                  v-model="perusahaan"
                  placeholder="Pilih Perusahaan"
                  size="md"
                  :search="true"
                  :options="others.perusahaan.list"
                  text-field="nama"
                  value-field="id" />
              </Label>

              <Label label="PIC">
                <TextField
                  class="tw-w-full"
                  v-model="formData.pic"
                  placeholder="Masukkan nama PIC"
                  disabled
                  size="md" />
              </Label>
              <FlexBox full jusEnd>
                <Button
                  :trigger="submitPengeluaran"
                  :loading="formLoading"
                  icon="mdi mdi-check"
                  class="tw-py-2 tw-px-4 tw-mt-4">
                  Ajukan Pengeluaran
                </Button>
              </FlexBox>
            </div>
          </template>
        </Card>
      </SlideRightX>
    </Modal>

    <!-- Konfirmasi Pengeluaran Modal -->
    <Modal
      ref="konfirmasiPengeluaranModal"
      id="konfirmasiPengeluaranModal"
      :centered="true">
      <SlideRightX
        :duration-enter="0.3"
        :duration-leave="0.3"
        :delay-in="0.1"
        :delay-out="0.1"
        :initial-x="-20"
        :x="20">
        <Card no-subheader>
          <template #header>
            <div class="tw-flex tw-justify-between tw-items-center">
              <span>Konfirmasi Pengeluaran</span>
            </div>
          </template>
          <template #content>
            <div class="tw-space-y-4 tw-w-full">
              <Label label="No Pengeluaran">
                <TextField
                  class="tw-w-full"
                  v-model="konfirmasiData.no_pengeluaran"
                  size="md"
                  disable />
              </Label>

              <Label label="Jumlah Pengeluaran">
                <TextField
                  class="tw-w-full"
                  v-model="formattedJumlahPengeluaran"
                  size="md"
                  disable />
              </Label>
              <Label label="Jumlah Disetujui">
                <TextField
                  class="tw-w-full"
                  v-model="formattedJumlahAcc"
                  size="md"
                  disable />
              </Label>

              <Label label="Keterangan Pengeluaran">
                <TextField
                  class="tw-w-full"
                  v-model="konfirmasiData.keterangan_pengeluaran"
                  disable />
              </Label>
              <Label label="Tanggal Pengajuan">
                <TextField
                  class="tw-w-full"
                  v-model="konfirmasiData.tanggal_pengajuan"
                  disable />
              </Label>
              <Label label="Tanggal Disetujui">
                <TextField
                  class="tw-w-full"
                  v-model="konfirmasiData.tanggal_acc"
                  disable />
              </Label>

              <Label label="PIC">
                <TextField
                  class="tw-w-full"
                  v-model="konfirmasiData.pic"
                  placeholder="Masukkan nama PIC"
                  size="md"
                  disable />
              </Label>

              <FlexBox full jusEnd>
                <Button
                  :trigger="submitKonfirmasi"
                  :loading="konfirmasiLoading"
                  icon="mdi mdi-check"
                  class="tw-py-2 tw-px-4 tw-mt-4">
                  Konfirmasi
                </Button>
              </FlexBox>
            </div>
          </template>
        </Card>
      </SlideRightX>
    </Modal>
  </FlexBox>
</template>
