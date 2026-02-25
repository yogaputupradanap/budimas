<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Table from "@/src/components/ui/table/Table.vue";
import {listProdukColumns} from "@/src/model/tableColumns/stock-transfer/listProduk";
import Button from "@/src/components/ui/Button.vue";
import {BFormInput} from "bootstrap-vue-next";
import {computed, ref, watch} from "vue";
import {encode, fetchWithAuth} from "@/src/lib/utils";
import {useAlert} from "@/src/store/alert";
import {transferService} from "@/src/services/stockTransfer";
import {useOthers} from "@/src/store/others";
import {useUser} from "@/src/store/user";

const alert = useAlert();
const user = useUser();

const nota = ref();
const cabangFrom = ref();
const cabangTo = ref();
const selectedPerusahaan = ref(null);

const filteredBranches = computed(() => {
  if (!others.cabang.list || !user.user.value) return [];
  return others.cabang.list
});

const filteredPrincipals = computed(() => {
  if (!others.principal.list || !user.user.value) return [];
  return others.principal.list.filter(
      (principal) =>
          principal.id_perusahaan === selectedPerusahaan.value
  );
});

const selPrincipal = ref();
const selProduk = ref(null);
const uom1 = ref();
const uom2 = ref();
const uom3 = ref();
const listAddStock = ref([]);

const others = useOthers();
const produk = ref([]);
const loadingAdd = ref(false);
const loadingSend = ref(false);
const keyAdd = ref(0);

const fields = computed(() => [
  nota,
  cabangFrom,
  cabangTo,
  selPrincipal,
  selProduk,
]);

const uomFIelds = computed(() => [uom1, uom2, uom3]);

const removeRow = (val) => {
  const {rowIndex} = val;
  listAddStock.value.splice(rowIndex, 1);
  keyAdd.value++;
};

const reset = () => {
  fields.value.forEach((val) => {
    val.value = null;
  });

  uomFIelds.value.forEach((val) => {
    val.value = null;
  });

  listAddStock.value = [];
  keyAdd.value++;
};

const checkMainFields = () => {
  const mainFields = [nota, cabangFrom, cabangTo];
  return mainFields.some(
      (val) => val.value === null || val.value === undefined || val.value === ""
  );
};

watch(
    () => others.cabang.list,
    (newList) => {
      if (newList.length > 0 && user.user.value?.id_cabang) {
        const userBranch = newList.find(
            (branch) =>
                branch.id === user.user.value.id_cabang &&
                branch.id_perusahaan === user.user.value.id_perusahaan
        );
        if (userBranch) {
          cabangFrom.value = userBranch.id;
        }
      }
    },
    {immediate: true}
);

const checkProductFields = () => {
  const productFields = [selPrincipal, selProduk];
  return productFields.some(
      (val) => val.value === null || val.value === undefined || val.value === ""
  );
};
const checkUomFields = () => {
  const uomValues = [
    uom1.value ? parseInt(uom1.value) : 0,
    uom2.value ? parseInt(uom2.value) : 0,
    uom3.value ? parseInt(uom3.value) : 0,
  ];

  return uomValues.every((val) => val === 0);
};

const getProduk = async () => {
  selProduk.value = null;

  try {
    const encodeWhere = encode({
      "id_principal = ": `'${selPrincipal.value}'`,
    });
    const productOptions = await fetchWithAuth(
        "GET",
        `/api/base/produk?where=${encodeWhere}`
    );

    produk.value = productOptions;
  } catch (error) {
    alert.setMessage(error, "danger");
  }
};

const addProduk = async () => {
  try {
    if (checkProductFields()) throw "Principal dan Produk harus diisi";
    if (checkUomFields()) throw "Minimal salah satu UOM harus lebih dari 0";

    loadingAdd.value = true;
    const body = {
      products: [
        {
          id_principal: selPrincipal.value,
          id_produk: selProduk.value,
          uom_1: uom1.value ? parseInt(uom1.value) : 0,
          uom_2: uom2.value ? parseInt(uom2.value) : 0,
          uom_3: uom3.value ? parseInt(uom3.value) : 0,
        },
      ],
    };

    const [uoms] = await fetchWithAuth(
        "POST",
        `/api/produk-uom/get-uoms`,
        body
    );
    const namaProduk = produk.value.find((val) => val.id == selProduk.value);

    const produkWithUoms = {
      nama_produk: namaProduk.nama,
      id_produk: selProduk.value,
      id_principal: selPrincipal.value,
      uom_1: uoms["carton"],
      uom_2: uoms["box"],
      uom_3: uoms["pieces"],
    };

    listAddStock.value.push(produkWithUoms);
    keyAdd.value++;
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loadingAdd.value = false;
  }
};

