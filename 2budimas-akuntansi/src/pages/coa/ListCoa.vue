<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Button from "@/src/components/ui/Button.vue";
import {onMounted, ref, watch, computed} from "vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import TextField from "@/src/components/ui/formInput/TextField.vue";
import useCoaCategory from "@/src/lib/useCoaCategory";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import {usePagination} from "@/src/lib/usePagination";
import {useFiltering} from "@/src/lib/useFiltering";
import {useSorting} from "@/src/lib/useSorting";
import {useFetchPaginateV2} from "@/src/lib/useFetchPaginateV2";
import Modal from "@/src/components/ui/Modal.vue";
import {useOthers} from "@/src/store/others";
import {fetchWithAuth, sessionDisk} from "@/src/lib/utils";
import {useUser} from "@/src/store/user";
import {$swal} from "@/src/components/ui/SweetAlert.vue";
import {listPreviewCoa} from "@/src/model/tableColumns/coa/listPreviewCoa";
import axios from "axios";
import useCoa from "@/src/lib/useCoa";
import usePrincipal from "@/src/lib/usePrincipal";

const namaAkunFilter = ref("");
const nomorAkunFilter = ref("");
const selectedStatusAkunModal = ref(null);
const selectedPerusahaanFilter = ref(null);
const selectedKategoriFilter = ref(null);
const selectedStatusAkunFilter = ref(null);
const namaAkunModal = ref("");
const nomorAkunModal = ref("");
const selectedPerusahaanModal = ref(null);
const selectedKategoriModal = ref(null);
const selectedParentModal = ref(null);
const selectedPrincipalModal = ref(null);
const selectedDetailCoa = ref({
  nama_perusahaan: "",
  nomor_akun: "",
  nama_akun: "",
  nama_kategori: "",
  nama_parent: "",
  nama_principal: "",
  total_used: 0,

});
const selectedCoa = ref(null);

const errorMessage = ref({
  perusahaan: "",
  nomorAkun: "",
  namaAkun: "",
  kategori: ""
});

const others = useOthers()
const user = useUser()
const {getCoaCategory, coaCategories, loading: loadingCoa} = useCoaCategory()
const {getPrincipal, loading: loadingPrincipal, principal} = usePrincipal()
const {getCoa, coa, loading: loadingCoaOptions, getCoalist2} = useCoa()
const tipeModal = ref(1); // 1 tambah, 2 update
const triggerFetch = ref(0);
const laodingSubmit = ref(false);
const advancedFilters = ref([]);
const coaOptions = ref([]);
const principalOptions = ref([]);
const {onPaginationChange, pagination} = usePagination();
const {onColumnFilterChange, globalFilters} = useFiltering();
const {onSortingChange, sorting} = useSorting();
const statusAkunOption = [
  {label: "Aktif", value: true},
  {label: "Tidak Aktif", value: false},
]
const modalCOA = ref(null);
const modalDetailCoa = ref(null);
const showModalUpdate = (row) => {
  modalCOA.value.show();
  selectedCoa.value = row.id_coa;
  namaAkunModal.value = row.nama_akun;
  nomorAkunModal.value = row.nomor_akun;
  selectedPerusahaanModal.value = row.id_perusahaan;
  selectedKategoriModal.value = row.id_kategori;
  selectedStatusAkunModal.value = row.is_active;
  errorMessage.value = {
    perusahaan: "",
    nomorAkun: "",
    namaAkun: "",
    kategori: ""
  };
  selectedPrincipalModal.value = row.principal_id;
  selectedParentModal.value = row.parent_id;
  tipeModal.value = 2;
};
const shomModalTambah = () => {
  modalCOA.value.show();
  namaAkunModal.value = "";
  nomorAkunModal.value = "";
  selectedPerusahaanModal.value = null;
  selectedKategoriModal.value = null;
  selectedCoa.value = null;
  selectedStatusAkunModal.value = null;
  selectedParentModal.value = null;
  selectedPrincipalModal.value = null;
  errorMessage.value = {
    perusahaan: "",
    nomorAkun: "",
    namaAkun: "",
    kategori: ""
  };
  tipeModal.value = 1;
};

