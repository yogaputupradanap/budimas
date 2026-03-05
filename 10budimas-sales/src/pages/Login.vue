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
import axios from "axios";
import { apiUrl, sessionDisk } from "../lib/utils";
import { useRememberMe } from "../lib/useRememberMe";
import { useAlert } from "../store/alert";

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
  const body = {
    email: values.email,
    password: values.password,
  };
  loading.value = true;

  try {
    const signIn = await axios.post(`${apiUrl}/api/auth/sales/login`, body);

    if (Object.keys(signIn.data).length) {
      sessionDisk.setSession("authUser", signIn.data);
      localLoginField.setLocalLoginInfo("user",  signIn.data);
      setLocalLoginInfo(body);
      window.location.reload();
    } else {
      resetForm();
      alert.setMessage(
        "email atau password yang anda masukkan ada yang salah",
        "danger"
      );
    }
  } catch (error) {
    console.log(error.response.data)
    alert.setMessage(error?.response?.data, 'danger');
  }
});
</script>

<template>
  <FlexBox full jus-center it-center class="tw-h-[85vh]">
    <FlexBox
      flex-col
      jus-center
      it-center
      gap="extra large"
      :style="[{ width: '370px' }]">
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
          <FlexBox jus-between>
            <span>
              <BFormCheckbox
                v-model="rememberMe"
                value="true"
                unchecked-value="false"
                class="tw-border tw-border-slate-500">
                Remember Me
              </BFormCheckbox>
            </span>
          </FlexBox>
          <FlexBox full jus-center>
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
