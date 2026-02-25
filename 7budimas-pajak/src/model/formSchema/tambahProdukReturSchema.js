import { number, object, string } from "yup";

export const tambahProdukReturSchema = object({
  namaProduk: number()
    .typeError("value harus bertipe number 😢")
    .required("Nama produk tidak boleh kosong 😢")
    .label("namaProduk"),
  pieces: number()
    .typeError("value harus bertipe numeric 😢")
    .required("Pieces tidak boleh kosong 😢")
    .label("pieces"),
  box: number()
    .typeError("value harus bertipe numeric 😢")
    .required("Box tidak boleh kosong 😢")
    .label("box"),
  karton: number()
    .typeError("value harus bertipe numeric 😢")
    .required("karton tidak boleh kosong 😢"),
  keteranganRetur: string().optional(),
});
