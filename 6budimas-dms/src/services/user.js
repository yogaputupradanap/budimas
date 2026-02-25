import axios from "axios";
import { apiUrl, encode, fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class user extends baseService {
  #signInUrl;
  #baseUrl;


  constructor() {
    super();

    const baseUrlOn = encode(["on users.id_jabatan = jabatan.id", "on users.id_cabang = cabang.id"])
    const baseUrlColumns = encode(["users.*", "jabatan.nama as nama_jabatan", "cabang.nama as nama_cabang"])
    const baseUrlJoin = encode(["jabatan", "cabang"])

    this.#signInUrl = "/api/auth/dms/login";
    this.#baseUrl = `/api/base/users/all?on=${baseUrlOn}&columns=${baseUrlColumns}&join=${baseUrlJoin}`;

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
      throw error?.response?.data || ''
    }
  }

   async getUserInfo(id) {
    try {
      const paramClause = encode({
        "users.id = ": id,
      });
      const param = `&clause=${paramClause}`;
      const url = `${this.#baseUrl}${param}`;
      const userInfo = await fetchWithAuth("GET", url);
      console.log("ui", userInfo);
      return Promise.resolve(userInfo[0]);
    } catch (error) {
      this.throwError(error);
    }
  }
}

export const userService = new user();