const showDetailCoa = (row) => {
  modalDetailCoa.value.show();
  selectedDetailCoa.value = row;
}

const handleFilter = () => {
  advancedFilters.value = [];
  const dataFilter = []
  if (selectedKategoriFilter.value) {
    dataFilter.push({
      column: "kategori_id",
      value: selectedKategoriFilter.value,
    });
  }
  if (namaAkunFilter.value) {
    dataFilter.push({
      column: "nama_akun",
      value: `${namaAkunFilter.value}`,
    });
  }
  if (nomorAkunFilter.value) {
    dataFilter.push({
      column: "nomor_akun",
      value: `${nomorAkunFilter.value}`,
    });
  }
  if (selectedPerusahaanFilter.value) {
    dataFilter.push(
        {
          column: "id_perusahaan",
          value: selectedPerusahaanFilter.value,
        }
    )
  }

  if (selectedStatusAkunFilter.value !== null) {
    dataFilter.push(
        {
          column: "is_active",
          value: String(selectedStatusAkunFilter.value),
        }
    )
  }

  advancedFilters.value = dataFilter;
}

const handleDelete = async (row) => {
  const isConfirm = await $swal.confirm(
    `Apakah Anda yakin ingin menghapus COA ${row.id_coa} - ${row.nama_akun}?`
  );
  if (!isConfirm) {
    return;
  }

  const [resJurnalMal, resCoa] = await Promise.all([getJurnalSettingUseCoa(row.id_coa), getCoaUseCoa(row.id_coa)])
  if (resJurnalMal.length > 0) {
    $swal.error(`Gagal menghapus data coa karena sudah digunakan di jurnal setting: ${resJurnalMal.map(item => item.nama_mal).join(", ")}`);
    return;
  }
  if (resCoa.length > 0) {
    $swal.error(`Gagal menghapus data coa karena sudah digunakan di coa: ${resCoa.map(item => item.nama_akun).join(", ")}`)
    return
  }

  laodingSubmit.value = true;
  try {
    const clause = {
      id_coa: row.id_coa
    }

    const body = {
      is_deleted: true,
      deleted_at: new Date().toISOString(),
    }

    await axios.put(
      `${process.env.VUE_APP_API_URL}/api/base/coa`,
      body,
      {
        params: {
          id_coa: row.id_coa
        },
        headers: {
          Authorization: `Bearer ${sessionDisk.getSession("authUser").token}`,
        }
      }
    )
    $swal.success("Data coa berhasil dihapus.");
    // refresh table
    triggerFetch.value += 1;
  } catch (error) {
    console.log("Error deleting coa:", error);
    $swal.error("Gagal menghapus data coa: " + error);
  } finally {
    laodingSubmit.value = false;
  }
};

const getJurnalSettingUseCoa = async (id_coa) => {
  try {

    const response = await fetchWithAuth(
        "GET",
        `/api/akuntansi/coa-used-jurnal?id_coa=${id_coa}`,
    )
    return response;
  } catch (error) {
    console.log("Error fetching jurnal setting:", error);
    throw error;
  }
}

const getCoaUseCoa = async (id_coa) => {
  try {

    const response = await fetchWithAuth(
        "GET",
        `/api/akuntansi/coa-used-coa?id_coa=${id_coa}`,
    )
    return response;
  } catch (error) {
    console.log("Error fetching coa:", error);
    throw error;
  }
}

