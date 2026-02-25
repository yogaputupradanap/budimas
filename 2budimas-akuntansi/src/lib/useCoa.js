import {ref} from "vue";
import {fetchWithAuth} from "@/src/lib/utils";

const useCoa = () => {
    const loading = ref(false)
    const coa = ref([])
    const coaMain = ref([])
    
    const getCoa = async (id_perusahaan) => {
        loading.value = true;
        try {
            // Hapus "=" agar tidak error 500
            const clause = { "id_perusahaan =": id_perusahaan }; 
            const url = `/api/base/coa/all?clause=${encodeURIComponent(JSON.stringify(clause))}`;
            const res = await fetchWithAuth("GET", url);
            
            // PERBAIKAN: Masukkan ke coa.value, BUKAN getCoa.value
            if (res && Array.isArray(res.result)) {
                coa.value = res.result;
            } else if (res && res.pages && Array.isArray(res.pages.result)) {
                coa.value = res.pages.result;
            } else if (Array.isArray(res)) {
                coa.value = res;
            } else {
                coa.value = [];
            }
        } catch (e) {
            console.error("Error fetching Coa:", e);
            coa.value = [];
        } finally {
            loading.value = false;
        }
    };

    const getCoaMain = async (id_perusahaan) => {
    loading.value = true;
    try {
        const clause = { "id_perusahaan =": id_perusahaan };
        const url = `/api/base/coa/all?clause=${encodeURIComponent(JSON.stringify(clause))}`;
        const res = await fetchWithAuth("GET", url);
        
        // console.log("Response Asli API:", res);

        // PERBAIKAN DI SINI:
        // Karena response Anda adalah { result: [...] }, maka ambil res.result
        if (res && Array.isArray(res.result)) {
            coaMain.value = res.result;
        } else if (res && res.pages && Array.isArray(res.pages.result)) {
            coaMain.value = res.pages.result;
        } else if (Array.isArray(res)) {
            coaMain.value = res;
        } else {
            coaMain.value = [];
        }

        // console.log("Hasil akhir coaMain.value (setelah fix):", coaMain.value);
    } catch (e) {
        console.error("Error fetching Coa Main:", e);
        coaMain.value = [];
    } finally {
        loading.value = false;
    }
}

    const getCoaByParentId = async (id_perusahaan, parent_ids) => {
        loading.value = true
        try {
            const clause = {
                "id_perusahaan = ": id_perusahaan,
                "is_deleted = ": `'false'`,
                "is_active = ": `'true'`
            }
            const whereOr = {
                "parent_id": parent_ids, // parent_ids harus berupa array [1, 2, 3]
                "id_coa": parent_ids
            };
            const url = `/api/base/coa/all?clause=${encodeURIComponent(JSON.stringify(clause))}&whereOr=${encodeURIComponent(JSON.stringify(whereOr))}`
            const res = await fetchWithAuth("GET", url)
            return res || []
        } catch (e) {
            console.error("Error fetching Coa:", e)
            return []
        } finally {
            loading.value = false
        }
    }

    return {
        getCoa,
        getCoaByParentId,
        getCoaMain,
        coaMain,
        loading,
        coa
    }
}

export default useCoa;