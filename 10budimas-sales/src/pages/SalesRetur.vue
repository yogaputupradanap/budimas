<script setup>
import FlexBox from "../components/ui/FlexBox.vue";
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import { computed, nextTick, reactive, ref } from "vue";
import { useCommonForm } from "../lib/useCommonForm";
import { tambahProdukReturSchema } from "../model/formSchema";
import Modal from "../components/ui/Modal.vue";
import SelectInput from "../components/ui/formInput/SelectInput.vue";
import TextField from "../components/ui/formInput/TextField.vue";
import Table from "../components/ui/table/Table.vue";
import { confirmListReturColumns, listReturColumns } from "../model/tableColumns";
import { apiUrl, deepCopy, fetchWithAuth, sessionDisk } from "../lib/utils";
import Empty from "../components/ui/Empty.vue";
import { usePrincipal } from "../store/principal";
import VueDatePicker from "@vuepic/vue-datepicker";
import Loader from "../components/ui/Loader.vue";
import { useSales } from "../store/sales";
import { useKunjungan } from "../store/kunjungan";
import Button from "../components/ui/Button.vue";
import { useAlert } from "../store/alert";
import { $swal } from "@/src/components/ui/SweetAlert.vue";


const principal = usePrincipal();
const kunjungan = useKunjungan();
const sales = useSales();
const notaFakturList = ref([]);
const alert = useAlert();
const searchField = ref("");
const notaFaktur = reactive({ name: "", id: 0 });
const productOptions = ref([]);
const listReturTable = ref([]);
const listRealReturTable = ref([]);
const rowIndex = ref(0);
const tanggalRetur = ref(new Date());
const user = sessionDisk.getSession("authUser");
const listReturRequestBefore = ref([]);
const loadingFaktur = ref(true);
const errorKeterangan = ref("");
const keteranganOption = ref([
  {
    text: "Produk Rusak"
  },
  {
    text: "Produk Kadaluarsa"
  },
  {
    text: "Lainnya"
  }
]);
const selectedKeterangan = ref("");
const selectedFaktur = ref();
const { configProps, defineField, handleSubmit, resetForm } = useCommonForm(
  tambahProdukReturSchema
);
const [namaProduk, namaProdukProps] = defineField("namaProduk", configProps);
const [piecesBad, piecesBadProps] = defineField("piecesBad", configProps);
const [piecesGood, piecesGoodProps] = defineField("piecesGood", configProps);
const [boxBad, boxBadProps] = defineField("boxBad", configProps);
const [boxGood, boxGoodProps] = defineField("boxGood", configProps);
const [kartonGood, kartonGoodProps] = defineField("kartonGood", configProps);
const [kartonBad, kartonBadProps] = defineField("kartonBad", configProps);
const [
  keteranganRetur,
  keteranganReturProps
] = defineField("keteranganRetur", configProps);

const editModalRetur = ref();
const searchModal = ref();
const submitModal = ref();
const isEdit = ref(false);
const returTableKey = ref(0);

const totalPenjualan = computed(() =>
  listReturTable.value.reduce((total, value) => total + value.subtotalorder, 0)
);

const searchNota = async () => {
  if (!searchField.value) return (notaFakturList.value = []);

  const plafonId = JSON.stringify(principal.idPlafons);
  loadingFaktur.value = true;
  searchModal.value.show();

  notaFakturList.value = await fetchWithAuth(
    "GET",
    `${apiUrl}/api/sales/search-invoice?id_plafon=${plafonId}&search=${searchField.value}`
  ) || [];

  loadingFaktur.value = false;
};

const calculateKonversi = (value, data_konversi) => {
  const konversi = {
    pieces: 0,
    box: 0,
    karton: 0
  };
  const level1 = data_konversi.find(
    (val) => val.level === 1
  );
  const level2 = data_konversi.find(
    (val) => val.level === 2
  );
  const level3 = data_konversi.find(
    (val) => val.level === 3
  );
  konversi.pieces = value.pieces + (value.box * level2.faktor_konversi) + (value.karton * level3.faktor_konversi);
  konversi.box = Math.floor(konversi.pieces / level2.faktor_konversi);
  konversi.karton = Math.floor(konversi.pieces / level3.faktor_konversi);

  return konversi;
};

