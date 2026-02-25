<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Button from "@/src/components/ui/Button.vue";
import {$swal} from "@/src/components/ui/SweetAlert.vue";
import {ref, watch} from "vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import {useOthers} from "@/src/store/others";
import {fetchWithAuth} from "@/src/lib/utils";
import useRekening from "@/src/lib/useRekeningPerusahaan";
import VueDatePicker from "@vuepic/vue-datepicker";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import {listPreviewTransaksi} from "@/src/model/tableColumns/transaksi/listPreviewTransaksi";
import {usePagination} from "@/src/lib/usePagination";
import {useFiltering} from "@/src/lib/useFiltering";
import {useSorting} from "@/src/lib/useSorting";
import {useFetchPaginateV2} from "@/src/lib/useFetchPaginateV2";
import Modal from "@/src/components/ui/Modal.vue";

const others = useOthers();
const id_perusahaan = ref(null);
const id_rekening_perusahaan = ref(null);
const selectedTanggal = ref(null);
const selectedPerusahaanModal = ref(null);
const nominalFormatted = ref(0);
const selectedTanggalModal = ref();
const selectedRekeningModal = ref(null);
const nominal = ref(0);
const tipeModal = ref(1);
const selectedTipeModal = ref(null);
const keteranganModal = ref(null);
const selectedStatusModal = ref(null);
const errorMessage = ref({
  tanggal: "",
  perusahaan: "",
  rekeningPerusahaan: "",
  nominal: "",
  tipe: "",
});

const advancedFilters = ref([]);
const modalTransaksi = ref(null);
const {loading: loadingPerusahaan, getRekeningPerusahaan, rekeningPerusahaan} = useRekening()
const {
  loading: loadingPerusahaanModal,
  getRekeningPerusahaan: getRekeningPerusahaanModal,
  rekeningPerusahaan: rekeningPerusahaanModal
} = useRekening()
const laodingSubmit = ref(false);
const triggerFetch = ref(0);
const optionTipe = ref([
  {id: 1, nama: "Debit"},
  {id: 2, nama: "Kredit"},
]);
const optionStatus = ref([
  {id: 0, nama: "Pending"},
  {id: 2, nama: "Confirmed"},
  {id: 3, nama: "Posted"},
]);
const selectedTipe = ref(null);
const selectedTransaksi = ref(null)


const handleCariData = async () => {
  // await handleUnggah();
  advancedFilters.value = [];
  const dataFilter = []
  if (selectedTanggal.value) {
    dataFilter.push({
      column: "tanggal_transaksi",
      value: selectedTanggal.value,
    });
  }
  if (id_rekening_perusahaan.value) {
    dataFilter.push({
      column: "id_rekening_perusahaan",
      value: id_rekening_perusahaan.value,
    });
  }
  if (selectedTipe.value) {
    dataFilter.push({
      column: "tipe_transaksi",
      value: selectedTipe.value,
    });
  }
  advancedFilters.value = dataFilter;

};

const shomModalTambah = () => {
  selectedTanggalModal.value = null;
  selectedPerusahaanModal.value = null;
  selectedRekeningModal.value = null;
  nominal.value = 0;
  nominalFormatted.value = 0;
  selectedTipeModal.value = null;
  keteranganModal.value = null;
  selectedStatusModal.value = null;
  modalTransaksi.value.show();
  selectedStatusModal.value = 0;
  errorMessage.value = {
    tanggal: "",
    perusahaan: "",
    rekeningPerusahaan: "",
    nominal: "",
    tipe: "",
  };
  tipeModal.value = 1; // add modal
}

const tambahTransaksi = async () => {

  // reset error message
  errorMessage.value = {
    tanggal: "",
    perusahaan: "",
    rekeningPerusahaan: "",
    nominal: "",
    tipe: "",
  };

  // validation
  let isValid = true;
  if (!selectedTanggalModal.value) {
    errorMessage.value.tanggal = "Tanggal transaksi wajib diisi.";
    isValid = false;
  }
  if (!selectedPerusahaanModal.value) {
    errorMessage.value.perusahaan = "Perusahaan wajib dipilih.";
    isValid = false;
  }
  if (!selectedRekeningModal.value) {
    errorMessage.value.rekeningPerusahaan = "Rekening perusahaan wajib dipilih.";
    isValid = false;
  }
  if (!nominal.value || nominal.value <= 0) {
    errorMessage.value.nominal = "Nominal wajib diisi dan harus lebih dari 0.";
    isValid = false;
  }
  if (!selectedTipeModal.value) {
    errorMessage.value.tipe = "Tipe wajib dipilih.";
    isValid = false;
  }

  if (!isValid) {
    return;
  }

  const isConfirm = await $swal.confirm(
      "Apakah Anda yakin ingin menambahkan data transaksi ini?",
  );
  if (!isConfirm) {
    return;
  }

  laodingSubmit.value = true;
  try {
    const payload = {
      tanggal_transaksi: selectedTanggalModal.value,
      id_rekening_perusahaan: selectedRekeningModal.value,
      tipe: selectedTipeModal.value,
      keterangan: keteranganModal.value,
      nominal: nominal.value
    };
    await fetchWithAuth(
        "POST",
        `/api/akuntansi/insert-transaksi`,
        payload,
    )
    $swal.success("Data transaksi berhasil ditambahkan.");
    modalTransaksi.value.hide();
    // reset form
    selectedTanggalModal.value = null;
    selectedPerusahaanModal.value = null;
    selectedRekeningModal.value = null;
    nominal.value = 0;
    nominalFormatted.value = 0;
    selectedTipeModal.value = null;
    keteranganModal.value = null;
    selectedStatusModal.value = null;

    // refresh table
    triggerFetch.value += 1;
  } catch (error) {
    console.log("Error adding transaksi:", error);
    $swal.error("Gagal menambahkan data transaksi: " + error);
  } finally {
    laodingSubmit.value = false;
  }
}

