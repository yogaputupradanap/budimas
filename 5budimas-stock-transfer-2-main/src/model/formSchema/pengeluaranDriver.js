import {object, string, number, mixed, date} from "yup"

export const pengeluaranSchema = object({
    id_driver: mixed().required('driver tidak boleh kosong').label('id_driver'),
    tanggal: date().required("tanggal berangkat tidak boleh kosong").label('tanggal'),
    tujuan: string().required("tujuan tidak boleh kosong").label('tujuan'),
    helper: string().required("helper tidak boleh kosong").label('helper'),
    km_berangkat: number().required("Km berangkat tidak boleh kosong").label('km_berangkat'),
    km_pulang: number().required("Km pulang tidak boleh kosong").label('km_pulang'),
    km_isi_bbm: number().required("Km isi bbm tidak boleh kosong").label('km_isi_bbm'),
    isi_bbm_liter: number().required("isi bbm liter tidak boleh kosong").label('isi_bbm_liter'),
    isi_bbm_rupiah: number().required("isi bbm rupiah tidak boleh kosong").label('isi_bbm_rupiah'),
    uang_saku: number().required("uang saku tidak boleh kosong").label('uang_saku')
})