const selectNotaFaktur = async (id) => {
  selectedFaktur.value = notaFakturList.value.find((val) => val.id === id);
  const options = deepCopy(selectedFaktur.value.products);
  const initDataTable = deepCopy(selectedFaktur.value.products);

  notaFaktur.name = selectedFaktur.value.no_faktur;
  productOptions.value = options.map((option) => {
    const optionTemp = {
      ...option,
      ...option.produk
    };

    delete optionTemp.produk;

    return optionTemp;
  });

  listReturTable.value = initDataTable.map((value) => ({
    ...value,
    total_penjualan: selectedFaktur.value.total_penjualan,
    keteranganRetur: ""
  }));

  searchModal.value.hide();
  returTableKey.value++;
  listReturRequestBefore.value = await getIsHaveReturBefore(selectedFaktur.value.id_sales_order);
};


const updateProduk = handleSubmit((value) => {

  if (!selectedKeterangan.value || (selectedKeterangan.value === "Lainnya" && !keteranganRetur.value)) {
    errorKeterangan.value = "Keterangan retur harus diisi";
    return;
  } else {
    errorKeterangan.value = "";
  }

  const retur = listReturTable.value.find(
    (val) => val.id_produk === value.namaProduk
  );

  if (!retur) {
    $swal.error("Produk tidak ditemukan");
    return;
  }


  const dataTotalAfterKonversiTemp = calculateKonversi({
    pieces: retur.pieces_delivered,
    box: retur.box_delivered,
    karton: retur.karton_delivered
  }, retur.konversi);

  const dataTotalReturBadTemp = calculateKonversi({
    pieces: value.piecesBad,
    box: value.boxBad,
    karton: value.kartonBad
  }, retur.konversi);

  const dataTotalReturGoodTemp = calculateKonversi({
    pieces: value.piecesGood,
    box: value.boxGood,
    karton: value.kartonGood
  }, retur.konversi);

  const dataReturBeforeTemp = listReturRequestBefore.value.filter(
    (item) => item.id_produk === value.namaProduk
  );

  let dataTotalReturBefore = {
    pieces: 0,
    box: 0,
    karton: 0
  };

  // INFO if have retur before
  if (dataReturBeforeTemp) {
    dataTotalReturBefore = dataReturBeforeTemp.reduce(
      (acc, item) => {
        const dataKonversi = calculateKonversi(
          {
            pieces: item.pieces_diajukan + item.pieces_good_diajukan,
            box: item.box_diajukan + item.box_good_diajukan,
            karton: item.karton_diajukan + item.karton_good_diajukan
          },
          retur.konversi
        );

        // Tambahkan ke akumulator
        acc.pieces += dataKonversi.pieces || 0;
        acc.box += dataKonversi.box || 0;
        acc.karton += dataKonversi.karton || 0;

        return acc;
      },
      {
        pieces: 0,
        box: 0,
        karton: 0
      }
    );
  }


  if (dataTotalReturBadTemp.pieces < 0 && dataTotalReturGoodTemp.pieces < 0) {
    $swal.error("Jumlah retur tidak boleh kurang dari 0");
    return;
  }

  // INFO if pieces retur is 0, remove from listRealReturTable and listReturTable
  if ((dataTotalReturGoodTemp.pieces + dataTotalReturBadTemp.pieces) === 0) {
    listRealReturTable.value = listRealReturTable.value.filter(
      (val) => val.id_produk !== retur.id_produk
    );
    const newRetur = {
      ...retur,
      pieces_retur: 0,
      box_retur: 0,
      karton_retur: 0,
      keteranganRetur: ""
    };

    listReturTable.value[rowIndex.value] = newRetur;
    returTableKey.value++;
    closeFormModal();
    return;
  }


  if (dataTotalAfterKonversiTemp.pieces < ((dataTotalReturGoodTemp.pieces + dataTotalReturBadTemp.pieces) + dataTotalReturBefore.pieces)) {
    $swal.error(
      "Jumlah retur sudah melebihi penerimaan"
    );
    return;
  }

  const newRetur = {
    ...retur,
    pieces_retur_bad: value.piecesBad,
    box_retur_bad: value.boxBad,
    karton_retur_bad: value.kartonBad,
    pieces_retur_good: value.piecesGood,
    box_retur_good: value.boxGood,
    karton_retur_good: value.kartonGood,
    keteranganRetur:
      selectedKeterangan.value === "Lainnya"
        ? keteranganRetur.value
        : selectedKeterangan.value
  };

  listReturTable.value[rowIndex.value] = newRetur;

  const isExist = listRealReturTable.value.find(
    (val) => val.id_produk === newRetur.id_produk
  );
  if (isExist) {
    listRealReturTable.value = [
      ...listRealReturTable.value.filter(
        (val) => val.id_produk !== newRetur.id_produk
      ),
      newRetur
    ];
  } else {
    listRealReturTable.value = [
      ...listRealReturTable.value,
      newRetur
    ];
  }

  returTableKey.value++;
  closeFormModal();
});

