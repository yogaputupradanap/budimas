import { ref } from "vue";

export function useSorting() {
  const sorting = ref([]);

  const onSortingChange = (updater) => {
    sorting.value =
      updater instanceof Function ? updater(sorting.value) : updater;
  };

  return {
    onSortingChange,
    sorting
  };
}