const updateTransaksi = async () => {

  // reset error message
  errorMessage.value = {
    tanggal: "",
    perusahaan: "",
    rekeningPerusahaan: "",
    nominal: "",
    tipe: "",
  };

  // validation
  let isValid = true;
  if (!selectedTanggalModal.value) {
    errorMessage.value.tanggal = "Tanggal transaksi wajib diisi.";
    isValid = false;
  }
  if (!selectedPerusahaanModal.value) {
    errorMessage.value.perusahaan = "Perusahaan wajib dipilih.";
    isValid = false;
  }
  if (!selectedRekeningModal.value) {
    errorMessage.value.rekeningPerusahaan = "Rekening perusahaan wajib dipilih.";
    isValid = false;
  }
  if (!nominal.value || nominal.value <= 0) {
    errorMessage.value.nominal = "Nominal wajib diisi dan harus lebih dari 0.";
    isValid = false;
  }
  if (!selectedTipeModal.value) {
    errorMessage.value.tipe = "Tipe wajib dipilih.";
    isValid = false;
  }

  if (!isValid) {
    return;
  }

  const isConfirm = await $swal.confirm(
      "Apakah Anda yakin ingin mengupdate data transaksi ini?",
  );
  if (!isConfirm) {
    return;
  }

  laodingSubmit.value = true;
  try {
    const payload = {
      tanggal_transaksi: selectedTanggalModal.value,
      id_rekening_perusahaan: selectedRekeningModal.value,
      tipe: selectedTipeModal.value,
      keterangan: keteranganModal.value,
      nominal: nominal.value,
      id_mutasi_acc: selectedTransaksi.value

    };
    await fetchWithAuth(
        "PUT",
        `/api/akuntansi/update-transaksi`,
        payload,
    )
    $swal.success("Data transaksi berhasil diupdate.");
    modalTransaksi.value.hide();
    // reset form
    selectedTanggalModal.value = null;
    selectedPerusahaanModal.value = null;
    selectedRekeningModal.value = null;
    nominal.value = 0;
    nominalFormatted.value = 0;
    selectedTipeModal.value = null;
    keteranganModal.value = null;
    selectedStatusModal.value = null;
    selectedTransaksi.value = null

    // refresh table
    triggerFetch.value += 1;
  } catch (error) {
    console.log("Error update transaksi:", error);
    $swal.error("Gagal mengupdate data transaksi: " + error);
  } finally {
    laodingSubmit.value = false;
  }
}

const handleDelete = async (row) => {
  const isConfirm = await $swal.confirm(
      "Apakah Anda yakin ingin menghapus data transaksi ini?",
  );
  if (!isConfirm) {
    return;
  }

  laodingSubmit.value = true;
  try {
    const clause = {
      "id_mutasi_acc = ": `'${row.id_mutasi_acc}'`
    }
    await fetchWithAuth(
        "DELETE",
        `/api/base/accounting_entry?where=` + encodeURIComponent(JSON.stringify(clause)),
    )
    $swal.success("Data transaksi berhasil dihapus.");
    // refresh table
    triggerFetch.value += 1;
  } catch (error) {
    console.log("Error deleting transaksi:", error);
    $swal.error("Gagal menghapus data transaksi: " + error);
  } finally {
    laodingSubmit.value = false;
  }
}

