import axios from "axios";
import CryptoJS from "crypto-js";
import { format } from "date-fns";

const API_URL = process.env.VUE_APP_API_URL;
const APP_SECRET = process.env.VUE_APP_SECRETS;

/**
 * Class for encrypting and decrypting data using AES encryption.
 */
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

/**
 * Represents a session object that handles setting, getting, deleting, and clearing session data using cookies.
 */
class session {
  constructor() {
    this.enc = new encryption();
  }

  setSession(cname, cvalue) {
    // Creates an expires header that expires 7 days after the user enters the page
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
    // Decrypts and returns the data associated with the certificate. This is the inverse of ` authority `
    for (let i = 0; i < ca.length; i++) {
      // Remove the end of the expression if it is a comma. This is used to avoid " inlining
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

/**
 * Represents a local storage disk with encryption capabilities.
 */
class localstorageDisk {
  constructor() {
    this.enc = new encryption();
  }

  setLocalStorage(key, item) {
    if (item) {
      return localStorage.setItem(key, this.enc.encrypt(JSON.stringify(item)));
    }

    localStorage.setItem(key, null);
  }

  getLocalStorage(key) {
    const local = localStorage.getItem(key);

    if (local !== "null" && local) return JSON.parse(this.enc.decrypt(local));

    return null;
  }

  removeLocalStorage(items) {
    items.forEach((item) => {
      localStorage.removeItem(item);
    });
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
      Authorization: `Bearer ${sessionDisk.getSession("authUser").token}`
    }
  });

/**
 * Get the current time in a formatted clock string.
 * @returns {string} A formatted clock string in the format "hh:mm" with leading zeros if necessary.
 */
export const getClock = () => {
  let clock = new Date();

  const formatClock = new Intl.DateTimeFormat("default", {
    hour12: true,
    hour: "numeric",
    minute: "numeric"
  }).format(clock);

  const formatString =
    formatClock[0].length < 2 ? formatClock.padStart(8, "0") : formatClock;
  return formatString;
};

/**
 * Parses a number into a currency format using the German locale (de-DE).
 * @param {number} number - The number to be formatted as currency.
 * @returns {string} The formatted currency string.
 */
export const parseCurrency = (number) =>
  new Intl.NumberFormat("de-DE", {
    maximumFractionDigits: 2
  }).format(number);

/**
 * Performs an authenticated fetch request using the provided method, URL, and body.
 * @param {string} method - The HTTP method for the request (e.g., GET, POST, PUT, DELETE).
 * @param {string} url - The URL to send the request to.
 * @param {object} body - The data to be sent in the request body (optional).
 * @returns {Promise} A Promise that resolves with the response data if successful, or rejects with an error.
 */
export const authFetch = (method, url, body) => {
  // eslint-disable-next-line no-async-promise-executor
  return new Promise(async (resolve, reject) => {
    let res;
    try {
      let params = {
        method,
        url,
        headers: {
          Authorization: `Bearer ${sessionDisk.getSession("authUser").token}`
        }
      };

      if (method === "POST") params["data"] = body || {};

      res = await axios(params);

      resolve(res);
    } catch (error) {
      reject(error?.response?.data || "");
    }
  });
};

/**
 * Performs a fetch request with authentication, retrying up to 4 times if the request fails.
 * @param {string} method - The HTTP method for the request (e.g., GET, POST).
 * @param {string} url - The URL to fetch data from.
 * @param {object} body - The data to be sent in the request body.
 * @returns {Promise} A promise that resolves with the fetched data or rejects with an error message.
 */
/**
 * Dekripsi sederhana menggunakan XOR - untuk demo
 * @param {string} encoded - Base64 string terenkripsi
 * @param {string} key - Kunci enkripsi
 * @returns {string} - Data yang didekripsi
 */
function simpleDecrypt(encoded, key) {
  // Decode base64
  const encryptedBytes = Uint8Array.from(atob(encoded), (c) => c.charCodeAt(0));
  const keyBytes = new TextEncoder().encode(key);
  const decrypted = new Uint8Array(encryptedBytes.length);

  for (let i = 0; i < encryptedBytes.length; i++) {
    decrypted[i] = encryptedBytes[i] ^ keyBytes[i % keyBytes.length];
  }

  return new TextDecoder().decode(decrypted);
}

/**
 * Mendekripsi respons terenkripsi dari API
 * @param {Object} encryptedResponse - Respons terenkripsi
 * @returns {Object} Data yang didekripsi
 */
function decryptResponse(encryptedResponse) {
  // Pastikan response memiliki format yang benar
  if (!encryptedResponse.encrypted || !encryptedResponse.data) {
    throw new Error("Invalid encrypted response format");
  }

  try {
    // Dekripsi data menggunakan metode sederhana
    const decryptedText = simpleDecrypt(encryptedResponse.data, APP_SECRET);

    // Parse JSON hasil dekripsi
    return JSON.parse(decryptedText);
  } catch (error) {
    console.error("Error decrypting response:", error);
    throw error;
  }
}

// Modifikasi fetchWithAuth untuk menangani response terenkripsi
export const fetchWithAuth = async (method, url, body) => {
  return new Promise(async (resolve, reject) => {
    let retryCount = 0;
    let error = "";

    try {
      while (retryCount < 4) {
        const res = await authFetch(method, url, body).catch((err) => {
          error = err;
        });

        if (res?.status === 200) {
          // Cek apakah response dienkripsi
          if (res.data && res.data.encrypted === true) {
            try {
              // Dekripsi data
              const decrypted = decryptResponse(res.data);
              resolve(decrypted);
              return;
            } catch (decryptError) {
              console.error("Decryption failed:", decryptError);
              resolve(res.data);
              return;
            }
          } else {
            // Jika tidak dienkripsi
            resolve(res.data);
            return;
          }
        } else {
          console.log("An error occurred, retrying to fetch data...");
          retryCount++;
        }
      }

      throw error;
    } catch (error) {
      console.log("Exception occurred: ", error);
      reject(error);
    }
  });
};

/**
 * Check if a value is NaN and return 0 if it is, otherwise return the original value.
 * @param {number} value - The value to check for NaN.
 * @returns {number} - The original value if not NaN, otherwise 0.
 */
export const checkNaN = (value) => (isNaN(value) ? 0 : value);

/**
 * Creates a deep copy of the given value using JSON serialization.
 * @param {any} value - The value to be deep copied.
 * @returns {any} A deep copy of the input value.
 */
export const deepCopy = (value) => {
  return JSON.parse(JSON.stringify(value));
};

/**
 * Calculates the discount value based on the voucher information and criteria provided.
 * @param {object} voucher - The voucher object containing discount information.
 * @param {number} criterion1 - The first criterion for calculating the discount.
 * @param {number} criterion2 - The second criterion for calculating the discount.
 * @returns {number} The calculated discount value.
 */
export const discountWithNilaiDiskon = (voucher, criterion1, criterion2) => {
  const voucherTable = voucher.kode_voucher.split("-").slice(-1)[0];
  const maxDiscountValue =
    (voucher[`persentase_diskon_${voucherTable}`] / 100) * criterion1;

  // Computes nilai discount based on voucher diskon and criterion values
  if (maxDiscountValue > voucher.nilai_diskon) {
    const nilaiDiskon = (voucher.nilai_diskon / criterion1) * 100;
    const disc = (nilaiDiskon / 100) * (criterion2 ? criterion2 : criterion1);
    return disc;
  }

  return maxDiscountValue;
};

/**
 * Logs out the user by clearing local storage, session storage, and reloading the page.
 * @returns None
 */
export const logout = () => {
  localDisk.clearLocalStorage();
  sessionDisk.clearSession();

  window.location.reload();
};

/**
 * Converts a long number into a string representation with abbreviated units.
 * @param {number} num - The number to be converted.
 * @param {number} [threshold=2] - The number of decimal places to round to.
 * @returns {string} The formatted string representation of the number with units.
 */
export function formatLongNumberToString(num, threshold = 2) {
  var stringNum = "";
  const abbreviations = {
    Ribu: 1000,
    Juta: 1000000,
    Miliar: 1000000000
  };

  for (const key in abbreviations) {
    if (num >= abbreviations[key]) {
      stringNum = (num / abbreviations[key]).toFixed(threshold) + " " + key;
    }
  }

  return stringNum;
}

/**
 * Returns the month string in Indonesian based on the given month number.
 * @param {number} month - The month number (1-12).
 * @returns {string} The month name in Indonesian.
 */
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
    12: "Desember"
  };

