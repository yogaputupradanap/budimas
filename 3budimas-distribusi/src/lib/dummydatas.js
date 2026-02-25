export const listPembayarandata = [
  {
    no: 1,
    notaTagihan: "NT001",
    kodeCustomer: "C001",
    namaCustomer: "John Doe",
    kodePrincipal: "KP001",
    totalBayar: 500,
    jatuhTempo: "2024-02-01",
    tglBayar: "",
    status: "Pending",
  },
  {
    no: 2,
    notaTagihan: "NT002",
    kodeCustomer: "C002",
    namaCustomer: "Jane Smith",
    kodePrincipal: "KP002",
    totalBayar: 750,
    jatuhTempo: "2024-02-05",
    tglBayar: "2024-02-03",
    status: "Paid",
  },
  {
    no: 3,
    notaTagihan: "NT003",
    kodeCustomer: "C003",
    namaCustomer: "Robert Johnson",
    kodePrincipal: "KP003",
    totalBayar: 600,
    jatuhTempo: "2024-02-10",
    tglBayar: "",
    status: "Pending",
  },
  {
    no: 4,
    notaTagihan: "NT004",
    kodeCustomer: "C004",
    namaCustomer: "Emily Davis",
    kodePrincipal: "KP004",
    totalBayar: 900,
    jatuhTempo: "2024-02-15",
    tglBayar: "2024-02-12",
    status: "Paid",
  },
  {
    no: 5,
    notaTagihan: "NT005",
    kodeCustomer: "C005",
    namaCustomer: "Michael Williams",
    kodePrincipal: "KP005",
    totalBayar: 700,
    jatuhTempo: "2024-02-20",
    tglBayar: "",
    status: "Pending",
  },
];

export const KunjunganData = [
  {
    No: 1,
    kodeCustomer: "C001",
    namaCustomer: "John Doe",
    statusKunjungan: "sudah",
  },
  {
    No: 2,
    kodeCustomer: "C002",
    namaCustomer: "Jane Smith",
    statusKunjungan: "belum",
  },
  {
    No: 3,
    kodeCustomer: "C003",
    namaCustomer: "Robert Johnson",
    statusKunjungan: "sudah",
  },
];

export const stockOpnameData = [
  {
    no: 1,
    kodePrincipal: "KP001",
    namaPrincipal: "Principal 1",
    status: "Active",
  },
  {
    no: 2,
    kodePrincipal: "KP002",
    namaPrincipal: "Principal 2",
    status: "Inactive",
  },
  {
    no: 3,
    kodePrincipal: "KP003",
    namaPrincipal: "Principal 3",
    status: "Active",
  },
];

export const listNotaFakturData = [
  { notaFaktur: "NF001", jumlah: 1500000, status: "Paid" },
  { notaFaktur: "NF002", jumlah: 800000, status: "Pending" },
  { notaFaktur: "NF003", jumlah: 2500000, status: "Paid" },
  { notaFaktur: "NF004", jumlah: 1200000, status: "Pending" },
  { notaFaktur: "NF005", jumlah: 500000, status: "Paid" },
];

export const historyOrderData = [
  {
    notaOrder: "NO001",
    kodeCustomer: "123",
    namaCustomer: "John Doe",
    kodePrincipal: "KP001",
    totalBayar: 1500000,
    tanggalOrder: "2024-02-01",
    status: "Pending",
  },
  {
    notaOrder: "NO002",
    kodeCustomer: "456",
    namaCustomer: "Jane Smith",
    kodePrincipal: "KP002",
    totalBayar: 800000,
    tanggalOrder: "2024-02-05",
    status: "Paid",
  },
  {
    notaOrder: "NO003",
    kodeCustomer: "789",
    namaCustomer: "Robert Johnson",
    kodePrincipal: "KP003",
    totalBayar: 2500000,
    tanggalOrder: "2024-02-10",
    status: "Pending",
  },
  {
    notaOrder: "NO004",
    kodeCustomer: "101",
    namaCustomer: "Emily Davis",
    kodePrincipal: "KP004",
    totalBayar: 1200000,
    tanggalOrder: "2024-02-15",
    status: "Paid",
  },
  {
    notaOrder: "NO005",
    kodeCustomer: "112",
    namaCustomer: "Michael Williams",
    kodePrincipal: "KP005",
    totalBayar: 500000,
    tanggalOrder: "2024-02-20",
    status: "Pending",
  },
];

