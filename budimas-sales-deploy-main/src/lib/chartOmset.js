import { ref } from "vue";
import { formatLongNumberToString, parseCurrency } from "./utils";

/**
 * Generates an array of month options with text and value properties.
 * @returns An array of month options with text and value properties.
 */
export const getMonthOptions = () => {
  const months = [
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember",
  ];
  const bulan = months.map((month, index) => ({
    text: month,
    value: (index + 1).toString(),
  }));
  return bulan;
};

/**
 * Generates an array of year options for a dropdown menu.
 * The array includes the current year and the four previous years.
 * @returns {Array} An array of year options in the format { text: string, value: string }.
 */
export const getYearOptions = () => {
  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: 5 }, (_, i) => currentYear - i);
  const tahun = years.map((year) => ({
    text: year.toString(),
    value: year.toString(),
  }));
  return tahun;
};

export function useChart() {

  const chartOptions = {
    chart: {
      height: 350,
      type: "area",
      stacked: false,
    },
    dataLabels: {
      enabled: true,
      formatter: function (val) {
        return formatLongNumberToString(val, 0);
      },
    },
    stroke: {
      curve: "smooth",
    },
    title: {
      text: "Omset",
      align: "middle",
    },
    markers: {
      size: 0,
      hover: {
        sizeOffset: 6,
      },
    },
    yaxis: {
      labels: {
        formatter: function (val) {
          return formatLongNumberToString(val, 0);
        },
        axisBorder: {
          show: false
        },
        axisTicks: {
          show: false
        }
      },
    },
    xaxis: {
      type: "datetime",
    },
    tooltip: {
      y: {
        formatter: function(value, { series, seriesIndex, dataPointIndex, w }) {
          return `Rp. ${parseCurrency(value || 0)}`
        }
      }
    }
  };

  const options = ref(chartOptions);
  const series = ref([
    {
      name: "Order",
      data: [],
    },
    {
      name: "Realisasi",
      data: [],
    },
    {
      name: "Retur",
      data: [],
    },
  ]);

  const setOptions = (values) => (options.value = values);
  const setSeries = (values) => (series.value = values);

  /**
   * Transforms the given orders, realitations, and returns data into a format suitable for a series.
   * @param {Array} orders - The array of orders data.
   * @param {Array} realitations - The array of realitations data.
   * @param {Array} returns - The array of returns data.
   * @returns None
   */
  const transformSeries = (orders, realitations, returns) => {
    const orderData = orders?.map((order) => {
      return {
        x: order?.tanggal,
        y: order?.omset,
      };
    });
    const realisasiData = realitations?.map((realitation) => {
      return {
        x: realitation?.tanggal,
        y: realitation?.omset,
      };
    });
    const returnData = returns?.map((retur) => {
      return {
        x: retur?.tanggal,
        y: retur?.omset,
      };
    });

    series.value[0].data = orderData;
    series.value[1].data = realisasiData;
    series.value[2].data = returnData;
  };

  return {
    options,
    series,
    setOptions,
    setSeries,
    transformSeries,
  };
}
