import AddStockOpname from "@/src/pages/stock-opname/AddStockOpname.vue";
import DetailStockOpname from "@/src/pages/stock-opname/DetailStockOpname.vue";
import ListStockOpname from "@/src/pages/stock-opname/ListStockOpname.vue";


export const stockOpname = [
    {
        path: "/stock-opname",
        name: "Stock Opname",
        component: ListStockOpname,
    },
    {
        path: "/stock-opname/detail-stock-opname/:id",
        name: "Stock Opname ",
        component: DetailStockOpname
    },
    {
        path: "/stock-opname/add-stock-opname",
        name: "Stock Opname  ",
        component: AddStockOpname
    }
]