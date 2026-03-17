<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Label from "@/src/components/ui/Label.vue";
import { BFormInput } from "bootstrap-vue-next";
import Table from "@/src/components/ui/table/Table.vue";
import Button from "@/src/components/ui/Button.vue";
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { useUser } from "@/src/store/user";
import { useOthers } from "@/src/store/others";
import { storeToRefs } from "pinia";
import { useRoute, useRouter } from "vue-router";
import { listDetailEskalasiColumns } from "@/src/model/tableColumns/list-eskalasi/listDetailEskalasi";
import { stockOpnameService } from "@/src/services/stockOpname";
import { useAlert } from "@/src/store/alert";
import { formatRupiah } from "@/src/lib/utils";
import Swal from "sweetalert2";
import ServerTable from "@/src/components/ui/table/ServerTable.vue";

const others = useOthers();
const route = useRoute();
const router = useRouter();
const { stockOpname } = storeToRefs(others);

onUnmounted(() => {
  stockOpname.value.produks = [];
});

onMounted(async () => {
  try {
    await others.getOneStockOpnameDetail(route.params.id);

    if (stockOpname.value && stockOpname.value.produks?.length > 0) {
      kode_so.value = stockOpname.value.produks[0]?.kode_so || '';
      tanggal.value = stockOpname.value.produks[0]?.tanggal_so || '';
      principal.value = stockOpname.value.produks[0]?.nama_principal || '';
      jumlah_produk.value = stockOpname.value.produks?.length || 0;
      keterangan.value = stockOpname.value.produks[0]?.ket_so || '';
      status.value = stockOpname.value.produks[0]?.status_so || '';

      const principalId = stockOpname.value.produks[0]?.id_principal;

      if (principalId) {
        const conversionFactors = await stockOpnameService.getProdukByPrincipal(principalId);

        if (Array.isArray(conversionFactors)) {
          const conversionMap = {}
          conversionFactors.forEach(product => {
            conversionMap[product.id_produk] = {
              konversi_uom_1: product.konversi_uom_1,
              konversi_uom_2: product.konversi_uom_2,
              konversi_uom_3: product.konversi_uom_3,
              label_uom_1: product.label_uom_1,
              label_uom_2: product.label_uom_2,
              label_uom_3: product.label_uom_3
            };
          });

          stockOpname.value.produks = stockOpname.value.produks.map(product => {
            const uomData = conversionMap[product.id_produk];
            if (uomData) {
              return {
                ...product,
                konversi_uom_1: Number(uomData.konversi_uom_1) || 1,
                konversi_uom_2: Number(uomData.konversi_uom_2) || 0,
                konversi_uom_3: Number(uomData.konversi_uom_3) || 0,
                label_uom_1: uomData.label_uom_1 || 'Pcs',
                label_uom_2: uomData.label_uom_2 || '',
                label_uom_3: uomData.label_uom_3 || ''
              };
            }

            console.log(`No UOM Found for product ID ${product.id_produk}, using defaults`);
            return {
              ...product,
            }
          })

          localStore.value = Date.now();
          stockOpname.value.produks.forEach(product => {
            updateUomValues(product);
          })
        }
      }
    }
  } catch (error) {
    console.error("Error loading data:", error);
    alert.setMessage(error, "danger");
  }
});

const alert = useAlert();
const userStore = useUser();
const isServerTable = ref(false);
const loadingSubmit = ref(false);
const kode_so = ref("");
const total = computed(() => {
  return stockOpname.value.produks.reduce((acc, val) => {
    return acc + val.subtotal;
  }, 0);
});
const totalSelisih = computed(() => {
  return stockOpname.value.produks.reduce((acc, val) => {
    return acc + val.subtotal_selisih;
  }, 0);
});
const tanggal = ref("");
const principal = ref("");
const jumlah_produk = ref("");
const keterangan = ref("");
const status = ref("");
const localStore = ref(null);

const updateUomValues = (product, uomType) => {
  const conv1 = Number(product.konversi_uom_1 || product.faktor_konversi || 1);
  const conv2 = Number(product.konversi_uom_2 || 0);
  const conv3 = Number(product.konversi_uom_3 || 0);

  // Get UOM values as numbers
  const uom1 = Number(product.uom_1) || 0;
  const uom2 = Number(product.uom_2) || 0;
  const uom3 = Number(product.uom_3) || 0;

  // Calculate total stock using conversion factors
  let totalStock = 0;
  totalStock += uom1 * conv1;

  if (conv2 > 0) totalStock += uom2 * conv2;
  if (conv3 > 0) totalStock += uom3 * conv3;

  // Update product values
  const harga = Number(product.harga) || 0;
  const stokSistem = Number(product.stok_sistem) || 0;

  product.stok = totalStock;
  product.subtotal = totalStock * harga;
  product.subtotal_selisih = (totalStock - stokSistem) * harga;
  localStore.value = Date.now();
};

