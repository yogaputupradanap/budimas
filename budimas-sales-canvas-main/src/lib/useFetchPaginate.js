import { ref, watch, onMounted } from "vue";
import { fetchWithAuth } from "./utils";

export function useFetchPaginate(
  query = "",
  { pagination, sorting, globalFilters, initialSortColumn } = {}
) {
  const data = ref([]);
  const count = ref(0);
  const loading = ref(false);
  const key = ref(0);
  const totalPage = ref(0);

  const getData = async () => {
    try {
      if (!query.value) return;
      loading.value = true;

      const mainParams = new URLSearchParams();
      const filterParam = new URLSearchParams();

      // Determine sorting field and order
      const getField = sorting?.value?.[0]?.id || initialSortColumn || "id";
      const getOrder = sorting?.value?.[0]?.desc ? "desc" : "asc";

      mainParams.append("limit", pagination?.value?.pageSize || 10);
      mainParams.append("page", (pagination?.value?.pageIndex || 0) + 1);
      mainParams.append("order", getOrder);
      mainParams.append("field", getField);

      // Append filters if they exist
      if (
        globalFilters?.value?.value?.text &&
        globalFilters.value.value.columns
      ) {
        filterParam.append("filters", globalFilters.value.value.text);
        filterParam.append("columns", globalFilters.value.value.columns);
      }

      let url;
      if (query.value.includes('?')) {
        url = `${query.value}&${mainParams.toString()}&${filterParam.toString()}`;
      } else {
        url = `${query.value}?${mainParams.toString()}&${filterParam.toString()}`;
      }

      const response = await fetchWithAuth("GET", url);
      if (response) {
        if (Array.isArray(response)) {
          data.value = response;
          count.value = response.length;
          totalPage.value = Math.max(1, Math.ceil(response.length / (pagination?.value?.pageSize || 10)));
        } else if (response.pages) {
          data.value = response.pages || [];
          count.value = response.total_data || 0;
          totalPage.value = response.total_pages || Math.max(1, Math.ceil((response.total_data || 0) / (pagination?.value?.pageSize || 10)));
        } else {
          console.warn("Unexpected response format:", response);
          data.value = [];
          count.value = 0;
          totalPage.value = 0;
        }
      } else {
        data.value = [];
        count.value = 0;
        totalPage.value = 0;
      }
    } catch (error) {
      data.value = [];
      count.value = 0;
      totalPage.value = 0;
    } finally {
      loading.value = false;
      key.value++;
    }
  };

  watch(
    [() => pagination?.value, () => sorting?.value, () => globalFilters?.value, () => query.value],
    getData,
    { deep: true }
  );

  onMounted(() => {
    setTimeout(getData, 100);
  });

  return [data, count, loading, totalPage, key];
}