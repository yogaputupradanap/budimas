import { encode, fetchWithAuth, GetKeyArray, ToParams } from "../lib/utils";
import { baseService } from "./baseService";

class PajakService extends baseService {
  #baseUrl;
  constructor() {
    super();

    this.#baseUrl = `${process.env.VUE_APP_API_URL}/api/pajak`;

    this.apiEndpoints = {
      getDraftFakturUrl: `${this.#baseUrl}/get-draf-list-faktur`,
      getFinalFakturUrl: `${this.#baseUrl}/get-final-list-faktur`,
      getDetailDraftFakturUrl: `${this.#baseUrl}/get-detail-draf-faktur`,
      exportXmlDraftPajakUrl: `${this.#baseUrl}/export-xml-draf-pajak`,
      getFakturByFileUrl: `${this.#baseUrl}/get-faktur-by-file`,
      addFakturPajakUrl: `${this.#baseUrl}/add-data-to-pajak`,
    };
    this.setServiceName("pajak");
  }

  async getDraftFaktur(clause = {}) {
    try {
      Object.keys(clause).forEach((key) => {
        if (clause[key] === null) {
          delete clause[key];
        }
      });
      console.log(clause);
      const params = ToParams(clause);

      const finalURL = `${this.apiEndpoints.getDraftFakturUrl}?${params}`;
      const response = await fetchWithAuth("GET", finalURL, clause);
      return Promise.resolve(response);
    } catch (error) {
      return error
    }
  }

  async getFinalFaktur(clause = {}) {
    try {
      Object.keys(clause).forEach((key) => {
        if (clause[key] === null) {
          delete clause[key];
        }
      });
      console.log(clause);
      const params = ToParams(clause);

      const finalURL = `${this.apiEndpoints.getFinalFakturUrl}?${params}`;
      const response = await fetchWithAuth("GET", finalURL, clause);
      return Promise.resolve(response);
    } catch (error) {
      return error
    }
  }

  async exportXmlDraftPajak(id = {}) {
    try {
      let arr_id = GetKeyArray(id);
      let clause = { id_faktur: arr_id };
      const params = ToParams(clause);
      const finalURL = `${this.apiEndpoints.exportXmlDraftPajakUrl}?${params}`;
      const response = await fetchWithAuth("GET", finalURL);
      return Promise.resolve(response);
    } catch (error) {
      return error
    }
  }
  async GetDetailDraftFaktur(id) {
    try {
      const finalURL = `${this.apiEndpoints.getDetailDraftFakturUrl}/${id}`;
      const response = await fetchWithAuth("GET", finalURL);
      return Promise.resolve(response);
    } catch (error) {
      return error
    }
  }

  async getFakturByFile(no_faktur = []) {
    try {
      const clause = {
        no_faktur_arr: no_faktur,
      };
      const params = ToParams(clause);
      const finalURL = `${this.apiEndpoints.getFakturByFileUrl}?${params}`;
      const response = await fetchWithAuth("GET", finalURL);
      return Promise.resolve(response);
    } catch (error) {
      return error
    }
  }

  async AddFakturPajak(body = {}) {
    try {
      const finalURL = `${this.apiEndpoints.addFakturPajakUrl}`;
      const response = await fetchWithAuth("POST", finalURL, body);
      return Promise.resolve(response);
    } catch (error) {
      return error
    }
  }
}

const pajakService = new PajakService();
export { pajakService };
