import { ref, watch, onMounted } from "vue";
import { fetchWithAuth } from "./utils";

export function useFetchPaginate(
  query = "",
  { pagination, sorting, globalFilters, initialSortColumn, filterColum } = {}
) {
  const data = ref([]);
  const count = ref(0);
  const loading = ref(false);
  const key = ref(0);
  const totalPage = ref(0);

  const getData = async () => {
    try {
      loading.value = true;

      const mainParams = new URLSearchParams();
      const filterParam = new URLSearchParams();

      // Determine sorting field and order
      const getField = sorting?.value?.[0]?.id || initialSortColumn || "id";
      const getOrder = sorting?.value?.[0]?.desc ? "desc" : "asc";

      // Append main query parameters
      mainParams.append("limit", pagination?.value?.pageSize);
      mainParams.append("page", pagination?.value?.pageIndex);
      mainParams.append("order", getOrder);
      mainParams.append("field", getField);
      const filterColum = []
      const regex = /\bnot\b/i
      globalFilters.value.value.columns.forEach(element => {
        if (!regex.test(element)) {
          filterColum.push(element)
        }
      });
      // Append filters if they exist
      if (
        globalFilters?.value?.value?.text &&
        globalFilters.value.value.columns
      ) {
        filterParam.append("filters", globalFilters.value.value.text);
        filterParam.append("columns", filterColum);
      }

      const url = `${query}${mainParams.toString()}&${filterParam.toString()}`;
      const response = await fetchWithAuth("GET", url);

      if (response) {
        data.value = response.pages || [];
        count.value = response.total_data || 0;
        totalPage.value = Math.max(
          1,
          Math.ceil(response.total_data / (pagination?.value?.pageSize || 10))
        );
      } else {
        console.warn("No response or invalid data structure received.");
      }
    } catch (error) {
      console.error("Error during data fetch:", error);
    } finally {
      loading.value = false;
      key.value++;
    }
  };

  // Watch for changes in reactive dependencies
  watch(
    [() => pagination?.value, () => sorting?.value, () => globalFilters?.value],
    getData,
    { deep: true }
  );

  onMounted(getData);

  // Return named properties for better usability
  return [data, count, loading, totalPage, key];
}