export const vouchers = [
  {
    id: 1,
    namaVoucher: "DISCOUNT10",
    tipeDiskon: "Percentage",
    kuotaVoucher: "1000",
    tanggalBerlaku: "2024-02-01",
    tanggalBerakhir: "2024-02-28",
    promo: "Get 10% off",
    syaratDanKetentuan: "Valid for all products.",
    diskon1: 1,
    diskon2: 0,
    diskon3: 0,
  },
  {
    id: 2,
    namaVoucher: "FREEDELIVERY",
    tipeDiskon: "Free Delivery",
    kuotaVoucher: "500",
    tanggalBerlaku: "2024-03-01",
    tanggalBerakhir: "2024-03-31",
    promo: "Free delivery on orders over $50",
    syaratDanKetentuan: "Applicable to orders with a minimum value of $50.",
    diskon1: 0,
    diskon2: 2,
    diskon3: 0,
  },
  {
    id: 3,
    namaVoucher: "SALE20",
    tipeDiskon: "Fixed Amount",
    kuotaVoucher: "800",
    tanggalBerlaku: "2024-04-01",
    tanggalBerakhir: "2024-04-30",
    promo: "Save $20 on your purchase",
    syaratDanKetentuan: "Minimum purchase of $100 required.",
    diskon1: 0,
    diskon2: 0,
    diskon3: 3,
  },
  {
    id: 4,
    namaVoucher: "NEWUSER25",
    tipeDiskon: "Percentage",
    kuotaVoucher: "200",
    tanggalBerlaku: "2024-05-01",
    tanggalBerakhir: "2024-05-31",
    promo: "25% off for new users",
    syaratDanKetentuan: "Valid for first-time users only.",
    diskon1: 0,
    diskon2: 4,
    diskon3: 0,
  },
  {
    id: 5,
    namaVoucher: "LOYALTY15",
    tipeDiskon: "Percentage",
    kuotaVoucher: "300",
    tanggalBerlaku: "2024-06-01",
    tanggalBerakhir: "2024-06-30",
    promo: "15% off for loyal customers",
    syaratDanKetentuan: "Applicable to customers with more than 5 orders.",
    diskon1: 0,
    diskon2: 0,
    diskon3: 5,
  },
];

export const principalDatas = [
  {
    id: 1,
    no: 1,
    kodePrincipal: "KP001",
    namaPrincipal: "Principal A",
    status: "Sudah",
  },
  {
    id: 2,
    no: 2,
    kodePrincipal: "KP002",
    namaPrincipal: "Principal B",
    status: "Belum",
  },
  {
    id: 3,
    no: 3,
    kodePrincipal: "KP003",
    namaPrincipal: "Principal C",
    status: "Sudah",
  },
  {
    id: 4,
    no: 4,
    kodePrincipal: "KP004",
    namaPrincipal: "Principal D",
    status: "Sudah",
  },
  {
    id: 5,
    no: 5,
    kodePrincipal: "KP005",
    namaPrincipal: "Principal E",
    status: "Belum",
  },
];

export const listOrderDatas = [
  [
    {
      produk: "Product A",
      uom3: 10,
      uom2: 20,
      uom1: 30,
      harga: 1000,
      disc1: 5,
      disc2: 0,
      disc3: 0,
      totalDisc: 50,
      jumlahHarga: 950,
      voucher: "",
    },
    {
      produk: "Product B",
      uom3: 15,
      uom2: 25,
      uom1: 35,
      harga: 1500,
      disc1: 0,
      disc2: 10,
      disc3: 0,
      totalDisc: 150,
      jumlahHarga: 1350,
      voucher: "DISCOUNT10",
    },
    {
      produk: "Product C",
      uom3: 20,
      uom2: 30,
      uom1: 40,
      harga: 2000,
      disc1: 0,
      disc2: 0,
      disc3: 15,
      totalDisc: 300,
      jumlahHarga: 1700,
      voucher: "SALE20",
    },
    {
      produk: "Product D",
      uom3: 25,
      uom2: 35,
      uom1: 45,
      harga: 2500,
      disc1: 0,
      disc2: 0,
      disc3: 0,
      totalDisc: 0,
      jumlahHarga: 2500,
      voucher: "",
    },
    {
      produk: "Product E",
      uom3: 30,
      uom2: 40,
      uom1: 50,
      harga: 3000,
      disc1: 10,
      disc2: 5,
      disc3: 5,
      totalDisc: 400,
      jumlahHarga: 2600,
      voucher: "NEWUSER25",
    },
  ],
];

