<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import CardTextIcon from "../components/ui/CardTextIcon.vue";
import CheckoutCard from "../components/ui/CheckoutCard.vue";
import { useRoute, useRouter } from "vue-router";
import FlexBox from "../components/ui/FlexBox.vue";
import { useKunjungan } from "../store/kunjungan";
import { useDashboard } from "../store/dashboard";
import { computed, onMounted, ref } from "vue";

// global states
const kunjungan = useKunjungan();
const dashboard = useDashboard();

const router = useRouter();
const route = useRoute();
const statusParam = route.query.status;
const loading = ref(false);

const checkoutButtonActive = computed(() => statusParam !== "2");

const handleCheckout = async () => {
  if (!checkoutButtonActive.value) return;

  loading.value = true;
  await kunjungan.checkInOutKunjungan(
    kunjungan.activeKunjungan.kunjungan.id,
    2
  );
  loading.value = false;
  return router.back();
};

const cardicons = [
  {
    icon: "mdi-account-key",
    text: "Stock Opname",
    url: "/kunjungan/daftar-kunjungan-toko/dashboard-menu-kunjungan-toko/daftar-barang-principal",
    trigger: async () => {
      // Set active untuk pembayaran dan sales request
      dashboard.setActiveButton("pembayaran", true);
      return router.push(
        "/kunjungan/daftar-kunjungan-toko/dashboard-menu-kunjungan-toko/daftar-barang-principal"
      );
    },
  },
  {
    icon: "mdi-currency-usd",
    text: "Pembayaran",
    url: "/kunjungan/daftar-kunjungan-toko/dashboard-menu-kunjungan-toko/pembayaran",
    active: dashboard.getActiveButton("pembayaran"),
    trigger: async () => {
      // Set active untuk stock opname dan sales request
      dashboard.setActiveButton("sales request", true);
      return router.push(
        "/kunjungan/daftar-kunjungan-toko/dashboard-menu-kunjungan-toko/pembayaran"
      );
    },
  },
  {
    icon: "mdi-clipboard-text",
    text: "Sales Request",
    url: "/kunjungan/daftar-kunjungan-toko/dashboard-menu-kunjungan-toko/sales-request",
    active:
      typeof dashboard.getActiveButton("sales request") === "object"
        ? dashboard.getActiveButton("sales request")["value"]
        : dashboard.getActiveButton("sales request"),
  },
  {
    icon: "mdi-ticket-percent",
    text: "Voucher",
    url: "/kunjungan/daftar-kunjungan-toko/dashboard-menu-kunjungan-toko/voucher",
  },
  {
    icon: "mdi-sync",
    text: "Sales Retur",
    url: "/kunjungan/daftar-kunjungan-toko/dashboard-menu-kunjungan-toko/sales-retur",
  },
];

onMounted(() => {
  console.log(
    "active buttton sales request : ",
    dashboard.getActiveButton("sales request")
  );
});
</script>

<template>
  <FlexBox full flex-col gap="large" class="tw-pl-4 md:tw-h-[75vh] tw-h-auto">
    <SlideRightX
      class="tw-w-full tw-flex tw-flex-wrap lg:tw-justify-start tw-gap-4 tw-rounded-2xl"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <SlideRightX
        v-for="(card, index) in cardicons"
        class="tw-w-full lg:tw-w-auto"
        :key="card?.icon"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.1 * (0.3 * (index + 1))"
        :delay-out="0.1 * (0.3 * (index + 1))"
        :initial-x="-40"
        :x="40">
        <CardTextIcon
          :icon="card?.icon"
          :text="card?.text"
          :trigger="card?.trigger"
          :replace-url="card?.replaceUrl"
          :url="card?.url"
          :active="card?.active" />
      </SlideRightX>

      <SlideRightX
        class="tw-w-full lg:tw-w-auto"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.1 * (0.3 * (cardicons.length + 1))"
        :delay-out="0.1 * (0.3 * (cardicons.length + 1))"
        :initial-x="-40"
        :x="40">
        <CheckoutCard
          icon="mdi-logout-variant"
          text="Check Out"
          :active="checkoutButtonActive"
          :trigger="handleCheckout"
          replaceUrl="/kunjungan/daftar-kunjungan-toko" />
      </SlideRightX>
    </SlideRightX>
  </FlexBox>
</template>
