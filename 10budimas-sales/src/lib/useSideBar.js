/**
 * Vue composition functions for managing the state of minimize and mobile minimize flags.
 * @module MinimizeFlags
 */
import { ref } from "vue";

const isMinimize = ref(false);
const isMobileMinimize = ref(true);

const setMinimize = (value) => (isMinimize.value = value);
const setMobileMinimize = (value) => (isMobileMinimize.value = value);

export { isMinimize, setMinimize, isMobileMinimize, setMobileMinimize };
