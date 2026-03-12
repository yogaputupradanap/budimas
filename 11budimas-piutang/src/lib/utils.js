import axios from "axios";
import CryptoJS from "crypto-js";

const API_URL = process.env.VUE_APP_API_URL;
const APP_SECRET = process.env.VUE_APP_SECRETS;

class encryption {
    encrypt(item) {
        if (!item) return "";
        try {
            return CryptoJS.AES.encrypt(item, APP_SECRET).toString();
        } catch (e) {
            return "";
        }
    }

    decrypt(item) {
        if (!item) return "";
        try {
            const decrypt = CryptoJS.AES.decrypt(item, APP_SECRET);
            const text = decrypt.toString(CryptoJS.enc.Utf8);
            return text; // Akan mengembalikan "" jika gagal/salah kunci
        } catch (error) {
            return "";
        }
    }
}

class session {
    constructor() {
        this.enc = new encryption();
    }

    setSession(cname, cvalue) {
        const d = new Date();
        d.setTime(d.getTime() + 7 * 24 * 60 * 60 * 1000);
        let expires = "expires=" + d.toUTCString();

        let encryptedValue = this.enc.encrypt(JSON.stringify(cvalue));
        // Encode URI Component untuk menangani karakter spesial dalam cipher AES
        document.cookie = cname + "=" + encodeURIComponent(encryptedValue) + ";" + expires + ";path=/";
    }

    getSession(cname) {
        let name = cname + "=";
        let decodedCookie = document.cookie;
        let ca = decodedCookie.split(";");
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i].trim();
            if (c.indexOf(name) == 0) {
                try {
                    let rawValue = decodeURIComponent(c.substring(name.length, c.length));
                    let decryptValue = this.enc.decrypt(rawValue);

                    // Proteksi: jangan parse jika hasil decrypt kosong atau hanya spasi
                    if (!decryptValue || decryptValue.trim() === "") return null;

                    return JSON.parse(decryptValue);
                } catch (e) {
                    console.error(`Error parsing session ${cname}:`, e);
                    return null;
                }
            }
        }
        return null;
    }

    deleteSession(cname) {
        document.cookie = cname + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    }

    clearSession() {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i];
            const eqPos = cookie.indexOf("=");
            const name = eqPos > -1 ? cookie.substr(0, eqPos).trim() : cookie.trim();
            this.deleteSession(name);
        }
    }
}

class LocalStorageDisk {
    constructor() {
        this.enc = new encryption();
    }

    setLocalStorage(key, item) {
        if (item === undefined || item === null) {
            localStorage.removeItem(key);
            return;
        }
        const encrypted = this.enc.encrypt(JSON.stringify(item));
        localStorage.setItem(key, encrypted);
    }

    getLocalStorage(key) {
        try {
            const local = localStorage.getItem(key);

            // Cek jika data memang tidak ada
            if (!local || local.trim() === "" || local === "null" || local === "undefined") {
                return null;
            }

            // 1. Coba Decrypt
            const decrypted = this.enc.decrypt(local);
            if (decrypted && decrypted.trim() !== "") {
                try {
                    return JSON.parse(decrypted);
                } catch (e) {
                    // Jika decrypt berhasil tapi JSON invalid, lanjut ke fallback
                }
            }

            // 2. Fallback: Coba parse sebagai JSON biasa (untuk data lama/tidak terenkripsi)
            // Pastikan local bukan string random hasil enkripsi yang gagal
            if (local.startsWith("{") || local.startsWith("[")) {
                return JSON.parse(local);
            }
            
            return null;
        } catch (err) {
            console.error(`Gagal mengambil data [${key}]:`, err.message);
            return null;
        }
    }

    removeLocalStorage(items) {
        if (Array.isArray(items)) {
            items.forEach((item) => localStorage.removeItem(item));
        } else {
            localStorage.removeItem(items);
        }
    }

    clearLocalStorage() {
        localStorage.clear();
    }
}

export const localDisk = new LocalStorageDisk();

export const sessionDisk = new session();

export const apiUrl = API_URL;

export const axiosPostFetch = (url, body) =>
  axios.post(url, body, {
    headers: {
      Authorization: `Bearer HorusBudimas`,
    },
  });