const handleChange = (event) => {
  let rawValue = event.target.value
      .replace(/[^0-9,]/g, "") // Hapus semua kecuali angka & koma
      .replace(/,/g, "."); // Ubah koma menjadi titik (karena parseFloat butuh titik)

  if (rawValue === "") rawValue = "0";

  const numericValue = parseFloat(rawValue) || 0; // Konversi ke angka

  // Format angka sesuai dengan Rupiah (1.000,23)
  const formattedValue = new Intl.NumberFormat("id-ID", {
    minimumFractionDigits: rawValue.includes(".") ? 3 : 0, // Tambah desimal jika ada titik
    maximumFractionDigits: 3,
  }).format(numericValue);

  nominal.value = numericValue;
  nominalFormatted.value = `${formattedValue}`;

  // console.log({
  //   nominal: nominalFormatted.value,
  //   numeric: nominal.value
  // });
};

const showModalUpdate = (row) => {
  modalTransaksi.value.show();
  tipeModal.value = 2; // update modal
  selectedTanggalModal.value = row.tanggal_transaksi;
  selectedPerusahaanModal.value = row.id_perusahaan;
  selectedRekeningModal.value = row.id_rekening_perusahaan;
  nominal.value = row.nominal;
  nominalFormatted.value = new Intl.NumberFormat("id-ID", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 3,
  }).format(row.nominal);
  selectedTipeModal.value = row.tipe_transaksi;
  keteranganModal.value = row.keterangan;
  selectedStatusModal.value = row.status;
  selectedTransaksi.value = row.id_mutasi_acc;
  errorMessage.value = {
    tanggal: "",
    perusahaan: "",
    rekeningPerusahaan: "",
    nominal: "",
    tipe: "",
  };
}

const {onPaginationChange, pagination} = usePagination();
const {onColumnFilterChange, globalFilters} = useFiltering();
const {onSortingChange, sorting} = useSorting();

const [data, count, loading, totalPage, key] = useFetchPaginateV2(
    `/api/akuntansi/get-list-transaksi?`,
    {
      pagination,
      sorting,
      globalFilters,
      initialSortColumn: "tanggal_transaksi",
      advancedFilters: advancedFilters,
      isRunOnMounted: true,
      triggerFetch
    }
);

watch(
  [() => id_perusahaan.value, () => selectedPerusahaanModal.value],
  async ([newFilterId, newModalId], [oldFilterId, oldModalId]) => {
    
    // Untuk Filter Luar
    if (newFilterId && newFilterId !== oldFilterId) {
      await getRekeningPerusahaan(newFilterId);
    } else if (!newFilterId) {
      rekeningPerusahaan.value = [];
    }

    // Untuk Modal
    if (newModalId && newModalId !== oldModalId) {
      await getRekeningPerusahaanModal(newModalId);
    } else if (!newModalId) {
      rekeningPerusahaanModal.value = [];
    }
  }
);


</script>

