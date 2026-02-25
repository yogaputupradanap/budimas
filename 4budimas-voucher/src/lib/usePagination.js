import { ref } from "vue";

export function usePagination(initialSize = 5) {
  const pagination = ref({
    pageSize: initialSize,
    pageIndex: 0,
  });

  const onPaginationChange = (updater) => {
    pagination.value =
      updater instanceof Function ? updater(pagination.value) : updater;
  };

  return {
    onPaginationChange,
    pagination
  };
}
