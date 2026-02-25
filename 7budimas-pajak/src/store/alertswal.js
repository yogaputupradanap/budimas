import { defineStore } from "pinia";
import Swal from "sweetalert2";

export const useAlertSwal = defineStore("alertSwal", {
  state: () => ({
    defaultTimer: 2000,
  }),

  actions: {
    // Backward compatible: sama API dengan versi toast
    setMessage(message, variant = "success", dismissCountDown = 2000) {
      switch (variant) {
        case "success":
          return this.success(message, { timer: dismissCountDown });
        case "danger":
          return this.danger(message, { timer: dismissCountDown });
        case "warning":
          return this.warning(message, { timer: dismissCountDown });
        default:
          return this.success(message, { timer: dismissCountDown });
      }
    },

    // Modal sukses (auto close)
    success(message, options = {}) {
      const {
        title = "Berhasil memperbarui",
        timer = this.defaultTimer,
        showConfirmButton = false,
        ...rest
      } = options;
      return Swal.fire({
        title,
        text: message,
        icon: "success",
        timer,
        timerProgressBar: true,
        showConfirmButton,
        ...rest,
      });
    },

    // Modal error/danger (auto close)
    danger(message, options = {}) {
      const {
        title = "Gagal",
        timer = this.defaultTimer,
        showConfirmButton = false,
        ...rest
      } = options;
      return Swal.fire({
        title,
        text: message,
        icon: "error",
        timer,
        timerProgressBar: true,
        showConfirmButton,
        ...rest,
      });
    },

    // Modal warning (auto close)
    warning(message, options = {}) {
      const {
        title = "Peringatan",
        timer = this.defaultTimer,
        showConfirmButton = false,
        ...rest
      } = options;
      return Swal.fire({
        title,
        text: message,
        icon: "warning",
        timer,
        timerProgressBar: true,
        showConfirmButton,
        ...rest,
      });
    },

    // Modal konfirmasi (return boolean)
    async confirm({
      title = "Konfirmasi",
      text = "Apakah Anda yakin?",
      confirmButtonText = "Ya",
      cancelButtonText = "Batal",
      icon = "question",
      showDenyButton = false,
      ...rest
    } = {}) {
      const result = await Swal.fire({
        title,
        text,
        icon,
        showCancelButton: true,
        showDenyButton,
        confirmButtonText,
        cancelButtonText,
        focusCancel: true,
        reverseButtons: true,
        ...rest,
      });
      return result.isConfirmed === true;
    },
  },
});