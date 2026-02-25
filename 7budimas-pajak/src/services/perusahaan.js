  import { encode, fetchWithAuth } from "../lib/utils";
  import { baseService } from "./baseService";

  class Perusahaan extends baseService {
      #baseURL;


      constructor() {
          super();

          const baseColumns = encode([
              "id",
              "nama",
          ]);

          this.#baseURL = `/api/base/perusahaan?columns=${baseColumns}`;
          this.setServiceName("perusahaan");
      }


      async getAllPerusahaan() {
          try {
              const perusahaan = await fetchWithAuth("GET", this.#baseURL);
              return perusahaan;
          } catch (error) {
              this.throwError(error);
          }
      }

  }




  const perusahaanService = new Perusahaan();
  export { perusahaanService };