  return monthStrings[month];
};

export function getCompactTimestamp() {
  const now = new Date();

  // Get components in local time zone
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");
  const seconds = String(now.getSeconds()).padStart(2, "0");

  // Return compact format
  return `${year}${month}${day}${hours}${minutes}${seconds}`;
}

export const parse = (item) => JSON.parse(item);

export const dateNow = () => format(new Date(), "yyyy-MM-dd");

export const encode = (value) => encodeURIComponent(JSON.stringify(value));

export const parseNumberFromCurrency = (value, { precision = false } = {}) => {
  let removedDots = value.replace(/[a-zA-Z.]/g, "");
  if (precision) removedDots = removedDots.replace(",", ".");

  console.log(removedDots);
  return precision ? Number(removedDots) : parseInt(removedDots);
};

export const toRupiah = (value) => {
  if (value === null || value === undefined) return "Rp 0";

  // Pastikan value adalah number
  const numValue = typeof value === "string" ? parseFloat(value) : value;

  // Format angka dengan 2 digit desimal
  const withDecimal = numValue.toFixed(2);

  // Cek apakah 2 digit terakhir adalah ,00
  const hasZeroDecimals = withDecimal.endsWith(".00");

  // Jika ,00 gunakan format tanpa desimal
  const formattedNumber = hasZeroDecimals
    ? Math.floor(numValue)
      .toString()
      .replace(/\B(?=(\d{3})+(?!\d))/g, ".")
    : withDecimal.replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, ".");

  return `Rp ${formattedNumber}`;
};

export const tipeSetoran = (tipe) => {
  const tipeSetoran = {
    1: "Tunai",
    2: "Non Tunai"
  };

  return tipeSetoran[tipe] || "Tipe Setoran Tidak Diketahui";
};

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
export const statusFakturText = (status) => {
  const statusText = {
    "-1": "denied",
    0: "draft",
    1: "printed",
    2: "unpaid",
    3: "paid",
    4: "canceled"
  };

  return statusText[status] || "Tidak Diketahui";
};

export const statusOrderText = (status) => {
  const statusText = {
    "-1": "denied",
    0: "draft",
    1: "booked",
    2: "scheduled",
    3: "picked",
    4: "shipping",
    5: "revision",
    6: "delivered",
    7: "canceled",
    8: "return",
    9: "reschedule",
    10: "rescheduled",
    11: "reshipping"
  };

  return statusText[status] || "Tidak Diketahui";
};
