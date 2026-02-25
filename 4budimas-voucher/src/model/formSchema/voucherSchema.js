import { date, mixed, number, object, string, ref, array } from "yup";

export const voucherSchema = object({
  id_principal: number()
    .typeError("ID principal harus berupa angka")
    .required("ID principal tidak boleh kosong")
    .label("id_principal"),

  id_produk: array()
    .of(object())
    .when(["tipe_voucher", "jenis_voucher"], {
      is: (tipe, jenis) => {
        // Untuk V2 dan V3 dengan jenis produk (1), wajib pilih produk
        if ((tipe === 2 || tipe === 3) && jenis === 0) return true;
        // Untuk V1, tidak perlu pilih produk
        return false;
      },
      then: (schema) =>
        schema
          .required("Produk harus dipilih")
          .min(1, "Minimal pilih 1 produk"),
      otherwise: (schema) => schema.optional(),
    })
    .label("id_produk"),

  id_cabang: array()
    .of(object())
    .when(["tipe_voucher", "jenis_voucher"], {
      is: (tipe, jenis) => (tipe === 2 || tipe === 3) && jenis === 0,
      then: (schema) => schema.required("Cabang harus dipilih"),
      otherwise: (schema) => schema.optional(),
    })
    .label("id_cabang"),

  kategori_voucher: mixed()
    .when(["tipe_voucher", "jenis_voucher"], {
      is: (tipe, jenis) => (tipe === 2 || tipe === 3) && jenis === 0,
      then: (schema) =>
        number()
          .typeError("Kategori voucher harus berupa angka")
          .required("Kategori voucher harus dipilih"),
      otherwise: (schema) => schema.nullable(),
    })
    .label("kategori_voucher"),
  nama: string()
    .required("Nama tidak boleh kosong")
    .min(2, "Masukkan minimal 2 karakter")
    .label("nama"),

  tipe_voucher: number()
    .typeError("Tipe voucher harus berupa angka")
    .required("Tipe voucher tidak boleh kosong")
    .label("klasifikasi_voucher"),

  persen_diskon: mixed()
    .when(["tipe_voucher", "kategori_voucher", "jenis_voucher"], {
      is: (tipe, kategori, jenis) => {
        // Untuk tipe voucher 1, selalu wajib
        if (tipe === 1) return true;

        // Untuk V2/V3 jenis reguler, selalu wajib seperti V1
        if ((tipe === 2 || tipe === 3) && jenis === 1) return true;

        // Untuk tipe 2/3 jenis produk, wajib hanya jika kategori = persen (1)
        if ((tipe === 2 || tipe === 3) && jenis === 0 && kategori === 1)
          return true;

        return false;
      },
      then: (schema) =>
        number()
          .typeError("Persen diskon harus berupa angka")
          .required("Persen diskon harus diisi")
          .min(0, "Persen diskon tidak boleh kurang dari 0")
          .max(100, "Persen diskon tidak boleh lebih dari 100"),
      otherwise: (schema) =>
        mixed()
          .nullable()
          .transform((value) => null),
    })
    .label("persen_diskon"),

  nilai_diskon: string()
    .when(["tipe_voucher", "kategori_voucher"], {
      is: (tipe, kategori) => (tipe === 2 || tipe === 3) && kategori === 2,
      then: (schema) => schema.required("Nilai diskon harus diisi"),
      otherwise: (schema) => schema.optional(),
    })
    .label("nilai_diskon"),

  // minimal_total_pembelian: string()
  //   .when("tipe_voucher", {
  //     is: 1,
  //     then: (schema) =>
  //       schema.required("Minimal total pembelian tidak boleh kosong"),
  //     otherwise: (schema) => schema.optional(),
  //   })
  //   .label("minimal_total_pembelian"),

  minimal_subtotal_pembelian: string()
    .when(["tipe_voucher", "jenis_voucher"], ([tipeVoucher, jenisVoucher]) => {
      // Wajib untuk V1 atau V2/V3 jenis reguler
      if (
        tipeVoucher === 1 ||
        ((tipeVoucher === 2 || tipeVoucher === 3) && jenisVoucher === 1)
      ) {
        return string().required(
          "Minimal subtotal pembelian tidak boleh kosong"
        );
      } else {
        return string().optional();
      }
    })
    .label("minimal_subtotal_pembelian"),

  keterangan: string().nullable().label("keterangan"),

  id_customer: array()
    .of(object())
    .when(["tipe_voucher", "jenis_voucher"], {
      is: (tipe, jenis) => tipe === 3 && jenis === 0,
      then: (schema) => schema.required("Customer harus dipilih"),
      otherwise: (schema) => schema.optional(),
    })
    .label("id_customer"),

  tanggal_mulai: date()
    .typeError("Tanggal mulai harus berupa tanggal yang valid")
    .when(["tipe_voucher", "jenis_voucher"], {
      is: (tipe, jenis) => {
        // Perlu tanggal untuk V2/V3 dengan jenis produk (0)
        if ((tipe === 2 || tipe === 3) && jenis === 0) return true;
        // Tidak perlu tanggal untuk V1 atau V2/V3 dengan jenis reguler (1)
        return false;
      },
      then: (schema) => schema.required("Tanggal mulai tidak boleh kosong"),
      otherwise: (schema) => schema.nullable(),
    })
    .label("tanggal_mulai"),

  tanggal_kadaluarsa: date()
    .typeError("Tanggal kadaluarsa harus berupa tanggal yang valid")
    .when(["tipe_voucher", "jenis_voucher"], {
      is: (tipe, jenis) => {
        // Perlu tanggal untuk V2/V3 dengan jenis produk (0)
        if ((tipe === 2 || tipe === 3) && jenis === 0) return true;
        // Tidak perlu tanggal untuk V1 atau V2/V3 dengan jenis reguler (1)
        return false;
      },
      then: (schema) =>
        schema
          .required("Tanggal kadaluarsa tidak boleh kosong")
          .min(
            ref("tanggal_mulai"),
            "Tanggal kadaluarsa harus setelah tanggal mulai"
          ),
      otherwise: (schema) => schema.nullable(),
    })
    .label("tanggal_kadaluarsa"),

  status_diskon: number()
    .typeError("Status diskon harus berupa angka")
    .required("Status diskon tidak boleh kosong")
    .label("status_diskon"),

  limit: string().optional().label("limit"),

  upload_file: mixed()
    .nullable()
    .optional()
    .test(
      "fileType",
      "Extensi file harus bertipe jpg, jpeg, atau png",
      (file) => {
        if (!file) return true; // Jika tidak ada file, validasi berhasil
        return /\.(jpe?g|png)$/i.test(file.name);
      }
    )
    .test("fileSize", "Ukuran file maksimal 2MB", (file) => {
      if (!file) return true; // Jika tidak ada file, validasi berhasil
      return file.size <= 2 * 1024 * 1024;
    })
    .label("upload_file"),

  syarat_ketentuan: string()
    .required("Syarat ketentuan tidak boleh kosong")
    .label("syarat_ketentuan"),

  syarat_wajib: string()
    .required("Syarat wajib tidak boleh kosong")
    .label("syarat_wajib"),

  level_uom: number()
    .when(["tipe_voucher", "jenis_voucher"], {
      is: (tipe, jenis) => tipe === 2 && jenis === 0,
      then: (schema) =>
        number()
          .typeError("Level UOM harus berupa angka")
          .required("Level UOM harus dipilih")
          .oneOf([1, 2, 3], "Level UOM harus berupa 1, 2, atau 3"),
      otherwise: (schema) => schema.nullable(),
    })
    .label("level_uom"),

  minimal_jumlah_produk: mixed()
    .when(["tipe_voucher", "jenis_voucher"], {
      is: (tipe, jenis) => tipe === 2 && jenis === 0,
      then: (schema) =>
        number()
          .typeError("Minimal Jumlah produk harus berupa angka")
          .required("Minimal Jumlah produk harus diisi")
          .min(1, "Minimal Jumlah produk minimal 1"),
      otherwise: (schema) => schema.nullable(),
    })
    .label("minimal_jumlah_produk"),
  jenis_voucher: number()
    .when("tipe_voucher", {
      is: (val) => val === 2 || val === 3,
      then: (schema) =>
        number()
          .typeError("Jenis voucher harus berupa angka")
          .required("Jenis voucher harus dipilih")
          .oneOf([0, 1], "Jenis voucher harus dipilih"),
      otherwise: (schema) => schema.nullable(),
    })
    .label("jenis_voucher"),
});
