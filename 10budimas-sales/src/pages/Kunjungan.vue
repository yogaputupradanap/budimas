<!-- eslint-disable vue/multi-word-component-names -->
<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import Table from "../components/ui/table/Table.vue";
import { kunjunganColumns } from "../model/tableColumns";
import Information from "../components/ui/Information.vue";
import Card from "../components/ui/Card.vue";
import FlexBox from "../components/ui/FlexBox.vue";
import { nextTick, onMounted, ref } from "vue";
import { useKunjungan } from "../store/kunjungan";
import { sessionDisk } from "../lib/utils";
import { useSales } from "../store/sales";
import Skeleton from "../components/ui/Skeleton.vue";
import Modal from "../components/ui/Modal.vue";

const kunjungan = useKunjungan();
const sales = useSales();
const user = sessionDisk.getSession("authUser");
const rute = ref();
const modal = ref();
const kunjunganInformations = [
  {
    buttonColor: "tw-bg-green-500",
    buttonText: "Done",
    buttonTextColor: "tw-text-white",
    information: "Status sudah kunjungan",
  },
  {
    buttonColor: "tw-bg-blue-500",
    buttonText: "To Do",
    buttonTextColor: "tw-text-white",
    information: "Status Sedang Kunjungan",
  },
  {
    buttonColor: "tw-bg-gray-300",
    buttonText: "Check In",
    information: "Status Belum Kunjungan",
  },
];

const openModal = (values) => {
  rute.value = values.value;
  nextTick(() => modal.value.show());
};

onMounted(() => {
  kunjungan.getListKunjungan(user.id_user);
});
</script>

<template>
  <div
    class="tw-flex tw-flex-col tw-justify-center tw-items-start tw-gap-4 lg:tw-px-4 tw-px-0"
  >
    <SlideRightX
      class="tw-w-full tw-px-2 tw-flex tw-flex-col tw-gap-8 tw-bg-white tw-rounded-2xl"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40"
    >
      <Card :no-subheader="kunjungan.activeKunjungan.kunjungan">
        <template #header>Status Check In</template>
        <template #subheader v-if="!kunjungan.activeKunjungan.kunjungan">
          Saat ini, anda belum melakukan check-in, silahkan pilih customer
          terlebih dahulu untuk check in !
        </template>
        <template #content>
          <FlexBox class="tw-pb-10 tw-justify-center lg:tw-flex-row tw-flex-col">
            <FlexBox flex-col gap="small">
              <span class="font-bold">Sales :</span>
              <Skeleton
                class="lg:tw-w-64 tw-w-full tw-h-10"
                v-if="sales.loading"
              />
              <BFormInput
                class="lg:tw-w-64 tw-w-full tw-h-10"
                plaintext
                :model-value="sales.salesUser.nama"
                v-else
              />
            </FlexBox>
            <FlexBox flex-col gap="small">
              <span class="font-bold">Customer :</span>
              <Skeleton
                class="lg:tw-w-64 tw-w-full tw-h-10"
                v-if="kunjungan.loading"
              />
              <BFormInput
                class="lg:tw-w-64 tw-w-full tw-h-10"
                :title="
                  kunjungan.activeKunjungan?.kunjungan?.nama_customer || ''
                "
                placeholder="Pilih Kunjungan"
                plaintext
                :model-value="
                  kunjungan.activeKunjungan?.kunjungan?.nama_customer || ''
                "
                v-else
              />
            </FlexBox>
            <FlexBox flex-col gap="small">
              <span class="font-bold">Tanggal Kunjungan :</span>
              <Skeleton
                class="lg:tw-w-64 tw-w-full tw-h-10"
                v-if="kunjungan.loading"
              />
              <BFormInput
                class="lg:tw-w-64 tw-w-full tw-h-10"
                placeholder="Pilih Kunjungan"
                plaintext
                :model-value="
                  kunjungan.activeKunjungan?.kunjungan?.tanggal || ''
                "
                v-else
              />
            </FlexBox>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40"
      class="tw-w-full tw-bg-white tw-px-2 tw-flex tw-items-center tw-flex-col tw-rounded-2xl tw-gap-8 tw-pb-10"
    >
      <Card no-subheader>
        <template #header>Daftar Kunjungan Toko</template>
        <template #content>
          <Modal ref="modal" id="modal">
            <Card dense no-subheader class="tw-p-4">
              <template #header>
                <span class="tw-text-xl tw-font-bold tw-text-black">
                  Rute Atau Detail Alamat
                </span>
              </template>
              <template #content>
                <FlexBox full flex-col>
                  <FlexBox flex-col gap="small">
                    <h3 class="tw-text-black tw-font-bold tw-text-lg">
                      Latitude
                    </h3>
                    <span class="tw-text-sm">{{ rute?.latitude }}</span>
                  </FlexBox>
                  <FlexBox flex-col gap="small">
                    <h3 class="tw-text-black tw-font-bold tw-text-lg">
                      Longitude
                    </h3>
                    <span class="tw-text-sm">{{ rute?.longitude }}</span>
                  </FlexBox>
                  <FlexBox flex-col gap="small">
                    <h3 class="tw-text-black tw-font-bold tw-text-lg">
                      Alamat
                    </h3>
                    <span class="tw-text-sm tw-lowercase">
                      {{ rute?.alamat }}
                    </span>
                  </FlexBox>
                </FlexBox>
              </template>
            </Card>
          </Modal>
          <Table
            :key="kunjungan.tableKey"
            :table-data="kunjungan.listKunjungan"
            :columns="kunjunganColumns"
            :loading="kunjungan.loading"
            @open-row-modal="openModal"
          />
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.3"
      :delay-out="0.3"
      :initial-x="-40"
      :x="40"
      class="tw-w-full tw-bg-white tw-px-2 tw-flex tw-items-center tw-flex-col tw-rounded-2xl tw-gap-8"
    >
      <Information :informations="kunjunganInformations" />
    </SlideRightX>
  </div>
</template>
