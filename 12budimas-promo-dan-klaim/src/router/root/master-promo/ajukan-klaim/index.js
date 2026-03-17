import AjukanKlaim from "@/src/pages/master-promo/ajukan-klaim/AjukanKlaim.vue"

const children = [
    {
        path: "",
        name: "Ajukan Klaim",
        component: AjukanKlaim,
        props: true
    }
]

export const ajukanKlaim = [
    {
        path: "ajukan-klaim/:kode_promo",
        children
    }
]