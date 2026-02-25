import { ref, watch, onMounted } from "vue";
import { fetchWithAuth } from "./utils";

export function useFetchPaginate(
  query = "",
  { pagination, sorting, globalFilters, initialSortColumn } = {}
) {
  const data = ref([]);
  const count = ref(0);
  const loading = ref(true);
  const key = ref(0);
  const totalPage = ref(0);

  const getData = async () => {
    try {
      loading.value = true;

      const checkJoinTable = query.split("&").length > 1;
      const joinedField = initialSortColumn;
      const getField = sorting.value.length
        ? sorting.value[0].id
        : initialSortColumn || 'id';
      
      console.log('get field : ', getField)
      const getOrder = !sorting.value.length
        ? "asc"
        : sorting.value[0].desc
        ? "desc"
        : "asc";

      const limit = `limit=${pagination.value.pageSize}`;
      const page = `page=${pagination.value.pageIndex}`;
      const order = `order=${getOrder}`;
      const field = `field=${getField}`;
      const filters = `filters=${globalFilters.value.value.text}`;
      const columns = `columns=${globalFilters.value.value.columns}`;

      const filterWithColumns =
        globalFilters.value.value.text && globalFilters.value.value.columns
          ? `&${filters}&${columns}`
          : "";

      const url = `${query}${limit}&${page}&${order}&${limit}&${field}${filterWithColumns}`;

      const get = await fetchWithAuth("GET", url);

      data.value = get?.pages;
      count.value = get?.total_data;
      const curr_page = Math.ceil(get?.total_data / pagination.value.pageSize);

      totalPage.value = curr_page <= 0 ? 1 : curr_page;
    } catch (error) {
      console.log("paginate fetch error : ", error);
    } finally {
      loading.value = false;
      key.value++;
    }
  };

  watch([pagination, sorting, globalFilters], () => {
    getData();
  });

  onMounted(() => {
    getData();
  });

  return [data, count, loading, totalPage, key];
}
