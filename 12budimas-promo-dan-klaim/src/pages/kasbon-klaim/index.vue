<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import Button from "@/src/components/ui/Button.vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import Modal from "@/src/components/ui/Modal.vue";
import Table from "@/src/components/ui/table/Table.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import { useTableSearch } from "@/src/lib/useTableSearch";
import { useFetchPaginate } from "@/src/lib/useFetchPaginate";
import { BFormInput } from "bootstrap-vue-next";
import { ref, onMounted, computed, inject } from "vue";
import { kasbonKlaimColumn } from "@/src/model/tableColumns/kasbon-klaim";
import { useSorting } from "@/src/lib/useSorting";
import { promoService } from "@/src/services/promo";
import { principalService } from "@/src/services/principal";
import { useFiltering } from "@/src/lib/useFiltering";
import { usePagination } from "@/src/lib/usePagination";
import { useUser } from "@/src/store/user";
import { fetchWithAuth } from "@/src/lib/utils";


const tanggalPengajuan = ref(null);
const selectedPrincipal = ref(null);
const user = useUser();

const userId = ref(user?.user?.value?.id || null);
const dropdownLoading = ref(false);
const isResetting = ref(false);
const $swal = inject("$swal");

const tipeKasbonList = [
    { id: 1, nama: 'Tunai' },
    { id: 2, nama: 'Non Tunai' }
]

const picDisplayName = computed(() => {
  return user?.user?.value?.nama || 'User';
});

const dropdownData = ref({
  principal: [],
});

const addPengajuanKasbon = ref();
const formLoading = ref(false);

const formData = ref({
    id_principal: null,
    tanggal_pengajuan: null,
    nominal_kasbon: 0,
    keterangan: "",
    tipe_kasbon: 0,
});

const { endpoints } = promoService;
const { onSortingChange, sorting } = useSorting();
const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();

const [data, count, loading, totalPage, key] = useFetchPaginate(
  `${endpoints.kasbonKlaim}`,
  {
    pagination,
    sorting,
    globalFilters,
    initialSortColumn: "kode_kasbon_klaim",
  }
);

const fieldPool = [selectedPrincipal, tanggalPengajuan];

const queryEntries = computed(() => {
  if (isResetting.value) return [];
  const entries = [
    ["id_principal=", selectedPrincipal.value],
    ["tanggal_pengajuan=", tanggalPengajuan.value],
  ];

  if (globalFilters.text && globalFilters.text.trim() !== "") {
    entries.push(["filters=", globalFilters.text]);
  }
  return entries.filter(([_, v]) => v !== undefined && v !== null && v !== "");
});

const options = {
  initialColumnName: "kode_kasbon_klaim",
  checkFieldFilterFunc: (val) => val[1] === undefined || val[1] === null,
  filterFunction: (val) => val[1] !== undefined && val[1] !== null,
  asArgument: true,
};

const [
    clientData,  
    buttonText,
    ,    
    isServerTable,     
    clientKey,        
    searchQuery,       
    reset 
] = useTableSearch(endpoints.kasbonKlaim, fieldPool, queryEntries, options);

const resetFilters = () => {
  fieldPool.forEach((val) => (val.value = null));
  tanggalPengajuan.value = null;
  selectedPrincipal.value = null;
  globalFilters.text = "";
  isServerTable.value = true;
};

const showAddModal = () => {
  formData.value = {
    id_principal: null,
    tanggal_pengajuan: null,
    nominal_kasbon: 0,
    keterangan: "",
    tipe_kasbon: 0,
  };
  addPengajuanKasbon.value.show();
};

const formValidation = () => {
    if (!formData.value.id_principal) {
        $swal.error("Principal harus dipilih");
        return false;
    }
    if (!formData.value.tanggal_pengajuan) {
        $swal.error("Tanggal pengajuan harus ditentukan");
        return false;
    }
    if (!formData.value.nominal_kasbon || formData.value.nominal_kasbon <= 0) {
        $swal.error("Nominal kasbon harus diisi dengan benar");
        return false    ;
    }
    return true;
}

const submitKasbonForm = async () => {
  if (!formValidation()) return;
  formLoading.value = true;
  
  try {
    let tanggalFormatted = formData.value.tanggal_pengajuan
    if (tanggalFormatted instanceof Date) {
      tanggalFormatted = tanggalFormatted.toISOString().split('T')[0];
    } else if (typeof tanggalFormatted === 'string' && tanggalFormatted.includes('T')) {
      tanggalFormatted = tanggalFormatted.split('T')[0];
    }

    const payload = {
      id_principal: formData.value.id_principal,
      tanggal_pengajuan: tanggalFormatted,
      nominal_kasbon_diajukan: Number(formData.value.nominal_kasbon),
      nominal_kasbon_disetujui: Number(formData.value.nominal_kasbon), 
      keterangan: formData.value.keterangan,
      tipe_kasbon: formData.value.tipe_kasbon,
      id_user_pengaju: userId.value,
    };
    await fetchWithAuth("POST",
      `${endpoints.kasbonKlaim}/ajukan`,
      payload
    );
    $swal.success("Kasbon berhasil diajukan!");
    addPengajuanKasbon.value.hide();
    pagination.value = { ...pagination.value };
  } catch (error) {
    console.error("Error submitting kasbon:", error);
  } finally {
    formLoading.value = false;
  }
};

