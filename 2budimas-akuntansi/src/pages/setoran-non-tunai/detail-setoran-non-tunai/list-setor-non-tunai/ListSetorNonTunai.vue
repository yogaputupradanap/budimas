<script setup>
import FlexBox from "@/src/components/ui/FlexBox.vue";
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import Card from "@/src/components/ui/Card.vue";
import Button from "@/src/components/ui/Button.vue";
import Table from "@/src/components/ui/table/Table.vue";
import { listSetorTunaiColumn } from "@/src/model/tableColumns/setoran-tunai/listSetorTunai";
import { listSetorTunaiDummy } from "@/src/lib/dummydatas";
import Label from "@/src/components/ui/Label.vue";
</script>

<template>
  <FlexBox full flex-col>
    <SlideRightX
      class="slide-container tw-z-10"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card no-subheader>
        <template #header>Detail Transfer</template>
        <template #content>
          <div class="form-grid-card">
            <Label label="Total Setoran">
              <BFormInput
                model-value="Rp. 24.000.000"
                disabled
                placeholder="Total Setoran" />
            </Label>
            <Label label="Total Tagihan">
              <BFormInput
                model-value="Rp. 24.000.000"
                disabled
                placeholder="Total Tagihan" />
            </Label>
            <Label label="Saldo">
              <BFormInput
                model-value="Rp. 24.000.000"
                disabled
                placeholder="Total Tagihan" />
            </Label>
            <Label label="Jumlah Faktur">
              <BFormInput model-value="2" disabled placeholder="Faktu" />
            </Label>
          </div>
          <FlexBox full class="tw-mt-8">
            <Table
              :columns="listSetorTunaiColumn"
              :table-data="listSetorTunaiDummy" />
          </FlexBox>
          <FlexBox full jus-end>
            <Button icon="mdi mdi-close" class="tw-bg-red-500 tw-px-4 tw-h-[34px]">Tolak</Button>
            <Button icon="mdi mdi-check" class="tw-bg-green-500 tw-px-4 tw-h-[34px]">Submit</Button>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
