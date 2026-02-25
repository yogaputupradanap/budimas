export const jurnalSetting = [
    {
        path: "/journal-setting",
        name: "journal Setting ",
        component: () => import("@/src/pages/jurnal-setting/ListJurnalSetting.vue"),
    },
    {
        path: "/journal-setting/add",
        name: "journal Setting  ",
        component: () => import("@/src/pages/jurnal-setting/AddJurnalSetting.vue"),
    }, {
        path: "/journal-setting/edit/:id",
        name: "journal Setting   ",
        component: () => import("@/src/pages/jurnal-setting/EditJurnalSetting.vue"),
    },
]