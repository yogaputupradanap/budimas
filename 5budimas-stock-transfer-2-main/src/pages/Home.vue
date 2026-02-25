<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import FlexBox from "../components/ui/FlexBox.vue";
import CardTextIcon from "../components/ui/CardTextIcon.vue";
import { useUser } from "../store/user";
import { computed } from "vue";

const userStore = useUser();
const cardIcons = [
  {
    icon: "mdi-view-dashboard",
    text: "Stock Transfer",
    url: "stock-transfer",
  },
  {
    icon: "mdi-checkbox-marked",
    text: "Konfirmasi",
    url: "konfirmasi",
  },
  {
    icon: "mdi-truck-delivery",
    text: "Pengiriman",
    url: "pengiriman",
  },
  {
    icon: "mdi-package-variant",
    text: "Status Pengiriman",
    url: "status-pengiriman",
  },
  {
    icon: "mdi-dolly",
    text: "Penerimaan Barang",
    url: "penerimaan-barang",
  },
  {
    icon: "mdi-list-box",
    text: "List Eskalasi",
    url: "list-eskalasi",
  },
];

const userAccessCard = computed(() => {
  return userStore.userAccess.map((val) => {
    return { ...cardIcons.find((i) => i["url"] === val["name"]) };
  });
});
</script>

<template>
  <FlexBox full flex-col h-full>
    <SlideRightX
      class="tw-w-full tw-grid tw-grid-cols-1 lg:tw-grid-cols-2 xl:tw-grid-cols-4 2xl:tw-grid-cols-5 lg:tw-justify-start tw-gap-4 tw-rounded-2xl"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <SlideRightX
        v-for="(card, index) in userAccessCard"
        :key="card?.icon"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.1 * (0.3 * (index + 1))"
        :delay-out="0.1 * (0.3 * (index + 1))"
        :initial-x="-40"
        :x="40">
        <CardTextIcon
          full
          :icon="card?.icon"
          :text="card?.text"
          :trigger="card?.trigger"
          :replace-url="card?.replaceUrl"
          :url="`/${card?.url}`"
          :active="card?.active" />
      </SlideRightX>
    </SlideRightX>
  </FlexBox>
</template>
