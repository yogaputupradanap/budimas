import { computed, ref, watch } from "vue";
import { useAlert } from "../store/alert";
import { fetchWithAuth } from "./utils";

export function useTableSearch(
  baseUrl,
  fieldEntries = [], // watched entries for buttonText
  queryEntries, // used for build clause
  {
    initialColumnName,
    filterFunction = null,
    reduceFunction = null,
    checkFieldFilterFunc = (val) => val[1] === "",
    additionalCheckFieldFilterFunc = null,
    asArgument = false,
  } = {}
) {
  const alert = useAlert();

  const data = ref(null);
  const isServerTable = ref(true);
  const searchEntries = computed(() => queryEntries.value);
  const searchLoading = ref(false);
  const key = ref(0);

  const buttonText = ref({
    text: "Cari Data",
    icon: "mdi mdi-magnify",
  });

  // check if all search entries equal to already defined comparison function
  const checkAllSearchField = computed(() => {
    let entries = [...searchEntries.value];

    if (additionalCheckFieldFilterFunc)
      entries = [...searchEntries.value].filter(additionalCheckFieldFilterFunc);

    return entries.every(checkFieldFilterFunc);
  });

  // building argument from entries if asArgument parameter true
  const buildArgument = (searchEntriesParam = [[]]) => {
    return searchEntriesParam.reduce((acc, val, idx) => {
      acc += `${val[0]}${val[1]}`;
      if (idx !== searchEntriesParam.length - 1) acc += "&";
      return acc;
    }, "");
  };

  // building clause for search url
  const buildClause = () => {
    let entries = [...searchEntries.value];

    if (filterFunction) entries = [...entries].filter(filterFunction);
    if (reduceFunction) entries = [...entries].reduce(reduceFunction, []);

    if (!asArgument) {
      const searchObject = Object.fromEntries(entries);
      const objectSearch = JSON.stringify(searchObject);
      return encodeURIComponent(objectSearch);
    }

    const argument = buildArgument(entries);
    return argument;
  };

  const reset = () => {
    fieldEntries.forEach((val) => (val.value = null));
    data.value = [];
    key.value++;
  };

  const getButtonText = () => {
    buildClause();
    if (!isServerTable.value && checkAllSearchField.value) {
      buttonText.value = {
        text: "Reload",
        icon: "mdi mdi-reload",
      };
    } else {
      buttonText.value = {
        text: "Cari Data",
        icon: "mdi mdi-magnify",
      };
    }
  };

const searchQuery = async () => {
    const clause = buildClause();
    const field = initialColumnName ? `&field=${initialColumnName}` : "";

    const argument = asArgument
      ? `?${clause}${field}`
      : `&clause=${clause}${field}`;
    const url = `${baseUrl}${argument}&no-paginate=true`;

    try {
      searchLoading.value = true;
      const res = await fetchWithAuth("GET", url);

      // PERBAIKAN: Jangan langsung data.value = res
      // Pastikan kita mengambil array yang ada di dalam res.result
      if (res && Array.isArray(res.result)) {
        data.value = res.result;
      } else if (res && res.pages && Array.isArray(res.pages.result)) {
        data.value = res.pages.result;
      } else if (Array.isArray(res)) {
        data.value = res;
      } else {
        // Jika API error atau mengembalikan objek error, kasih array kosong
        data.value = [];
      }

    } catch (error) {
      // Jika fetch gagal, pastikan data dikosongkan agar tabel tidak render data lama
      data.value = [];
      alert.setMessage(error, "danger");
    } finally {
      searchLoading.value = false;
      isServerTable.value = checkAllSearchField.value;
      key.value++;
      getButtonText();
    }
  };

  watch(fieldEntries, () => getButtonText());

  return [
    data,
    buttonText,
    searchLoading,
    isServerTable,
    key,
    searchQuery,
    reset
  ];
}
