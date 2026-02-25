<script setup>
import FlexBox from "../components/ui/FlexBox.vue";
import Image from "../components/ui/Image.vue";
import Budimas from "../assets/images/logo-budimas-black.png";
import TextField from "../components/ui/formInput/TextField.vue";
import PasswordField from "../components/ui/formInput/PasswordField.vue";
import { useCommonForm } from "../lib/useCommonForm";
import { loginSchema } from "../model/formSchema";
import Button from "../components/ui/Button.vue";
import { ref } from "vue";
import { localDisk, sessionDisk } from "../lib/utils";
import { useAlert } from "../store/alert";
import { userService } from "../services/user";
import { useRememberMe } from "../lib/useRememberMe";
import { userAksesService } from "../services/userAkses";
import { useUser } from "../store/user";

const { rememberMe, localLoginField, setLocalLoginInfo } = useRememberMe();

const { defineField, configProps, handleSubmit, resetForm } = useCommonForm(
  loginSchema,
  localLoginField
);

const [email, emailProps] = defineField("email", configProps);
const [password, passwordField] = defineField("password", configProps);
const loading = ref(false);
const alert = useAlert();

const onSubmit = handleSubmit(async (values) => {
  loading.value = true;
  console.log("[Login] Attempting sign in with values:", values);

  try {
  const signIn = await userService.signIn(values.email, values.password);

  if (signIn && Object.keys(signIn).length > 0) {
    console.log("[Login] Valid sign-in data received:", signIn);

    // Simpan data user ke session (tidak termasuk password)
    const { password, ...userData } = signIn;
    sessionDisk.setSession("authUser", userData);

    // Ambil hak akses berdasarkan id_user
    const hakAkses = await userAksesService.getUserAkses(signIn.id_user);
    console.log(hakAkses);
    
    localDisk.setLocalStorage("hakakses", hakAkses);

    const userStore = useUser();
    userStore.userAccessList = hakAkses;

    // Simpan info login (email saja, hindari password)
    setLocalLoginInfo({
      email: values.email,
      // jangan simpan password
    });

    // Disarankan reload state store daripada reload seluruh halaman
    // Contoh: panggil action store untuk refresh user dan hak akses

    window.location.reload(); // jika memang perlu reload halaman
  } else {
    resetForm();
    alert.setMessage("Username atau password salah", "danger");
  }
} catch (error) {
  console.error("Login error:", error);
  alert.setMessage("Terjadi kesalahan saat login", "danger");
} finally {
    loading.value = false;
    console.log("[Login] Loading state set to false");
  }
});
</script>

<template>
  <FlexBox full jus-center it-center class="tw-h-[90vh]">
    <FlexBox
      flex-col
      jus-center
      it-center
      gap="extra large"
      :style="[{ width: '400px' }]"
    >
      <Image :src="Budimas" object-fit="contain" class="tw-mb-4" />
      <FlexBox full class="tw-pb-6">
        <BForm novalidate class="tw-w-full tw-flex tw-flex-col tw-gap-6">
          <TextField
            placeholder="Enter your email"
            type="email"
            label-for="input-1"
            label="Email"
            group-id="input-group-1"
            v-model="email"
            :config-props="emailProps"
          />
          <PasswordField
            placeholder="Minimum 8 characters"
            label-for="input-2"
            label="Password*"
            group-id="input-group-2"
            v-model="password"
            :config-props="passwordField"
          />
          <FlexBox jus-between no-left-padding>
            <span>
              <BFormCheckbox
                v-model="rememberMe"
                value="true"
                unchecked-value="false"
                class="tw-border tw-border-slate-500"
              >
                Remember Me
              </BFormCheckbox>
            </span>
            <span class="tw-text-blue-700">Forgot Password ?</span>
          </FlexBox>
          <FlexBox full jus-center no-left-padding>
            <Button
              :trigger="onSubmit"
              :loading="loading"
              type="submit"
              class="tw-bg-blue-500 tw-w-full tw-h-10 tw-border-none"
            >
              Login
            </Button>
          </FlexBox>
        </BForm>
      </FlexBox>
    </FlexBox>
  </FlexBox>
</template>
