import { object, string, mixed, number } from "yup";

export const pembayaranSchema = object({
  jumlahBayar: string()
    .required("Jumlah pembayaran tidak boleh kosong")
    .min(4, "Masukkan minimal 4 karakter")
    .label("jumlahBayar"),
});