const sendTransfer = async () => {
  try {
    if (checkMainFields()) throw "Nota dan Cabang harus diisi";
    if (listAddStock.value.length === 0) throw "minimal harus ada 1 produk";
    if (cabangFrom.value === cabangTo.value)
      throw "Cabang tujuan tidak boleh sama dengan cabang awal";

    loadingSend.value = true;
    const body = {
      nota_stock_transfer: nota.value,
      id_cabang_awal: cabangFrom.value,
      id_cabang_tujuan: cabangTo.value,
      products: [...listAddStock.value],
    };

    await transferService.postStockTransfer("add", body);
    alert.setMessage("success adding stock tranfer request", "success");
    reset();
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loadingSend.value = false;
  }
};

watch(selPrincipal, (newValue) => newValue && getProduk());
watch(selectedPerusahaan, (newValue) => {
  selPrincipal.value = null;
  selProduk.value = null;
  produk.value = [];
  listAddStock.value = [];
  keyAdd.value++;
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
        :x="40">
      <Card no-subheader>
        <template #header>Pilih Cabang</template>
        <template #content>
          <FlexBox
              full
              gap="small"
              it-end
              class="tw-flex-wrap md:tw-flex-nowrap">
            <Label full label="Nota Stock Transfer">
              <BFormInput v-model="nota" placeholder="Nota Stock Transfer"/>
            </Label>
            <Label full label="Dari">
              <SelectInput
                  placeholder="Pilih Cabang Awal"
                  size="md"
                  v-model="cabangFrom"
                  :search="true"
                  :options="filteredBranches"
                  text-field="nama"
                  value-field="id"/>
            </Label>
            <Label full label="Ke">
              <SelectInput
                  placeholder="Pilih Cabang Tujuan"
                  size="md"
                  v-model="cabangTo"
                  :search="true"
                  :options="filteredBranches"
                  text-field="nama"
                  value-field="id"/>
            </Label>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
        class="slide-container tw-z-10"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.2"
        :delay-out="0.1"
        :initial-x="-40"
        :x="40">
      <Card no-subheader>
        <template #header>Form Add Stock Transfer</template>
        <template #content>
          <FlexBox flex-col full>
            <FlexBox
                full
                gap="small"
                it-end
                class="tw-flex-wrap md:tw-flex-nowrap">
              <Label full label="Perusahaan">
                <SelectInput
                    :no-dynamic-placing="true"
                    placeholder="Pilih Perusahaan"
                    v-model="selectedPerusahaan"
                    size="md"
                    :search="true"
                    :options="others.perusahaan.list"
                    text-field="nama"
                    value-field="id"/>
              </Label>
              <Label full label="Principal">
                <SelectInput
                    :no-dynamic-placing="true"
                    placeholder="Pilih Principal"
                    v-model="selPrincipal"
                    size="md"
                    :disabled="!selectedPerusahaan"
                    :search="true"
                    :options="filteredPrincipals"
                    text-field="nama"
                    value-field="id"/>
              </Label>
              <Label full label="Produk">
                <SelectInput
                    :no-dynamic-placing="true"
                    placeholder="Pilih Produk"
                    v-model="selProduk"
                    size="md"
                    :search="true"
                    :options="produk"
                    text-field="nama"
                    value-field="id"/>
              </Label>
            </FlexBox>
            <FlexBox full it-end class="tw-flex-wrap md:tw-flex-nowrap">
              <Label full label="UOM 3 (karton)">
                <BFormInput type="number" placeholder="Jumlah" v-model="uom1"/>
              </Label>
              <Label full label="UOM 2 (box)">
                <BFormInput type="number" placeholder="Jumlah" v-model="uom2"/>
              </Label>
              <Label full label="UOM 1 (pieces)">
                <BFormInput type="number" placeholder="Jumlah" v-model="uom3"/>
              </Label>
              <Button
                  :loading="loadingAdd"
                  :trigger="addProduk"
                  class="tw-h-[37px] tw-w-full"
                  icon="mdi mdi-plus">
                Tambah Produk
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
        :delay-in="0.3"
        :delay-out="0.1"
        :initial-x="-40"
        :x="40">
      <Card no-subheader>
        <template #header>List Stock</template>
        <template #content>
          <Table
              :key="keyAdd"
              @remove-row="removeRow"
              class="tw-mt-10"
              :columns="listProdukColumns"
              :table-data="listAddStock"/>
          <FlexBox class="tw-mt-10" full jus-end gap="medium">
            <Button
                :loading="loadingSend"
                :trigger="sendTransfer"
                icon="mdi mdi-check"
                class="tw-bg-green-600 tw-text-white tw-px-6 tw-py-2">
              Tambah Stock Transfer
            </Button>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
