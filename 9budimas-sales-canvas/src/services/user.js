import axios from "axios";
import { apiUrl, encode, fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class user extends baseService {
  #signInUrl;
  #baseUrl;
  #baseJoinUrl;

  constructor() {
    super();

    this.baseUrlOn = encode([
      "on users.id_jabatan = jabatan.id",
      "on users.id_cabang = cabang.id",
      "on sales.id_user = users.id",
      "on principal.id = sales.id_principal",
    ]);
    this.baseUrlColumns = encode([
      "users.*",
      "jabatan.nama as nama_jabatan",
      "cabang.nama as nama_cabang",
      "principal.nama as principal",
      "principal.id as principal_id",
    ]);
    this.baseUrlJoin = encode(["jabatan", "cabang", "sales", "principal"]);

    this.#signInUrl = "/api/auth/sales-canvas/login";
    this.#baseUrl = `/api/base/users/all`;
    this.#baseJoinUrl = `${this.#baseUrl}?on=${this.baseUrlOn}&columns=${this.baseUrlColumns}&join=${this.baseUrlJoin}`;

    this.setServiceName("user");
  }

  async signIn(email, password) {
    try {
      const sign = await axios({
        method: "POST",
        url: `${apiUrl}${this.#signInUrl}`,
        data: {
          email,
          password,
        },
      });
      return Promise.resolve(sign);
    } catch (error) {
      throw error?.response?.data || "";
    }
  }

  async getUserInfo(id) {
    try {
      const paramsClause = { "users.id = ": id, "users.id_jabatan in ": "(22)" };
      const url = `${this.#baseJoinUrl}&clause=${encode(paramsClause)}`;

      const userInfo = await fetchWithAuth("GET", url);
      console.log("User Information Raw: ", userInfo);

      // --- PERBAIKAN DI SINI ---
      // Karena formatnya { result: [...], status: 200 }
      if (userInfo && userInfo.result && userInfo.result.length > 0) {
        return Promise.resolve(userInfo.result[0]); 
      }
      
      // Jika data tidak ditemukan
      return Promise.resolve(null);
      
    } catch (error) {
      this.throwError(error);
    }
  }
}

export const userService = new user();
