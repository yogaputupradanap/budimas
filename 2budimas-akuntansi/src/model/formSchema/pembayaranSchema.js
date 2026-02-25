import { object, string, mixed } from "yup";

const filteType = ["png", "jpg", "jpeg"];
export const pembayaranSchema = object({
  notaFaktur: string()
    .required("Nota faktur tidak boleh kosong 😢")
    .label("notaFaktur"),
  jumlahBayar: string()
    .required("Jumlah pembayaran tidak boleh kosong 😢")
    .min(3, "Masukkan minimal 3 karakter 😢")
    .label("jumlahBayar"),
  metodePembayaran: string()
    .required("Metode pembayaran tidak boleh kosong")
    .label("metodePembayaran"),
  buktiTransfer: mixed()
    .required("Bukti transfer tidak boleh kosong")
    .test({
      message: "Extensi file harus bertipe jpg, jpeg, png ",
      test(file) {
        return file && !filteType.includes(file.name);
      },
    })
    .label("buktiTransfer"),
});
