import { ref } from "vue";

export function useFiltering() {
  const globalFilters = ref({
    state: "idle",
    value: {
      text: "",
      columns: [],
    },
  });

  const onColumnFilterChange = (updater) => {
    const newState = {
      state: "typing",
      value:
        updater instanceof Function
          ? updater(globalFilters.value.value)
          : updater,
    };

    globalFilters.value = newState;
  };

  return {
    globalFilters,
    onColumnFilterChange,
  };
}
