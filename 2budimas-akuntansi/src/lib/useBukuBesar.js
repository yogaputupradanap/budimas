import { onMounted, ref, watch } from "vue";
import { fetchWithAuth } from "./utils";

export function useBukuBesar(
  query = "",
  {
    pagination,
    sorting,
    globalFilters,
    initialSortColumn,
    initialSortDirection = "asc",
    columNotUsed = [],
    advancedFilters = [],
    isRunOnMounted = true,
    triggerFetch = null,
  } = {}
) {
  const data = ref([]);
  const count = ref(0);
  const loading = ref(false);
  const key = ref(0);
  const totalPage = ref(0);
  const summary = ref({});

  const getData = async () => {
    try {
      loading.value = true;

      const mainParams = new URLSearchParams();
      const filterParams = new URLSearchParams();
      const advancedParams = new URLSearchParams();

      // ===== SORTING =====
      const getField =
        sorting?.value?.[0]?.id || initialSortColumn || "id";

      const getOrder = sorting?.value?.[0]
        ? sorting.value[0].desc
          ? "desc"
          : "asc"
        : initialSortDirection;

      // ===== PAGINATION =====
      const pageSize = pagination?.value?.pageSize || 10;
      const pageIndex = (pagination?.value?.pageIndex || 0) + 1; // backend biasanya mulai dari 1

      mainParams.append("limit", pageSize);
      mainParams.append("page", pageIndex);
      mainParams.append("order", getOrder);
      mainParams.append("field", getField);

      // ===== GLOBAL FILTER =====
      if (
        globalFilters?.value?.value?.text &&
        globalFilters?.value?.value?.columns?.length
      ) {
        const columnsFiltered = globalFilters.value.value.columns.filter(
          (col) =>
            !/\bnot\b/i.test(col) &&
            !columNotUsed.includes(col)
        );

        filterParams.append("filters", globalFilters.value.value.text);
        filterParams.append("columns", columnsFiltered.join(","));
      }

      // ===== ADVANCED FILTER =====
      if (advancedFilters?.value?.length > 0) {
        advancedFilters.value.forEach((filter) => {
          if (filter.value) {
            advancedParams.append(filter.id, filter.value);
          }
        });
      }

      // ===== FINAL URL =====
      const separator = query.includes("?") ? "&" : "?";

const finalUrl =
  `${query}${separator}${mainParams.toString()}` +
  `&${filterParams.toString()}` +
  `&${advancedParams.toString()}`;

      console.log("=== FINAL URL ===", finalUrl);

      const response = await fetchWithAuth("GET", finalUrl);

      console.log("=== RESPONSE DARI BACKEND ===", response);

      if (response) {
        data.value = response.result || [];
        count.value = response.count || 0;
        summary.value = response.summary || {};

        totalPage.value = Math.max(
          1,
          Math.ceil(count.value / pageSize)
        );
      } else {
        console.warn("Response kosong.");
      }
    } catch (error) {
      console.error("Error during fetch buku besar:", error);
    } finally {
      loading.value = false;
      key.value++;
    }
  };

  // ===== WATCH =====
  watch(
    [
      () => pagination?.value,
      () => sorting?.value,
      () => globalFilters?.value,
      () => advancedFilters?.value,
      () => triggerFetch?.value,
    ],
    getData,
    { deep: true }
  );

  // ===== MOUNT =====
  onMounted(() => {
    if (isRunOnMounted) {
      getData();
    }
  });

  return [data, count, loading, totalPage, key, summary];
}