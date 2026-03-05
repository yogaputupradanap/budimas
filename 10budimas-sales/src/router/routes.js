import { root } from "./root";
import { summaryReport } from "./root/dashboard/summaryReport";
import { Loginn } from "./root/login";
import { daftarKunjunganToko } from "./root/kunjungan/daftarKunjunganToko";
import { dashboardMenu } from "./root/kunjungan/daftarKunjunganToko/dashboardMenu";
import { history } from "./root/history";
import { pembayaran } from "./root/kunjungan/daftarKunjunganToko/dashboardMenu/pembayaran";
import { salesRequest } from "./root/kunjungan/daftarKunjunganToko/dashboardMenu/salesRequest";
import { StockOpnamee } from "./root/kunjungan/daftarKunjunganToko/dashboardMenu/stockOpname";
import { voucher } from "./root/kunjungan/daftarKunjunganToko/dashboardMenu/voucher";
import { detailPembayaran } from "./root/kunjungan/daftarKunjunganToko/dashboardMenu/pembayaran/detailPembayaran";
import { salesRetur } from "./root/kunjungan/daftarKunjunganToko/dashboardMenu/salesRetur";
import { rekapPembayaran } from "./root/rekap-pembayaran";

export const routes = root.concat(
  summaryReport,
  Loginn,
  daftarKunjunganToko,
  dashboardMenu,
  history,
  pembayaran,
  salesRequest,
  StockOpnamee,
  voucher,
  detailPembayaran,
  salesRetur,
  rekapPembayaran
);