const tambahCoa = async () => {

  // reset error message
  errorMessage.value = {
    namaAkun: "",
    nomorAkun: "",
    perusahaan: "",
    kategori: ""
  };

  // validation
  let isValid = true;
  if (!namaAkunModal.value) {
    errorMessage.value.namaAkun = "Nama akun wajib diisi.";
    isValid = false;
  }
  if (!nomorAkunModal.value) {
    errorMessage.value.nomorAkun = "Nomor akun wajib diisi.";
    isValid = false;
  }
  if (!selectedPerusahaanModal.value) {
    errorMessage.value.perusahaan = "Perusahaan wajib dipilih.";
    isValid = false;
  }
  if (!selectedKategoriModal.value) {
    errorMessage.value.kategori = "Kategori wajib dipilih.";
    isValid = false;
  }

  if (!isValid) {
    return;
  }

  const isConfirm = await $swal.confirm(
      "Apakah Anda yakin ingin menambahkan data coa ini?",
  );
  if (!isConfirm) {
    return;
  }


  laodingSubmit.value = true;
  try {

    const payload = {
      nama_akun: namaAkunModal.value,
      nomor_akun: nomorAkunModal.value,
      id_perusahaan: selectedPerusahaanModal.value,
      id_kategori: selectedKategoriModal.value,
      created_by: user.user.value.id,
      parent_id: selectedParentModal.value || null,
      principal_id: selectedPrincipalModal.value || null,
    };
    await fetchWithAuth(
        "POST",
        `/api/akuntansi/insert-coa`,
        payload,
    )
    $swal.success("Data coa berhasil ditambahkan.");
    modalCOA.value.hide();
    // reset form
    namaAkunModal.value = "";
    nomorAkunModal.value = "";
    selectedPerusahaanModal.value = null;
    selectedKategoriModal.value = null;


    // refresh table
    triggerFetch.value += 1;
  } catch (error) {
    console.log("Error adding coa:", error);
    $swal.error("Gagal menambahkan data coa: " + error);
  } finally {
    laodingSubmit.value = false;
  }
}

const updateCoa = async () => {

  // reset error message
  errorMessage.value = {
    namaAkun: "",
    nomorAkun: "",
    perusahaan: "",
    kategori: ""
  };

  // validation
  let isValid = true;
  if (!namaAkunModal.value) {
    errorMessage.value.namaAkun = "Nama akun wajib diisi.";
    isValid = false;
  }
  if (!nomorAkunModal.value) {
    errorMessage.value.nomorAkun = "Nomor akun wajib diisi.";
    isValid = false;
  }
  if (!selectedPerusahaanModal.value) {
    errorMessage.value.perusahaan = "Perusahaan wajib dipilih.";
    isValid = false;
  }
  if (!selectedKategoriModal.value) {
    errorMessage.value.kategori = "Kategori wajib dipilih.";
    isValid = false;
  }

  if (!isValid) {
    return;
  }


  const isConfirm = await $swal.confirm(
      "Apakah Anda yakin ingin mengupdate data coa ini?",
  );

  if (!isConfirm) {
    return;
  }

  const [resJurnalMal, resCoa] = await Promise.all([getJurnalSettingUseCoa(selectedCoa.value), getCoaUseCoa(selectedCoa.value)])
  if (resJurnalMal.length > 0 && !selectedStatusAkunModal.value) {
    $swal.error(`Gagal menonaktifkan data coa karena sudah digunakan di jurnal setting: ${resJurnalMal.map(item => item.nama_mal).join(", ")}`);
    return;
  }
  if (resCoa.length > 0 && !selectedStatusAkunModal.value) {
    $swal.error(`Gagal menonaktifkan data coa karena sudah digunakan di coa: ${resCoa.map(item => item.nama_akun).join(", ")}`)
    return
  }

  laodingSubmit.value = true;
  try {
    const payload = {
      nama_akun: namaAkunModal.value,
      nomor_akun: nomorAkunModal.value,
      id_perusahaan: selectedPerusahaanModal.value,
      id_kategori: selectedKategoriModal.value,
      id_coa: selectedCoa.value,
      is_active: selectedStatusAkunModal.value,
      parent_id: selectedParentModal.value || null,
      principal_id: selectedPrincipalModal.value || null,
    };
    await fetchWithAuth(
        "PUT",
        `/api/akuntansi/update-coa`,
        payload,
    )
    $swal.success("Data coa berhasil diupdate.");
    modalCOA.value.hide();
    // reset form
    namaAkunModal.value = "";
    nomorAkunModal.value = "";
    selectedPerusahaanModal.value = null;
    selectedKategoriModal.value = null;
    selectedCoa.value = null;
    selectedStatusAkunModal.value = null;

    // refresh table
    triggerFetch.value += 1;
  } catch (error) {
    console.log("Error update coa:", error);
    $swal.error("Gagal mengupdate data coa: " + error);
  } finally {
    laodingSubmit.value = false;
  }
}