const tableColumns = computed(() => {
  return listDetailEskalasiColumns(updateUomValues);
});

const closeEskalasi = async () => {
  try {
    const result = await Swal.fire({
      title: "Konfirmasi Close Eskalasi",
      text: `Anda akan menutup eskalasi Stock Opname dengan kode ${kode_so.value}. Perubahan akan disimpan ke database. Lanjutkan?`,
      icon: "question",
      showCancelButton: true,
      confirmButtonText: "Ya, Close Eskalasi",
      cancelButtonText: "Batal",
      confirmButtonColor: "#28a745",
      focusConfirm: false
    });

    if (!result.isConfirmed) {
      return;
    }

    loadingSubmit.value = true;

    // Ensure all numeric values are properly converted to numbers
    const formattedProduks = stockOpname.value.produks.map(product => ({
      id_produk: Number(product.id_produk),
      uom_1: Number(product.uom_1) || 0,
      uom_2: Number(product.uom_2) || 0,
      uom_3: Number(product.uom_3) || 0,
      stok: Number(product.stok) || 0,
      harga: Number(product.harga) || 0,
      bad_stock: Number(product.bad_stock) || 0,
      stok_sistem: Number(product.stok_sistem) || 0,
      subtotal: Number(product.subtotal) || 0,
      subtotal_selisih: Number(product.subtotal_selisih) || 0,
      keterangan: product.ket_produk || ""
    }));

    const data = {
      id_stock_opname: parseInt(route.params.id),
      id_user: parseInt(userStore.user.value.id),
      id_cabang: parseInt(userStore.user.value?.id_cabang),
      id_perusahaan: parseInt(userStore.user.value?.id_perusahaan),
      data_produks: formattedProduks,
      total: Number(total.value) || 0,
      total_selisih: Number(totalSelisih.value) || 0
    };

    await stockOpnameService.putStockOpname("eskalasi closed", data);
    alert.setMessage("Eskalasi berhasil ditutup", "success");
    await router.replace("/list-eskalasi");
  } catch (error) {
    alert.setMessage(error, "danger");
  } finally {
    loadingSubmit.value = false;
  }
};

watch(stockOpname.value, () => {
  kode_so.value = stockOpname.value.produks[0]?.kode_so;
  tanggal.value = stockOpname.value.produks[0]?.tanggal_so;
  principal.value = stockOpname.value.produks[0]?.nama_principal;
  jumlah_produk.value = stockOpname.value.produks?.length;
  keterangan.value = stockOpname.value.produks[0]?.ket_so;
  status.value = stockOpname.value.produks[0]?.status_so;
});
</script>

<template>
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
        <template #header>Detail Eskalasi Stock Opname</template>
        <template #content>
          <div class="form-grid-card-3-menu tw-items-end">
            <Label label="Kode Stock Opname">
              <BFormInput disabled v-model="kode_so" placeholder="Cari Nama" />
            </Label>
            <Label label="Tanggal">
              <BFormInput disabled v-model="tanggal" placeholder="Cari SKU" />
            </Label>
            <Label label="Principal">
              <BFormInput
                  disabled
                  v-model="principal"
                  placeholder="Cari Cabang"
              />
            </Label>
            <Label label="Jumlah Produk">
              <BFormInput
                  disabled
                  v-model="jumlah_produk"
                  placeholder="Cari Cabang"
              />
            </Label>
            <Label label="Keterangan">
              <BFormInput
                  disabled
                  v-model="keterangan"
                  placeholder="Cari Cabang"
              />
            </Label>
            <Label label="Status">
              <BFormInput disabled v-model="status" placeholder="Cari Cabang" />
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
              :columns="listStockColumns"
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
              :key="localStore || []"
              :columns="tableColumns"
              :loading="stockOpname.loading"
              :table-data="stockOpname.produks"
              :classic="true"
          />
          <div class="tw-flex tw-justify-end tw-w-full tw-mt-4 tw-space-x-5">
            <h3 class="tw-text-black tw-font-bold tw-text-end">
              Total Selisih {{ formatRupiah(totalSelisih) }}
            </h3>
          </div>
          <div class="tw-flex tw-justify-end tw-w-full tw-mt-4 tw-space-x-5">
            <h3 class="tw-text-black tw-font-bold tw-text-end">
              Total {{ formatRupiah(total) }}
            </h3>
          </div>
          {{ userStore.user?.id_jabatan }}
          <div
              v-if="
              status === 'eskalasi' && userStore.user.value.id_jabatan !== 9
            "
              class="tw-flex tw-justify-end tw-w-full tw-mt-4 tw-space-x-3"
          >
            <Button
                class="btn-c-danger tw-text-base tw-py-2 tw-px-5"
                icon="mdi mdi-close"
                :loading="loadingSubmit"
                :trigger="closeEskalasi"
            >
              Close Eskalasi
            </Button>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
