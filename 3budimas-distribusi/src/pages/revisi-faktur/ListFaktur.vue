<script setup>
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import StatusBar from "@/src/components/ui/StatusBar.vue";
import {useShipping} from "@/src/store/shipping";
import {useRoute, useRouter} from "vue-router";
import {useKepalaCabang} from "@/src/store/kepalaCabang";
import {computed, inject, onMounted, ref} from "vue";
import {apiUrl, calculateProductDiscounts, calculateProductSubtotal, fetchWithAuth,} from "@/src/lib/utils";
import {useAlert} from "@/src/store/alert";
import {downloadPdf2} from "@/src/lib/faktur";
import jsPDF from "jspdf";
import {listFakturCol} from "@/src/model/tableColumns/revisi-faktur/listFakturCol";

const shipping = useShipping();
const kepalaCabang = useKepalaCabang();
const router = useRoute();
const route = useRouter();
const tableKey = ref(0);
const tableData = ref([]);
const fakturInfo = ref({});
const idRute = router.params.id_rute;
const idCabang = kepalaCabang?.kepalaCabangUser?.id_cabang;
const idArmada = router.query.id_armada;
const idDriver = router.query.id_driver;
const deliveringDate = router.query.delivering_date;
const isPrintingAllFaktur = ref(false);
const isDataLoaded = ref(false);
const alert = useAlert();
const $swal = inject("$swal");
const kodeRute = computed(() => fakturInfo.value?.kode || "");
const getAllFakturName = () => {
  return `Revisi-Faktur-${kodeRute.value || "unknown"}-${
    fakturInfo.value?.nama_armada || "unknown"
  }-${fakturInfo.value?.nama_driver || "unknown"}-${
    deliveringDate || "unknown"
  }`;
};
const tableRef = ref(null);

const forceLoading = ref(true);

const getResource = async () => {
  isDataLoaded.value = false;

  const resFakturInfo = await shipping.getListRuteRevisiFaktur(idCabang);
  const res = await shipping.getListFakturRevisiFaktur(
    idCabang,
    idRute,
    idArmada,
    idDriver,
    deliveringDate
  );

  tableData.value = res.list_faktur_shipping || [];

  const filteredFakturInfo = resFakturInfo.find(
    (item) =>
      item.delivering_date === deliveringDate &&
      item.id_armada == idArmada &&
      item.id_driver == idDriver &&
      item.id_rute == idRute
  );

  fakturInfo.value = filteredFakturInfo || {};

  tableKey.value++;

  isDataLoaded.value = true;
  forceLoading.value = false;
};