const getIsHaveReturBefore = async (id_sales_order) => {
  try {
    const response = await fetchWithAuth(
      "GET",
      `${apiUrl}/api/sales/check-retur?id_sales_order=${id_sales_order}`
    );
    return response;
  } catch (error) {
    console.error("Error checking retur:", error);
    return [];
  }
};

const openEditModal = (values) => {
  namaProduk.value = values.value.namaProduk;
  const retur = listReturTable.value.find(
    (val) => val.id_produk === values.value.namaProduk
  );

  piecesBad.value = retur.pieces_retur_bad || 0;
  piecesGood.value = retur.pieces_retur_good || 0;
  kartonBad.value = retur.karton_retur_bad || 0;
  kartonGood.value = retur.karton_retur_good || 0;
  boxBad.value = retur.box_retur_bad || 0;
  boxGood.value = retur.box_retur_good || 0;
  rowIndex.value = values.rowIndex;
  const readKeterangan = listReturTable.value[values.rowIndex].keteranganRetur;
  const checkKeterangan = keteranganOption.value.some(
    (val) => val.text === readKeterangan
  );

  selectedKeterangan.value = readKeterangan.length
    ? checkKeterangan
      ? readKeterangan
      : "Lainnya"
    : "";

  keteranganRetur.value = checkKeterangan ? "" : readKeterangan;

  nextTick(() => {
    editModalRetur.value.show();
  });
};

const closeFormModal = () => {
  resetForm();
  selectedKeterangan.value = "";
  editModalRetur.value.hide();
};

const sendRetur = async () => {

  if (!listRealReturTable.value.length) {
    $swal.error("Tidak ada produk retur yang dipilih");
    return;
  }

  const isConfirm = await $swal.confirm(
    `Apakah anda yakin ingin mengirim retur untuk faktur ${selectedFaktur.value.no_faktur}?`
  );

  if (!isConfirm) return;
  const retur = {
    ...selectedFaktur.value,
    id_sales: user.id_sales,
    tanggal_request_retur: tanggalRetur.value ? tanggalRetur.value.toISOString().split("T")[0] : new Date().toISOString().split("T")[0],
    products: listRealReturTable.value.map((produk) => ({
      id_sales_order_detail: produk.id,
      id_produk: produk.id_produk,
      harga_satuan: produk.hargaorder,
      keterangan_retur: produk.keteranganRetur,
      pieces_retur_good: produk.pieces_retur_good || 0,
      pieces_retur_bad: produk.pieces_retur_bad || 0,
      box_retur_good: produk.box_retur_good || 0,
      box_retur_bad: produk.box_retur_bad || 0,
      karton_retur_good: produk.karton_retur_good || 0,
      karton_retur_bad: produk.karton_retur_bad || 0
    }))
  };
  try {
    await fetchWithAuth("POST", `${apiUrl}/api/sales/sales-retur`, retur);

    listReturTable.value = [];
    listRealReturTable.value = [];
    returTableKey.value++;
    submitModal.value.hide();
    alert.setMessage("Berhasil buat request retur");
    $swal.success(
      `Berhasil buat request retur`
    );

  } catch (error) {
    alert.setMessage(`Error : ${error}`, "error");
    $swal.error(
      `Gagal buat request retur, silahkan coba lagi`
    );
  }
};
</script>

