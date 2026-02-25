import { fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class principal extends baseService {
  constructor() {
    super();

    this.principalUrl = "/api/base/principal";

    this.setServiceName("principal");
  }

  async getPrincipals() {
    try {
      const result = await fetchWithAuth("GET", this.principalUrl);
      return result;
    } catch (error) {
      console.error(error);
      this.throwError(error);
    }
  }
}

export const principalService = new principal();
