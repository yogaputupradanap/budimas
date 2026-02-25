<!-- SweetAlert.vue -->
<template>
  <!-- Komponen ini tidak memerlukan template karena hanya berisi kode utilitas -->
</template>

<script>
import Swal from "sweetalert2";

// Konfigurasi default
const defaultOptions = {
  title: "Konfirmasi",
  text: "Apakah Anda yakin?",
  icon: "question",
  showCancelButton: true,
  confirmButtonText: "Ya",
  cancelButtonText: "Tidak",
  reverseButtons: true,
  allowOutsideClick: false,
  customClass: {
    confirmButton: "btn btn-success",
    cancelButton: "btn btn-danger",
  },
  buttonsStyling: true,
};

// Tipe alert yang tersedia
const alertTypes = {
  SUCCESS: {
    icon: "success",
    title: "Berhasil!",
    confirmButtonText: "OK",
  },
  ERROR: {
    icon: "error",
    title: "Kesalahan!",
    confirmButtonText: "OK",
  },
  WARNING: {
    icon: "warning",
    title: "Peringatan!",
    confirmButtonText: "OK",
  },
  INFO: {
    icon: "info",
    title: "Informasi",
    confirmButtonText: "OK",
  },
  QUESTION: {
    icon: "question",
    title: "Konfirmasi",
    showCancelButton: true,
    confirmButtonText: "Ya",
    cancelButtonText: "Tidak",
  },
  CONFIRM_DELETE: {
    icon: "warning",
    title: "Hapus Data",
    text: "Data yang dihapus tidak dapat dikembalikan!",
    showCancelButton: true,
    confirmButtonText: "Ya, hapus!",
    cancelButtonText: "Batal",
    confirmButtonColor: "#d33",
  },
  CONFIRM_SUBMIT: {
    icon: "question",
    title: "Konfirmasi Submit",
    text: "Apakah Anda yakin ingin mengirim data ini?",
    showCancelButton: true,
    confirmButtonText: "Ya, submit!",
    cancelButtonText: "Batal",
  },
  LOADING: {
    title: "Memproses...",
    allowOutsideClick: false,
    showConfirmButton: false,
    didOpen: () => {
      Swal.showLoading();
    },
  },
};

// Fungsi utama
const $swal = {
  // Alert biasa
  fire(options = {}) {
    return Swal.fire({
      ...defaultOptions,
      ...options,
    });
  },

  // Alert dengan tipe yang sudah didefinisikan
  async show(type, customOptions = {}) {
    const options = {
      ...defaultOptions,
      ...alertTypes[type],
      ...customOptions,
    };
    return await Swal.fire(options);
  },

  // Alert konfirmasi umum
  async confirm(message, options = {}) {
    const result = await Swal.fire({
      ...defaultOptions,
      text: message,
      ...options,
    });
    return result.isConfirmed;
  },

  // Alert sukses
  success(message, options = {}) {
    return Swal.fire({
      icon: "success",
      title: "Berhasil!",
      text: message,
      confirmButtonText: "OK",
      ...options,
    });
  },

  // Alert error
  error(message, options = {}) {
    return Swal.fire({
      icon: "error",
      title: "Kesalahan!",
      html: message,
      confirmButtonText: "OK",
      confirmButtonColor: "#d33",
      ...options,
    });
  },

  // Alert warning
  warning(message, options = {}) {
    return Swal.fire({
      icon: "warning",
      title: "Peringatan!",
      text: message,
      confirmButtonText: "OK",
      ...options,
    });
  },

  // Alert info
  info(message, options = {}) {
    return Swal.fire({
      icon: "info",
      title: "Informasi",
      text: message,
      confirmButtonText: "OK",
      ...options,
    });
  },

  // Alert konfirmasi hapus
  async confirmDelete(
    message = "Data yang dihapus tidak dapat dikembalikan!",
    options = {}
  ) {
    const result = await Swal.fire({
      icon: "warning",
      title: "Hapus Data",
      text: message,
      showCancelButton: true,
      confirmButtonText: "Ya, hapus!",
      cancelButtonText: "Batal",
      confirmButtonColor: "#d33",
      cancelButtonColor: "#1976d2",
      ...options,
    });
    return result.isConfirmed;
  },

  // Alert konfirmasi submit
  async confirmSubmit(
    message = "Apakah Anda yakin ingin mengirim data ini?",
    options = {}
  ) {
    const result = await Swal.fire({
      icon: "question",
      title: "Konfirmasi Submit",
      html: message,
      confirmButtonColor: "#28a745",
      cancelButtonColor: "#1976d2",
      showCancelButton: true,
      cancelButtonText: "Batal",
      confirmButtonText: "Ya, submit!",
      ...options,
    });
    return result.isConfirmed;  
  },

  async confirmTolak(
    message = "Apakah Anda yakin ingin menolak data ini?",
    options = {}
  ) {
    const result = await Swal.fire({
      icon: "warning",
      title: "Konfirmasi Tolak",
      html: message,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#1976d2",
      showCancelButton: true,
      cancelButtonText: "Batal",
      confirmButtonText: "Ya, tolak!",
      ...options,
    });
    return result.isConfirmed;
  },
  async confirmEdit(
    message = "Apakah Anda yakin ingin mengedit data ini?",
    options = {}
  ) {
    const result = await Swal.fire({
      icon: "question",
      title: "Konfirmasi Edit",
      html: message,
      confirmButtonColor: "#28a745",
      cancelButtonColor: "#1976d2",
      showCancelButton: true,
      cancelButtonText: "Batal",
      confirmButtonText: "Ya, edit!",
      ...options,
    });
    return result.isConfirmed;
  },

  // Alert loading
  loading(message = "Memproses...") {
    return Swal.fire({
      title: message,
      allowOutsideClick: false,
      showConfirmButton: false,
      didOpen: () => {
        Swal.showLoading();
      },
    });
  },

  // Close alert
  close() {
    Swal.close();
  },

  // Toast notification
  toast(options = {}) {
    const defaultToastOptions = {
      toast: true,
      position: "top-end",
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: true,
    };

    return Swal.fire({
      ...defaultToastOptions,
      ...options,
    });
  },

  // Toast success
  toastSuccess(message, options = {}) {
    return this.toast({
      icon: "success",
      title: message,
      ...options,
    });
  },

  // Toast error
  toastError(message, options = {}) {
    return this.toast({
      icon: "error",
      title: message,
      ...options,
    });
  },

  // Toast warning
  toastWarning(message, options = {}) {
    return this.toast({
      icon: "warning",
      title: message,
      ...options,
    });
  },

  // Toast info
  toastInfo(message, options = {}) {
    return this.toast({
      icon: "info",
      title: message,
      ...options,
    });
  },

  // Update alert content
  update(options) {
    Swal.update(options);
  },
};

// Buat plugin untuk Vue
const SweetAlertPlugin = {
  install(app) {
    app.config.globalProperties.$swal = $swal;
    app.provide("$swal", $swal);
  },
};

export { $swal, SweetAlertPlugin };

export default {
  name: "SweetAlert",
};
</script>