<template>
  <FlexBox full flex-col class="lg:tw-pl-6 tw-pl-2">
    <SlideRightX
      class="tw-w-full tw-z-20"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card dense no-subheader class="tw-pb-10">
        <template #header>Form Pengajuan Retur</template>
        <template #content>
          <FlexBox flex-col gap="small">
            <span class="tw-font-semibold">Sales</span>
            <BFormInput
              :title="sales?.salesUser?.nama"
              disabled
              :model-value="sales?.salesUser?.nama" />
          </FlexBox>
          <FlexBox flex-col gap="small">
            <span class="tw-font-semibold">Customer</span>
            <BFormInput
              disabled
              :title="kunjungan.activeKunjungan?.kunjungan?.nama_customer"
              :model-value="
                  kunjungan.activeKunjungan?.kunjungan?.nama_customer
                " />
          </FlexBox>
          <FlexBox flex-col gap="small">
            <span class="tw-font-semibold">Tanggal Retur</span>
            <VueDatePicker
              v-model="tanggalRetur"
              :enable-time-picker="false"
              placeholder="mm/dd/yyyy"
              disabled="true"
              :teleport="true"
              auto-apply />
          </FlexBox>
          <FlexBox flex-col gap="small">
            <span class="tw-font-semibold">Nota Faktur</span>
            <BFormInput
              disabled
              :title="notaFaktur?.name"
              :model-value="
                  notaFaktur?.name
                " />
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="tw-w-full tw-z-20"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card dense no-subheader class="tw-pb-10">
        <template #header>Cari Nota Faktur</template>
        <template #content>
          <FlexBox full jus-center>
            <FlexBox full flex-col it-center>
              <!-- <span>Input nota faktur</span> -->
              <div class="tw-w-full md:tw-w-[400px] lg:tw-w-[420px] tw-flex tw-gap-2">
                <BFormInput v-model="searchField" @keyup.enter="searchNota"
                            placeholder="Klik cari atau tekan enter..."
                />
                <BButton class="tw-bg-blue-500" @click="searchNota">
                  <i class="mdi mdi-magnify tw-mr-2"></i>
                  Cari
                </BButton>
              </div>
              <Modal ref="searchModal" id="searchModal">
                <Card dense no-subheader class="tw-p-4">
                  <template #header>
                    <span class="tw-text-black">Hasil Cari</span>
                  </template>
                  <template #content>
                    <FlexBox
                      full
                      jus-center
                      it-center
                      class="tw-h-64"
                      v-if="loadingFaktur">
                      <Loader />
                    </FlexBox>
                    <FlexBox full jus-center it-center v-else>
                      <FlexBox full flex-col it-end v-if="notaFakturList.length">
                        <div
                          class="tw-w-full tw-border tw-border-slate-400 hover:tw-bg-blue-500 hover:tw-text-white tw-cursor-pointer tw-transition-all tw-duration-500 tw-p-2 tw-rounded-md"
                          v-for="nota in notaFakturList"
                          :key="nota.id"
                          @click="selectNotaFaktur(nota.id)">
                          <span class="">{{ nota.no_faktur }}</span>
                        </div>
                        <span class="tw-text-xs tw-pr-2 tw-text-slate-500">
                          {{ notaFakturList.length }} Nota faktur ditemukan
                        </span>
                      </FlexBox>
                      <Flexbox v-else class="tw-py-16">
                        <Empty text="Kata kunci tidak ditemukan" />
                      </Flexbox>
                    </FlexBox>
                  </template>
                </Card>
              </Modal>
            </FlexBox>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="tw-w-full tw-z-20"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.3"
      :delay-out="0.3"
      :initial-x="-40"
      :x="40">
      <Card dense no-subheader class="tw-pb-10">
        <template #header>List Retur</template>
        <template #content>
          <FlexBox full flex-col it-end :class="[!listReturTable.length && 'tw-py-28']">
            <Table
              v-if="listReturTable.length"
              :columns="listReturColumns"
              :table-data="listReturTable"
              :key="returTableKey"
              @open-row-modal="openEditModal"
              hide-footer
              classic
              hide-toolbar />
            <Empty v-else text="List Retur Kosong" />
            <BButton
              @click="submitModal.show()"
              v-if="listReturTable.length"
              class="tw-bg-green-500"
              size="sm">
              <i class="mdi mdi-check tw-mr-2"></i>
              Submit
            </BButton>
            <!-- INFO Modal Daftar Produk-->
            <Modal id="submitModal" size="lg" ref="submitModal">
              <Card no-subheader>
                <template #header>Daftar Produk Retur</template>
                <template #content>
                  <FlexBox full>
                    <Table
                      :key="returTableKey"
                      :columns="confirmListReturColumns"
                      :table-data="listRealReturTable"
                      hide-footer
                      classic
                      hide-toolbar />
                  </FlexBox>
                  <FlexBox full jus-end>
                    <BButton
                      @click="submitModal.hide()"
                      class="tw-bg-red-500"
                      size="sm">
                      Cancel
                    </BButton>
                    <Button
                      class="tw-bg-green-500"
                      size="sm"
                      :trigger="sendRetur">
                      Submit
                    </Button>
                  </FlexBox>
                </template>
              </Card>
            </Modal>
          </FlexBox>
          <!-- * Modal Tambah Produk-->
          <Modal
            id="editModalRetur"
            ref="editModalRetur"
            @modal-closed="closeFormModal()">
            <Card dense no-subheader no-main-center class="tw-p-4">
              <template #header>
                <span class="tw-text-black">Tambah Produk Retur</span>
              </template>
              <template #content>
                <FlexBox full>
                  <BForm
                    novalidate
                    class="tw-w-full tw-flex tw-flex-col tw-gap-6">
                    <BFormGroup
                      id="input-group-1"
                      label="Nama Produk:"
                      label-for="input-1"
                      v-bind="namaProdukProps">
                      <SelectInput
                        placeholder="Pilih Produk"
                        text-field="nama"
                        search
                        value-field="id_produk"
                        size="md"
                        :options="productOptions"
                        v-model="namaProduk"
                        :disabled="true" />
                    </BFormGroup>
                    <div class="tw-grid tw-grid-cols-2 tw-gap-10">
                      <TextField
                        group-id="input-group-2"
                        label-for="input-2"
                        :config-props="piecesBadProps"
                        v-model="piecesBad"
                        type="number"

                        label="Jml UOM 1 / Pieces (Bad)"
                        placeholder="Jumlah dalam Pieces" />
                      <TextField
                        group-id="input-group-2"
                        label-for="input-2"
                        :config-props="piecesGoodProps"
                        v-model="piecesGood"
                        type="number"

                        label="Jml UOM 1 / Pieces (Good)"
                        placeholder="Jumlah dalam Pieces" />
                      <TextField
                        group-id="input-group-3"
                        label-for="input-3"
                        :config-props="boxBadProps"
                        v-model="boxBad"
                        type="number"
                        label="Jml UOM 2 / Box (Bad)"
                        placeholder="Jumlah dalam box" />
                      <TextField
                        group-id="input-group-3"
                        label-for="input-3"
                        :config-props="boxGoodProps"
                        v-model="boxGood"
                        type="number"
                        label="Jml UOM 2 / Box (Good)"
                        placeholder="Jumlah dalam box" />
                      <TextField
                        group-id="input-group-4"
                        label-for="input-4"
                        :config-props="kartonBadProps"
                        v-model="kartonBad"
                        type="number"
                        label="Jml UOM 3 / Karton (Bad)"
                        placeholder="Jumlah dalam Karton" />
                      <TextField
                        group-id="input-group-4"
                        label-for="input-4"
                        :config-props="kartonGoodProps"
                        v-model="kartonGood"
                        type="number"
                        label="Jml UOM 3 / Karton (Good)"
                        placeholder="Jumlah dalam Karton" />
                    </div>
                    <div class="tw-flex tw-flex-col tw-gap-2">
                      <span class="tw-text-lg">Keterangan Retur</span>
                      <SelectInput
                        placeholder="Pilih Alasan"
                        size="md"
                        value-field="text"
                        :options="keteranganOption"
                        v-model="selectedKeterangan" />
                      <BFormTextarea
                        v-if="selectedKeterangan === 'Lainnya'"
                        id="textarea"
                        v-model="keteranganRetur"
                        :config-props="keteranganReturProps"
                        placeholder="Masukkan Alasan"
                        rows="8" />
                      <span
                        v-if="errorKeterangan"
                        class="tw-text-red-500 tw-text-sm">
                        {{ errorKeterangan }}
                      </span>
                    </div>
                    <FlexBox full jus-end>
                      <BButton
                        @click="updateProduk"
                        type="submit"
                        class="tw-bg-green-500 tw-border-none">
                        {{ isEdit ? "Update" : "Submit" }}
                      </BButton>
                    </FlexBox>
                  </BForm>
                </FlexBox>
              </template>
            </Card>
          </Modal>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
