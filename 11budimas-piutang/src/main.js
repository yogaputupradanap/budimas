import { createApp } from "vue";
import { createPinia } from "pinia";
import router from "./router/index";
import App from "./App.vue";
import VWave from "v-wave";

// 1. Impor komponen FlexBox kamu
import FlexBox from "./components/ui/FlexBox.vue"; 

const app = createApp(App);

import { BootstrapVueNext } from "bootstrap-vue-next";
import "bootstrap-styles/css/bootstrap.css";
import "bootstrap-vue-next/dist/bootstrap-vue-next.css";
import "./style/css/custom.css";
import "./index.css";
import "@vuepic/vue-datepicker/dist/main.css";

app.use(createPinia());
app.use(router);
app.use(BootstrapVueNext);
app.use(VWave);

// 2. Daftarkan secara global
app.component("FlexBox", FlexBox);

app.mount("#app");