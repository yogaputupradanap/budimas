<script setup>
import {nextTick, onMounted, ref, watch} from "vue";
import {useRouter} from "vue-router";
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import TextField from "@/src/components/ui/formInput/TextField.vue";
import Button from "@/src/components/ui/Button.vue";
import {$swal} from "@/src/components/ui/SweetAlert.vue";

import {fetchWithAuth} from "@/src/lib/utils";
import {useOthers} from "@/src/store/others";
import {useUser} from "@/src/store/user";
import useFiturMal from "@/src/lib/useFiturMal";
import useModul from "@/src/lib/useModul";
import useCoa from "@/src/lib/useCoa";
import useSourceModul from "@/src/lib/useSourceModul";

/* -------------------------------------------------------
   🧠 STATE MANAGEMENT
------------------------------------------------------- */
const router = useRouter();
const others = useOthers();
const user = useUser();

const selectedPerusahaan = ref(null);
const namaJurnalSetting = ref("");
const selectedModul = ref(null);
const selectedCoaMain = ref(null);
const selectedTipeTransaksi = ref(null);
const selectedSourceData = ref(null);
const selectedFiturAkhir = ref(null);
const dataTableJournalSetting = ref([]);
const isForAnotherPrincipal = ref(false);
const checkBoxAnotherPrincipal = ref(null)

const dataJurnalMalDetail = ref([
  {id_mal_detail: null, id_coa: null, type: null, id_source_data: null, keterangan: null},
]);

const dataJurnalMalDetailAnotherPrincipal = ref([]);
const optionsForAnotherPrincipal = ref([]);
const laodingSubmit = ref(false);

const errorMessage = ref({
  perusahaan: "",
  namaJurnalSetting: "",
  fiturAkhir: "",
  modul: "",
  mainCoa: "",
});

/* -------------------------------------------------------
    📦 STORE & API DATA
------------------------------------------------------- */
const { fiturMal, loading: loadingFiturMal, getFiturMal } = useFiturMal();
const { modul, getModul, loading: loadingModul } = useModul();

// Panggil satu kali, destructure semua
const { 
    coa, 
    coaMain, 
    loading: loadingCoaMain,
    getCoa, 
    getCoaMain, 
    getCoaByParentId 
} = useCoa();

const { 
    sourceModul, 
    getSourceModul, 
    loading: loadingSourceModul 
} = useSourceModul();

/* -------------------------------------------------------
   ⚙️ CONSTANT OPTIONS
------------------------------------------------------- */
const tipeTransaksiOption = [
  {label: "Debit", value: 1},
  {label: "Credit", value: 2},
];

/* -------------------------------------------------------
   🧩 FORM HANDLERS
------------------------------------------------------- */
const tambahBarisJurnalMalDetail = () => {
  dataJurnalMalDetail.value.push({
    id_mal_detail: null,
    id_coa: null,
    type: null,
    id_source_data: null,
    keterangan: null,
  });
};

const tambahBarisJurnalMalDetailAnotherPrincipal = () => {
  const rows = []
  dataJurnalMalDetail.value.forEach((item) => {
    const coaSelected = coa.value.find((c) => c.id_coa === item.id_coa);
    rows.push({type: item.type, id_coa_parent: coaSelected.parent_id, id_coa: null});
  });
  dataJurnalMalDetailAnotherPrincipal.value.push(rows);
}

const deleteRowDataJurnalMalDetail = (index) => {
  if (isForAnotherPrincipal.value) {
    dataJurnalMalDetailAnotherPrincipal.value = []
    isForAnotherPrincipal.value = false
  }
  dataJurnalMalDetail.value.splice(index, 1);
};

/* -------------------------------------------------------
   🔁 WATCHERS
------------------------------------------------------- */
watch(selectedPerusahaan, (val) => {
  selectedCoaMain.value = null;
  resetCoaInDetails();
  if (val) {
    getCoaMain(val);
    getCoa(val);
  } else {
    coaMain.value = [];
  }
});

