<script setup>
import Card from "../components/ui/Card.vue";
import Information from "../components/ui/Information.vue";
import { listPembayarandata } from "../lib/dummydatas";
import { ListPembayaranColumn } from "../model/tableColumns";
import Table from "../components/ui/table/Table.vue";
import SlideRightX from "../components/animation/SlideRightX.vue";
import FlexBox from "../components/ui/FlexBox.vue";

const KunjunganTokoInformations = [
  {
    buttonColor: "tw-bg-blue-500",
    buttonText: "Bayar",
    buttonTextColor: "tw-text-white",
    information: "Status Lunas",
  },
  {
    buttonColor: "tw-bg-gray-300",
    buttonText: "Bayar",
    information: "Status Belum Lunas",
  },
];
</script>

<template>
  <FlexBox flex-col class="tw-pl-6">
    <SlideRightX
      class="tw-w-full tw-bg-white tw-rounded-lg tw-shadow-lg"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40"
    >
      <Card>
        <template #header>List Pembayaran</template>
        <template #subheader>Silahkan cek pembayaran terlebih dahulu</template>
        <template #content>
          <Table
            :columns="ListPembayaranColumn"
            :table-data="listPembayarandata"
          />
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="tw-bg-white tw-rounded-lg tw-shadow-lg tw-w-full"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.3"
      :delay-out="0.3"
      :initial-x="-40"
      :x="40"
    >
      <Information :informations="KunjunganTokoInformations" />
    </SlideRightX>
  </FlexBox>
</template>
