import { ref } from "vue";

export function useQuery(url, fetcher) {
  const data = ref(null);
  const loading = ref(false);

  const fetchData = async () => {
    try {
      loading.value = true;
      data.value = await fetcher(url);
    } catch (error) {
      const message = `error in useQuery : ${error}`;
      console.log(message);
      throw message;
    } finally {
      loading.value = false;
    }
  };

  fetchData();

  return {data, loading};
}