const [data, count, loading, totalPage, key] = useFetchPaginateV2(
    `/api/akuntansi/get-list-coa?`, // Hapus tanda tanya
    {
      pagination,
      sorting,
      globalFilters,
      initialSortColumn: "id_coa",
      initialSortDirection: "desc",
      // GANTI advancedFilters menjadi additionalParams jika backend menangkap flat
      additionalParams: {
        nama_akun: namaAkunFilter.value,
        nomor_akun: nomorAkunFilter.value,
        kategori_id: selectedKategoriFilter.value,
        id_perusahaan: selectedPerusahaanFilter.value,
        is_active: selectedStatusAkunFilter.value,
      },
      isRunOnMounted: true,
      triggerFetch
    }
);

watch(
    () => selectedPerusahaanModal.value,
    async (newValue) => {
      if (newValue) {
        await getCoa(newValue);
        if (tipeModal.value === 2) {
          const selectedCoaItem = coa.value.find(coaItem => coaItem.id_coa === selectedCoa.value);
          if (selectedCoaItem && selectedCoaItem.id_perusahaan !== newValue) {
            selectedCoa.value = null;
          }
          coaOptions.value = coa.value.filter(coaItem => coaItem.id_coa !== selectedCoa.value);
        } else {
          coaOptions.value = coa.value;
        }
      } else {
        coaOptions.value = [];
      }
    }
)

watch(
  () => selectedPerusahaanModal.value,
  async (newValue) => {
    if (newValue) {
      await getPrincipal(newValue);

      // Pastikan kita mengambil array dari properti yang tepat (misal: .data atau .result)
      // Gunakan Array.isArray untuk keamanan ekstra
      const principalList = Array.isArray(principal.value) 
                            ? principal.value 
                            : (principal.value?.data || []);

      if (tipeModal.value === 2) {
        // Gunakan list yang sudah dipastikan array
        const selectedPrincipalItem = principalList.find(
          principalItem => principalItem.id === selectedPrincipalModal.value
        );

        if (selectedPrincipalItem && selectedPrincipalItem.id_perusahaan !== newValue) {
          selectedPrincipalModal.value = null;
        }
      }
      
      // Update options dengan list yang sudah bersih
      principalOptions.value = principalList;
    } else {
      principalOptions.value = [];
    }
  }
)

const cleanTableData = computed(() => {
  // Berdasarkan log: Variasi 1 adalah data.value, Variasi 2 adalah data.value.result
  return data.value?.result || [];
});
onMounted(() => {
  getCoaCategory();
});

</script>

