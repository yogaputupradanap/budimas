<script setup>
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Vouchers from "@/src/components/Vouchers.vue";
import { listVoucher } from "@/src/model/tableColumns/voucher/listVoucher";
import { voucherDummy } from "@/src/lib/dummydatas";
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
      <Vouchers tipe-voucher="2" :data="voucherDummy" :column="listVoucher" />
    </SlideRightX>
  </FlexBox>
</template>
