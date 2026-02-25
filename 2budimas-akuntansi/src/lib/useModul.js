import {ref} from "vue";
import {fetchWithAuth} from "@/src/lib/utils";

const useModul = () => {
    const loading = ref(false)
    const modul = ref([])
    const getModul = async () => {
        loading.value = true
        try {
            const res = await fetchWithAuth("GET", "/api/base/modul")
            modul.value = res || []
        } catch (e) {
            console.error("Error fetching Modul:", e)
            return []
        } finally {
            loading.value = false
        }
    }

    return {
        getModul,
        loading,
        modul
    }
}

export default useModul;