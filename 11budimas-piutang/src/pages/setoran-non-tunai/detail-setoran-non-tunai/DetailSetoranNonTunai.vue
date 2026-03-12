<script setup>
import { ref } from 'vue';

const loadingData = ref()
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
        <template #header>Informasi Piutang</template>
        <template #content>
          <div class="form-grid-card">
            <Label label="Nama Sales">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                model-value=""
                disabled />
            </Label>
            <Label label="Jumlah Customer">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                model-value=""
                disabled />
            </Label>
            <Label label="Total Setoran">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                model-value=""
                disabled />
            </Label>
            <Label label="Tanggal Setor">
              <Skeleton v-if="loadingData" class="skeleton" />
              <BFormInput
                v-else
                model-value=""
                disabled />
            </Label>
          </div>
        </template>
      </Card>
    </SlideRightX>
  </FlexBox>
</template>