export const productList = [
  { name: "Product 1", id: 1, principleId: 1, harga: 10000 },
  { name: "Product 2", id: 2, principleId: 2, harga: 11000 },
  { name: "Product 3", id: 3, principleId: 3, harga: 12000 },
  { name: "Product 4", id: 4, principleId: 4, harga: 13000 },
  { name: "Product 5", id: 5, principleId: 5, harga: 14000 },
  { name: "Product 6", id: 6, principleId: 1, harga: 15000 },
  { name: "Product 7", id: 7, principleId: 2, harga: 16000 },
  { name: "Product 8", id: 8, principleId: 3, harga: 17000 },
  { name: "Product 9", id: 9, principleId: 4, harga: 18000 },
  { name: "Product 10", id: 10, principleId: 5, harga: 19000 },
  { name: "Product 11", id: 11, principleId: 1, harga: 20000 },
  { name: "Product 12", id: 12, principleId: 2, harga: 21000 },
  { name: "Product 13", id: 13, principleId: 3, harga: 22000 },
  { name: "Product 14", id: 14, principleId: 4, harga: 23000 },
  { name: "Product 15", id: 15, principleId: 5, harga: 24000 },
];

export const listFreeProductsData = [
  {
    no: 1,
    kodeVoucher: 1,
    deskripsiProduk: "Product A",
    jumlahProduk: 10,
    uom: "pcs",
    idProduk: 1,
  },
  {
    no: 2,
    kodeVoucher: 2,
    deskripsiProduk: "Product B",
    jumlahProduk: 5,
    uom: "pcs",
    idProduk: 2,
  },
  {
    no: 3,
    kodeVoucher: 3,
    deskripsiProduk: "Product C",
    jumlahProduk: 20,
    uom: "pcs",
    idProduk: 3,
  },
  {
    no: 4,
    kodeVoucher: 3,
    deskripsiProduk: "Product D",
    jumlahProduk: 8,
    uom: "pcs",
    idProduk: 3,
  },
  {
    no: 5,
    kodeVoucher: 4,
    deskripsiProduk: "Product E",
    jumlahProduk: 15,
    uom: "pcs",
    idProduk: 4,
  },
];

export const sisaPlafonData = [
  {
    namaPrincipal: "Principal A",
    sisaPlafon: 5000,
    piutang: 2000,
  },
  {
    namaPrincipal: "Principal B",
    sisaPlafon: 8000,
    piutang: 3500,
  },
  {
    namaPrincipal: "Principal C",
    sisaPlafon: 10000,
    piutang: 4000,
  },
];

export const listReturData = [
  {
    notaFaktur: "NF001",
    principalId: 1,
    produk: [
      {
        produkId: 1,
        name: "Product 1",
        uom3: 1,
        uom2: 1,
        uom1: 1,
        harga: 230000,
        jmlHarga: 2300,
        keteranganRetur: 227700,
      },
      {
        produkId: 11,
        name: "Product 11",
        uom3: 1,
        uom2: 1,
        uom1: 1,
        harga: 80000,
        jmlHarga: 14280,
        keteranganRetur: 225720,
      },
    ],
  },
  {
    notaFaktur: "NF002",
    principalId: 2,
    produk: [
      {
        produkId: 2,
        name: "Product 2",
        uom3: 1,
        uom2: 1,
        uom1: 1,
        harga: 80000,
        jmlHarga: 14280,
        keteranganRetur: 225720,
      },
      {
        produkId: 12,
        name: "Product 12",
        uom3: 1,
        uom2: 1,
        uom1: 1,
        harga: 230000,
        jmlHarga: 2300,
        keteranganRetur: 227700,
      },
    ],
  },
  {
    notaFaktur: "NF003",
    principalId: 3,
    produk: [
      {
        produkId: 3,
        name: "Product 3",
        uom3: 1,
        uom2: 1,
        uom1: 1,
        harga: 230000,
        jmlHarga: 2300,
        keteranganRetur: 227700,
      },
      {
        produkId: 13,
        name: "Product 13",
        uom3: 1,
        uom2: 1,
        uom1: 1,
        harga: 80000,
        jmlHarga: 14280,
        keteranganRetur: 225720,
      },
    ],
  },
  {
    notaFaktur: "NF004",
    principalId: 4,
    produk: [
      {
        produkId: 4,
        name: "Product 4",
        uom3: 1,
        uom2: 1,
        uom1: 1,
        harga: 80000,
        jmlHarga: 14280,
        keteranganRetur: 225720,
      },
      {
        produkId: 14,
        name: "Product 14",
        uom3: 1,
        uom2: 1,
        uom1: 1,
        harga: 230000,
        jmlHarga: 2300,
        keteranganRetur: 227700,
      },
    ],
  },
  {
    notaFaktur: "NF005",
    principalId: 5,
    produk: [
      {
        produkId: 5,
        name: "Product 5",
        uom3: 1,
        uom2: 1,
        uom1: 1,
        harga: 230000,
        jmlHarga: 2300,
        keteranganRetur: 227700,
      },
      {
        produkId: 15,
        name: "Product 15",
        uom3: 1,
        uom2: 1,
        uom1: 1,
        harga: 80000,
        jmlHarga: 14280,
        keteranganRetur: 225720,
      },
    ],
  },
];

