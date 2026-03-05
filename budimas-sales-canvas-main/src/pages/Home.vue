<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import FlexBox from "../components/ui/FlexBox.vue";
import CardTextIcon from "../components/ui/CardTextIcon.vue";
import { useUser } from "../store/user";
import { computed } from "vue";
import { useRouter } from "vue-router";
import { logout } from "../lib/utils";

const userStore = useUser();
const router = useRouter();

const cardIcons = [
  {
    text: "Canvas Request",
    url: "canvas-request",
    icon: "mdi-account-check",
  },
  {
    text: "Canvas Order",
    url: "canvas-order",
    icon: "mdi-clipboard-list",
  },
  {
    text: "Rekap Pembayaran",
    url: "rekap-pembayaran",
    icon: "mdi-clipboard-list",
  },
  {
    icon: "mdi-logout",
    text: "Logout",
    url: "logout",
  },
];

const userAccessCard = computed(() => {
  return cardIcons.filter((card) => {
    if (card.text === "Logout") return true;
    return userStore.hasAccess(card.url);
  })
});

const handleLogout = () => {
  logout();
  userStore.$reset();
  router.push("/login");
};
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
      :x="40"
    >
      <SlideRightX
        v-for="(card, index) in userAccessCard"
        class="tw-w-full lg:tw-w-auto"
        :key="card?.icon"
        :duration-enter="0.6"
        :duration-leave="0.6"
        :delay-in="0.1 * (0.3 * (index + 1))"
        :delay-out="0.1 * (0.3 * (index + 1))"
        :initial-x="-40"
        :x="40"
      >
        <CardTextIcon
          :icon="card?.icon"
          :text="card?.text"
          :trigger="card?.trigger"
          :replace-url="card?.replaceUrl"
          :url="`/${card?.url}`"
          :active="card?.active"
          :class="card?.text === 'Logout' ? 'tw-bg-red-500 tw-text-white' : ''"
          @click="card?.text === 'Logout' ? handleLogout() : null"
        />
      </SlideRightX>
    </SlideRightX>
  </FlexBox>
</template>