const fetchDropdownData = async () => {
  dropdownLoading.value = true;
  try {
    const principals = await principalService.getAllprincipal();
    dropdownData.value.principal = principals;
  } catch (error) {
    console.error("Error fetching dropdown data:", error);
    dropdownData.value.principal = [];
  } finally {
    dropdownLoading.value = false;
  }
};

onMounted(async () => {
  await fetchDropdownData();
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
      :x="40"
    >
      <Card no-subheader>
        <template #header>Filter Kasbon Klaim</template>
        <template #content>
            <div class="form-grid-card tw-items-end">
            <Label label="Tangal Pengajuan">
              <VueDatePicker
                v-model="tanggalPengajuan"
                :enable-time-picker="false"
                placeholder="yyyy-mm-dd"
                :teleport="true"
                auto-apply
              />
            </Label>
            <Label label="Principal">
              <SelectInput
                v-model="selectedPrincipal"
                placeholder="Pilih Data"
                size="md"
                :search="true"
                :options="dropdownData.principal"
                :loading="dropdownLoading"
                text-field="nama"
                value-field="id"
              />
            </Label>
            <div class="tw-flex tw-gap-2">
              <Button
                :trigger="resetFilters"
                icon="mdi mdi-reload"
                class="tw-h-[38px] tw-w-full xl:tw-w-32 tw-bg-red-500"
              >
                Reset
              </Button>
              <Button
                :trigger="searchQuery"
                :icon="buttonText.icon"
                icon="mdi mdi-magnify"
                class="tw-h-[38px] tw-w-full xl:tw-w-32"
              >
                {{ buttonText.text }}
              </Button>
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
  <FlexBox full flex-col>
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
            <template #header>List Kasbon Klaim</template>
            <template #content>
            <FlexBox full jusEnd class="tw-px-4">
                <Button
                :trigger="showAddModal"
                icon="mdi mdi-plus"
                class="tw-py-2 tw-px-4"
                >
                    Tambah Kasbon
                </Button>
            </FlexBox>
            <ServerTable
                v-if="isServerTable"
                table-width="tw-w-full"
                :columns="kasbonKlaimColumn"
                :key="key"
                :table-data="data"
                :loading="loading"
                :on-pagination-change="onPaginationChange"
                :on-global-filters-change="onColumnFilterChange"
                :on-sorting-change="onSortingChange"
                :pagination="pagination"
                :sorting="sorting"
                :filter="globalFilters"
                :page-count="totalPage"
                :total-data="count"
            />
            <Table
                v-else
                :key="clientKey"
                :columns="kasbonKlaimColumn"
                :table-data="clientData?.pages || []"
            />
            <Modal 
                ref="addPengajuanKasbon" 
                id="addPengajuanKasbon" 
                :centered="true"
            >
                <SlideRightX
                    :duration-enter="0.3"
                    :duration-leave="0.3"
                    :delay-in="0.1"
                    :delay-out="0.1"
                    :initial-x="-20"
                    :x="20">
                    <Card no-subheader>
                        <template #header>Pengajuan Kasbon</template>
                        <template #content>
                            <div class="tw-space-y-4 tw-w-full">
                                <Label label="Principal">
                                    <SelectInput
                                        size="md"
                                        placeholder="Pilih Principal"
                                        :search="true"
                                        :options="dropdownData.principal"
                                        v-model="formData.id_principal"
                                        text-field="nama"
                                        value-field="id"
                                        :disabled="formLoading"
                                    />
                                </Label>
                                <Label label="Tanggal Pengajuan">
                                    <VueDatePicker
                                        v-model="formData.tanggal_pengajuan"
                                        :enable-time-picker="false"
                                        placeholder="yyyy-mm-dd"
                                        :teleport="true"
                                        auto-apply
                                        :disabled="formLoading"
                                    />
                                </Label>
                                <Label label="Nominal Kasbon">
                                    <BFormInput
                                        v-model="formData.nominal_kasbon"
                                        type="number"
                                        placeholder="Masukkan nominal kasbon"
                                        :disabled="formLoading"
                                    />
                                </Label>
                                <Label label="PIC">
                                    <BFormInput
                                        :model-value="picDisplayName"
                                        readonly
                                        :class="'tw-bg-gray-200'"
                                        :disabled="formLoading"
                                    />
                                </Label>
                                <Label label="Tipe Kasbon">
                                    <SelectInput
                                        placeholder="Pilih Tipe"
                                        :search="false"
                                        :options="tipeKasbonList"
                                        v-model="formData.tipe_kasbon"
                                        text-field="nama"
                                        value-field="id"
                                        :disabled="formLoading"
                                    />
                                </Label>
                                <Label label="Keterangan">
                                    <BFormInput
                                        v-model="formData.keterangan"
                                        placeholder="Masukkan keterangan"
                                        :disabled="formLoading"
                                    />
                                </Label>
                                <FlexBox full jusEnd>
                                    <Button
                                        :trigger="submitKasbonForm"
                                        :loading="formLoading"
                                        icon="mdi mdi-check"
                                        class="tw-py-2 tw-px-4 tw-mt-4 tw-bg-green-500">
                                        Ajukan Kasbon
                                    </Button>
                                </FlexBox>
                            </div>
                        </template>
                    </Card>
                </SlideRightX>
            </Modal>
            </template>
        </Card>
    </SlideRightX>
  </FlexBox>
</template>
