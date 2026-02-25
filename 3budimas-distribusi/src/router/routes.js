import {root} from "./root";
import {summaryReport} from "./root/dashboard/summaryReport";
import {listOrder} from "./root/order/summaryOrder";
import {ListShippings} from "./root/shipping";
import {realitations} from "./root/realisasi";
import {fakturShipping} from "./root/shipping/fakturShipping";
import {detailShipping} from "./root/shipping/fakturShipping/detailShipping";
import {detailPickings} from "./root/picking/addPicking/detailPicking";
import {addPickings} from "./root/picking/addPicking";
import {pickings} from "./root/picking";
import {realisasiDetail} from "./root/realisasi/fakturRealisasi/realisasiDetail";
import {fakturRealisasiRoutes} from "./root/realisasi/fakturRealisasi"; // Updated import
import {distrbutionHistory} from "./root/distribusi/history";
import {detailDistrbutionHistory} from "./root/distribusi/history/detail";
import {driver} from "./root/driver/index";
import {addDriver} from "./root/driver/addDriver/index";
import {updateDriver} from "./root/driver/updateDriver/index";
import {konfirmasiOrder} from "./root/konfirmasi-order";
import {detailKonfirmasiOrder} from "./root/konfirmasi-order/detail";
import {detailKonfirmasiVoucher} from "./root/konfirmasi-order/detail/voucher";
import {detailKonfirmasiVoucherRegular} from "./root/konfirmasi-order/detail/verifikasi-voucher-regular";
import {Loginn} from "./root/login";
import {jadwalDanRute} from "./root/jadwal/armada";
import {pilihArmada} from "./root/jadwal/armada/pilih-armada";
import {jadwal} from "./root/jadwal";
import {revisiFaktur} from "./root/revisi-faktur";
import {listFakturRoutes} from "./root/revisi-faktur/listfaktur";
import {DetailRevisiFakturRoutes} from "./root/revisi-faktur/listfaktur/detailRevisiFaktur";
import {ReturRoutes} from "@/src/router/root/retur";

export const routes = root.concat(
    summaryReport,
    listOrder,
    ListShippings,
    realitations,
    jadwal,
    jadwalDanRute,
    pilihArmada,
    detailShipping,
    fakturShipping,
    detailPickings,
    addPickings,
    pickings,
    fakturRealisasiRoutes, // Updated usage
    realisasiDetail,
    distrbutionHistory,
    detailDistrbutionHistory,
    Loginn,
    driver,
    addDriver,
    updateDriver,
    konfirmasiOrder,
    detailKonfirmasiOrder,
    detailKonfirmasiVoucher,
    detailKonfirmasiVoucherRegular,
    revisiFaktur,
    listFakturRoutes,
    DetailRevisiFakturRoutes,
    ReturRoutes
);
