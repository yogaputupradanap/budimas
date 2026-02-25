<script setup>
import { ref, onMounted, computed } from "vue";
import SlideRightX from "../components/animation/SlideRightX.vue";
import Card from "../components/ui/Card.vue";
import FlexBox from "../components/ui/FlexBox.vue";
import RouterButton from "../components/ui/RouterButton.vue";
import ArmadaCalendar from "../components/ui/ArmadaCalendar.vue";
import ArmadaEventModal from "../components/ui/ArmadaEventModal.vue";
import { apiUrl, fetchWithAuth, localDisk } from "../lib/utils";
import Loader from "../components/ui/Loader.vue";

const jadwalArmada = ref([]);
const isLoading = ref(true);
const error = ref(null);

const showEventModal = ref(false);
const selectedEvent = ref(null);

const idCabang = ref(null);

const calendarEvents = computed(() => {
  return jadwalArmada.value.map((item) => ({
    id: `${item.id_armada}-${item.delivering_date}-${item.id_rute}`,
    title: `${item.kode_rute} - [${item.nama_armada}]`,
    start: item.delivering_date,
    allDay: true,
    extendedProps: { ...item },
  }));
});

const getResource = async () => {
  idCabang.value = localDisk.getLocalStorage("id_cabang_distribusi");
  if (!idCabang.value) return;

  isLoading.value = true;
  error.value = null;

  try {
    const response = await fetchWithAuth(
      "GET",
      `${apiUrl}/api/distribusi/get-jadwal-armada?id_cabang=${idCabang.value}`
    );

    jadwalArmada.value = response ?? [];
  } catch (err) {
    console.error(err);
    error.value = "Gagal memuat data jadwal armada";
  } finally {
    isLoading.value = false;
  }
};

const refreshCalendar = async () => {
  showEventModal.value = false;
  await getResource();
};

const handleEventClick = (eventInfo) => {
  selectedEvent.value = eventInfo;
  showEventModal.value = true;
};

const closeModal = () => {
  showEventModal.value = false;
};

onMounted(() => {
  idCabang.value = localDisk.getLocalStorage("id_cabang_distribusi");

  if (!idCabang.value) {
    console.warn("id_cabang tidak ditemukan di localStorage");
    isLoading.value = false;
    return;
  }

  getResource();
});
</script>

<template>
  <div class="tw-flex tw-flex-col tw-gap-4 lg:tw-px-4 tw-px-0 tw-min-h-[80vh]">
    <SlideRightX
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">

      <Card :no-subheader="true" class="tw-mb-6">
        <template #header>Jadwal Armada</template>

        <template #content>
          <FlexBox full jusEnd class="tw-mb-4">
            <RouterButton
              to="/jadwal/jadwal-dan-rute"
              icon="mdi mdi-plus-circle-outline"
              class="tw-px-4">
              Penjadwalan
            </RouterButton>
          </FlexBox>

          <FlexBox v-if="isLoading" full jusCenter itCenter class="tw-h-[70vh]">
            <Loader />
          </FlexBox>

          <div
            v-else-if="error"
            class="tw-bg-red-50 tw-border tw-border-red-200 tw-rounded-md tw-p-4 tw-my-4">
            {{ error }}
          </div>

          <div v-else class="tw-w-full tw-py-5">
            <ArmadaCalendar
              :events="calendarEvents"
              initialView="dayGridMonth"
              eventColor="tw-bg-blue-500"
              height="700px"
              @event-click="handleEventClick" />
          </div>
        </template>
      </Card>
    </SlideRightX>

    <ArmadaEventModal
      :show="showEventModal"
      :event-data="selectedEvent"
      @close="closeModal"
      @deleted="refreshCalendar"
      @updated="refreshCalendar" />
  </div>
</template>
