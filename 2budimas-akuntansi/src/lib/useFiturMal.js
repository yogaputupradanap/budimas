import {ref} from "vue";
import {fetchWithAuth} from "@/src/lib/utils";

const useFiturMal = () => {
    const loading = ref(false)
    const fiturMal = ref([])
    const getFiturMal = async () => {
        loading.value = true
        try {
            const res = await fetchWithAuth("GET", "/api/base/fitur_mal")
            fiturMal.value = res || []
        } catch (e) {
            console.error("Error fetching Fitur Akhir:", e)
            return []
        } finally {
            loading.value = false
        }
    }

    return {
        getFiturMal,
        loading,
        fiturMal
    }
}

export default useFiturMal;