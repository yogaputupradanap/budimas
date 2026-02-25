<script setup>
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import FormVoucher from "@/src/components/FormVoucher.vue";
import FlexBox from "@/src/components/ui/FlexBox.vue";
</script>

<template>
  <FlexBox full flex-col>
    <SlideRightX
      class="slide-container tw-justify-end"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <FormVoucher />
    </SlideRightX>
  </FlexBox>
</template>
