import canvasRequest from "@/src/pages/canvas-request";
import AddCanvasRequest from "@/src/pages/canvas-request/add/AddCanvasRequest.vue";
import DetailCanvasRequest from "@/src/pages/canvas-request/detail";

const children = [
  {
    path: "", 
    name: "Canvas Request", 
    component: canvasRequest
  },
  {
    path: "add-request", 
    name: "Tambah Canvas Request", 
    component: AddCanvasRequest
  },
  {
    path: ":id", 
    name: "Detail Canvas Request", 
    component: DetailCanvasRequest
  }
];

export const canvasRequestRoute = [
  {
    path: "/canvas-request", children
  },
];