<template>
  <Modal ref="modalTransaksi" id="modalTransaksi" size="md" :centered="true">
    <SlideRightX
        :duration-enter="0.3"
        :duration-leave="0.3"
        :delay-in="0.1"
        :delay-out="0.1"
        :initial-x="-20"
        :x="20">
      <Card no-subheader>
        <template #header>
          <div class="tw-flex tw-justify-start tw-items-start">
            <span>{{ tipeModal === 1 ? 'Tambah Transaksi' : 'Update Transaksi' }}</span>
          </div>
        </template>
        <template #content>
          <div class="tw-space-y-4 tw-w-full">
            <Label label="Tanggal Transaksi">
              <VueDatePicker
                  v-model="selectedTanggalModal"
                  model-type="yyyy-MM-dd"
                  format="yyyy-MM-dd"
                  :clearable="true"
                  :enable-time-picker="false"
                  placeholder="yyyy-MM-dd"
                  auto-apply/>
              <p class="tw-text-red-500 tw-text-sm" v-if="errorMessage.tanggal">{{ errorMessage.tanggal }}</p>
            </Label>

            <Label label="Perusahaan">
              <Skeleton class="tw-w-full tw-h-[34px]" v-if="others.perusahaan.loading" />
              <SelectInput
                  v-else
                  v-model="selectedPerusahaanModal"
                  placeholder="Pilih Data"
                  size="md"
                  :search="true"
                  :options="others.perusahaan.list"
                  text-field="nama"
                  value-field="id"
              />
              <p class="tw-text-red-500 tw-text-sm" v-if="errorMessage.perusahaan">{{ errorMessage.perusahaan }}</p>
            </Label>

            <Label label="Bank">
              <Skeleton class="tw-w-full tw-h-[34px]" v-if="loadingPerusahaanModal" />
              <SelectInput
                  v-model="selectedRekeningModal"
                  :options="rekeningPerusahaanModal"
                  text-field="nama_bank"
                  value-field="id_rekening_perusahaan"
                  :disabled="!selectedPerusahaanModal || loadingPerusahaanModal"
                  :search="true"
              />
              <p class="tw-text-red-500 tw-text-sm" v-if="errorMessage.rekeningPerusahaan">{{ errorMessage.rekeningPerusahaan }}</p>
            </Label>

            <Label label="Nominal">
              <input
                  v-model="nominalFormatted"
                  type="text"
                  @input="handleChange"
                  class="tw-border tw-border-gray-300 tw-rounded-md tw-px-3 tw-py-2 tw-w-full focus:tw-outline-none focus:tw-ring-2 focus:tw-ring-blue-500"
                  placeholder="Masukkan nominal"
              />
              <p class="tw-text-red-500 tw-text-sm" v-if="errorMessage.nominal">{{ errorMessage.nominal }}</p>
            </Label>

            <Label label="Tipe">
              <SelectInput
                  v-model="selectedTipeModal"
                  placeholder="Pilih Data"
                  :options="optionTipe"
                  text-field="nama"
                  value-field="id"
              />
              <p class="tw-text-red-500 tw-text-sm" v-if="errorMessage.tipe">{{ errorMessage.tipe }}</p>
            </Label>

            <Label label="Keterangan">
              <textarea
                  v-model="keteranganModal"
                  class="tw-border tw-border-gray-300 tw-rounded-md tw-px-3 tw-py-2 tw-w-full focus:tw-outline-none focus:tw-ring-2 focus:tw-ring-blue-500"
                  placeholder="Masukkan keterangan"
                  rows="3"
              ></textarea>
            </Label>

            <Label label="Status">
              <SelectInput
                  v-model="selectedStatusModal"
                  :disabled="true"
                  :options="optionStatus"
                  text-field="nama"
                  value-field="id"
              />
            </Label>

            <div class="tw-flex tw-gap-2 tw-justify-end">
              <Button
                  :loading="laodingSubmit"
                  :trigger="tipeModal === 1 ? tambahTransaksi : updateTransaksi"
                  icon="mdi mdi-check"
                  class="tw-h-[38px] tw-w-full xl:tw-w-32"
              >
                {{ tipeModal === 1 ? 'Tambah' : 'Update' }}
              </Button>
              <Button
                  :trigger="() => modalTransaksi.hide()"
                  icon="mdi mdi-close"
                  class="tw-h-[38px] tw-w-full xl:tw-w-32 tw-bg-red-500"
              >
                Batal
              </Button>
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </Modal>

  <FlexBox full flex-col>
    <SlideRightX class="slide-container tw-z-10" :duration-enter="0.6">
      <Card no-subheader>
        <template #header>Form Transaksi</template>
        <template #content>
          <div class="form-grid-card-5-col tw-items-end">
            <Label label="Tanggal Transaksi">
              <VueDatePicker v-model="selectedTanggal" model-type="yyyy-MM-dd" format="yyyy-MM-dd" auto-apply :enable-time-picker="false"/>
            </Label>
            
            <Label label="Perusahaan">
              <Skeleton class="tw-w-full tw-h-[34px]" v-if="others.perusahaan.loading" />
              <SelectInput
                  v-else
                  v-model="id_perusahaan"
                  :options="others.perusahaan.list"
                  text-field="nama"
                  value-field="id"
                  :search="true"
              />
            </Label>

            <Label label="Bank (Filter Luar)">
              <Skeleton class="tw-w-full tw-h-[34px]" v-if="loadingPerusahaan" />
              <SelectInput
                  v-else
                  v-model="id_rekening_perusahaan"
                  :disabled="!id_perusahaan || loadingPerusahaan"
                  :options="rekeningPerusahaan"
                  text-field="nama_bank"
                  value-field="id_rekening_perusahaan"
                  :search="true"
              />
            </Label>

            <Label label="Tipe">
              <SelectInput v-model="selectedTipe" :options="optionTipe" text-field="nama" value-field="id" />
            </Label>

            <Button :trigger="handleCariData" icon="mdi mdi-magnify" class="tw-h-[38px]">
              Cari Data
            </Button>
          </div>
        </template>
      </Card>
    </SlideRightX>

    <SlideRightX class="slide-container tw-justify-end" :duration-enter="0.6" :delay-in="0.2">
      <Card no-subheader>
        <template #header>Preview Transaksi</template>
        <template #content>
          <FlexBox full jusEnd class="tw-mb-4">
            <Button :loading="laodingSubmit" :trigger="shomModalTambah" icon="mdi mdi-plus">
              Tambah
            </Button>
          </FlexBox>
          <ServerTable
              :columns="listPreviewTransaksi(showModalUpdate, handleDelete)"
              :key="key"
              :table-data="data?.result || []"
              :loading="loading"
              :on-pagination-change="onPaginationChange"
              :on-global-filters-change="onColumnFilterChange"
              :on-sorting-change="onSortingChange"
              :pagination="pagination"
              :sorting="sorting"
              :filter="globalFilters"
              :page-count="totalPage"
              :total-data="count"/>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>