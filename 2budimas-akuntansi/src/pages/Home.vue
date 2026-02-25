<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import FlexBox from "../components/ui/FlexBox.vue";
import CardTextIcon from "../components/ui/CardTextIcon.vue";
import {useUser} from "../store/user";
import {computed} from "vue";
import {useRouter} from "vue-router";
import {logout} from "../lib/utils";

const userStore = useUser();
const router = useRouter();

const cardIcons = [
  {
    icon: "mdi-clipboard-file",
    text: "Jurnal",
    url: "jurnal",
  },
  // {
  //   icon: "mdi-file-document",
  //   text: "Surat Tagihan Sales",
  //   url: "surat-tagihan-sales",
  // },
  {
    text: "Setoran Tunai",
    url: "setoran-tunai",
    icon: "mdi-cash",
  },
  {
    icon: "mdi-credit-card",
    text: "Setoran Non Tunai",
    url: "setoran-non-tunai",
  },
  {
    icon: "mdi-clipboard-check",
    text: "Hutang",
    url: "tagihan-purchasing",
  },
  {
    icon: "mdi-cash-multiple",
    text: "Pengeluaran Kasir",
    url: "pengeluaran-kasir",
  },
  {
    icon: "mdi-clipboard-text",
    text: "Laporan Kasir",
    url: "laporan-kasir",
  },
  {
    icon: "mdi-file-document",
    text: "LPH",
    url: "lph",
  },
  {
    icon: "mdi-logout",
    text: "Logout",
    url: "logout",
  },
  {
    text: "Transaksi",
    url: "transaksi",
    icon: "mdi-clipboard-check-outline",
  },
  {
    icon: "mdi-clipboard-check-outline",
    text: "Mutasi",
    url: "mutasi",
  },
  {
    text: "COA",
    url: "coa",
    icon: "mdi-account-check-outline"
  },
  {
    text: "Jurnal Setting",
    url: "journal-setting",
    icon: "mdi-cog-outline"
  },
  {
    text: "Buku Besar",
    url: "buku-besar",
    icon: "mdi-cog-outline"
  }
];

const userAccessCard = computed(() => {
  console.log("===== DEBUG MENU =====");
  console.log("userStore.userAccess:", userStore.userAccess);
  console.log("cardIcons:", cardIcons);

  if (!Array.isArray(userStore.userAccess)) {
    console.warn("userAccess bukan array");
    return [];
  }

  const mapped = userStore.userAccess.map((val) => {
    // console.log("mapping akses:", val);

    const found = cardIcons.find((i) => i.url === val.name);

    // console.log("found icon:", found);

    return found || null;
  });

  // console.log("mapped result:", mapped);

  return mapped.filter(Boolean);
});
</script>

<template>
  <FlexBox full flex-col h-full>
    <SlideRightX
        class="tw-w-full tw-flex tw-flex-wrap lg:tw-justify-start tw-gap-4 tw-rounded-2xl"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.1"
        :delay-out="0.1"
        :initial-x="-40"
        :x="40">
      <SlideRightX
          v-for="(card, index) in userAccessCard"
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
            :url="`/${card?.url}`"
            :active="card?.active"/>
      </SlideRightX>
    </SlideRightX>
  </FlexBox>
</template>
