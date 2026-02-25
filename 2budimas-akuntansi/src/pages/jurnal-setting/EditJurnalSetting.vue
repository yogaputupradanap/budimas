<script setup>
import { onMounted, ref, watch, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import TextField from "@/src/components/ui/formInput/TextField.vue";
import Button from "@/src/components/ui/Button.vue";
import { $swal } from "@/src/components/ui/SweetAlert.vue";

import { fetchWithAuth } from "@/src/lib/utils";
import { useOthers } from "@/src/store/others";
import { useUser } from "@/src/store/user";
import useFiturMal from "@/src/lib/useFiturMal";
import useModul from "@/src/lib/useModul";
import useCoa from "@/src/lib/useCoa";
import useSourceModul from "@/src/lib/useSourceModul";

/* -------------------------------------------------------
    🧠 STATE MANAGEMENT
------------------------------------------------------- */
const router = useRouter();
const route = useRoute();
const others = useOthers();
const user = useUser();

const selectedPerusahaan = ref(null);
const namaJurnalSetting = ref("");
const selectedModul = ref(null);
const selectedCoaMain = ref(null);
const selectedFiturAkhir = ref(null);
const laodingSubmit = ref(false);

// Inisialisasi data dengan struktur detail kosong agar v-for tidak error
const data = ref({
    detail: []
});

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
const { getCoaMain, coa: coaMain, loading: loadingCoaMain } = useCoa();
const { getCoa, coa, loading: loadingCoa } = useCoa();
const { sourceModul, getSourceModul, loading: loadingSourceModul } = useSourceModul();

/* -------------------------------------------------------
    ⚙️ CONSTANT OPTIONS
------------------------------------------------------- */
const tipeTransaksiOption = [
    { label: "Debit", value: 1 },
    { label: "Credit", value: 2 },
];

/* -------------------------------------------------------
    🧩 FORM HANDLERS
------------------------------------------------------- */
const tambahBarisJurnalMalDetail = () => {
    if (!data.value.detail) data.value.detail = [];
    data.value.detail.push({
        id_mal_detail: null,
        id_coa: null,
        type: null,
        id_source_data: null,
        keterangan: null,
        urutan: data.value.detail.length + 1,
        id_modul: selectedModul.value
    });
};

const deleteBarisJurnalMalDetail = (index) => {
    data.value.detail.splice(index, 1);
};

/* -------------------------------------------------------
    🔁 WATCHERS
------------------------------------------------------- */
watch(selectedPerusahaan, async (val) => {
    if (val) {
        // Pastikan memanggil API
        await getCoaMain(val);
        await getCoa(val);
    } else {
        coaMain.value = [];
        coa.value = [];
    }
});

watch(selectedFiturAkhir, async (val) => {
    if (val) {
        await getSourceModul(val);
    } else {
        sourceModul.value = [];
    }
});

/* -------------------------------------------------------
    🧰 UTILITIES
------------------------------------------------------- */
const getResource = async () => {
    try {
        const res = await fetchWithAuth("GET", `/api/akuntansi/get-jurnal-mal-detail/${route.params.id}`);
        
        // Pastikan detail selalu array
        const detailData = res.data?.detail || [];
        console.log(res.data);
        data.value = {
            ...res.data,
            detail: detailData
        };

        // Trigger fetch data pendukung secara eksplisit
        if (res.data.id_perusahaan) {
            getCoaMain(res.data.id_perusahaan);
            getCoa(res.data.id_perusahaan);
        }
        if (res.data.id_fitur_mal) {
            getSourceModul(res.data.id_fitur_mal);
        }

    } catch (err) {
        console.error("Error fetch resource:", err);
    }
};
/* -------------------------------------------------------
    🧾 FORM SUBMIT & VALIDATION
------------------------------------------------------- */
const validateCoa = () => {
    if (!data.value.detail || data.value.detail.length === 0) return false;
    for (const item of data.value.detail) {
        if (!item.id_coa || !item.type || !item.id_source_data) {
            $swal.warning("Semua baris detail jurnal harus diisi lengkap (Akun, Tipe, Sumber Data)");
            return false;
        }
    }
    return true;
};

const isHaveDuplicateCoa = () => {
  const coaIds = data.value.detail
      .map((item) => item.id_coa)
      .filter(Boolean);

  const countMap = coaIds.reduce((acc, id) => {
    acc[id] = (acc[id] || 0) + 1;
    return acc;
  }, {});

  const duplicateIds = Object.keys(countMap).filter((id) => countMap[id] > 1);

  if (duplicateIds.length === 0) return null;

  // PERBAIKAN: Ambil list sebagai array murni
  const coaList = coa.value?.pages || coa.value || [];

  const duplicateNames = duplicateIds
      .map((id) => {
        // Tambahkan pengecekan Array.isArray sebelum .find()
        const found = Array.isArray(coaList) ? coaList.find((c) => c.id_coa == id) : null;
        return found ? found.nama_akun : `(id: ${id})`;
      })
      .filter(Boolean);

  return `Terdapat Duplicate COA: ${duplicateNames.join(", ")}. Apakah ingin melanjutkan?`;
};

const handleSubmit = async () => {
    errorMessage.value = { perusahaan: "", namaJurnalSetting: "", fiturAkhir: "", mainCoa: "" };

    if (!selectedPerusahaan.value) errorMessage.value.perusahaan = "Perusahaan harus diisi";
    if (!namaJurnalSetting.value) errorMessage.value.namaJurnalSetting = "Nama Jurnal Setting harus diisi";
    if (!selectedFiturAkhir.value) errorMessage.value.fiturAkhir = "Fitur Akhir harus diisi";
    if (!selectedCoaMain.value) errorMessage.value.mainCoa = "Main COA harus diisi";

    if (Object.values(errorMessage.value).some((v) => v)) return;
    if (!validateCoa()) return;

    const duplicateMsg = isHaveDuplicateCoa();
    const isConfirm = duplicateMsg ? await $swal.confirm(duplicateMsg) : await $swal.confirm("Simpan perubahan jurnal setting?");
    
    if (!isConfirm) return;

    laodingSubmit.value = true;
    try {
        const payload = {
            id_perusahaan: selectedPerusahaan.value,
            id_fitur_mal: selectedFiturAkhir.value,
            nama_mal: namaJurnalSetting.value,
            id_modul: selectedModul.value,
            id_jurnal_mal: Number(route.params.id),
            id_coa_main: selectedCoaMain.value,
            detail: data.value.detail,
        };
        await fetchWithAuth("PUT", `/api/akuntansi/update-jurnal-mal`, payload);
        $swal.success("Berhasil memperbarui data");
        router.push("/journal-setting");
    } catch (err) {
        $swal.error(err || "Gagal menyimpan data");
    } finally {
        laodingSubmit.value = false;
    }
};

/* -------------------------------------------------------
    📊 SAFE OPTIONS (Computed)
------------------------------------------------------- */
// Memastikan SelectInput selalu menerima Array, sehingga .find() tidak crash
const fiturMalOptions = computed(() => {
    const raw = fiturMal.value?.pages?.result || fiturMal.value?.pages || fiturMal.value;
    return Array.isArray(raw) ? raw : [];
});

const modulOptions = computed(() => {
    const raw = modul.value?.pages?.result || modul.value?.pages || modul.value;
    return Array.isArray(raw) ? raw : [];
});

const coaMainOptions = computed(() => {
    const raw = coaMain.value?.pages?.result || coaMain.value?.pages || coaMain.value;
    return Array.isArray(raw) ? raw : [];
});

const coaOptions = computed(() => {
    const raw = coa.value?.pages?.result || coa.value?.pages || coa.value;
    return Array.isArray(raw) ? raw : [];
});

const sourceModulOptions = computed(() => {
    const raw = sourceModul.value?.pages?.result || sourceModul.value?.pages || sourceModul.value;
    return Array.isArray(raw) ? raw : [];
});
/* -------------------------------------------------------
    🚀 LIFECYCLE
------------------------------------------------------- */
onMounted(() => {
    getFiturMal();
    getModul();
    getResource();
    getCoaMain();
    
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
                    :disabled="true"
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
                    :options="fiturMalOptions"
                    :disabled="true"
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
                <SelectInput
                    v-else
                    v-model="selectedCoaMain"
                    placeholder="Pilih Data"
                    size="md"
                    :disabled="!selectedPerusahaan"
                    :search="true"
                    :options="coaMainOptions"
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
            <div v-for="(dat,index) in data.detail"
                 class="tw-border-b last-of-type:tw-border-b-0 tw-p-2 form-grid-card-5-col">
              <Label label="Akun">
                <SelectInput
                    v-model="dat.id_coa"
                    class="tw-w-full"
                    placeholder="Pilih Akun"
                    size="md"
                    :options="coaOptions"
                    :disabled="!selectedPerusahaan"
                    :virtual-scroll="true"
                    text-field="nama_akun"
                    value-field="id_coa"
                />
              </Label>
              <BFormRadioGroup
                  v-model="dat.type"
                  :options="tipeTransaksiOption"
                  value-field="value"
                  text-field="label"
                  label="Tipe Transaksi"
                  class="tw-flex tw-gap-2  tw-items-center"
              />
              <Label label="Sumber Data">
                <SelectInput
                    v-model="dat.id_source_data"
                    class="tw-w-full"
                    placeholder="Pilih Sumber Data"
                    size="md"
                    :disabled="!selectedFiturAkhir"
                    :options="modulOptions"
                    text-field="nama_kolom_view"
                    value-field="id_source_data"
                />
              </Label>
              <Label label="Keterangan">
                <SelectInput
                    v-model="dat.id_source_data"
                    class="tw-w-full"
                    placeholder="Pilih Sumber Data"
                    size="md"
                    :disabled="true"
                    :options="sourceModulOptions"
                    text-field="keterangan"
                    value-field="id_source_data"
                />
              </Label>
              <Button class="tw-self-end tw-mt-6" :trigger="() => deleteBarisJurnalMalDetail(index)"
                      icon="mdi  mdi-delete"
                      :disabled="data.detail.length === 1"
                      variant="danger"
                      size="md">
                Hapus
              </Button>
            </div>
            <Button class="tw-self-end tw-mt-6" :trigger="tambahBarisJurnalMalDetail" icon="mdi mdi-plus"
                    variant="primary"
                    size="md">
              Tambah
            </Button>
          </div>
          <div class="tw-flex tw-w-full tw-justify-end">
            <Button
                :loading="laodingSubmit"
                :trigger="handleSubmit"
                icon="mdi mdi-content-save"
                size="md">
              Edit Jurnal Setting
            </Button>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>