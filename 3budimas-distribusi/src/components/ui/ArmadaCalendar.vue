<script setup>
import { ref, onMounted, computed, watch } from "vue";
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import listPlugin from "@fullcalendar/list";
import interactionPlugin from "@fullcalendar/interaction";
import idLocale from "@fullcalendar/core/locales/id";

const props = defineProps({
  events: {
    type: Array,
    default: () => [],
  },
  initialView: {
    type: String,
    default: "dayGridMonth",
  },
  height: {
    type: String,
    default: "700px",
  },
});

const emit = defineEmits(["eventClick"]);

const calendarApi = ref(null);
const calendarOptions = ref({
  plugins: [dayGridPlugin, timeGridPlugin, listPlugin, interactionPlugin],
  initialView: "dayGridMonth",
  locale: idLocale,
  headerToolbar: {
    left: "prev,next today",
    center: "title",
    right: "dayGridMonth,listMonth",
  },
  events: props.events,
  eventClick: (clickInfo) => {
    emit("eventClick", clickInfo.event);
  },
  eventClassNames: [props.eventColor],
  height: props.height,
  editable: false,
  dayMaxEvents: true,
  firstDay: 1,
  buttonText: {
    today: "Hari Ini",
    month: "Bulan",
    week: "Minggu",
    day: "Hari",
    list: "List",
  },
  allDayText: "",
  noEventsText: "Tidak ada jadwal",
});

// Watch perubahan events dan memperbarui kalender
watch(
  () => props.events,
  (newEvents) => {
    calendarOptions.value.events = newEvents;

    if (calendarApi.value) {
      calendarApi.value.getApi().refetchEvents();
    }
  },
  { deep: true }
);

function changeView(viewName) {
  if (calendarApi.value) {
    calendarApi.value.getApi().changeView(viewName);
  }
}

// Mendapatkan referensi kalender setelah mounted
onMounted(() => {
  // Update manual height jika perlu
  calendarOptions.value.height = props.height;
});

// Mengekspos fungsi-fungsi ke komponen induk
defineExpose({
  changeView,
});
</script>

<template>
  <div class="tw-w-full">
    <FullCalendar ref="calendarApi" :options="calendarOptions" />
  </div>
</template>

<style>
.fc-event {
  cursor: pointer;
  border: none;
  padding: 2px 4px;
  border-radius: 4px;
}

.fc-event-title {
  font-weight: 500;
}

/* Pastikan elemen fullcalendar menempati lebar penuh */
.fc {
  width: 100%;
}

.fc-toolbar-title {
  font-size: 1.25rem !important;
  font-weight: 600;
}

.fc-header-toolbar {
  margin-bottom: 1rem !important;
}

/* Tambahan untuk tampilan yang lebih baik pada mobile */
@media (max-width: 768px) {
  .fc-toolbar {
    flex-direction: column;
    gap: 0.5rem;
  }

  .fc-toolbar-title {
    font-size: 1rem !important;
  }
}
</style>
