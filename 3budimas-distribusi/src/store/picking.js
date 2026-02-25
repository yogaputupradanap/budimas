import { defineStore } from "pinia";
import { apiUrl, fetchWithAuth, localDisk } from "../lib/utils";
import { useKepalaCabang } from "./kepalaCabang";
import { useRoute } from "vue-router";

const localRutePicking = localDisk.getLocalStorage("rute_picking");
const localAddPicking = localDisk.getLocalStorage("add_picking");
const localDetailPicking = localDisk.getLocalStorage("detail_picking");

const listPicking = {
  rutePicking: localRutePicking,
  loading: true,
  error: null,
};
const listAddPicking = {
  addPicking: localAddPicking,
  loading: true,
  error: null,
};
const listDetailPicking = {
  detailPicking: localDetailPicking,
  loading: true,
  error: null,
};

export const usePicking = defineStore("picking", {
  state: () => ({
    listPicking,
    isFromPicking: false,
    listAddPicking,
    listDetailPicking,
  }),
  actions: {
    resetPickingState(stateName) {
      Object.assign(this[stateName], eval(stateName));
    },
    async getRutePicking(idCabang) {
      try {
        this.listPicking.loading = true;
        this.listPicking.rutePicking = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/distribusi/get-rute-picking?id=${idCabang}`
        );
        this.isFromPicking = true;
        localDisk.setLocalStorage("rute_picking", this.listPicking.rutePicking);
      } catch (error) {
        this.listPicking.error = error;
        console.error("Error fetching data:", error);
      } finally {
        this.listPicking.loading = false;
      }
    },
    async getListAddPicking(
      rute_id,
      id_cabang,
      id_armada,
      id_driver,
      delivering_date
    ) {
      try {
        this.listAddPicking.loading = true;

        const addPicking = await fetchWithAuth(
          "GET",
          `${apiUrl}/api/distribusi/get-add-picking?id=${id_cabang}&rute_id=${rute_id}&id_armada=${id_armada}&id_driver=${id_driver}&delivering_date=${delivering_date}`
        );

        const restructure = addPicking.map((val) => {
          let jumlah = val.jumlah_picked;
          const konversi3 = val.konversi3;
          const konversi2 = val.konversi2;

          let karton = Math.floor(jumlah / konversi3);
          jumlah = jumlah % konversi3;

          let box = Math.floor(jumlah / konversi2);
          jumlah = jumlah % konversi2;

          let pieces = jumlah;

          const keterangan = `${karton} karton, ${box} box, ${pieces} pieces`;

          return {
            ...val,
            keterangan,
            calculated_karton: karton,
            calculated_box: box,
            calculated_pieces: pieces,
          };
        });

        this.listAddPicking.addPicking = restructure;
        localDisk.setLocalStorage(
          "add_picking",
          this.listAddPicking.addPicking
        );
      } catch (error) {
        this.listAddPicking.error = error;
        console.log(error);
      } finally {
        this.listAddPicking.loading = false;
      }
    },
    async getDetailListPicking(id_produk) {
  const kepalaCabang = useKepalaCabang();
  let idCabang = kepalaCabang.kepalaCabangUser.id_cabang;

  const router = useRoute();
  const productid = router.params.id_produk;

  try {
    this.listDetailPicking.loading = true;

    const detailPicking = await fetchWithAuth(
  "GET",
  `${apiUrl}/api/distribusi/daftar-picking-toko?id_cabang=${idCabang}&id_rute=${router.params.id_rute}&id_produk=${productid}&id_order_detail=${router.query.id_order_detail}`
);

// console.log(router.params.productid);
const data = detailPicking.result || [];
console.log(data);

const restructure = data.map((val) => ({
  ...val,
  picking: val.total_in_pieces || 0,
}));

this.listDetailPicking.detailPicking = restructure;
localDisk.setLocalStorage("detail_picking", restructure);
}catch (error) {
    this.listDetailPicking.error = error;
    console.log(error);
  } finally {
    this.listDetailPicking.loading = false;
  }
},
  },
});
