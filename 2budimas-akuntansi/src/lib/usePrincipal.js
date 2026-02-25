import { ref } from "vue";
import { fetchWithAuth } from "@/src/lib/utils";

const usePrincipal = () => {
    const loading = ref(false)
    const principal = ref([])

    const getPrincipal = async (id_perusahaan) => {
        if (!id_perusahaan) return;

        loading.value = true
        try {
            // 1. PERBAIKAN: Hapus tanda "=" untuk menghindari blokir backend (Error 500)
            const clause = {
                "id_perusahaan =": id_perusahaan,
            }
            
            const url = `/api/base/principal/all?clause=${encodeURIComponent(JSON.stringify(clause))}`
            const res = await fetchWithAuth("GET", url)
            
            // 2. PERBAIKAN: Mapping data dengan fallback yang aman
            // Mengecek apakah data ada di res.result, res.pages.result, atau res itu sendiri
            if (res && Array.isArray(res.result)) {
                principal.value = res.result;
            } else if (res && res.pages && Array.isArray(res.pages.result)) {
                principal.value = res.pages.result;
            } else {
                principal.value = Array.isArray(res) ? res : [];
            }

        } catch (e) {
            console.error("Error fetching Principal:", e)
            principal.value = []
        } finally {
            loading.value = false
        }
    }

    return {
        getPrincipal,
        loading,
        principal
    }
}

export default usePrincipal;