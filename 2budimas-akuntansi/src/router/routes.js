import {root} from "./root";
import {Loginn} from "./root/login";
import {dashboard} from "./root/dashboard";
import {listJurnal} from "./root/jurnal";
import {listTagihanSales} from "./root/surat-tagihan-sales";
import {listSetoranTunai} from "./root/setoran-tunai";
import {listSetoranNonTunai} from "./root/setoran-non-tunai";
import {listTagihanPurchasing} from "./root/tagihan-purchasing";
import {listPengeluaranKasir} from "./root/pengeluaran-kasir";
import {listLaporanKasir} from "./root/laporan-kasir";
import {lph} from "./root/lph";
import {mutasi} from "@/src/router/root/mutasi";
import {transaksi} from "@/src/router/root/transaksi";
import {coa} from "@/src/router/root/coa";
import {jurnalSetting} from "@/src/router/root/jurnal-setting";
import { bukubesar } from "@/src/router/root/buku-besar";  

export const routes = root.concat(
    dashboard,
    Loginn,
    listJurnal,
    listTagihanSales,
    listSetoranTunai,
    listSetoranNonTunai,
    listTagihanPurchasing,
    listPengeluaranKasir,
    listLaporanKasir,
    lph,
    mutasi,
    transaksi,
    coa,
    jurnalSetting,
    bukubesar
);