watch(selectedFiturAkhir, (val) => {
  resetSourceDataInDetails();
  sourceModul.value = [];
  if (val) getSourceModul(val);
});

watch(isForAnotherPrincipal, async (val) => {
  if (!val) {
    dataJurnalMalDetailAnotherPrincipal.value = [];
    return;
  }
  let noValid = false
  dataJurnalMalDetail.value.forEach(
      (item) => {
        if (!item.id_coa || !item.type || !item.id_source_data) {
          noValid = true
        }
      }
  )
  if (noValid) {
    $swal.warning("Semua data di detail jurnal setting harus diisi terlebih dahulu");
    await nextTick();
    isForAnotherPrincipal.value = false; // uncheck checkbox di UI
    return;
  }

  const rows = [];
  const parentIds = [];

  dataJurnalMalDetail.value.forEach((item) => {
    const coaSelected = coa.value.find((c) => c.id_coa === item.id_coa);
    if (coaSelected) {
      rows.push({type: item.type, id_coa_parent: coaSelected.parent_id, id_coa: null});
      parentIds.push({parent_id: coaSelected.parent_id, id_coa: coaSelected.id_coa});
    }
  });
  const idsCoaParent = parentIds.map(item => item.parent_id).filter(item => item).join(",");
  if (!idsCoaParent) {
    $swal.warning("Tidak ada COA yang valid untuk principal lain");
    await nextTick();
    isForAnotherPrincipal.value = false; // uncheck checkbox di UI
    return;
  }
  const res = await getCoaByParentId(selectedPerusahaan.value, idsCoaParent);
  const sorted = [];

  parentIds.forEach((pid) => {
    const filtered = res.filter((c) =>
        pid.parent_id
            ? c.parent_id === pid.parent_id || c.id_coa === pid.parent_id
            : c.id_coa === pid.id_coa
    );
    sorted.push(filtered);
  });

  dataJurnalMalDetailAnotherPrincipal.value = [rows];
  optionsForAnotherPrincipal.value = sorted;
});

watch(dataJurnalMalDetail,
    () => {
      isForAnotherPrincipal.value = false
      dataJurnalMalDetailAnotherPrincipal.value = [];
    },
    {deep: true}
)

/* -------------------------------------------------------
   🧰 UTILITIES
------------------------------------------------------- */
const resetCoaInDetails = () => {
  dataJurnalMalDetail.value = dataJurnalMalDetail.value.map((i) => ({...i, id_coa: null}));
};

const resetSourceDataInDetails = () => {
  dataJurnalMalDetail.value = dataJurnalMalDetail.value.map((i) => ({...i, id_source_data: null}));
};

/* -------------------------------------------------------
   🧾 FORM SUBMIT
------------------------------------------------------- */

const validateCoa = () => {
  for (const item of dataJurnalMalDetail.value) {
    if (!item.id_coa || !item.type || !item.id_source_data) {
      $swal.warning("Semua Akun di detail jurnal setting harus diisi");
      return false;
    }
  }
  for (const item of dataJurnalMalDetailAnotherPrincipal.value) {
    for (const subItem of item) {
      if (!subItem.id_coa) {
        $swal.warning("Semua Akun di detail jurnal setting untuk principal lain harus diisi");
        return false;
      }
    }
  }
  return true;
};
const isHaveDuplicateCoa = () => {
  // Kumpulkan semua id_coa dari detail utama dan another principal
  const coaIds = dataJurnalMalDetail.value
      .map((item) => item.id_coa)
      .filter(Boolean);

  for (const item of dataJurnalMalDetailAnotherPrincipal.value) {
    for (const subItem of item) {
      if (subItem.id_coa_parent === null || !subItem.id_coa) continue;
      coaIds.push(subItem.id_coa);
    }
  }

  // Hitung frekuensi untuk cari duplikat
  const countMap = coaIds.reduce((acc, id) => {
    acc[id] = (acc[id] || 0) + 1;
    return acc;
  }, {});

  // Ambil id yang muncul lebih dari 1x
  const duplicateIds = Object.keys(countMap).filter((id) => countMap[id] > 1);

  if (duplicateIds.length === 0) {
    return null;
  }

  // Ambil nama akun dari store coa.value
  const duplicateNames = duplicateIds
      .map((id) => {
        const found = coa.value.find((c) => c.id_coa == id);
        return found ? found.nama_akun : `(id: ${id})`;
      })
      .filter(Boolean);

  return `Terdapat Duplicate COA di detail jurnal setting: ${duplicateNames.join(", ")}. Apakah anda ingin melanjutkan?`;
};


