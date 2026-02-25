<script setup>
import SlideRightX from "@/src/components/animation/SlideRightX.vue";
import FormVoucher from "@/src/components/FormVoucher.vue";
import FlexBox from "@/src/components/ui/FlexBox.vue";
import { onMounted, ref } from "vue";
import { useAlert } from "@/src/store/alert";
import { voucherService } from "@/src/services/voucher";
import { useRoute } from "vue-router";
import Loader from "@/src/components/ui/Loader.vue";
import Card from "@/src/components/ui/Card.vue";
import { parseCurrency } from "@/src/lib/utils";
import { useCabang } from "@/src/store/cabang";
import { useCustomer } from "@/src/store/customer";

const alert = useAlert();
const initValue = ref(null);
const route = useRoute();
const loading = ref(false);
const key = ref(0);
const customerStore = useCustomer();
const cabangStore = useCabang();

onMounted(getResource);

async function getResource() {
  try {
    loading.value = true;
    const id = route.query.id;
    const tipeVoucher = route.name.split(" ").at(-1);

    // Menggunakan API baru
    const data = await voucherService.getVoucherById(id, tipeVoucher);
    const customerObjects = data.customer
      ? data.customer.map((customerId) => {
          const customerObj = customerStore.customer.list.find(
            (c) => c.id === customerId
          );
          return (
            customerObj || { id: customerId, nama: `Customer ${customerId}` }
          );
        })
      : [];

    const cabangObjects = data.cabang
      ? data.cabang.map((cabangId) => {
          const cabangObj = cabangStore.cabang.list.find(
            (c) => c.id === cabangId
          );
          return cabangObj || { id: cabangId, nama: `Cabang ${cabangId}` };
        })
      : [];

    // Mapping data sesuai dengan format yang dibutuhkan FormVoucher
    const mappedData = {
      id: data.id,
      nama: data.nama_voucher,
      tipe_voucher: parseInt(tipeVoucher),
      id_principal: data.id_principal,
      id_produk: data.produk || [],
      id_cabang: cabangObjects,
      level_uom: data.level_uom,
      minimal_jumlah_produk: data.minimal_jumlah_produk,
      kategori_voucher: data.kategori_voucher,
      persen_diskon: data[`persentase_diskon_${tipeVoucher}`],
      nilai_diskon: parseCurrency(data.nominal_diskon),
      minimal_subtotal_pembelian: parseCurrency(
        data.minimal_subtotal_pembelian
      ),
      jenis_voucher: data.is_reguler,
      keterangan: data.keterangan,
      id_customer: customerObjects,
      tanggal_mulai:
        data.tanggal_mulai && data.is_reguler === 0
          ? new Date(data.tanggal_mulai)
          : null,
      tanggal_kadaluarsa:
        data.tanggal_kadaluarsa && data.is_reguler === 0
          ? new Date(data.tanggal_kadaluarsa)
          : null,
      status_diskon: data.status_voucher,
      limit: parseCurrency(data.budget_diskon),
      pic_voucher: data.pic_voucher,
      syarat_ketentuan: data.syarat_ketentuan,
      syarat_wajib: data.syarat_wajib,
    };

    console.log("Data voucher setelah mapping:", mappedData);
    initValue.value = mappedData;
  } catch (error) {
    console.error(error);
    alert.setMessage(error, "danger");
  } finally {
    loading.value = false;
    key.value++;
  }
}
</script>

<template>
  <FlexBox full flex-col>
    <SlideRightX
      class="slide-container tw-justify-end"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <FlexBox v-if="loading" full>
        <Card no-subheader>
          <template #header>Form Edit Voucher</template>
          <template #content>
            <FlexBox full jus-center it-center style="height: 350px">
              <Loader />
            </FlexBox>
          </template>
        </Card>
      </FlexBox>
      <FormVoucher :key="key" v-else :initial-value="initValue" />
    </SlideRightX>
  </FlexBox>
</template>