const printAllFaktur = async () => {
  try {
    isPrintingAllFaktur.value = true;

    // Dapatkan baris yang dipilih dari tabel
    const selectedRows = tableRef.value.getSelectedRow();

    // Jika tidak ada yang dipilih, tampilkan peringatan
    if (Object.keys(selectedRows).length === 0) {
      $swal.warning("Silakan pilih faktur yang ingin dicetak");
      isPrintingAllFaktur.value = false;
      return;
    }

    // Konfirmasi terlebih dahulu
    const isConfirm = await $swal.confirmSubmit();
    if (!isConfirm) {
      isPrintingAllFaktur.value = false;
      return;
    }

    // Ambil daftar ID faktur dari baris yang dipilih
    const selectedFaktur =
      tableData.value.filter((_, index) => selectedRows[index]) || [];

    const fakturIds = selectedFaktur.map((faktur) => faktur.id_sales_order);

    // Kumpulkan semua data faktur terlebih dahulu
    const allFakturData = [];

    for (let i = 0; i < fakturIds.length; i++) {
      const id_sales_order = fakturIds[i];

      const currentFaktur = selectedFaktur.find(
        (f) => f.id_sales_order === id_sales_order
      );

      await shipping.getListDetailFakturShipping(currentFaktur?.id_order_batch?currentFaktur?.id_order_batch: id_sales_order, currentFaktur?.id_order_batch, id_sales_order);

      if (
        shipping.listDetailFakturShipping.detailFakturInfo &&
        shipping.listDetailFakturShipping.detailFaktur
      ) {
        // Hitung rincian pembayaran untuk faktur ini
        const detailFaktur = shipping.listDetailFakturShipping.detailFaktur;
        const subtotal = calculateTotalSubtotal(detailFaktur);
        const totalOrderSubtotal = subtotal;
        const diskonNota = calculateTotalDiscount(
          detailFaktur,
          totalOrderSubtotal
        );
        const pajak = calculateTotalTax(detailFaktur, totalOrderSubtotal);
        const totalPenjualan = subtotal - diskonNota + pajak;

        // Persiapkan detail produk dengan rincian diskon untuk setiap produk
        const detailProduk = detailFaktur.map((product) => {
          // Dapatkan status voucher untuk produk ini
          const voucherStatus = shipping.getVoucherStatusForProduct(
            product.id_produk
          );

          // Hitung diskon dengan fungsi dari utils.js
          const discountResult = calculateProductDiscounts(
            product,
            voucherStatus,
            totalOrderSubtotal,
            "delivered"
          );

          // Kembalikan produk dengan detail diskon voucher
          return {
            id_produk: product.id_produk,
            nama_produk: product.nama_produk,
            kode_sku: product.kode_sku,
            harga_jual: product.harga_jual,
            karton_delivered: product.karton_delivered,
            box_delivered: product.box_delivered,
            pieces_delivered: product.pieces_delivered,
            puom1_nama: product.puom1_nama,
            puom2_nama: product.puom2_nama,
            puom3_nama: product.puom3_nama,
            subtotal: discountResult.subtotal,
            voucher_detail: {
              // Detail voucher reguler 1
              v1r_active: voucherStatus.v1r_active,
              v1r_nama: product.v1r_nama || null,
              v1r_persen: product.v1r_persen || 0,
              v1r_diskon: discountResult.diskon1r || 0,

              // Detail voucher reguler 2
              v2r_active: voucherStatus.v2r_active,
              v2r_nama: product.v2r_nama || null,
              v2r_persen: product.v2r_persen || 0,
              v2r_diskon: discountResult.diskon2r || 0,

              // Detail voucher reguler 3
              v3r_active: voucherStatus.v3r_active,
              v3r_nama: product.v3r_nama || null,
              v3r_persen: product.v3r_persen || 0,
              v3r_diskon: discountResult.diskon3r || 0,

              // Detail voucher produk 2
              v2p_active: voucherStatus.v2p_active,
              v2p_nama: product.v2p_nama || null,
              v2p_persen: product.v2p_persen || 0,
              v2p_nominal_diskon: product.v2p_nominal_diskon || 0,
              v2p_kategori_voucher: product.v2p_kategori_voucher || 0,
              v2p_diskon: discountResult.diskon2p || 0,

              // Detail voucher produk 3
              v3p_active: voucherStatus.v3p_active,
              v3p_nama: product.v3p_nama || null,
              v3p_persen: product.v3p_persen || 0,
              v3p_nominal_diskon: product.v3p_nominal_diskon || 0,
              v3p_kategori_voucher: product.v3p_kategori_voucher || 0,
              v3p_diskon: discountResult.diskon3p || 0,
            },
            total_diskon: discountResult.totalDiskon,
            ppn: discountResult.ppnValue,
            total_harga:
              discountResult.subtotal -
              discountResult.totalDiskon +
              discountResult.ppnValue,
          };
        });

        // Tambahkan data faktur dan pembayarannya
        allFakturData.push({
          id_sales_order,
          detail_faktur: shipping.listDetailFakturShipping.detailFaktur,
          faktur_info: shipping.listDetailFakturShipping.detailFakturInfo,
          rincian_pembayaran: {
            subtotal,
            diskon_nota: diskonNota,
            pajak,
            total_penjualan: totalPenjualan,
          },
          detail_produk: detailProduk,
          pembayaran_via_dropper:
            currentFaktur?.pembayaran_via_dropper || false,
        });
      }
    }

    // Kirim request ke API dengan data lengkap
    try {
      const response = await fetchWithAuth(
        "POST",
        `${apiUrl}/api/distribusi/submit-revisi-faktur`,
        {
          id_rute: idRute,
          id_cabang: idCabang,
          id_armada: idArmada,
          id_driver: idDriver,
          nama_fakturist: kepalaCabang?.kepalaCabangUser?.nama,
          delivering_date: deliveringDate,
          faktur_ids: [...new Set(fakturIds.map(ids=>typeof ids ==="string"? ids.split(','):ids).flat())], // Hapus duplikat ID faktur
          faktur_data: allFakturData,
        }
      );
      // const response = {
      //   status: "success",
      //   message: "Faktur berhasil diproses",
      // }; // Simulasi response sukses

      if (response.status === "success") {
        // Buat satu PDF dengan semua faktur
        if (allFakturData.length > 0) {
          const filename = getAllFakturName();
          await downloadAllFakturPdf(allFakturData, filename);
        }

        isPrintingAllFaktur.value = false;
        $swal.success(response.message || "Faktur berhasil diproses");
        route.back();
      } else {
        $swal.error(response.message || "Gagal memproses faktur");
        isPrintingAllFaktur.value = false;
      }
    } catch (error) {
      console.error("Error calling API:", error);
      $swal.error(error || "Terjadi kesalahan saat memproses faktur");
      isPrintingAllFaktur.value = false;
    }
  } catch (error) {
    console.error("Error printing all faktur:", error);
    isPrintingAllFaktur.value = false;
  }
};