<template>
  <Modal ref="modalCOA" id="modalCOA" size="md" :centered="true">
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
            <span>{{
                tipeModal === 1 ? 'Tambah Akun' : 'Update Akun'
              }}</span>
          </div>
        </template>
        <template #content>
          <div class="tw-space-y-4 tw-w-full">
            <Label label="Perusahaan">
              <Skeleton
                  class="tw-w-full tw-h-[34px]"
                  v-if="others.perusahaan.loading"
              />
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
            <Label label="Nama Akun">
              <TextField class="tw-w-full" v-model="namaAkunModal" placeholder="Masukkan Nama Akun"/>
              <p class="tw-text-red-500 tw-text-sm" v-if="errorMessage.namaAkun">{{ errorMessage.namaAkun }}</p>
            </Label>
            <Label label="Nomor Akun">
              <TextField class="tw-w-full" v-model="nomorAkunModal" placeholder="Masukkan Nomor Akun"/>
              <p class="tw-text-red-500 tw-text-sm" v-if="errorMessage.nomorAkun">{{ errorMessage.nomorAkun }}</p>
            </Label>
            <Label label="Kategori">
              <Skeleton
                  class="tw-w-full tw-h-[34px]"
                  v-if="loadingCoa"
              />
              <!-- <pre>{{ coaCategories }}</pre> -->
              <SelectInput
                  v-else
                  v-model="selectedKategoriModal"
                  placeholder="Pilih Data"
                  size="md"
                  :search="true"
                  :options="coaCategories.result || coaCategories"
                  :disabled="loadingCoa"
                  text-field="nama_kategori"
                  value-field="id_category"
              />
              <p class="tw-text-red-500 tw-text-sm" v-if="errorMessage.kategori">{{ errorMessage.kategori }}</p>
            </Label>
            <Label v-if="tipeModal ===2" label="Status Akun">
              <SelectInput
                  v-model="selectedStatusAkunModal"
                  placeholder="Pilih Data"
                  size="md"
                  :search="true"
                  :options="statusAkunOption"
                  text-field="label"
                  value-field="value"
              />
            </Label>
            <Label label="Parent">
              <Skeleton
                  class="tw-w-full tw-h-[34px]"
                  v-if="loadingCoaOptions"
              />
              <SelectInput
                  v-else
                  v-model="selectedParentModal"
                  placeholder="Pilih Data"
                  size="md"
                  :search="true"
                  :removable="true"
                  :virtual-scroll="true"
                  :options="coaOptions"
                  :disabled="!selectedPerusahaanModal"
                  text-field="nama_akun"
                  value-field="id_coa"
              />
            </Label>
            <Label label="Principal">
              <Skeleton
                  class="tw-w-full tw-h-[34px]"
                  v-if="loadingPrincipal"
              />
              <SelectInput
                  v-else
                  v-model="selectedPrincipalModal"
                  placeholder="Pilih Data"
                  size="md"
                  :search="true"
                  :removable="true"
                  :virtual-scroll="true"
                  :options="principal"
                  :disabled="!selectedPerusahaanModal"
                  text-field="nama"
                  value-field="id"
              />
            </Label>

            <div class="tw-flex tw-gap-2 tw-justify-end">
              <Button
                  :loading="laodingSubmit"
                  :trigger="tipeModal === 1 ? tambahCoa : updateCoa"
                  icon="mdi mdi-check"
                  class="tw-h-[38px] tw-w-full xl:tw-w-32"
              >
                {{
                  tipeModal === 1 ? 'Tambah' : 'Update'
                }}
              </Button>
              <Button
                  :trigger="() => modalCOA.hide()"
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
  <Modal ref="modalDetailCoa" id="modalDetailCoa" size="xl" :centered="true">
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
            <span>Detail COA</span>
          </div>
        </template>
        <template #content>
          <div class="tw-space-y-4  tw-w-full">
            <div class="form-grid-card-3-col">
              <Label label="Perusahaan">
                <TextField class="tw-w-full" :disable="true" v-model="selectedDetailCoa.nama_perusahaan"/>
              </Label>
              <Label label="Nomor Akun">
                <TextField class="tw-w-full" :disable="true" v-model="selectedDetailCoa.nomor_akun"/>
              </Label>
              <Label label="Nama Akun">
                <TextField class="tw-w-full" :disable="true" v-model="selectedDetailCoa.nama_akun"/>
              </Label>
              <Label label="Nama Kategori">
                <TextField class="tw-w-full" :disable="true" v-model="selectedDetailCoa.nama_kategori"/>
              </Label>
              <Label label="Parent">
                <TextField class="tw-w-full" :disable="true" v-model="selectedDetailCoa.nama_parent"/>
              </Label>
              <Label label="Principal">
                <TextField class="tw-w-full" :disable="true" v-model="selectedDetailCoa.nama_principal"/>
              </Label>
              <Label class="tw-col-span-3" label="Jumlah Dipakai di Jurnal Setting">
                <TextField class="tw-w-full" :disable="true" v-model="selectedDetailCoa.total_used"/>
              </Label>
            </div>

            <div class="tw-flex tw-gap-2 tw-justify-end">
              <Button
                  :trigger="() => modalDetailCoa.hide()"
                  icon="mdi mdi-close"
                  class="tw-h-[38px] tw-w-full xl:tw-w-32 tw-bg-red-500"
              >
                Tutup
              </Button>
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </Modal>
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
        <template #header>Filter COA</template>
        <template #content>
          <div class="form-grid-card-6-col tw-items-end">
            <Label label="Perusahaan">
              <Skeleton
                  class="tw-w-full tw-h-[34px]"
                  v-if="others.perusahaan.loading"
              />
              <SelectInput
                  v-else
                  v-model="selectedPerusahaanFilter"
                  placeholder="Pilih Data"
                  size="md"
                  :search="true"
                  :options="others.perusahaan.list"
                  text-field="nama"
                  value-field="id"
              />
            </Label>
            <Label label="Nama Akun">
              <TextField class="tw-w-full" v-model="namaAkunFilter" placeholder="Masukkan Nama Akun"/>
            </Label>
            <Label label="Nomor Akun">
              <TextField class="tw-w-full" v-model="nomorAkunFilter" placeholder="Masukkan Nomor Akun"/>
            </Label>
            <Label label="Kategori">
              <Skeleton
                  class="tw-w-full tw-h-[34px]"
                  v-if="loadingCoa"
              />
              <SelectInput
                  v-else
                  v-model="selectedKategoriFilter"
                  placeholder="Pilih Data"
                  size="md"
                  :search="true"
                  :options="coaCategories.result || coaCategories"
                  :disabled="loadingCoa"
                  text-field="nama_kategori"
                  value-field="id_category"
              />
            </Label>
            <Label label="Status">
              <SelectInput
                  v-model="selectedStatusAkunFilter"
                  placeholder="Pilih Data"
                  size="md"
                  :search="true"
                  :options="statusAkunOption"
                  text-field="label"
                  value-field="value"
              />
            </Label>

            <div class="tw-flex tw-gap-2">

              <Button
                  :trigger="handleFilter"
                  icon="mdi mdi-magnify"
                  class="tw-h-[38px] tw-w-full xl:tw-w-44"
              >
                Cari Data
              </Button>
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>

    <SlideRightX
        class="slide-container tw-justify-end"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.2"
        :delay-out="0.2"
        :initial-x="-40"
        :x="40"
    >
      <Card no-subheader>
        <template #header>List COA</template>
        <template #content>
          <FlexBox full jusEnd class="tw-mb-4">
            <Button
                :loading="laodingSubmit"
                :trigger="shomModalTambah"
                icon="mdi mdi-plus"
                class="tw-h-[38px] tw-w-full xl:tw-w-44"
            >
              Tambah
            </Button>
          </FlexBox>

          <ServerTable
            :columns="listPreviewCoa(showModalUpdate, handleDelete, showDetailCoa)"
            :key="key"
            :table-data="cleanTableData" 
            :loading="loading"
            :on-pagination-change="onPaginationChange"
            :on-global-filters-change="onColumnFilterChange"
            :on-sorting-change="onSortingChange"
            :pagination="pagination"
            :sorting="sorting"
            :filter="globalFilters"
            :page-count="totalPage"
            :total-data="cleanTableData.length > count ? cleanTableData.length : count"
          />
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>