<script setup>
import ClockAndToggle from "./ClockAndToggle.vue";
import UserInfo from "./UserInfo.vue";
import Avatar from "./Avatar.vue";
import { useUser } from "@/src/store/user";

const user = useUser()
const userInfos = ["nama", "nama_jabatan", "nama_cabang"];
const icons = ["mdi-account", "mdi-tag", "mdi-store"];

</script>

<template>
  <header
    id="header-wrapper"
    class="tw-w-full tw-h-16 tw-bg-white tw-hidden lg:tw-flex tw-justify-between tw-items-center tw-px-4">
    <ClockAndToggle />
    <div
      class="tw-flex tw-justify-start tw-items-center tw-gap-6 tw-text-blue-500 tw-text-sm">
      <UserInfo
        v-for="(icon, idx) in icons"
        :key="icon"
        :icon="icon"
        :loading="user?.loading || false"
        :user-info="user?.user?.value?.[userInfos[idx]] || ''" />
      <Avatar header-wrapper-id="header-wrapper" />
    </div>
  </header>
</template>
