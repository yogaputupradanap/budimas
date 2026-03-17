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
    text: "Master Promo",
    url: "master-promo",
    icon: "mdi-ticket-percent",
  },
  {
    text: "Log Penggunaan Promo",
    url: "log-penggunaan-promo",
    icon: "mdi-history",
  },
  {
    text: "List Klaim Promo",
    url: "klaim-promo",
    icon: "mdi-clipboard-list",
  },
  {
    text: "Kasbon Klaim",
    url: "kasbon-klaim",
    icon: "mdi-cash-edit",
  },
  {
    icon: "mdi-logout",
    text: "Logout",
    url: "logout",
  },
];

const userAccessCard = computed(() => {
  return userStore.userAccess.map((val) => {
    return { ...cardIcons.find((i) => i["url"] === val["name"]) };
  });

  arr.push({
    icon: "mdi-logout",
    text: "Logout",
    url: "logout",
  });

  return arr;
});

const handleLogout = () => {
  localStorage.removeItem("user");
  localStorage.removeItem("hakakses");
  userStore.$reset(); // Reset store jika menggunakan Pinia

  // Redirect ke halaman login
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
          @click="card?.text === 'Logout' ? logout() : null"
        />
      </SlideRightX>
    </SlideRightX>
  </FlexBox>
</template>
