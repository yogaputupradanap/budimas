<script setup>
import {defineEmits, defineModel, defineProps, nextTick, onMounted, onUnmounted, ref, watchEffect,} from "vue";
import {enableAnimations} from "../../../lib/settings";
import Fuse from "fuse.js";
import anime from "animejs";
import {RecycleScroller} from "vue-virtual-scroller";
import "vue-virtual-scroller/dist/vue-virtual-scroller.css";

const props = defineProps([
  "options",
  "modelValue",
  "placeholder",
  "size",
  "textField",
  "valueField",
  "maxSelectedDisplayed",
  "search",
  "removable",
  "disabled",
  "noDynamicPlacing",
  "itemsSize",
  "virtualScroll",
  "serverSearch"
]);
const model = defineModel();
const emits = defineEmits(["change", "search"]);

const showOptions = ref(false);
const optionsArray = ref(props.options);
const selectRef = ref();
const optionRef = ref();
const selectedOptionRef = ref();
const filterText = ref("");

const selectedOptionText = ref(model.value || "");
const selectedOptionValue = ref(model.value);
const placeTop = ref(false);
const selectInputSize =
    props.size === "sm"
        ? "tw-h-8"
        : props.size === "md"
            ? "tw-h-[37px]"
            : props.size === "lg"
                ? "tw-h-16"
                : props.size === "xl"
                    ? "tw-h-20"
                    : "tw-h-full";

const enter = (el, done) => {
  anime.set(el, {translateY: placeTop.value ? 10 : -10, opacity: 0});
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

const placingOptions = () => {
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
      if (props.noDynamicPlacing) return;
      placingOptions();
    });
  }

  nextTick(() => {
    if (props.virtualScroll) return;
    const selectedOptions = selectedOptionRef.value;
    const optionContainer = optionRef.value;

    if (selectedOptions && selectedOptions.length) {
      const selectedElement = selectedOptions.find((option) =>
          option.classList.contains("tw-bg-[#01579b]")
      );

      if (selectedElement && optionContainer) {
        const optionTop = selectedElement.offsetTop;
        optionContainer.scrollTop =
            optionTop -
            optionContainer.clientHeight / 2 +
            selectedElement.clientHeight / 2;
      }
    }
  });
};

const selectOption = (text, value, options) => {
  selectedOptionText.value = text;
  selectedOptionValue.value = value;
  const optionsValue = options.filter(
      (option) => option[props.valueField || "value"] === value
  )[0][props.valueField || "value"];
  model.value = optionsValue;

  emits("change", optionsValue);
};

const filterOptions = (field) => {
  if (!filterText.value || filterText.value == "") {
    optionsArray.value = props.options;
    return;
  }

  if (props.serverSearch) {
    emits("search", filterText.value);
    return;
  }

  const fuse = new Fuse(props.options, {keys: [field]});

  optionsArray.value = fuse
      .search(filterText.value)
      .map((result) => result?.item);
};

const clearSelection = () => {
  selectedOptionText.value = "";
  selectedOptionValue.value = "";
  model.value = ""; // reset v-model agar reactive ke parent
  filterText.value = "";
  optionsArray.value = props.options;
  showOptions.value = false; // tutup dropdown kalau lagi terbuka
  emits("change", ""); // biar parent tahu value di-reset
};


onMounted(() => {
  window.addEventListener("mousedown", handleClickOutside);
});

onUnmounted(() => {
  window.removeEventListener("mousedown", handleClickOutside);
});

watchEffect(() => {
  optionsArray.value = props.options;

  if (model.value === null || model.value === undefined || model.value === "") {
    selectedOptionValue.value = "";
    selectedOptionText.value = "";
  } else {
    selectedOptionValue.value = model.value;
  }

  if (model.value === null || model.value === undefined || model.value === "") {
    return selectedOptionText.value;
  }

  const foundOption = props.options.find(
      (option) => option[props.valueField || "value"] === model.value
  );

  if (foundOption) {
    selectedOptionText.value = foundOption[props.textField || "text"];
  }
});
</script>

