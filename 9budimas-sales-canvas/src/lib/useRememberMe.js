import { ref, watch } from "vue";
import { localDisk, parse } from "./utils";

export function useRememberMe() {
  const localLoginField = localDisk.getLocalStorage("login_field") || {};
  const localRememberMe = localDisk.getLocalStorage("remember_me") || false;

  const rememberMe = ref(localRememberMe);

  const setLocalLoginInfo = (value) => {
    const rememberMeBool = parse(rememberMe.value);

    if (rememberMeBool) localDisk.setLocalStorage("login_field", value);
  };

  watch(rememberMe, (newValue) => {
    const rememberMeBool = parse(newValue);
    localDisk.setLocalStorage("remember_me", newValue);

    if (!rememberMeBool) localDisk.removeLocalStorage(["login_field"]);
  });

  return { rememberMe, localLoginField, setLocalLoginInfo };
}