const calculateTotalSubtotal = (detailFaktur) => {
  let total = 0;
  if (detailFaktur && detailFaktur.length > 0) {
    detailFaktur.forEach((product) => {
      // Gunakan mode "delivered" untuk revisi faktur
      total += calculateProductSubtotal(product, "delivered");
    });
  }
  return total;
};
// Fungsi untuk menghitung total diskon dari detail faktur
const calculateTotalDiscount = (detailFaktur, totalOrderSubtotal) => {
  let totalDiscount = 0;

  if (detailFaktur && detailFaktur.length > 0) {
    detailFaktur.forEach((product) => {
      // Dapatkan status voucher untuk produk ini
      const voucherStatus = shipping.getVoucherStatusForProduct(
        product.id_produk
      );

      // Hitung diskon dengan fungsi dari utils.js menggunakan mode "delivered"
      const discountResult = calculateProductDiscounts(
        product,
        voucherStatus,
        totalOrderSubtotal,
        "delivered"
      );
      totalDiscount += discountResult.totalDiskon;
    });
  }

  return totalDiscount;
};

// Fungsi untuk menghitung total pajak dari detail faktur
const calculateTotalTax = (detailFaktur, totalOrderSubtotal) => {
  let totalTax = 0;

  if (detailFaktur && detailFaktur.length > 0) {
    detailFaktur.forEach((product) => {
      const voucherStatus = shipping.getVoucherStatusForProduct(
        product.id_produk
      );

      // Gunakan mode "delivered" untuk revisi faktur
      const discountResult = calculateProductDiscounts(
        product,
        voucherStatus,
        totalOrderSubtotal,
        "delivered"
      );
      totalTax += discountResult.ppnValue;
    });
  }

  return totalTax;
};

const downloadAllFakturPdf = async (allFakturData, filename) => {
  try {
    const doc = new jsPDF({
      orientation: "portrait",
      unit: "mm",
      format: "letter",
    });

    let currentStartPage = 1;

    for (let i = 0; i < allFakturData.length; i++) {
      const fakturInfo = allFakturData[i].faktur_info;
      const detailFaktur = allFakturData[i].detail_faktur;

      const useExistingDoc = i === 0 ? doc : doc;
      if (i > 0) {
        doc.addPage();
      }

      const result = await downloadPdf2(
        fakturInfo,
        detailFaktur,
        filename,
        false,
        useExistingDoc,
        true,
        1,
        currentStartPage,
        "delivered"
      );

      currentStartPage += result.totalPages;
    }

    doc.save(`${filename}.pdf`);
  } catch (error) {
    console.error("Error generating all faktur PDF:", error);
    $swal.error("Terjadi kesalahan saat mencetak faktur");
  }
};

onMounted(() => getResource());
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px-0">
    <SlideRightX
      class=""
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card :no-subheader="true">
        <template #header>Faktur</template>
        <template #content>
          <div class="status-field-container-4-col tw-mb-5">
            <StatusBar
              :loading="shipping.listFakturShipping.loading"
              label="Cabang :"
              :value="
                kepalaCabang?.kepalaCabangUser?.kepalaCabang?.nama_cabang
              " />
            <StatusBar
              :loading="shipping.listFakturShipping.loading"
              label="Rute :"
              :value="kodeRute" />
            <StatusBar
              :loading="shipping.listFakturShipping.loading"
              label="Jumlah Toko :"
              :value="fakturInfo?.jumlah_toko || ''" />
            <StatusBar
              :loading="shipping.listFakturShipping.loading"
              label="Jumlah Nota :"
              :value="fakturInfo?.jumlah_nota || ''" />
          </div>
          <div class="status-field-container-4-col tw-mb-5">
            <StatusBar
              :loading="shipping.listFakturShipping.loading"
              label="Armada :"
              :value="fakturInfo?.nama_armada || ''" />
            <StatusBar
              :loading="shipping.listFakturShipping.loading"
              label="Driver :"
              :value="fakturInfo?.nama_driver || ''" />
          </div>
        </template>
      </Card>

      <Card :no-subheader="true" class="tw-mt-10">
        <template #header>List Faktur</template>
        <template #content>
          <div class="tw-w-full">
            <Table
              ref="tableRef"
              :key="tableKey"
              :loading="forceLoading"
              :table-data="tableData"
              :columns="listFakturCol" />
          </div>
          <div class="tw-flex tw-w-full tw-justify-end tw-mb-7 tw-gap-2">
            <BButton
              @click="printAllFaktur"
              :disabled="!isDataLoaded || isPrintingAllFaktur"
              class="tw-bg-fuchsia-500 tw-border-none">
              <i class="mdi mdi-printer"></i>
              &nbsp;
              <p>
                {{
                  isPrintingAllFaktur ? "Memproses..." : "Cetak Ulang Faktur"
                }}
              </p>
            </BButton>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </div>
</template>
