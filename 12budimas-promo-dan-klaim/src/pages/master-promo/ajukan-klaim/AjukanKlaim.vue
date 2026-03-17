<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import Button from "@/src/components/ui/Button.vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import Table from "@/src/components/ui/table/Table.vue";
import { useTableSearch } from "@/src/lib/useTableSearch";
import { ajukanKlaimColumn } from "@/src/model/tableColumns/master-promo/ajukan-klaim";
import { BFormInput, BFormCheckbox } from "bootstrap-vue-next";
import { ref, onMounted, computed, watch } from "vue";
import { parseCurrency } from "@/src/lib/utils";
import { useSorting } from "@/src/lib/useSorting";
import { promoService } from "@/src/services/promo";
import { useFiltering } from "@/src/lib/useFiltering";
import { usePagination } from "@/src/lib/usePagination";
import { $swal } from "@/src/components/ui/SweetAlert.vue";
import { useUser } from "@/src/store/user";
import { useRoute, useRouter } from "vue-router";

const userId = computed(() => userStore.user?.value?.id)
const kodePromo = computed(() => route.params.kode_promo);
const fakturList = computed(() => {
  const arr = Array.isArray(klaimData.value?.pages) ? klaimData.value.pages : [];
  return arr;
});

const getCurrentDate = ref(new Date().toLocaleDateString())
const selectedKategoriKlaim = ref(null);
const klaimKategoriData = ref([]);
const promoData = ref(null);
const noKlaim = ref("");

const inputValues = ref({ pph: 0 })
const checkboxStates = ref({
  dpp: false,
  dppPlusPpn: true,
  dppMinusPph: false,
  dppPlusPpnMinusPph: false,
})

const route = useRoute();
const router = useRouter();
const userStore = useUser();
const { onSortingChange, sorting } = useSorting();
const { onPaginationChange, pagination } = usePagination();
const { onColumnFilterChange, globalFilters } = useFiltering();

const isInputDisabled = computed(() => ({
  dpp: !checkboxStates.value.dpp && !checkboxStates.value.dppPlusPpn && 
        !checkboxStates.value.dppMinusPph && !checkboxStates.value.dppPlusPpnMinusPph,
  ppn: !checkboxStates.value.dppPlusPpn && !checkboxStates.value.dppPlusPpnMinusPph,
  pph: !checkboxStates.value.dppMinusPph && !checkboxStates.value.dppPlusPpnMinusPph,
}))

const totalCalculatedDPP = computed(() => {
  return fakturList.value.reduce((sum, faktur) => sum + Number(faktur.calculated_dpp || 0), 0);
});

const totalCalculatedPPNValue = computed(() => {
  return fakturList.value.reduce((sum, faktur) => sum + Number(faktur.calculated_ppn_value || 0), 0);
});

const totalEstimasiKlaim = computed(() => {
  return fakturList.value.reduce((sum, faktur) => sum + Number(faktur.estimasi_klaim || 0), 0);
});

const averagePPNPercent = computed(() => {
  if (fakturList.value.length === 0) return 0;
  const totalPercent = fakturList.value.reduce(
    (sum, faktur) => sum + Number(faktur.ppn || 0), 0);
  return (totalPercent / fakturList.value.length).toFixed(1);
});

const formattedTotalEstimasiKlaim = computed(() => parseCurrency(totalEstimasiKlaim.value));
const formattedTotal = computed(() => parseCurrency(totalCalculation.value));

const totalCalculation = computed(() => {
  const dppNum = Number(totalCalculatedDPP.value);
  const ppnNum = Number(totalCalculatedPPNValue.value);
  const pphNum = Number(inputValues.value.pph);

  if (checkboxStates.value.dpp) return dppNum;
  if (checkboxStates.value.dppPlusPpn) return dppNum + ppnNum;
  if (checkboxStates.value.dppMinusPph) return dppNum - pphNum;
  if (checkboxStates.value.dppPlusPpnMinusPph) return dppNum + ppnNum - pphNum;
  
  return 0;
});

const { endpoints } = promoService;

const fieldPool = [kodePromo];
const queryEntries = computed(() => [
  ["kode_promo=", kodePromo.value]
]);

const options = {
  initialColumnName: "no_faktur",
  checkFieldFilterFunc: (val) => val[1] === undefined || val[1] === null,
  filterFunction: (val) => val[1] !== undefined && val[1] !== null,
  asArgument: true,
};

