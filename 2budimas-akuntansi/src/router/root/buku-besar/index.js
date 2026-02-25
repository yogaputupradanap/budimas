// Di file router Anda
export const bukubesar = [
    {
        path: "/buku-besar",
        name: "Buku Besar",
        // Tambahkan webpackChunkName seperti di bawah ini
        component: () => import(/* webpackChunkName: "halaman-bukubesar" */ "@/src/pages/buku-besar/buku-besar.vue"),
    },
]