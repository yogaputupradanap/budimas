import { encode, fetchWithAuth } from "../lib/utils";
import { baseService } from "./baseService";

class userAkses extends baseService {
  #baseurl;

  constructor() {
    super();
    const baseUrlColumn = encode(["fitur.*"])
    const baseUrlJoin = encode(["fitur"])
    const baseUrlOn = encode(["on users_akses.id_fitur = fitur.id"])

    this.#baseurl = `/api/base/users_akses/all?columns=${baseUrlColumn}&join=${baseUrlJoin}&on=${baseUrlOn}`;

    this.setServiceName("user akses")
  }

async getUserAkses(idUser) {
  try {
    const encodeClause = encode({ "users_akses.id_user = ": idUser });
    const clause = `&clause=${encodeClause}`;

    const response = await fetchWithAuth("GET", `${this.#baseurl}${clause}`);
    
    // console.log("Raw Response dari API:", response);

    // AMBIL DATA DARI PROPERTY .result
    const dataAkses = response?.result; 

    // Cek apakah dataAkses adalah Array
    if (!dataAkses || !Array.isArray(dataAkses)) {
      console.warn(`[User Akses] Property 'result' bukan array atau kosong untuk ID ${idUser}`);
      return []; 
    }

    // Lakukan sorting pada dataAkses
    return dataAkses.sort((a, b) => (a.id || 0) - (b.id || 0));

  } catch (err) {
    console.error("Error saat mengambil hak akses:", err);
    return []; 
  }
}
}

const userAksesService = new userAkses();
export { userAksesService };