export const getClock = () => {
  let clock = new Date();

  const formatClock = new Intl.DateTimeFormat("default", {
    hour12: true,
    hour: "numeric",
    minute: "numeric",
  }).format(clock);

  const formatString =
    formatClock[0].length < 2 ? formatClock.padStart(8, "0") : formatClock;
  return formatString;
};

export const parseCurrency = (number) =>
  new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
  }).format(number);

export const authFetch = (method, url, body) => {
  return new Promise(async (resolve, reject) => {
    let res;
    try {
      let params = {
        method,
        url,
        headers: {
          Authorization: `Bearer ${sessionDisk.getSession("authUser").token}`,
        },
      };

      if (method === "POST" || method === "PUT") params["data"] = body || {};

      res = await axios(params);

      resolve(res);
    } catch (error) {
      reject(error?.response?.data || "");
    }
  });
};

export const fetchWithAuth = async (method, url, body) => {
  return new Promise(async (resolve, reject) => {
    const URL = `${apiUrl}${url}`;

    let retryCount = 0;
    let error = "";
    // console.log("try fetching in auth fetch");

    try {
      while (retryCount < 1) {
        const res = await authFetch(method, URL, body).catch((err) => {
          error = err;
        });
        if (res?.status === 200) {
          resolve(res.data);
          return;
        } else {
          console.log("An error occurred, retrying to fetch data...");
          retryCount++;
        }
      }

      throw error;
    } catch (error) {
      reject(error);
    }
  });
};

export const checkNaN = (value) => (isNaN(value) ? 0 : value);

export const deepCopy = (value) => {
  return JSON.parse(JSON.stringify(value));
};

export const logout = () => {
  localDisk.clearLocalStorage();
  sessionDisk.clearSession();

  window.location.reload();
};

export const formatLongNumberToString = (num, threshold = 2) => {
  var stringNum = "";
  const abbreviations = {
    Ribu: 1000,
    Juta: 1000000,
    Miliar: 1000000000,
  };

  for (const key in abbreviations) {
    if (num >= abbreviations[key]) {
      stringNum = (num / abbreviations[key]).toFixed(threshold) + " " + key;
    }
  }

  return stringNum;
};

export const getMonthString = (month) => {
  const monthStrings = {
    1: "Januari",
    2: "Februari",
    3: "Maret",
    4: "April",
    5: "Mei",
    6: "Juni",
    7: "Juli",
    8: "Agustus",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Desember",
  };

  return monthStrings[parseInt(month)];
};

export const getDayString = (day) => {
  const dayString = {
    0: "minggu",
    1: "senin",
    2: "selasa",
    3: "rabu",
    4: "kamis",
    5: "jumat",
    6: "sabtu",
  };

  return dayString[parseInt(day)];
};

export const trimText = (text = "", treshold = 0) => {
  return text.length > treshold ? `${text.substring(0, treshold)} ....` : text;
};

export const getDateNow = (
  now = new Date(),
  useSlash = true,
  timeOnly = false
) => {
  const date = now.getDate().toString();
  const month = (now.getMonth() + 1).toString();
  const year = now.getFullYear();

  const formatDate = date.length > 1 ? date : "0" + date;
  const formatMonth = month.length > 1 ? month : "0" + month;

  const isUseSlash = useSlash ? "/" : "-";

  if (timeOnly) {
    const nowTime = getClock();

    if (/(pm)/gi.test(nowTime)) {
      let o = parseInt(nowTime.substring(0, 2)) + 12;
      return o + nowTime.substring(2, 5);
    }

    return nowTime.substring(0, 5);
  }

  return `${formatDate}${isUseSlash}${formatMonth}${isUseSlash}${year}`;
};

export const simpleDateNow = (date = Date.now()) => {
  return new Date(date).toISOString().split("T")[0];
};