<template>
  <div
      ref="selectRef"
      tabindex="0"
      @click.self="!disabled && openOptions()"
      :class="[
      'tw-w-full tw-border tw-rounded-md tw-relative tw-px-2 tw-flex tw-justify-between tw-items-center tw-cursor-pointer',
      !disabled
        ? 'tw-border-gray-200 hover:tw-border-gray-400 hover:tw-bg-gray-50 focus:tw-outline-none focus:tw-ring-4 focus:tw-ring-blue-200'
        : 'tw-border-gray-300 tw-bg-gray-200 tw-cursor-not-allowed',
      selectInputSize,
    ]">
    <span
        :title="selectedOptionText"
        @click="!disabled && openOptions()"
        :class="[
        'tw-text-sm tw-select-none tw-truncate',
        selectedOptionText !== null &&
        selectedOptionText !== undefined &&
        selectedOptionText !== ''
          ? 'tw-text-gray-900'
          : 'tw-text-gray-500',
        disabled && 'tw-font-medium tw-text-gray-600/70',
      ]">
      <template
          v-if="
          selectedOptionText !== null &&
          selectedOptionText !== undefined &&
          selectedOptionText !== ''
        ">
        {{ selectedOptionText }}
      </template>
      <template v-else>
        <span class="tw-text-gray-500">{{ props.placeholder || "Pilih" }}</span>
      </template>
    </span>
    <div class="tw-flex tw-items-center">
     <span
         v-if="
    !disabled &&
    selectedOptionText !== null &&
    selectedOptionText !== undefined &&
    selectedOptionText !== '' &&
    props.removable
  "
         class="mdi mdi-close tw-text-xl tw-text-gray-400 tw-mr-2 tw-cursor-pointer hover:tw-text-gray-600 tw-transition-all tw-duration-200"
         @click.stop="clearSelection"
     />

      <span
          @click="!disabled && openOptions()"
          :class="[
        'mdi mdi-chevron-down tw-text-xl tw-transition-all tw-duration-300 tw-ease-in-out tw-text-gray-500',
        showOptions && 'tw-rotate-180',
      ]"></span>
    </div>
    <Transition @enter="enter" @leave="leave">
      <div
          ref="optionRef"
          v-if="showOptions"
          :class="[
          'tw-w-full tw-max-h-60 tw-z-50 tw-overflow-auto tw-shadow-xl tw-select-none tw-absolute tw-flex tw-flex-col tw-gap-1 tw-px-2 tw-py-2 tw-bg-white tw-border tw-border-gray-300 tw-rounded-md tw-left-0',
          placeTop ? 'tw-bottom-[120%]' : 'tw-top-[120%]',
        ]">
        <div class="tw-bg-white tw-sticky -tw-top-2 tw-pt-1">
          <BFormInput
              v-if="props.search"
              v-model="filterText"
              @input="filterOptions(props.textField)"
              class="tw-h-8 tw-mb-3 tw-mt-2 placeholder:tw-text-sm tw-text-sm"
              placeholder="cari ..."/>
        </div>

        <!-- using virtual scroller if option datas too big -->
        <RecycleScroller
            @click="openOptions"
            v-if="props.options.length && props.virtualScroll"
            class="tw-overflow-y-auto tw-w-full"
            :items="optionsArray"
            :item-size="32"
            :key-field="props.valueField || 'value'"
            v-slot="{ item }">
          <div
              ref="selectedOptionRef"
              @click="
              selectOption(
                item[props.textField || 'text'],
                item[props.valueField || 'value'],
                options
              )
            "
              :class="[
              'tw-px-4 tw-py-2 tw-mb-2 tw-text-xs tw-rounded-sm hover:tw-bg-[#01579b] hover:tw-text-white tw-transition-all tw-duration-500 tw-ease-in-out tw-cursor-pointer tw-text-start',
              item[props.valueField || 'value'] === selectedOptionValue &&
                'tw-bg-[#01579b] tw-text-white tw-font-semibold',
            ]">
            {{ item[props.textField || "text"] }}
          </div>
        </RecycleScroller>

        <!-- using regular loop if option data not too large. option data < 1000 -->
        <div
            @click="openOptions"
            v-else-if="props.options.length && !props.virtualScroll"
            class="tw-w-full tw-flex tw-flex-col tw-gap-0"
            v-for="option in optionsArray"
            :key="option[props.valueField || 'value']">
          <span
              ref="selectedOptionRef"
              @click="
              selectOption(
                option[props.textField || 'text'],
                option[props.valueField || 'value'],
                options
              )
            "
              :class="[
              'tw-px-3 tw-py-2 tw-text-xs tw-rounded-sm hover:tw-bg-[#01579b] hover:tw-text-white tw-transition-all tw-duration-500 tw-ease-in-out tw-cursor-pointer tw-text-start',
              option[props.valueField || 'value'] === selectedOptionValue &&
                'tw-bg-[#01579b] tw-text-white tw-font-semibold',
            ]">
            {{ option[props.textField || "text"] }}
          </span>
        </div>
        <div
            v-else
            class="tw-w-full tw-h-14 tw-text-sm tw-flex tw-justify-center tw-items-center tw-text-slate-600">
          Tidak ada data pilihan
        </div>
      </div>
    </Transition>
  </div>
</template>
