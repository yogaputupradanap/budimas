import { fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class FakturService extends baseService {
  constructor() {
    super();

    const apiUrlPajak = process.env.VUE_APP_API_PAJAK_URL;
    const apiUrl = process.env.VUE_APP_API_URL;
    this.apiEndpoints = {
      addFaktur: `${apiUrlPajak}/api/pajak/add-faktur-pajak`,
      listFaktur: `${apiUrl}/api/pajak/get-list-faktur`,
      generatedFaktur: `${apiUrlPajak}/api/pajak/get-generated-faktur`,
      listGeneratedFaktur: `${apiUrlPajak}/api/pajak/get-list-generated-faktur`,
      detailFakturPajak: `${apiUrlPajak}/api/pajak/get-detail-list-generated-faktur`,
      listDetailFakturPajak: `${apiUrl}/api/pajak/get-faktur-detail`,
      listDraftFaktur: `${apiUrl}/api/pajak/get-draft-faktur`,
      listDraftDetailFaktur: `${apiUrl}/api/pajak/get-draft-faktur`,
    };
    this.setServiceName("faktur");
  }
  async GetListDraftFaktur() {
    try {
      const data = await fetchWithAuth("GET", this.listDraftFaktur);
      return { success: true, data: response.data || [] };
    } catch (e) {
      this.throwError(error);
      return { success: false, message: error.message };
    }
  }

  async GetDraftDetailwhFaktur() {
    try {
      const data = await fetchWithAuth("GET", this.listDraftDetailFakturd);
      return { success: true, data: response.data || [] };
    } catch (e) {
      this.throwError(error);
      return { success: false, message: error.message };
    }
  }

  async getListFaktur() {
    try {
      const [generatedData, listData] = await Promise.all([
        fetchWithAuth("GET", this.apiEndpoints.listGeneratedFaktur),
        fetchWithAuth("GET", this.apiEndpoints.listFaktur),
      ]);

      const generatedIds = new Set(
        (generatedData.data || []).map((item) => item.id)
      );
      const filteredData = (listData.pages || []).filter(
        (item) => !generatedIds.has(item.id)
      );

      return filteredData;
    } catch (error) {
      this.throwError(error);
      return [];
    }
  }

  async getListGeneratedFaktur() {
    try {
      const response = await fetchWithAuth(
        "GET",
        this.apiEndpoints.listGeneratedFaktur
      );
      return { success: true, data: response.data || [] };
    } catch (error) {
      this.throwError(error);
      return { success: false, message: error.message };
    }
  }

  async addFaktur(selectedData) {
    try {
      const response = await fetchWithAuth(
        "POST",
        this.apiEndpoints.addFaktur,
        selectedData
      );
      return response;
    } catch (error) {
      this.throwError(error);
      return { success: false, message: error.message };
    }
  }

  async getGeneratedFaktur(ids) {
    try {
      const idsParam = Array.isArray(ids) ? ids.join(",") : ids;
      const response = await fetchWithAuth(
        "GET",
        `${this.apiEndpoints.generatedFaktur}?ids=${idsParam}`
      );
      return { success: true, data: response.data };
    } catch (error) {
      this.throwError(error);
      return { success: false, message: error.message };
    }
  }

  async detailFakturPajak(no_faktur) {
    const param = `no_faktur=${no_faktur}`;
    try {
      const result = await fetchWithAuth(
        "GET",
        `${this.apiEndpoints.detailFakturPajak}?${param}`
      );

      return result;
    } catch (error) {
      this.throwError(error);
    }
  }

  async listDetailFakturPajak(no_faktur) {
    try {
      const result = await fetchWithAuth(
        "GET",
        `${this.apiEndpoints.listDetailFakturPajak}/${no_faktur}`
      );
      console.log("listDetailFakturPajak response:", result);
      return result;
    } catch (error) {
      console.error("listDetailFakturPajak error:", error);
      this.throwError(error);
    }
  }
}

const fakturService = new FakturService();
export { fakturService };
