<script setup>
import {
  nextTick,
  onMounted,
  onUnmounted,
  ref,
  watchEffect,
  defineProps,
  defineModel,
} from "vue";
import { enableAnimations } from "../../../lib/settings";
import Fuse from "fuse.js";
import anime from "animejs";

const props = defineProps([
  "options",
  "placeholder",
  "size",
  "textField",
  "valueField",
  "maxSelectedDisplayed",
  "errors",
  "label",
  "fieldname",
  "search",
]);
const model = defineModel();

const showOptions = ref(false);
const selectRef = ref();
const optionRef = ref();
const optionsArray = ref(props.options);
const placeTop = ref(false);
const selectInputSize =
  props.size === "sm"
    ? "tw-h-8"
    : props.size === "md"
    ? "tw-h-11"
    : props.size === "lg"
    ? "tw-h-16"
    : props.size === "xl"
    ? "tw-h-20"
    : "tw-h-full";
const selectedValueArray = ref(model.value || []);
const selectedTextArray = ref(
  selectedValueArray.value.length
    ? props.options
        .map((option) =>
          selectedValueArray.value.some(
            (sel) => sel === option[props.valueField || "text"]
          )
            ? option[props.textField || "text"]
            : null
        )
        .filter((option) => option != null)
    : []
);

const enter = (el, done) => {
  anime.set(el, { translateY: placeTop.value ? 10 : -10, opacity: 0 });
  anime({
    targets: el,
    translateY: 0,
    opacity: 1,
    duration: !enableAnimations ? 0 : 400,
    easing: "easeOutExpo",
    complete: done,
  });
};

const leave = (el, done) => {
  anime({
    targets: el,
    translateY: placeTop.value ? 10 : -10,
    duration: !enableAnimations ? 0 : 400,
    opacity: 0,
    easing: "easeOutExpo",
    complete: done,
  });
};

const handleClickOutside = (event) => {
  const selectElement = selectRef.value;
  if (showOptions.value && !selectElement.contains(event.target)) {
    showOptions.value = false;
    placeTop.value = false;
  }
};

const placeingOptions = () => {
  const el = optionRef.value;
  const windowInnerHeight = window.innerHeight;
  const getRect = el.getBoundingClientRect();
  const yPosition = getRect.bottom;
  placeTop.value = yPosition > windowInnerHeight;
};

const openOptions = () => {
  showOptions.value = !showOptions.value;

  if (!showOptions.value) {
    placeTop.value = false;
  }

  if (showOptions.value) {
    nextTick(() => {
      placeingOptions();
    });
  }
};

const isSelected = (valueField) => {
  return selectedValueArray.value.some((sel) => sel === valueField);
};

const selectOption = (text, value, options) => {
  const optionsValue = options.filter(
    (option) => option[props.valueField || "value"] === value
  )[0][props.valueField || "value"];

  if (isSelected(optionsValue)) {
    selectedTextArray.value = selectedTextArray.value.filter(
      (sel) => sel !== text
    );
    selectedValueArray.value = selectedValueArray.value.filter(
      (sel) => sel !== optionsValue
    );
  } else {
    selectedTextArray.value.push(text);
    selectedValueArray.value.push(optionsValue);
  }

  model.value = selectedValueArray.value;
};

const filterOptions = (text, field) => {
  if (!text) return (optionsArray.value = props.options);
  const fuse = new Fuse(props.options, { keys: [field] });

  optionsArray.value = fuse.search(text).map((result) => result?.item);
};

watchEffect(() => {
  optionsArray.value = props.options;

  if (!model.value) {
    selectedTextArray.value = [];
    selectedValueArray.value = [];
  }
});

onMounted(() => {
  window.addEventListener("mousedown", handleClickOutside);
});

onUnmounted(() => {
  window.removeEventListener("mousedown", handleClickOutside);
});
</script>

<template>
  <div class="tw-w-full tw-flex tw-flex-col tw-gap-2">
    <span v-if="label">
      {{ label }}
    </span>
    <div
      tabindex="0"
      ref="selectRef"
      @click.self="openOptions"
      :class="[
        `tw-w-full tw-border tw-border-gray-300 hover:tw-border-gray-400 hover:tw-bg-gray-50 focus:tw-outline-none focus:tw-ring-4 
        focus:tw-ring-blue-200 tw-select-none tw-rounded-md tw-relative tw-px-2 tw-flex tw-justify-between tw-items-center tw-cursor-pointer`,
        selectInputSize,
      ]">
      <div
        @click="openOptions"
        v-if="selectedTextArray.length"
        class="tw-text-gray-600 tw-text-xs tw-select-none tw-w-full tw-overflow-hidden tw-flex tw-gap-1">
        <span
          v-for="text in selectedTextArray"
          v-if="selectedTextArray.length < (maxSelectedDisplayed || 3)"
          :key="text"
          :title="text"
          class="tw-py-1 tw-px-2 tw-rounded-md tw-flex tw-justify-center tw-items-center tw-border tw-border-slate-300">
          {{ text?.length > 20 ? text?.substring(0, 15) + "...." : text }}
        </span>
        <span v-else>{{ selectedTextArray.length }} item dipilih</span>
      </div>
      <span @click="openOptions" v-if="!selectedTextArray.length">
        <span v-if="placeholder" class="tw-text-xs">
          {{ placeholder }}
        </span>
        <span v-else>Pilih</span>
      </span>
      <span
        :class="[
          'mdi mdi-chevron-down tw-text-xl tw-gray-600 tw-transition-all tw-duration-300 tw-ease-in-out',
          showOptions && 'tw-rotate-180',
        ]"></span>
      <Transition @enter="enter" @leave="leave">
        <div
          ref="optionRef"
          v-if="showOptions"
          :class="[
            'tw-w-full tw-max-h-60 tw-z-50 tw-overflow-auto tw-select-none tw-absolute tw-flex tw-flex-col tw-gap-1 tw-px-2 tw-py-2 tw-bg-white tw-border tw-border-slate-500 tw-rounded-md tw-left-0',
            placeTop ? 'tw-bottom-[120%]' : 'tw-top-[120%]',
          ]">
          <div class="tw-w-full tw-bg-white tw-sticky -tw-top-2 tw-pt-2">
            <BFormInput
              v-if="search"
              @input="filterOptions($event, textField)"
              class="tw-h-8 tw-mb-3 placeholder:tw-text-sm tw-text-sm"
              placeholder="cari ..." />
          </div>
          <div
            class="tw-w-full tw-flex tw-flex-col tw-gap-0"
            v-for="option in optionsArray"
            :key="option[valueField || 'value']">
            <span
              @click="
                selectOption(
                  option[textField || 'text'],
                  option[valueField || 'value'],
                  options
                )
              "
              :class="[
                'tw-px-3 tw-py-2 tw-text-xs tw-transition-all tw-rounded-sm tw-duration-500 tw-ease-in-out tw-cursor-pointer tw-text-start',
                isSelected(option[valueField || 'value'])
                  ? 'tw-bg-sky-700 tw-text-white hover:tw-text-white'
                  : 'hover:tw-text-white hover:tw-bg-sky-400',
              ]">
              {{ option[textField || "text"] }}
            </span>
          </div>
        </div>
      </Transition>
    </div>
    <span v-if="errors && fieldname" class="tw-text-red-500">
      {{ errors[fieldname] }}
    </span>
  </div>
</template>
