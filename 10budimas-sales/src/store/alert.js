import { defineStore } from "pinia";
import { toast } from "vue-sonner";

export const useAlert = defineStore("alert", {
  actions: {
    setMessage(message, variant = 'success', dissmissCountDown = 2000) {
      switch (variant) {
        case "success":
          toast.success(message);
          break;
        case "danger":
          toast.error(message);
          break;
        case "warning":
          toast.warning(message);
          break;
      }
    },
  },
});
