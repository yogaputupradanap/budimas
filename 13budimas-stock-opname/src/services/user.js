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

    this.#signInUrl = "/api/auth/stock-opname/login";
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
      const paramClause = encode({ "users.id = ": id, "users.id_jabatan in ": "(9,10,2)" });
      const param = `&clause=${paramClause}`;
      const url = `${this.#baseUrl}${param}`;
      
      const response = await fetchWithAuth("GET", url);
      
      // Perbaikan utama: akses response.result
      if (response && response.result && Array.isArray(response.result) && response.result.length > 0) {
        const userData = response.result[0];
        console.log('User found:', userData.nama, 'Cabang:', userData.id_cabang);
        return userData; 
      }
      
      console.warn('User tidak ditemukan atau struktur API berubah');
      return null; 
    } catch (error) {
      console.error('Error fetching user info:', error);
      throw error;
    }
  }
}

export const userService = new user();
