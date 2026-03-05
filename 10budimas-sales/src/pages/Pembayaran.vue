<script setup>
import Card from "../components/ui/Card.vue";
import Information from "../components/ui/Information.vue";
import { ListPembayaranColumn } from "../model/tableColumns";
import Table from "../components/ui/table/Table.vue";
import SlideRightX from "../components/animation/SlideRightX.vue";
import FlexBox from "../components/ui/FlexBox.vue";
import { computed, onMounted, ref } from "vue";
import { usePembayaran } from "../store/pembayaran";
import { useDashboard } from "../store/dashboard";
import Modal from "../components/ui/Modal.vue";
import Button from "../components/ui/Button.vue";
import Label from "../components/ui/Label.vue";
import SelectInput from "../components/ui/formInput/SelectInput.vue";
import Skeleton from "../components/ui/Skeleton.vue";
import { fetchWithAuth, formatCurrencyAuto } from "@/src/lib/utils";
import { $swal } from "@/src/components/ui/SweetAlert.vue";

const pembayaranStore = usePembayaran();
const dashboardStore = useDashboard();
const selectedFaktur = ref(null);
const modalRetur = ref(null);
const loadingDataModal = ref(false);
const selectedCN = ref(null);
const selectedNominalCNFormat = computed(
  () => {
    const data = selectedCN.value;
    if (data) {
      const dataSelected = creditNoteOptions.value.find(
        (item) => item.id_cn === data
      );
      return dataSelected ? formatCurrencyAuto(dataSelected.total_cn) : 0;
    } else {
      return 0;
    }
  }
);
const creditNoteOptions = ref([]);

const KunjunganTokoInformations = [
  {
    buttonColor: "tw-bg-blue-500",
    buttonText: "Lunas",
    buttonTextColor: "tw-text-white",
    information: "Status Lunas"
  },
  {
    buttonColor: "tw-bg-gray-300",
    buttonText: "Bayar",
    information: "Status Belum Lunas"
  }
];

const submitAddCn = async () => {
  if (!selectedCN.value) return;
  // loadingDataModal.value = true;
  loadingDataModal.value = false;
  const tagihan = selectedFaktur.value.total_penjualan - selectedFaktur.value.jumlah_bayar - selectedFaktur.value.nominal_retur;
  const dataCn = creditNoteOptions.value.find(
    (item) => item.id_cn === selectedCN.value
  );
  if (tagihan <= dataCn.total_cn) {
    $swal.error(
      `Nominal Credit Note melebihi tagihan. Tagihan: ${formatCurrencyAuto(tagihan)}, Credit Note: ${formatCurrencyAuto(dataCn.total_cn)}`
    );
    return;
  }

  const confirm = await $swal.confirmSubmit(
    "Apakah Anda yakin ingin menggunakan Credit Note ini?"
  );

  if (!confirm) return;

  try {
    const data = {
      id_faktur: selectedFaktur.value.id_faktur,
      id_cn: selectedCN.value
    };
    const res = await fetchWithAuth(
      "POST",
      `${process.env.VUE_APP_API_URL}/api/credit-note/use-credit-note`,
      data
    );
    selectedCN.value = null;
    $swal.success("Berhasil menambahkan Credit Note", res.message);
    modalRetur.value.hide();
    pembayaranStore.getFaktur();
  } catch (error) {
    console.error("Error adding credit note:", error);
    $swal.error(
      "Terjadi kesalahan saat menambahkan Credit Note. Silakan coba lagi."
    );
  } finally {
    loadingDataModal.value = false;
  }
};

const openModalRetur = async (data) => {
  // loadingDataModal.value = true;
  if (!data) {
    $swal.error("Pilih data faktur terlebih dahulu");
    return;
  }
  selectedCN.value = null;
  loadingDataModal.value = true;
  modalRetur.value.show();
  try {
    const res = await fetchWithAuth(
      "GET",
      `${process.env.VUE_APP_API_URL}/api/credit-note/get-list-credit-note?customer_id=${data.id_customer}&id_principal=${data.id_principal}`
    );
    creditNoteOptions.value = res.data;
    selectedFaktur.value = data;
    loadingDataModal.value = false;
  } catch (e) {
    console.error("Error fetching credit notes:", e);
    loadingDataModal.value = false;
    $swal.error(
      "Terjadi kesalahan saat mengambil data Credit Note. Silakan coba lagi."
    );
  }
};

onMounted(async () => {
  await pembayaranStore.getFaktur();
});
</script>

<template>
  <FlexBox flex-col class="md:tw-pl-6 tw-pl-0">
    <Modal ref="modalRetur" id="modalRetur" size="xl" :centered="true">
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
              <span>Penggunaan Retur</span>
            </div>
          </template>
          <template #content>
            <div class="tw-space-y-4 tw-w-full">
              <Label label="Pilih Credit Note">
                <Skeleton v-if="loadingDataModal" class="skeleton" />
                <SelectInput
                  v-else
                  v-model="selectedCN"
                  placeholder="Pilih Nominal Credit Note"
                  size="md"
                  :search="true"
                  :options="creditNoteOptions"
                  :virtual-scroll="true"
                  text-field="kode_cn"
                  value-field="id_cn" />
              </Label>
              <Label label="Nominal Retur">
                <Skeleton v-if="loadingDataModal" class="skeleton" />
                <BFormInput
                  v-else
                  :model-value="selectedNominalCNFormat"
                  disabled />
              </Label>
              <div class="tw-mt-4 tw-flex tw-gap-4 tw-justify-end">
                <Button
                  :loading="loadingDataModal"
                  :trigger="() => modalRetur.hide()"
                  icon="mdi mdi-close"
                  class="tw-h-[38px] tw-w-auto tw-px-6 tw-bg-gray-500 hover:tw-bg-gray-600">
                  Batal
                </Button>
                <Button
                  :loading="loadingDataModal"
                  :trigger="submitAddCn"
                  :disabled="!selectedCN"
                  icon="mdi mdi-check"
                  class="tw-h-[38px] tw-w-auto tw-px-6 tw-bg-green-500 hover:tw-bg-green-600">
                  Gunakan
                </Button>
              </div>
            </div>
          </template>
        </Card>
      </SlideRightX>
    </Modal>
    <SlideRightX
      class="tw-w-full tw-bg-white tw-rounded-lg tw-shadow-lg"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card>
        <template #header>List Pembayaran</template>
        <template #subheader>Silahkan cek pembayaran terlebih dahulu</template>
        <template #content>
          <div class="tw-w-full tw-px-8">
            <Table
              :key="pembayaranStore.tableKey"
              :loading="pembayaranStore.loading"
              :columns="ListPembayaranColumn(openModalRetur)"
              :table-data="pembayaranStore.listPembayaran"
              classic />
          </div>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="tw-bg-white tw-rounded-lg tw-shadow-lg tw-w-full"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.3"
      :delay-out="0.3"
      :initial-x="-40"
      :x="40">
      <Information :informations="KunjunganTokoInformations" />
    </SlideRightX>
  </FlexBox>
</template>
