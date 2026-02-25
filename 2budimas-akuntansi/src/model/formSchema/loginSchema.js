import { object, string } from "yup";

export const loginSchema = object({
  email: string()
    .required("Email tidak boleh kosong")
    .email("Email tidak valid")
    .label("email"),
  password: string()
    .required("Password tidak boleh kosong")
    .min(2, "Masukkan minimal 8 karakter")
    .label("password"),
});
