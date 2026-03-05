<script setup>
import FlexBox from "../components/ui/FlexBox.vue";
import CardTextIcon from "../components/ui/CardTextIcon.vue";
import Card from "../components/ui/Card.vue";
import Table from "../components/ui/table/Table.vue";
import { principalColumns } from "../model/tableColumns";
import { principalDatas } from "../lib/dummydatas";
import SlideRightX from "../components/animation/SlideRightX.vue";
import Information from "../components/ui/Information.vue";

const kunjunganInformations = [
  {
    buttonColor: "tw-bg-green-500",
    buttonText: "Done",
    buttonTextColor: "tw-text-white",
    information: "Status sudah check in principal",
  },
  {
    buttonColor: "tw-bg-blue-500",
    buttonText: "To Do",
    buttonTextColor: "tw-text-white",
    information: "Status Sedang check in principal",
  },
  {
    buttonColor: "tw-bg-gray-300",
    buttonText: "Check In",
    information: "Status Belum check in principal",
  },
];
</script>

<template>
  <FlexBox full flex-col class="lg:tw-pl-6 tw-pl-1">
    <SlideRightX
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40"
    >
      <RouterLink to="/check-out">
        <CardTextIcon
          icon="mdi mdi-logout-variant"
          text="Check Out"
          :style="[
            { backgroundColor: '#BD2727', color: 'white', width: '200px' },
          ]"
        />
      </RouterLink>
    </SlideRightX>
    <SlideRightX
      class="tw-w-full"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40"
    >
      <Card no-subheader>
        <template #header>
          <span class="tw-capitalize">daftar principal</span>
        </template>
        <template #content>
          <Table :columns="principalColumns" :table-data="principalDatas" />
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="tw-w-full tw-bg-white tw-rounded-xl"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.3"
      :delay-out="0.3"
      :initial-x="-40"
      :x="40"
    >
      <Information :informations="kunjunganInformations" />
    </SlideRightX>
  </FlexBox>
</template>
