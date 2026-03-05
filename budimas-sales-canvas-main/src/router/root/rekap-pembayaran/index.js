import PembayaranRekap from "@/src/pages/rekap-pembayaran";

const children = [
  {
    path: "", name: "Rekap Pembayaran", component: PembayaranRekap
  }
]

export const rekapPembayaranRoute = [
  {
    path: "/rekap-pembayaran", 
    children
  },
];