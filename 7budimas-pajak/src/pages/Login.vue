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

  try {
    const signIn = await userService.signIn(values.email, values.password);
    if (Object.keys(signIn.data).length) {
      sessionDisk.setSession("authUser", signIn.data);

      const hakAkses = await userAksesService.getUserAkses(signIn.data.id_user);
      localDisk.setLocalStorage("hakakses", hakAkses);
      console.log(hakAkses);
      setLocalLoginInfo({
        email: values.email,
        password: values.password,
      });

      window.location.reload();
    } else {
      resetForm();
      alert.setMessage("username atau password salah", "danger");
    }
  } catch (error) {
    alert.setMessage(error, "danger");
  }
});
</script>

<template>
  <FlexBox full jus-center it-center class="tw-h-[88vh]">
    <FlexBox
      flex-col
      jus-center
      it-center
      gap="extra large"
      :style="[{ width: '400px' }]">
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
            :config-props="emailProps" />
          <PasswordField
            placeholder="Minimum 8 characters"
            label-for="input-2"
            label="Password*"
            group-id="input-group-2"
            v-model="password"
            :config-props="passwordField" />
          <FlexBox jus-between no-left-padding>
            <span>
              <BFormCheckbox
                v-model="rememberMe"
                value="true"
                unchecked-value="false"
                class="tw-border tw-border-slate-500">
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
              class="tw-bg-blue-500 tw-w-full tw-h-10 tw-border-none">
              Login
            </Button>
          </FlexBox>
        </BForm>
      </FlexBox>
    </FlexBox>
  </FlexBox>
</template>
