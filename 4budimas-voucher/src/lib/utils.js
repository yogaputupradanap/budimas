import axios from "axios";
import CryptoJS from "crypto-js";
import Compressor from "compressorjs";

const API_URL = process.env.VUE_APP_API_URL;
const APP_SECRET = process.env.VUE_APP_SECRETS;

class encryption {
  encrypt(item) {
    const encrypt = CryptoJS.AES.encrypt(item, APP_SECRET).toString();

    return encrypt;
  }

  decrypt(item) {
    const decrypt = CryptoJS.AES.decrypt(item, APP_SECRET);
    const text = decrypt.toString(CryptoJS.enc.Utf8);

    return text;
  }
}

class session {
  constructor() {
    this.enc = new encryption();
  }

  setSession(cname, cvalue) {
    const d = new Date();
    d.setTime(d.getTime() + 1 * 24 * 60 * 60 * 1000);
    let expires = "expires=" + d.toUTCString();

    let encryptedValue = this.enc.encrypt(JSON.stringify(cvalue));

    document.cookie = cname + "=" + encryptedValue + ";" + expires + ";path=/";
  }

  getSession(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(";");
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == " ") {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        let decryptValue = this.enc.decrypt(c.substring(name.length, c.length));

        return JSON.parse(decryptValue);
      }
    }

    return null;
  }

  deleteSession(cname) {
    document.cookie =
      cname + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  }

  clearSession() {
    var cookies = document.cookie.split(";");

    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i];
      var eqPos = cookie.indexOf("=");
      var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
      document.cookie =
        name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    }
  }
}

class localstorageDisk {
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

            if (!local || local === "null" || local === "undefined") {
                return null;
            }

            const decrypted = this.enc.decrypt(local);

            if (!decrypted) return null;

            return JSON.parse(decrypted);
        } catch (err) {
            console.warn("localStorage corrupted:", key);
            localStorage.removeItem(key);
            return null;
        }
    }

    removeLocalStorage(items) {
        items.forEach((item) => localStorage.removeItem(item));
    }

    clearLocalStorage() {
        localStorage.clear();
    }
}

export const localDisk = new localstorageDisk();

export const sessionDisk = new session();

export const apiUrl = API_URL;

export const axiosPostFetch = (url, body) =>
  axios.post(url, body, {
    headers: {
      Authorization: `Bearer ugQCeKhIMnw1SNZnaGXif6YzG4EwHQ2wJ6ZLx8Q1IWajPvwuwhwCed7laXdX`,
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
  new Intl.NumberFormat("id-ID").format(number);

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
    console.log("try fetching in auth fetch");

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

export const parseNumberFromCurrency = (value) => {
  const removedDots = value.replace(/[a-zA-Z.]/g, "");
  return parseInt(removedDots);
};

export function compressImage(file, options = {}) {
  return new Promise((resolve, reject) => {
    if (!(file instanceof File)) {
      reject(new Error("The provided input is not a valid File."));
      return;
    }

    // Default options for compression
    const defaultOptions = {
      quality: 0.8, // Compression quality (0 to 1)
      maxWidth: 1920, // Maximum width for the image
      maxHeight: 1080, // Maximum height for the image
      convertSize: 5000000, // Files larger than this (in bytes) will be compressed
    };

    // Merge user options with default options
    const config = { ...defaultOptions, ...options };

    new Compressor(file, {
      quality: config.quality,
      maxWidth: config.maxWidth,
      maxHeight: config.maxHeight,
      convertSize: config.convertSize,

      success(compressedFile) {
        const toFileType = new File([compressedFile], compressedFile.name, {
          type: compressedFile.type,
        });
        resolve(toFileType);
      },

      error(err) {
        reject(err);
      },
    });
  });
}

export function haveSameShape(array1, array2) {
  if (!Array.isArray(array1) || !Array.isArray(array2)) return false;

  // Check if both arrays have the same length
  if (array1.length !== array2.length) return false;

  for (let i = 0; i < array1.length; i++) {
    const isArray1ElementArray = Array.isArray(array1[i]);
    const isArray2ElementArray = Array.isArray(array2[i]);

    // If one element is an array and the other is not, return false
    if (isArray1ElementArray !== isArray2ElementArray) return false;

    // If both elements are arrays, check their shapes recursively
    if (isArray1ElementArray && isArray2ElementArray) {
      if (!haveSameShape(array1[i], array2[i])) return false;
    }
  }

  return true;
}