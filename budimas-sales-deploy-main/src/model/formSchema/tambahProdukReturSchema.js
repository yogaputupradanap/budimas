import { number, object, string } from "yup";

export const tambahProdukReturSchema = object({
  namaProduk: number()
    .typeError("value harus bertipe number")
    .required("Nama produk tidak boleh kosong")
    .label("namaProduk"),
  piecesBad: number()
    .typeError("value harus bertipe numeric")
    .required("Pieces tidak boleh kosong")
    .label("pieces"),
  piecesGood: number()
    .typeError("value harus bertipe numeric")
    .required("Pieces tidak boleh kosong")
    .label("pieces"),
  boxBad: number()
    .typeError("value harus bertipe numeric")
    .required("Box tidak boleh kosong")
    .label("box"),
  boxGood: number()
    .typeError("value harus bertipe numeric")
    .required("Box tidak boleh kosong")
    .label("box"),
  kartonGood: number()
    .typeError("value harus bertipe numeric")
    .required("karton tidak boleh kosong"),
  kartonBad: number()
    .typeError("value harus bertipe numeric")
    .required("karton tidak boleh kosong"),
  keteranganRetur: string().optional()
});
