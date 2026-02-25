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

    const response = await fetchWithAuth(
      "GET",
      `${this.#baseurl}${clause}`
    );

    const data = Array.isArray(response?.result)
      ? response.result
      : [];

    return data.sort((a, b) => a.id - b.id);
  } catch (err) {
    this.throwError(err);
  }
}

}

const userAksesService = new userAkses();
export { userAksesService };
