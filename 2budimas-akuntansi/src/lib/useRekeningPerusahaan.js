import { ref } from 'vue';
import { fetchWithAuth } from "@/src/lib/utils";
import { $swal } from "@/src/components/ui/SweetAlert.vue";

const useRekeningPerusahaan = () => {
    const loading = ref(false);
    const rekeningPerusahaan = ref([]);

    const getRekeningPerusahaan = async (id_perusahaan) => {
        // Jika id_perusahaan null/undefined/kosong, langsung bersihkan list
        if (!id_perusahaan) {
            rekeningPerusahaan.value = [];
            return;
        }

        const columns = ['id_rekening_perusahaan', 'nama_bank'];
        
        /**
         * PERBAIKAN FORMAT CLAUSE:
         * Cobalah salah satu dari format berikut jika format pertama gagal.
         * Format 1 (Paling Umum): {'nama_kolom =': nilai} (Tanpa spasi sebelum atau sesudah =)
         */
        const clause = {
            'id_perusahaan =': id_perusahaan 
        };

        /* Catatan: Jika backend Anda menggunakan PHP PDO/Query Builder lama, 
        kadangkala mereka butuh tanda kutip manual:
        'id_perusahaan =': `'${id_perusahaan}'`
        */

        const url = `/api/base/rekening_perusahaan/all?columns=${encodeURIComponent(JSON.stringify(columns))}&clause=${encodeURIComponent(JSON.stringify(clause))}`;

        if (loading.value) return;
        loading.value = true;

        try {
            const res = await fetchWithAuth("GET", url);
            
            console.log("Response Raw:", res); // Ini akan memunculkan {result: Array(1), status: 'success'}

            // PERBAIKAN DI SINI:
            // Ambil dari res.result sesuai struktur response API Anda
            if (res && res.result && Array.isArray(res.result)) {
                rekeningPerusahaan.value = res.result;
            } else if (Array.isArray(res)) {
                rekeningPerusahaan.value = res;
            } else {
                rekeningPerusahaan.value = [];
            }

            console.log("Data Bank Loaded (Final):", rekeningPerusahaan.value);
        } catch (error) {
            console.error('Error fetching rekening:', error);
            rekeningPerusahaan.value = [];
        } finally {
            loading.value = false;
        }
    };

    return {
        rekeningPerusahaan,
        loading,
        getRekeningPerusahaan
    };
};

export default useRekeningPerusahaan;