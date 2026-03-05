import { object, number } from "yup";

export const rekapPembayaranSchema = object({
  tunai: number()
    .min(0, "Tunai tidak boleh kurang dari 0")
    .test(
      "max-setoran",
      "Tunai tidak boleh melebihi jumlah setoran",
      function (value) {
        const { jumlah_setoran } = this.parent;
        return value <= jumlah_setoran;
      }
    )
    .label("tunai"),
});
