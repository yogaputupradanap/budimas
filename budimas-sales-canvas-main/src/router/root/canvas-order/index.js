import CanvasOrder from "@/src/pages/canvas-order";
import { detailCanvasOrderRoute } from "@/src/router/root/canvas-order/detail";
import { tagihanPembayaranRoute } from "@/src/router/root/canvas-order/pembayaran";
import { listVoucherRoute } from "@/src/router/root/canvas-order/vouchers";
import { addCanvasOrderRoute } from "@/src/router/root/canvas-order/create";

export const canvasOrderRoute = [
  {
    path: "/canvas-order",
    children: [
      addCanvasOrderRoute,
      listVoucherRoute,
      detailCanvasOrderRoute,
      tagihanPembayaranRoute,
      {
        path: "",
        name: "Canvas Order",
        component: CanvasOrder,
      },
    ],
  },
];
