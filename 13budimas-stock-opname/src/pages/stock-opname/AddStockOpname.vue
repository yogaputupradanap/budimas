<script setup>
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Skeleton from "@/src/components/ui/Skeleton.vue";
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import { BFormInput } from "bootstrap-vue-next";
import Table from "@/src/components/ui/table/Table.vue";
import { listProdukColumns } from "@/src/model/tableColumns/stock-opname/listProduk";
import Button from "@/src/components/ui/Button.vue";
import { computed, onMounted, onUnmounted, reactive, ref, watch } from "vue";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";
import { useAlert } from "@/src/store/alert";
import { useUser } from "@/src/store/user";
import { useOthers } from "@/src/store/others";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";
import { stockOpnameService } from "@/src/services/stockOpname";
import Swal from "sweetalert2";

const others = useOthers();

const { brand, principal, stockOpname, stockCabang } = storeToRefs(others);

const alert = useAlert();
const principalSelected = ref(null);
const brandSelected = ref(null);
const userStore = useUser();
const router = useRouter();
const loadingSubmit = ref(false);
const isServerTable = ref(false);
const brandFiltered = ref([]);
const produks = ref([]);

const id_opname = ref("");
const tanggal = ref(new Date().toISOString().split("T")[0]);
const id_cabang = userStore.user.value?.id_cabang;
const Keterangan = ref("");
const id_perusahaan = userStore?.user.value?.id_perusahaan;
const id_user = userStore?.user.value.id;

onMounted(() => {
  others.getKodeStockOpname();
});

onUnmounted(() => {
  stockOpname.value.produks = [];
});

const localStore = ref(null);
const submitStockOpname = async () => {
  if (!principalSelected.value) {
    alert.setMessage("Principal harus diisi", "danger");
    return;
  }
  if (stockOpname.value.produks.length === 0) {
    alert.setMessage("Produk tidak boleh kosong", "danger");
    return;
  }

  const result = await Swal.fire({
    title: "Apakah Anda yakin?",
    text: "Data stock opname akan disimpan.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Ya, simpan!",
    cancelButtonText: "Batal",
  })

  if (!result.isConfirmed) {
    return;
  }

  loadingSubmit.value = true;
  const data = {
    id_perusahaan: id_perusahaan,
    id_cabang: id_cabang,
    id_principal: principalSelected.value,
    id_user_input: id_user,
    kode_so: stockOpname.value.id_stock_opname,
    keterangan: Keterangan.value,
    data_produks: produks.value,
    total: produks.value.reduce((acc, val) => acc + val.total, 0),
    total_selisih: produks.value.reduce(
      (acc, val) => acc + val.selisih * val.harga_produk,
      0
    ),
  };

  try {
    await stockOpnameService.postStockOpname("add", data);
    await others.getAllStockOpname();
    alert.setMessage("Stock Opname berhasil ditambahkan", "success");
    router.replace("/stock-opname");
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loadingSubmit.value = false;
  }
};

const cancelStockOpname = () => {
  router.replace("/stock-opname");
};

const mergeData = () => {
  produks.value = stockOpname.value.produks.map((item) => {
    const found = stockCabang.value.list.find(
      (el) => el.produk_id === item.id_produk
    );
    if (found) {
      return {
        ...item,
        stock_system: found.jumlah_good,
        selisih: item.stock - found.jumlah_good,
      };
    }
    return {
      ...item,
      stock_system: 0,
      selisih: item.jumlah,
    };
  });
};

const mergeDataWithBrand = () => {
  produks.value = produks.value.map((item) => {
    const found = stockCabang.value.list.find(
      (el) => el.produk_id === item.id_produk
    );
    if (found) {
      return {
        ...item,
        stock_system: found.jumlah_good,
        selisih: item.stock - found.jumlah_good,
      };
    }
    return {
      ...item,
      stock_system: 0,
      selisih: item.jumlah,
    };
  });
};

const filterBrand = () => {
  if (!principalSelected.value) return [];
  const id_brand = stockOpname.value.produks.map((item) => item.id_brand);
  brandFiltered.value = brand.value.list.filter((item) => {
    return id_brand.includes(item.id);
  });
};

watch(principalSelected, async (val) => {
  if (val) {
    brandSelected.value = null;
    await Promise.all([
      others.getProdukByPrincipal(val),
      others.getStockCabangByPrincipal(val, id_cabang),
    ]);
    mergeData();
    filterBrand();
  }
});

watch(brandSelected, async (val) => {
  if (val) {
    produks.value = stockOpname.value.produks.filter(
      (item) => item.id_brand === val
    );
    mergeDataWithBrand();
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
      :x="40"
    >
      <Card no-subheader>
        <template #header>Form Cari Stock Opname</template>
        <template #content>
          <div class="form-grid-card-4-menu tw-items-end">
            <Label label="Kode Stock Opname">
              <BFormInput
                v-model="stockOpname.id_stock_opname"
                disabled
                placeholder="Cari ID Opname"
              />
            </Label>
            <Label label="Tanggal Stock Opname">
              <BFormInput
                disabled
                v-model="tanggal"
                placeholder="Cari Customer"
              />
            </Label>
            <Label label="Principal" class="z-50">
              <Skeleton class="skeleton" v-if="principal.loading" />
              <SelectInput
                v-else
                v-model="principalSelected"
                placeholder="Pilih Principal"
                size="md"
                :search="true"
                class="tw-z-[9950]"
                :options="principal.list"
                text-field="nama"
                value-field="id"
              />
            </Label>
            <Label label="Brand" class="z-50">
              <Skeleton class="skeleton" v-if="brand.loading" />
              <SelectInput
                v-else
                v-model="brandSelected"
                placeholder="Pilih Brand"
                size="md"
                :search="true"
                :disabled="!principalSelected"
                class="tw-z-[9950]"
                :options="brandFiltered"
                text-field="nama"
                value-field="id"
              />
            </Label>
          </div>
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
      :x="40"
    >
      <Card no-subheader>
        <template #header>List Produk</template>
        <template #content>
          <ServerTable
            v-if="isServerTable"
            :columns="listProdukColumns(data)"
            :key="key"
            :table-data="stockOpname.produks"
            :loading="stockOpname.loading"
            :on-pagination-change="onPaginationChange"
            :on-global-filters-change="onColumnFilterChange"
            :on-sorting-change="onSortingChange"
            :pagination="pagination"
            :sorting="sorting"
            :filter="globalFilters"
            :page-count="totalPage"
            :total-data="count"
            classic="true"
          />
          <Table
            v-else
            :key="localStore || []"
            :columns="listProdukColumns(produks)"
            :table-data="produks"
            classic="true"
          />
          <div class="tw-flex tw-w-full tw-items-start tw-mt-4">
            <Label label="Keterangan">
              <textarea
                class="tw-border tw-resize-none tw-border-gray-300 tw-p-2 tw-rounded-lg"
                v-model="Keterangan"
                placeholder="Masukkan Keterangan SO"
                cols="50"
                rows="5"
              />
            </Label>
          </div>
          <div class="tw-flex tw-justify-end tw-w-full tw-mt-4 tw-space-x-3">
            <Button
              class="btn-c-danger tw-text-base tw-py-2 tw-px-5"
              icon="mdi mdi-close"
              :trigger="cancelStockOpname"
              >Cancel</Button
            >
            <Button
              class="btn-c-success tw-text-base tw-py-2 tw-px-5"
              icon="mdi mdi-check"
              :loading="loadingSubmit"
              :trigger="submitStockOpname"
              >Submit</Button
            >
          </div>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