export const numberToWords = (num) => {
  if (num === 0) return "nol";

  const belowTwenty = [
    "",
    "satu",
    "dua",
    "tiga",
    "empat",
    "lima",
    "enam",
    "tujuh",
    "delapan",
    "sembilan",
    "sepuluh",
    "sebelas",
    "dua belas",
    "tiga belas",
    "empat belas",
    "lima belas",
    "enam belas",
    "tujuh belas",
    "delapan belas",
    "sembilan belas",
  ];
  const tens = [
    "",
    "sepuluh",
    "dua puluh",
    "tiga puluh",
    "empat puluh",
    "lima puluh",
    "enam puluh",
    "tujuh puluh",
    "delapan puluh",
    "sembilan puluh",
  ];
  const thousands = ["", "ribu", "juta", "miliar"];

  const helper = (n) => {
    if (n === 0) return "";
    else if (n < 20) return belowTwenty[n] + " ";
    else if (n < 100) return tens[Math.floor(n / 10)] + " " + helper(n % 10);
    else return belowTwenty[Math.floor(n / 100)] + " ratus " + helper(n % 100);
  };

  let result = "";
  for (let i = 0; i < thousands.length && num > 0; i++) {
    if (num % 1000 !== 0) {
      result = helper(num % 1000) + thousands[i] + " " + result;
    }
    num = Math.floor(num / 1000);
  }

  return result.trim().replace("satu ratus", "seratus");
};

export const getVoucherDiscount = (vouchers, tipe_voucher, harga_jual) => {
  const getValueDiscount1 = vouchers.filter((item) => {
    let splitString = String(item.kode).split("-");
    let lastIndexValue = splitString[splitString.length - 1];
    return lastIndexValue == tipe_voucher;
  });

  const hargaJualProduk = harga_jual;
  const getDiscount = getValueDiscount1
    .map((item) => {
      let discount = (item.nilai_diskon / hargaJualProduk) * 100;
      return discount;
    })
    .reduce((acc, val) => val + acc, 0);

  return getDiscount;
};

export const status = {
  "admin gudang": 0,
  sales: 1,
  kasir: 2,
  audit: 3,
};

export const parse = (item) => JSON.parse(item);

export const encode = (value) => encodeURIComponent(JSON.stringify(value));

export const getSelectedRow = (selectedRow, sourceData) => {
  const keysArray = Object.keys(selectedRow.value);
  const getFilterData = (value) => {
    const atData = sourceData.at(parseInt(value));
    return atData;
  };
  const returnedData = keysArray.map(getFilterData);
  return returnedData;
};

export const statusSetoranList = [
  {
    name: "Admin Gudang",
    value: 0,
  },
  {
    name: "Sales",
    value: 1,
  },
  {
    name: "Kasir",
    value: 2,
  },
  {
    name: "Audit",
    value: 3,
  },
];

export const getTodayDate = (addDays = 0) => {
  const today = new Date();
  today.setDate(today.getDate() + addDays);
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, "0");
  const day = String(today.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
};

export const statusPengeluaranList = [
  { name: "Diajukan", value: 0 },
  { name: "Disetujui", value: 1 },
  { name: "Ditolak", value: 2 },
  { name: "Diberikan", value: 3 },
];

/**
 * Format angka untuk menampilkan mata uang dengan format Indonesia
 * dan otomatis menampilkan digit desimal jika ada
 *
 * @param {number} value - Nilai yang akan diformat
 * @return {string} - String angka yang sudah diformat
 */
export const formatCurrencyAuto = (value) => {
  if (value === null || value === undefined) return "0";

  // Convert to number if it's a string
  const numValue = typeof value === "string" ? parseFloat(value) : value;

  // Cek apakah nilai memiliki desimal
  const hasDecimal =
    String(numValue).includes(".") &&
    parseFloat(String(numValue).split(".")[1]) > 0;

  // Jika tidak memiliki desimal, tidak tampilkan desimal
  if (!hasDecimal) {
    return Math.floor(numValue).toLocaleString("id-ID").replace(/,/g, ".");
  }

  // Jika ada desimal, tampilkan dengan format Indonesia dan maksimal 2 digit desimal
  const formattedNumber = numValue.toFixed(2); // Bulatkan ke 2 digit desimal
  const parts = formattedNumber.split(".");
  const integerPart = parseInt(parts[0])
    .toLocaleString("id-ID")
    .replace(/,/g, ".");
  return `${integerPart},${parts[1]}`;
};

export const isCpOptions = [
  { name: "Tanggal Jatuh Tempo", value: 0 },
  { name: "Call Plan", value: 1 },
];