const [
  klaimData,
  ,
  klaimLoading,
  isServerTable,
  klaimKey,
  searchQuery,
] = useTableSearch(endpoints.promoListFaktur, fieldPool, queryEntries, options);

const fetchPromoDetails = async () => {
  if (!kodePromo) {
    console.error("Kode promo tidak ditemukan di URL.");
    return;
  }

  try {
    const response = await promoService.getDetailPromo({ kode_promo: kodePromo.value });
    promoData.value = Array.isArray(response) ? response[0] : response;
    await fetchKlaimCode();
  } catch (error) {
    console.error("Error fetching promo details:", error);  
    promoData.value = {};
    noKlaim.value = "";
  }
};

const fetchKlaimCode = async () => {
  try {
    const idPrincipal = promoData.value?.id_principal;
    if (!idPrincipal) return;

    const response = await promoService.generateKlaimCode(
      { id_principal: idPrincipal }
    );
    noKlaim.value = response.kode_klaim;
  } catch (error) {
    console.error("Error fetching klaim code:", error);
    noKlaim.value = "";
  }
}

const fetchKlaimKategori = async () => {
  try {
    const response = await promoService.getKlaimKategori();
    klaimKategoriData.value = response;
  } catch (error) {
    console.error("Error fetching klaim kategori:", error);
  }
}

const handleCheckboxChange = (checkboxName, event) => {
  Object.keys(checkboxStates.value).forEach(key => {
    checkboxStates.value[key] = false; 
  });
  checkboxStates.value[checkboxName] = event;
}

const validateForm = () => {
  if (!selectedKategoriKlaim.value) {
    $swal.error("Kategori Klaim harus dipilih");
    return false;
  }

  if (fakturList.value.length === 0) {
    $swal.error("Tidak ada data faktur untuk diajukan klaimnya");
    return false;
  }
  return true;
}

const handlePostAjukanKlaim = async () => {
  if (!validateForm()) return;
  const draftVoucherIds = fakturList.value.map(faktur => faktur.id);

  try {
    const payload = {
      kode_voucher: promoData.value?.kode_promo,
      nomor_klaim: noKlaim.value,
      dpp: totalCalculatedDPP.value,
      ppn: totalCalculatedPPNValue.value,
      pph: inputValues.value.pph,
      total_dpp: totalCalculatedDPP.value,
      total_ppn: totalCalculatedPPNValue.value,
      total_pph: inputValues.value.pph,
      total_klaim_diajukan: totalCalculation.value,
      tanggal_pengajuan_klaim: getCurrentDate.value,
      id_user_adm_klaim: userId.value,
      id_kategori_klaim: selectedKategoriKlaim.value,
      id_draft_voucher: draftVoucherIds,
    };
    await promoService.postAjukanKlaim(payload);
    $swal.success("Berhasil Mengajukan Klaim!");
    setTimeout(() => {
      router.replace({ name: "Master Promo" })
    }, 1000);
  } catch (error) {
    console.error("Error post ajukan klaim:", error);
    throw error;
  }
}

watch(checkboxStates, (newStates) => {
  const activeCheckbox = Object.entries(newStates).filter(([key, value]) => value)
  if (activeCheckbox.length > 1) {
    Object.keys(checkboxStates.value).forEach(key => {
      checkboxStates.value[key] = false; 
    });

    const lastActive = activeCheckbox[activeCheckbox.length - 1];
    checkboxStates.value[lastActive[0]] = true;
  } 
}, { deep: true });

