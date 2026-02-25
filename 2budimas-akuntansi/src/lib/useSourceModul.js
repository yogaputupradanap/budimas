import { ref } from "vue";
import { fetchWithAuth } from "@/src/lib/utils";

const useSourceModul = () => {
    const loading = ref(false);
    const sourceModul = ref([]);

    const getSourceModul = async (id_fitur_mal) => {
        if (!id_fitur_mal) return; // Guard clause jika id kosong

        loading.value = true;
        try {
            // 1. Perbaikan: Hapus tanda "=" agar tidak diblokir backend (Error 500)
            const clause = {
                'id_fitur_mal =': id_fitur_mal
            };

            const url = `/api/base/source_modul/all?clause=${encodeURIComponent(JSON.stringify(clause))}`;
            const res = await fetchWithAuth("GET", url);

            // 2. Perbaikan: Mapping data sesuai struktur { result: [...] }
            // Kita gunakan fallback agar fleksibel terhadap struktur API
            if (res && Array.isArray(res.result)) {
                sourceModul.value = res.result;
            } else if (res && res.pages && Array.isArray(res.pages.result)) {
                sourceModul.value = res.pages.result;
            } else if (Array.isArray(res)) {
                sourceModul.value = res;
            } else {
                sourceModul.value = [];
            }
        } catch (e) {
            console.error("Error fetching Source Modul:", e);
            sourceModul.value = [];
        } finally {
            loading.value = false;
        }
    };

    return {
        getSourceModul,
        loading,
        sourceModul
    };
};

export default useSourceModul;