const handleSubmit = async () => {
  // 1. Reset & Validasi Error
  errorMessage.value = { perusahaan: "", namaJurnalSetting: "", fiturAkhir: "", mainCoa: "" };

  if (!selectedPerusahaan.value) errorMessage.value.perusahaan = "Perusahaan harus diisi";
  if (!namaJurnalSetting.value) errorMessage.value.namaJurnalSetting = "Nama Jurnal Setting harus diisi";
  if (!selectedFiturAkhir.value) errorMessage.value.fiturAkhir = "Fitur Akhir harus diisi";
  if (!selectedCoaMain.value) errorMessage.value.mainCoa = "Main COA harus diisi";

  if (Object.values(errorMessage.value).some((v) => v)) return;
  if (!validateCoa()) return;

  // 2. Konfirmasi User
  const isHaveMessageDuplicate = isHaveDuplicateCoa();
  const confirmText = isHaveMessageDuplicate || "Apakah anda yakin ingin menyimpan data ini?";
  const isConfirm = await $swal.confirm(confirmText);
  if (!isConfirm) return;

  try {
    const detail = [];

    // 3. Mapping Detail Utama
    // Gunakan .forEach untuk push ke array (lebih tepat dibanding .map jika tidak mengambil return value)
    dataJurnalMalDetail.value.forEach((item, index) => {
      detail.push({
        id_coa: item.id_coa,
        type: item.type, // Pastikan nilainya 1 (debit) atau 2 (kredit) sesuai backend
        id_source_data: item.id_source_data, // Pastikan ini berisi ID yang valid dari source_modul
        urutan: index + 1,
      });
    });

    // 4. Mapping Detail untuk Principal Lain (jika ada)
    if (isForAnotherPrincipal.value) {
      dataJurnalMalDetailAnotherPrincipal.value.forEach((item) => {
        item.forEach((subItem, index) => {
          // Hanya push jika ada COA yang terpilih
          if (subItem.id_coa) { 
            detail.push({
              id_coa: subItem.id_coa,
              type: subItem.type,
              id_source_data: dataJurnalMalDetail.value[index].id_source_data,
              urutan: index + 1,
            });
          }
        });
      });
    }

    // 5. Konstruksi Payload
    const payload = {
      id_perusahaan: selectedPerusahaan.value,
      id_fitur_mal: selectedFiturAkhir.value,
      id_coa_main: selectedCoaMain.value, // Backend mengharapkan id_coa_main
      nama_mal: namaJurnalSetting.value,
      id_modul: selectedModul.value, // Tetap dikirim jika backend membutuhkan id_modul di level header
      detail: detail,
    };
    console.log("Payload yang dikirim:", JSON.stringify(payload, null, 2));

    // 6. Eksekusi API
    await fetchWithAuth("POST", `/api/akuntansi/insert-jurnal-mal`, payload);
    
    $swal.success("Data berhasil disimpan");
    router.push("/journal-setting");

  } catch (err) {
    console.error("Error submit jurnal setting:", err);
    // Tampilkan pesan error spesifik dari backend jika ada
    const msg = err.response?.data?.message || err.message || "Terjadi kesalahan saat menyimpan data";
    $swal.error(msg);
  }
};

