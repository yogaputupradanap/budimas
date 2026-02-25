<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Table from "@/src/components/ui/table/Table.vue";
import { detailLaporanKasirColumn } from "@/src/model/tableColumns/laporan-kasir/detail/detailLaporanKasirColumn";
import { setoranService } from "@/src/services/setoran";
import { computed, onMounted, ref } from "vue";
import Label from "@/src/components/ui/Label.vue";
import { useUser } from "@/src/store/user";
import { useRoute } from "vue-router";
import { fetchWithAuth, formatCurrencyAuto } from "@/src/lib/utils";
import SelectInput from "@/src/components/ui/formInput/SelectInput.vue";
import Button from "@/src/components/ui/Button.vue";
import ExcelJS from "exceljs";

const user = useUser();
const route = useRoute();
const { endpoints } = setoranService;

const loading = ref(false);
const detailLaporan = ref([]);
const laporanInfo = ref({});
const jenisFilter = ref(null);

const jenisOptions = [
  { text: "Pemasukan", value: "pemasukan" },
  { text: "Pengeluaran", value: "pengeluaran" },
];

// Filter data berdasarkan jenis yang dipilih
const filteredData = computed(() => {
  if (!jenisFilter.value) {
    return detailLaporan.value;
  }
  return detailLaporan.value.filter((item) => item.jenis === jenisFilter.value);
});

const fetchDetailLaporan = async () => {
  try {
    loading.value = true;
    const tanggal = route.query.tanggal;
    const id_cabang = user?.user?.value?.id_cabang;

    const response = await fetchWithAuth(
      "GET",
      `${endpoints.getDetailLaporanKasir}?id_cabang=${id_cabang}&tanggal=${tanggal}`
    );

    detailLaporan.value = response.detailLaporan || [];
    laporanInfo.value = response.laporanInfo || {};
  } catch (error) {
    console.error("Error fetching detail laporan:", error);
  } finally {
    loading.value = false;
  }
};

const cetakLaporanExcelJS = async () => {
  const headers = ["Tanggal", "Jenis", "PIC", "Nominal"];
  const dataRows = filteredData.value.map((item) => [
    route.query.tanggal,
    item.jenis.charAt(0).toUpperCase() + item.jenis.slice(1),
    item.pic,
    parseFloat(item.nominal) || 0,
  ]);
  const summaryRows = [
    [
      "Total Pemasukan",
      "",
      "",
      parseFloat(laporanInfo.value.total_pemasukan) || 0,
    ],
    [
      "Total Pengeluaran",
      "",
      "",
      parseFloat(laporanInfo.value.total_pengeluaran) || 0,
    ],
    ["Sisa Saldo", "", "", parseFloat(laporanInfo.value.sisa_saldo) || 0],
  ];
  const wb = new ExcelJS.Workbook();
  const ws = wb.addWorksheet("Detail Laporan Kasir");

  // Add header
  const headerRow = ws.addRow(headers);
  // Bold header row
  headerRow.font = { bold: true };

  // Add data rows
  dataRows.forEach((row) => ws.addRow(row));

  // Add summary rows and make them bold
  summaryRows.forEach((row) => {
    const summaryRow = ws.addRow(row);
    summaryRow.font = { bold: true };
  });

  // Format number columns with Rupiah format and align right
  const nominalCol = 4; // Column D (Nominal)
  ws.getColumn(nominalCol).numFmt = '"Rp "#,##0';
  ws.getColumn(nominalCol).alignment = { horizontal: "right" };

  // Merge summary cells
  const startRow = dataRows.length + 2;
  for (let i = 0; i < 3; i++) {
    ws.mergeCells(`A${startRow + i}:C${startRow + i}`);
  }

  // Autofit columns
  ws.columns.forEach((col, i) => {
    let maxLength = headers[i].length;
    ws.eachRow((row) => {
      const val = row.getCell(i + 1).value;
      if (val !== null && val !== undefined) {
        // For nominal column, calculate length based on formatted value
        if (i === 3) {
          // Nominal column (now index 3)
          const formattedLength = `Rp ${val.toLocaleString()}`.length;
          maxLength = Math.max(maxLength, formattedLength);
        } else {
          maxLength = Math.max(maxLength, val.toString().length);
        }
      }
    });
    // Add extra width for nominal column to accommodate Rp format
    col.width = i === 3 ? maxLength + 5 : maxLength + 2;
  });

  // Add border to all cells with value
  ws.eachRow({ includeEmpty: true }, (row) => {
    row.eachCell({ includeEmpty: true }, (cell) => {
      cell.border = {
        top: { style: "thin" },
        left: { style: "thin" },
        bottom: { style: "thin" },
        right: { style: "thin" },
      };
    });
  });

  // Download file
  const buffer = await wb.xlsx.writeBuffer();
  const blob = new Blob([buffer], {
    type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  });
  const filename = `Detail_Laporan_Kasir_${route.query.tanggal?.replace(
    /\//g,
    "-"
  )}_${Date.now()}.xlsx`;
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
};

onMounted(() => {
  fetchDetailLaporan();
});
</script>

<template>
  <FlexBox full flex-col>
    <SlideRightX
      class="slide-container"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card no-subheader>
        <template #header>
          <div class="tw-flex tw-justify-between tw-items-center">
            <span>Detail Laporan Kasir</span>
          </div>
        </template>
        <template #content>
          <FlexBox full>
            <Label label="Jenis Laporan : ">
              <SelectInput
                v-model="jenisFilter"
                size="md"
                :search="true"
                :options="jenisOptions"
                text-field="text"
                value-field="value"
                placeholder="Semua Jenis" />
            </Label>
          </FlexBox>
          <Table
            :columns="detailLaporanKasirColumn"
            :table-data="filteredData"
            :loading="loading"
            reactive />
          <div
            class="tw-flex tw-flex-col md:tw-flex-row tw-w-full tw-gap-4 tw-px-4">
            <div
              class="tw-p-4 tw-bg-green-50 tw-rounded-lg tw-border tw-border-green-200">
              <div class="tw-text-sm tw-text-green-600 tw-font-medium">
                Total Pemasukan
              </div>
              <div class="tw-text-lg tw-font-bold tw-text-green-700">
                {{ formatCurrencyAuto(laporanInfo.total_pemasukan || 0) }}
              </div>
            </div>
            <div
              class="tw-p-4 tw-bg-red-50 tw-rounded-lg tw-border tw-border-red-200">
              <div class="tw-text-sm tw-text-red-600 tw-font-medium">
                Total Pengeluaran
              </div>
              <div class="tw-text-lg tw-font-bold tw-text-red-700">
                {{ formatCurrencyAuto(laporanInfo.total_pengeluaran || 0) }}
              </div>
            </div>
            <div
              class="tw-p-4 tw-bg-gray-50 tw-rounded-lg tw-border tw-border-gray-200">
              <div class="tw-text-sm tw-text-gray-600 tw-font-medium">
                Sisa Saldo
              </div>
              <div
                :class="[
                  'tw-text-lg tw-font-bold',
                  (laporanInfo.sisa_saldo || 0) < 0
                    ? 'tw-text-red-700'
                    : 'tw-text-green-700',
                ]">
                {{ formatCurrencyAuto(laporanInfo.sisa_saldo || 0) }}
              </div>
            </div>
          </div>
          <FlexBox full jusEnd class="tw-px-4">
            <Button
              class="tw-px-4 tw-py-2 tw-bg-green-500"
              :icon="'mdi mdi-printer'"
              :trigger="cetakLaporanExcelJS">
              Cetak Laporan
            </Button>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