onMounted(async () => {
  fetchPromoDetails();
  fetchKlaimKategori();

  if (kodePromo.value) {
    await searchQuery();
  }
})
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
        <template #header>Ajukan Klaim</template>
        <template #content>
          <div
            full
            class="tw-grid tw-grid-cols-1 sm:tw-grid-cols-2 lg:tw-grid-cols-3 gap-4 tw-w-full tw-px-2"
          >
            <Label label="Tanggal :">
              <BFormInput
                :model-value="getCurrentDate"
                disabled
                placeholder="Tanggal"
              />
            </Label>
            <Label label="No Klaim">
              <BFormInput
                :model-value="noKlaim"
                disabled
                placeholder="No Klaim"
              />
            </Label>
            <Label label="Principal">
              <BFormInput
                :model-value="promoData?.principal"
                disabled
                placeholder="Principal"
              />
            </Label>
            <Label label="Kode Promo">
              <BFormInput
                :model-value="promoData?.kode_promo"
                disabled
                placeholder="Kode Promo"
              />
            </Label>
            <Label label="Nama Promo">
              <BFormInput
                :model-value="promoData?.nama_promo"
                disabled
                placeholder="Nama Promo"
              />
            </Label>
            <Label label="Total Klaim">
              <BFormInput
                :model-value="formattedTotalEstimasiKlaim"
                placeholder="Total klaim"
                disabled
              />
            </Label>
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
        <template #header>List Faktur</template>
        <template #content>
          <ServerTable
            v-if="isServerTable"
            table-width="tw-w-full"
            :columns="ajukanKlaimColumn"
            :key="klaimKey"
            :table-data="fakturList"
            :loading="klaimLoading"
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
            :key="`table-${klaimKey}`"
            :columns="ajukanKlaimColumn"
            :table-data="klaimData?.pages || []"
          />
          <div class="tw-flex tw-flex-col tw-gap-4 tw-w-full tw-px-2">
            <div class="tw-border-b tw-border-t">
              <div class="tw-grid tw-grid-cols-4 tw-max-w-2xl tw-mx-auto tw-py-4">
                <BFormCheckbox
                  :model-value="checkboxStates.dpp"
                  name="dpp"
                  class="tw-text-sm"
                  @update:model-value="(val) => handleCheckboxChange('dpp', val)"
                >
                  DPP
                </BFormCheckbox>
                <BFormCheckbox
                  :model-value="checkboxStates.dppPlusPpn"
                  name="dppPlusPpn"
                  class="tw-text-sm"
                  @update:model-value="(val) => handleCheckboxChange('dppPlusPpn', val)"
                >
                  DPP + PPN
                </BFormCheckbox>
                <BFormCheckbox
                  :model-value="checkboxStates.dppMinusPph"
                  name="dppMinusPph"
                  class="tw-text-sm"
                  @update:model-value="(val) => handleCheckboxChange('dppMinusPph', val)"
                >
                  DPP - PPH
                </BFormCheckbox>
                <BFormCheckbox
                  :model-value="checkboxStates.dppPlusPpnMinusPph"
                  name="dppPlusPpnMinusPph"
                  class="tw-text-sm"
                  @update:model-value="(val) => handleCheckboxChange('dppPlusPpnMinusPph', val)"
                >
                  DPP + PPN - PPH
                </BFormCheckbox>
              </div>
            </div>
            <div class="tw-grid tw-grid-cols-3 tw-gap-4">
              <Label label="DPP">
                <BFormInput 
                  placeholder="Nominal DPP" 
                  readonly
                  :model-value="parseCurrency(totalCalculatedDPP)"
                  :class="{ 'tw-bg-gray-200': isInputDisabled.dpp }"
                  />
              </Label>
              <Label :label="`PPN (${averagePPNPercent}%)`">
                <BFormInput 
                  placeholder="Nominal PPN" 
                  readonly
                  :model-value="parseCurrency(totalCalculatedPPNValue)"
                  :class="{ 'tw-bg-gray-200': isInputDisabled.ppn }"
                  />
              </Label>
              <Label label="PPh">
                <BFormInput 
                  placeholder="Nominal PPh" 
                  type="number" 
                  v-model="inputValues.pph"
                  :disabled="isInputDisabled.pph"
                  :class="{ 'tw-bg-gray-200': isInputDisabled.pph }"
                  />
              </Label>
            </div>
             <div class="tw-grid tw-grid-cols-3 tw-gap-4">
              <Label label="Kategori Klaim">
                <SelectInput
                  placeholder="Pilih Data"
                  size="md"
                  class="tw-border-neutral-300"
                  :search="true"
                  :options="klaimKategoriData"
                  text-field="nama"
                  value-field="id"
                  v-model="selectedKategoriKlaim"
                />
              </Label>
              <Label label="Total">
                <BFormInput
                  :model-value="formattedTotal"
                  disabled
                  placeholder="Total"
                />
              </Label>
            </div>
          </div>
          <FlexBox full jus-end>
            <Button
              icon="mdi mdi-check"
              class="tw-bg-green-500 tw-px-4 tw-h-[34px]"
              :trigger="handlePostAjukanKlaim"
              >
              Ajukan Klaim
              </Button>
          </FlexBox>
          </template>
        </Card>
    </SlideRightX>
  </FlexBox>
</template>
