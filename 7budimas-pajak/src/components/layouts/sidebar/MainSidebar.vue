<script setup>
import { watch } from "vue";
import { isMinimize } from "../../../lib/useSideBar";
import MobileSidebar from "./MobileSidebar.vue";
import { enableAnimations } from "../../../lib/settings";
import DesktopSidebar from "./DesktopSidebar.vue";
import anime from "animejs";

watch(isMinimize, () => {
  if (isMinimize.value) {
    anime.set("#sidebar", { width: "288px" });
    anime.set("#navButt", { width: "100%" });

    anime
      .timeline({
        easing: "easeOutExpo",
        duration: !enableAnimations ? 0 : 300,
      })
      .add({
        targets: "#navButtText",
        opacity: 0,
        translateX: 100,
        duration: !enableAnimations ? 0 : 300,
      })
      .add(
        {
          targets: "#navButt",
          width: "45%",
          duration: !enableAnimations ? 0 : 400,
        },
        "-=150"
        // "<0.1"
      )
      .add(
        {
          targets: "#navButtIcon",
          translateX: "10%",
          scale: 1.1,
          duration: !enableAnimations ? 0 : 300,
        },
        "-=100"
        // "<"
      )
      .add(
        {
          targets: "#sidebar",
          width: "86px",
          duration: !enableAnimations ? 0 : 300,
        },
        "-=200"
        // "<0.2"
      )
      .add(
        {
          targets: "#sideNavLogo",
          translateX: "40%",
          scale: 2,
          duration: !enableAnimations ? 0 : 300,
        },
        "-=300"
        // "<0"
      )
      .add(
        {
          targets: "#sideNavTextLogo",
          opacity: 0,
          duration: !enableAnimations ? 0 : 300,
        },
        "-=400"
        // "<0"
      );
  } else {
    anime.set("#navButt", { width: "35%" });
    anime
      .timeline({
        easing: "easeOutExpo",
        duration: !enableAnimations ? 0 : 300,
      })
      .add({
        targets: "#sidebar",
        width: "288px",
        duration: !enableAnimations ? 0 : 300,
      })
      .add(
        {
          targets: "#navButt",
          width: "100%",
          duration: !enableAnimations ? 0 : 400,
        },
        "-=100"
      )
      .add(
        {
          targets: "#sideNavLogo",
          translateX: "0%",
          scale: 1,
          duration: !enableAnimations ? 0 : 400,
        },
        "-=300"
      )
      .add(
        {
          targets: "#sideNavTextLogo",
          opacity: 1,
          duration: !enableAnimations ? 0 : 300,
        },
        "-=300"
      )
      .add(
        {
          targets: "#navButtIcon",
          translateX: "0%",
          scale: 1,
          duration: !enableAnimations ? 0 : 300,
        },
        "-=0"
      )
      .add(
        {
          targets: "#navButtText",
          opacity: 1,
          translateX: 0,
          duration: !enableAnimations ? 0 : 300,
        },
        "-=650"
      );
  }
});
</script>

<template>
  <MobileSidebar />
  <DesktopSidebar />
</template>