export const dataDetailShipping = [
  {
      nama: 'john doe',
      uom3: 'uom3',
      uom2: 'uom2',
      uom1: 'uom1',
      harga: 'harga',
      disc1: 'disc1',
      disc2: 'disc2',
      disc3: 'disc3',
      total_discount: 'total_discount',
      total_harga: 'total_harga',
      voucher: 'voucher'
  },
  {
      nama: 'john doe',
      uom3: 'uom3',
      uom2: 'uom2',
      uom1: 'uom1',
      harga: 'harga',
      disc1: 'disc1',
      disc2: 'disc2',
      disc3: 'disc3',
      total_discount: 'total_discount',
      total_harga: 'total_harga',
      voucher: 'voucher'
  },
  {
      nama: 'john doe',
      uom3: 'uom3',
      uom2: 'uom2',
      uom1: 'uom1',
      harga: 'harga',
      disc1: 'disc1',
      disc2: 'disc2',
      disc3: 'disc3',
      total_discount: 'total_discount',
      total_harga: 'total_harga',
      voucher: 'voucher'
  },
 ]

 export const listFakturShippings = [
  {
    faktur: "NFS987654",
    rute: "Solo - Pedan - Juwiring",
    customer: "Toko Berkah",
    kubikal: "750"
  },
  {
    faktur: "NFS123456",
    rute: "Solo - Pedan - Karangdowo",
    customer: "Toko Merah",
    kubikal: "80"
  },
  {
    faktur: "NFS456852",
    rute: "Solo - Cawas - Pedan",
    customer: "Toko Barokah",
    kubikal: "125"
  },
 ]

 export const listPicking = [
  {
    id: 1,
    kode: "SDP",
    nama: "Solo - Delanggu - Pedan",
    total_toko: 4,
    total_nota: 7,
    kubikal: 80
  },
  {
    id: 2,
    kode: "SDP",
    nama: "Solo - Delanggu - Pedan",
    total_toko: 4,
    total_nota: 7,
    kubikal: 80
  },
  {
    id: 3,
    kode: "SDP",
    nama: "Solo - Delanggu - Pedan",
    total_toko: 4,
    total_nota: 7,
    kubikal: 80
  },
 ]
 export const listProductAddPicking = [
  {
    id: 1,
    product_name: "SariWangi",
    product_id: "AW5468D",
    satuan: "Pieces",
    total_order: '678',
    total_picked: "195",
    keterangan:{
      karton: 6,
      box: 4,
      pieces: 6
    }
  },
  {
    id: 2,
    product_name: "SariWangi",
    product_id: "AW5468D",
    satuan: "Pieces",
    total_order: '678',
    total_picked: "195",
    keterangan:{
      karton: 6,
      box: 4,
      pieces: 6
    }
  },
  {
    id: 3,
    product_name: "SariWangi",
    product_id: "AW5468D",
    satuan: "Pieces",
    total_order: '678',
    total_picked: "195",
    keterangan:{
      karton: 6,
      box: 4,
      pieces: 6
    }
  },
 ]

 export const listProductDetailPicking = [
  {
    id: 1,
    shop_name: 'Toko Pelangi',
    total_order: "195"
  },
  {
    id: 2,
    shop_name: 'Toko Pelangi',
    total_order: "195"
  },
  {
    id: 3,
    shop_name: 'Toko Pelangi',
    total_order: "195"
  },
 ]

 export const listRealisasi = [
  {
    id: 1,
    faktur: "NFS2135498",
    order_date: "04-12-2024",
    customer: "Toko A",
    cubical: "123",
  },
  {
    id: 2,
    faktur: "NFS548526",
    order_date: "04-12-2024",
    customer: "Toko B",
    cubical: "231",
  },
  {
    id: 3,
    faktur: "NFS982468",
    order_date: "04-12-2024",
    customer: "Toko C",
    cubical: "321",
  },
 ]
 export const listRealisasiDetail = [
  {
    id: 1,
    product_name: "SariWangi",
    product_id: "AW5468D",
    satuan: "Pieces",
    total_picking: "195",
    keterangan:{
      karton: 6,
      box: 4,
      pieces: 6
    }
  },
  {
    id: 2,
    product_name: "SariWangi",
    product_id: "AW5468D",
    satuan: "Pieces",
    total_picking: "195",
    keterangan:{
      karton: 6,
      box: 4,
      pieces: 6
    }
  },
  {
    id: 3,
    product_name: "SariWangi",
    product_id: "AW5468D",
    satuan: "Pieces",
    total_picking: "195",
    keterangan:{
      karton: 6,
      box: 4,
      pieces: 6
    }
  },
 ]
 export const listOrder = [
  {
    id: 1,
    nota_order: "1",
    tanggal_order: "4/12/2023",
    customer: "PT. Wings",
    kode_principal: "awd341",
    principal: "PT. Wings",
    status_picking: "Done",
  },
  {
    id: 2,
    nota_order: "1",
    tanggal_order: "4/12/2023",
    customer: "PT. Wings",
    kode_principal: "awd341",
    principal: "PT. Wings",
    status_picking: "On Process",
  },
  {
    id: 3,
    nota_order: "1",
    tanggal_order: "4/12/2023",
    customer: "PT. Wings",
    kode_principal: "awd341",
    principal: "PT. Wings",
    status_picking: "Done",
  },
 ]

 export const listRuteDanArmada = [
  {
    id: 1,
    kode: "SDP",
    nama: "Solo - Delanggu - Pedan",
    jumlah_toko: 4,
    jumlah_nota: 7,
    kubikal: 80,
    armada: "-"
  },
  {
    id: 2,
    kode: "SDP",
    nama: "Solo - Delanggu - Pedan",
    jumlah_toko: 4,
    jumlah_nota: 7,
    kubikal: 80,
    armada: "-"
  },
 ]
 export const listShipping = [
  {
    id: 1,
    route_code: "SDP",
    route: "Solo - Delanggu - Pedan",
    total_shop: "7",
    total_note: "12",
    cubic: "80",
    armada: "Armada 1",
    driver: "Driver 1"
  },
  {
    id: 2,
    route_code: "SWC",
    route: "Solo - Wonosari - Ceper",
    total_shop: "6",
    total_note: "10",
    cubic: "86",
    armada: "Armada 2",
    driver: "Driver 1"
  },
  {
    id: 3,
    route_code: "SJC",
    route: "Solo - Juwiring - Cawas",
    total_shop: "9",
    total_note: "11",
    cubic: "85",
    armada: "Armada 3",
    driver: "Driver 1"
  },
 ]
 export const listHistoryDistribusi = [
  {
    id: 1,
    route_code: "SDP",
    route: "Solo - Delanggu - Pedan",
    prioritas: "4",
    kubikasi: "7",
    total_shop: "7",
    total_note: "12",
    nota_gagal: "0",
    status: "Terkirim"

  },
  {
    id: 2,
    route_code: "SWC",
    route: "Solo - Wonosari - Ceper",
    total_shop: "6",
    prioritas: "4",
    kubikasi: "7",
    total_shop: "8",
    total_note: "18",
    nota_gagal: "0",
    status: "Proses"

  },
  {
    id: 3,
    route_code: "SJC",
    route: "Solo - Juwiring - Cawas",
    prioritas: "4",
    kubikasi: "7",
    total_shop: "8",
    total_note: "18",
    nota_gagal: "0",
    status: "Gagal"

  },
]
  export const listDetailDistribusiHistory = [
    {
      id: 1,
      faktur: "NFS97898",
      nama_toko: "Toko Berkah",
      kubikasi: "72",
      keterangan: "-",
    },
    {
      id: 2,
      faktur: "NFS97866",
      nama_toko: "Toko Damai",
      kubikasi: "80",
      keterangan: "-",
    },
 ]
