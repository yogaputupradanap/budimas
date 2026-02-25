<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import FlexBox from "../components/ui/FlexBox.vue";
import CardTextIcon from "../components/ui/CardTextIcon.vue";
import { useUser } from "../store/user";
import { computed, watchEffect } from "vue";

const userStore = useUser();

const buttons = [
  {
    icon: "mdi-file-excel",
    title: "Import CSV",
    route: "import-csv",
  },
  {
    icon: "mdi-view-dashboard",
    title: "Stock Transfer",
    route: "stock-transfer",
  },
];

// watchEffect(() => {
//   console.log("===== DEBUG ACCESS =====");
//   console.log("userAccess:", userStore.userAccess);
//   console.log("USER ACCESS:", userStore.userAccess);

// });

const userAccessButtons = computed(() => {
  if (!userStore.userAccess?.length) {
    return [
      {
        title: "Dashboard",
        route: "dashboard",
        icon: "mdi-view-dashboard",
      },
      ...buttons,
    ];
  }

  return userStore.userAccess
    .map((val) => buttons.find((i) => i.route === val.name))
    .filter(Boolean);
});
</script>


<template>
  <FlexBox full flex-col h-full>
    <SlideRightX
      class="tw-w-full tw-grid tw-grid-cols-1 lg:tw-grid-cols-2 xl:tw-grid-cols-4 2xl:tw-grid-cols-5 tw-gap-4 tw-rounded-2xl"
    >
      <SlideRightX
        v-for="(card, index) in userAccessButtons"
        :key="index"
      >
        <CardTextIcon
          full
          :icon="card?.icon"
          :text="card?.title"
          :url="`/${card?.route}`"
        />
      </SlideRightX>
    </SlideRightX>
  </FlexBox>
</template>