/* -------------------------------------------------------
   🚀 LIFECYCLE
------------------------------------------------------- */
onMounted(() => {
  getFiturMal();
  getModul();
});
</script>


<template>
  <FlexBox full flex-col>
    <SlideRightX
        class="slide-container tw-z-20"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.1"
        :delay-out="0.1"
        :initial-x="-40"
        :x="40"
    >
      <Card no-subheader>
        <template #header>Tambah Jurnal Setting</template>
        <template #content>
          <div class="tw-w-full tw-space-y-6">
            <div class="form-grid-card-container-2-col">

              <Label label="Perusahaan">
                <Skeleton
                    class="tw-w-full tw-h-[34px]"
                    v-if="others.perusahaan.loading"
                />
                <SelectInput
                    v-else
                    v-model="selectedPerusahaan"
                    placeholder="Pilih Data"
                    size="md"
                    :search="true"
                    :options="others.perusahaan.list"
                    text-field="nama"
                    value-field="id"
                />
                <p class="tw-text-red-500 tw-text-sm" v-if="errorMessage.perusahaan">
                  {{ errorMessage.perusahaan }}</p>
              </Label>
              <Label label="Nama Jurnal Setting">
                <TextField class="tw-w-full" v-model="namaJurnalSetting" placeholder="Masukkan Nama Jurnal Setting"/>
                <p class="tw-text-red-500 tw-text-sm" v-if="errorMessage.namaJurnalSetting">
                  {{ errorMessage.namaJurnalSetting }}</p>
              </Label>
              <Label label="Letak Fitur Akhir">
                <Skeleton
                    class="tw-w-full tw-h-[34px]"
                    v-if="loadingFiturMal"
                />
                <SelectInput
                    v-else
                    v-model="selectedFiturAkhir"
                    placeholder="Pilih Data"
                    size="md"
                    :search="true"
                    :options="fiturMal?.result"
                    text-field="nama_fitur_mal"
                    value-field="id_fitur_mal"
                />
                <p class="tw-text-red-500 tw-text-sm" v-if="errorMessage.fiturAkhir">
                  {{ errorMessage.fiturAkhir }}</p>
              </Label>
              <Label label="Main COA">
                <Skeleton
                    class="tw-w-full tw-h-[34px]"
                    v-if="loadingCoaMain"
                />
                <!-- <pre>{{ coaMain }}</pre> -->
                <SelectInput
                    v-else
                    v-model="selectedCoaMain"
                    placeholder="Pilih Data"
                    size="md"
                    :disabled="!selectedPerusahaan"
                    :search="true"
                    :options="coaMain"
                    text-field="nama_akun"
                    value-field="id_coa"
                />
                <p class="tw-text-red-500 tw-text-sm" v-if="errorMessage.mainCoa">
                  {{ errorMessage.mainCoa }} </p>
              </Label>
            </div>
          </div>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
        class="slide-container tw-z-10"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.1"
        :delay-out="0.1"
        :initial-x="-40"
        :x="40"
    >
      <Card no-subheader no-header class="tw-mt-6">
        <template #content>
          <div class=" tw-w-full tw-p-2  tw-mt-4">
            <div v-for="(data,index) in dataJurnalMalDetail"
                 class="form-grid-card-5-col tw-border-b last-of-type:tw-border-b-0 tw-p-2">
              <Label label="Akun">
                <SelectInput
                    v-model="data.id_coa"
                    class="tw-w-full"
                    placeholder="Pilih Akun"
                    size="md"
                    :options="coa"
                    :disabled="!selectedPerusahaan"
                    :virtual-scroll="true"
                    text-field="nama_akun"
                    value-field="id_coa"
                />
              </Label>
              <BFormRadioGroup
                  v-model="data.type"
                  :options="tipeTransaksiOption"
                  value-field="value"
                  text-field="label"
                  label="Tipe Transaksi"
                  class="tw-flex tw-gap-2  tw-items-center"
              />
              <Label label="Sumber Data">
                <SelectInput
                    v-model="data.id_source_data"
                    class="tw-w-full"
                    placeholder="Pilih Sumber Data"
                    size="md"
                    :disabled="!selectedFiturAkhir"
                    :options="sourceModul"
                    text-field="nama_kolom_view"
                    value-field="id_source_data"
                />
              </Label>
              <Label label="Keterangan">
                <SelectInput
                    v-model="data.id_source_data"
                    class="tw-w-full"
                    placeholder="Pilih Sumber Data"
                    size="md"
                    :disabled="true"
                    :options="sourceModul"
                    text-field="keterangan"
                    value-field="id_source_data"
                />
              </Label>
              <div class="tw-flex tw-items-center">
                <Button
                    class="tw-w-full"
                    :trigger="()=>deleteRowDataJurnalMalDetail(index)"
                    icon="mdi mdi-delete"
                    :disabled="dataJurnalMalDetail.length ===1"
                    variant="danger"
                    size="md">
                  Hapus
                </Button>
              </div>
            </div>
            <Button class="tw-self-end tw-mt-6" :trigger="tambahBarisJurnalMalDetail" icon="mdi mdi-plus"
                    variant="primary"
                    size="md">
              Tambah
            </Button>
          </div>
          <div class="tw-flex tw-justify-start tw-w-full tw-gap-2 tw-mb-4">
            <BFormCheckbox ref="checkBoxAnotherPrincipal" v-model="isForAnotherPrincipal">
              Terapkan Jurnal Setting untuk principal lain
            </BFormCheckbox>
          </div>
          <template v-if="isForAnotherPrincipal">
            <div class=" tw-w-full tw-p-2  tw-mt-4">
              <div v-for="(dataDetail,indexDetail) in dataJurnalMalDetailAnotherPrincipal"
                   :class="[

    {
      'form-grid-card-1-col': dataDetail.length + 1 === 1,
      'form-grid-card-2-col': dataDetail.length + 1 === 2,
      'form-grid-card-3-col': dataDetail.length + 1 === 3,
      'form-grid-card-4-col': dataDetail.length + 1 === 4,
      'form-grid-card-5-col': dataDetail.length + 1 === 5,
      'form-grid-card-6-col': dataDetail.length + 1 === 6,
    }
  ]">
                <div v-for="(dataOption,index) in dataDetail">
                  <Label :label="dataOption.type ===1 ? 'Debit' : 'Credit'">
                    <SelectInput
                        v-model="dataJurnalMalDetailAnotherPrincipal[indexDetail][index].id_coa"
                        class="tw-w-full"
                        placeholder="Pilih Akun"
                        size="md"
                        :options="optionsForAnotherPrincipal[index]"
                        :disabled="!selectedPerusahaan"
                        :virtual-scroll="true"
                        text-field="nama_akun"
                        value-field="id_coa"
                    />
                  </Label>
                </div>
                <Button
                    class="tw-self-center tw-mt-6"
                    :trigger="()=>{dataJurnalMalDetailAnotherPrincipal.splice(indexDetail,1);}"
                    icon="mdi mdi-delete"
                    variant="danger"
                    size="md">
                  Hapus
                </Button>
              </div>
              <Button class="tw-self-end tw-mt-6" :trigger="tambahBarisJurnalMalDetailAnotherPrincipal"
                      icon="mdi mdi-plus"
                      variant="primary"
                      size="md">
                Tambah
              </Button>
            </div>
          </template>
          <div class="tw-flex tw-w-full tw-justify-end">
            <Button
                :loading="laodingSubmit"
                :trigger="handleSubmit"
                icon="mdi mdi-content-save"
                size="md">
              Tambah Jurnal Setting
            </Button>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>