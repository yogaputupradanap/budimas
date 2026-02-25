<script setup>
import {usePagination} from "@/src/lib/usePagination";
import {useFiltering} from "@/src/lib/useFiltering";
import {useSorting} from "@/src/lib/useSorting";
// import { useOthers } from "@/src/store/others";
import {useUser} from "@/src/store/user";
import {useFetchPaginateV2} from "@/src/lib/useFetchPaginateV2";
import ListSetoranTunaiKasir from "@/src/pages/setoran-tunai/ListSetoranTunaiKasir.vue";
import ListSetoranTunaiPiutang from "@/src/pages/setoran-tunai/ListSetoranTunaiPiutang.vue";

// const others = useOthers();
const user = useUser();
</script>

<template>
  <ListSetoranTunaiKasir v-if="user.user.value.id_jabatan !== 15"/>
  <ListSetoranTunaiPiutang v-else/>
</template>
