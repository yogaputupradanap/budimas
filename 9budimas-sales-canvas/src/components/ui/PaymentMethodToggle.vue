
<script setup>
import { BFormCheckbox, BFormInput } from 'bootstrap-vue-next';
import { ref, computed, watch, onMounted, inject } from 'vue';

const $swal = inject('$swal');

const props = defineProps({
  // Initial state
  totalAmount: {
    type: [Number, String],
    default: 0
  },
  initialReceivedAmount: {
    type: [Number, String],
    default: 0
  },
  initialPaymentActive: {
    type: Boolean,
    default: false
  },
  
  // Labels and text customization
  switchLabel: {
    type: String,
    default: 'Pembayaran COD'
  },
  totalAmountLabel: {
    type: String,
    default: 'Jumlah yang harus dibayar'
  },
  receivedAmountLabel: {
    type: String,
    default: 'Jumlah yang diterima'
  },
  
  // Placeholders
  totalAmountPlaceholder: {
    type: String,
    default: 'Rp 0'
  },
  receivedAmountPlaceholder: {
    type: String,
    default: '0'
  },
  
  // Formatting options
  currencyFormat: {
    type: Boolean,
    default: true
  },
  currencySymbol: {
    type: String,
    default: 'Rp'
  }
});

// Emit definition
const emit = defineEmits(['payment-change']);

// Reactive data
const isPaymentActive = ref(props.initialPaymentActive);
const receivedAmount = ref(props.initialReceivedAmount);

// Computed properties
const formattedTotalAmount = computed(() => {
  if (!props.totalAmount) return '';
  
  if (props.currencyFormat) {
    const amount = typeof props.totalAmount === 'string' 
      ? parseFloat(props.totalAmount) 
      : props.totalAmount;
    
    return `${props.currencySymbol} ${amount.toLocaleString('id-ID')}`;
  }
  
  return props.totalAmount;
});

const changeAmount = computed(() => {
  const received = parseFloat(receivedAmount.value) || 0;
  const total = parseFloat(props.totalAmount) || 0;
  return received - total;
});

// Watchers
watch(() => props.initialPaymentActive, (newVal) => {
  isPaymentActive.value = newVal;
});

watch(() => props.initialReceivedAmount, (newVal) => {
  receivedAmount.value = newVal;
});

watch(() => props.totalAmount, () => {
  emitPaymentData();
});

// Methods
const handlePaymentToggle = () => {
  if (!isPaymentActive.value) {
    receivedAmount.value = 0;
  }
  emitPaymentData();
};

const handleReceivedAmountChange = () => {
  emitPaymentData();
};

const emitPaymentData = () => {
  const paymentData = {
    isActive: isPaymentActive.value,
    totalAmount: parseFloat(props.totalAmount) || 0,
    receivedAmount: parseFloat(receivedAmount.value) || 0,
    changeAmount: changeAmount.value,
    isComplete: isPaymentActive.value && parseFloat(receivedAmount.value) >= parseFloat(props.totalAmount)
  };
  
  emit('payment-change', paymentData);
};

watch(receivedAmount, (newVal, oldVal) => {
  const total = parseFloat(props.totalAmount) || 0;
  const received = parseFloat(newVal) || 0;

  if (received > total) {
    $swal.warning('Jumlah yang diterima tidak boleh melebihi jumlah yang harus dibayar.');
    receivedAmount.value = total;
  }
});

onMounted(() => { emitPaymentData() });
</script>

<template>
  <div
    class="tw-w-fit tw-flex tw-mx-3 tw-items-center tw-gap-4 tw-mt-6 tw-mb-4 tw-p-4 tw-border tw-rounded-md"
    :class="
      isPaymentActive
        ? 'tw-border-green-400 tw-bg-green-50'
        : 'tw-border-gray-300 tw-bg-gray-50'
    ">
    
    <!-- Toggle Switch Section -->
    <div
      class="tw-flex tw-flex-col tw-items-center tw-border-r-2 tw-pr-4"
      :class="
        isPaymentActive
          ? 'tw-border-green-300'
          : 'tw-border-slate-300'
      ">
      <BFormCheckbox
        v-model="isPaymentActive"
        switch
        size="lg"
        class="tw-scale-125"
        @change="handlePaymentToggle" />
      <span class="tw-text-xs tw-font-medium tw-mt-2">
        {{ switchLabel }}
      </span>
    </div>

    <!-- Payment Input Fields -->
    <div class="tw-flex tw-gap-4">
      <!-- Jumlah yang harus dibayar -->
      <div class="tw-flex tw-flex-col">
        <label
          class="tw-text-sm tw-font-semibold tw-mb-2 tw-block"
          :class="
            isPaymentActive
              ? 'tw-text-green-700'
              : 'tw-text-gray-600'
          ">
          {{ totalAmountLabel }}
        </label>
        <BFormInput
          :disabled="true"
          :value="formattedTotalAmount"
          class="tw-w-48"
          :class="
            isPaymentActive
              ? 'tw-bg-green-100 tw-border-green-300 tw-text-green-800'
              : 'tw-bg-gray-100 tw-border-gray-300 tw-text-gray-500'
          "
          :placeholder="totalAmountPlaceholder" />
      </div>

      <!-- Jumlah yang diterima -->
      <div class="tw-flex tw-flex-col">
        <label
          class="tw-text-sm tw-font-semibold tw-mb-2 tw-block"
          :class="
            isPaymentActive
              ? 'tw-text-green-700'
              : 'tw-text-gray-600'
          ">
          {{ receivedAmountLabel }}
        </label>
        <BFormInput
          v-model="receivedAmount"
          :disabled="!isPaymentActive"
          type="number"
          class="tw-w-48"
          :class="
            isPaymentActive
              ? 'tw-bg-white tw-border-green-300 tw-text-green-800'
              : 'tw-bg-gray-100 tw-border-gray-300 tw-text-gray-500'
          "
          :placeholder="receivedAmountPlaceholder"
          @input="handleReceivedAmountChange" />
      </div>
    </div>
  </div>
</template>