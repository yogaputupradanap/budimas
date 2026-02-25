import {ref} from "vue";
import {fetchWithAuth} from "@/src/lib/utils";

const useCoaCategory = () => {
    const loading = ref(false)
    const coaCategories = ref([])
    const getCoaCategory = async () => {
        loading.value = true
        try {
            const res = await fetchWithAuth("GET", "/api/base/coa_category")
            coaCategories.value = res || []
        } catch (e) {
            console.error("Error fetching COA categories:", e)
            return []
        } finally {
            loading.value = false
        }
    }

    return {
        getCoaCategory,
        loading,
        coaCategories
    }
}

export default useCoaCategory;