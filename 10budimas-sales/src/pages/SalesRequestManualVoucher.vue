<script setup>
import SlideRightX from "../components/animation/SlideRightX.vue";
import FlexBox from "../components/ui/FlexBox.vue";
import Card from "../components/ui/Card.vue";
import { useCommonForm } from "@/src/lib/useCommonForm";
import { tambahProdukSchema } from "@/src/model/formSchema";
import SelectInput from "../components/ui/formInput/SelectInput.vue";
import TextField from "../components/ui/formInput/TextField.vue";
import { nextTick, onMounted, reactive, watch } from "vue";
import { ref, computed } from "vue";
import Table from "../components/ui/table/Table.vue";
import {
  sisaPlafonColumns,
  listOrderColumns,
  listFreeProductsColumns,
} from "@/src/model/tableColumns";
import Modal from "../components/ui/Modal.vue";
import {
  apiUrl,
  checkNaN,
  fetchWithAuth,
  parseCurrency,
  sessionDisk,
} from "../lib/utils";
import { usePiutang } from "../store/piutang";
import { useKunjungan } from "../store/kunjungan";
import { useSales } from "../store/sales";
import { useSalesRequest } from "../store/salesRequest";
import VueDatePicker from "@vuepic/vue-datepicker";
import { useVoucher } from "../store/voucher";
import { usePrincipal } from "../store/principal";
import MultipleSelect from "../components/ui/formInput/MultipleSelect.vue";
import { useAlert } from "../store/alert";
import Button from "../components/ui/Button.vue";
import { useDashboard } from "../store/dashboard";

// global state store
const kunjungan = useKunjungan();
const principal = usePrincipal();
const sales = useSales();
const piutang = usePiutang();
const salesRequestStore = useSalesRequest();
const voucher = useVoucher();
const alert = useAlert();
const principalStore = usePrincipal();
const dashboard = useDashboard();

// local state
const principalId = ref();
const salesRequest = ref([]);
const freeProducts = ref([]);
const tableRowIndex = ref(0);
const isEdit = ref(false);
const modal = ref();
const listVoucher = ref();
const lewatiModal = ref();
const principalProducts = ref([]);
const availableVoucher = ref([]);
const submitLoading = ref(false);
const potonganSales = ref(0);
const multiSelectRegularVoucher = ref([]);

// key local state to force some component to re render every key change
const tableKey = ref(0);
const selectKey = ref(0);

// form state
const { configProps, defineField, handleSubmit, resetForm } =
  useCommonForm(tambahProdukSchema);
const [namaProduk, namaProdukProps] = defineField("namaProduk", configProps);
const [pieces, piecesProps] = defineField("pieces", configProps);
const [box, boxProps] = defineField("box", configProps);
const [karton, kartonProps] = defineField("karton", configProps);
const [kodeVoucher] = defineField("kodeVoucher");

// local store
const headerFields = reactive({
  nota_order: "",
  tanggal_order: "",
});
const tanggalJatuhTempo = ref(null);
const keteranganTidakOrder = ref("");
const resetLewatiTextArea = () => (keteranganTidakOrder.value = "");
const selectedVouchers = ref({});
const selectedVouchers2 = ref({});

const voucherRegularSelected = computed(() =>
  multiSelectRegularVoucher.value.map((val) =>
    voucher.allVoucher.find((v) => v.kode_voucher === val)
  )
);

const subTotalBeforeDiscount = computed(() => {
  if (salesRequest.value) {
    return checkNaN(
      salesRequest.value
        .reduce((total, produk) => total + (produk.totalHarga || 0), 0)
        .toFixed(0)
    );
  }

  return 0;
});

const subTotal = computed(() => {
  if (salesRequest.value) {
    return checkNaN(
      salesRequest.value
        .reduce((total, produk) => total + produk.jumlahHarga, 0)
        .toFixed(0)
    );
  }

  return 0;
});

const diskon1Price = computed(() => {
  if (!multiSelectRegularVoucher.value.length) return 0;

  const diskon = multiSelectRegularVoucher.value
    .map((kode) => {
      return voucher.allVoucher.find(
        (voucher) => voucher.kode_voucher === kode
      );
    })
    .reduce((akumulasiDiskon, diskon) => {
      if (subTotal.value >= diskon?.minimal_total_pembelian) {
        const nilaiDiskon = discountWithNilaiDiskon(diskon, subTotal.value);
        return akumulasiDiskon - nilaiDiskon;
      }
    }, subTotal.value);

  return checkNaN(subTotal.value - diskon);
});

const diskon2Price = computed(() =>
  checkNaN(
    Object.values(selectedVouchers2.value).reduce(
      (total, val) => total + val,
      0
    )
  )
);

const nilaiTotalDiskon = computed(() =>
  checkNaN(diskon1Price.value + diskon2Price.value)
);

const subtotalAfterDiscount = computed(() => {
  if (!salesRequest.value.length) return 0;

  const diskonFinal = subTotal.value - diskon1Price.value;

  return diskonFinal;
});

const pajak = computed(() => {
  return checkNaN((11 / 100) * subtotalAfterDiscount.value);
});

const total = computed(() => {
  if (salesRequest.value.length) {
    const finalTotal =
      parseInt(subTotalBeforeDiscount.value) + parseInt(pajak.value);

    return checkNaN(finalTotal.toFixed(0));
  }

  return 0;
});

/**
 * mendapatkan diskon berdasarkan nilai_diskon
 * dari voucher, jika diskon asli melebihi nilai_diskon
 * maka diskon yang didapat tidak akan melebihi nilai diskon
 * @param voucher objek voucher
 * @param criterion1 nilai yang digunakan untuk mendapatkan
 * diskon asli, nilai diskon, dan diskon setelah kalkulasi
 * @param criterion2 nilai yang digunakan untuk diskon setelah kalkulasi
 * jika kosong akan digantikan parameter criterion1
 */
const discountWithNilaiDiskon = (voucher, criterion1, criterion2) => {
  const voucherTable = voucher.kode_voucher.split("-").slice(-1)[0];
  const maxDiscountValue =
    (voucher[`persentase_diskon_${voucherTable}`] / 100) * criterion1;

  if (maxDiscountValue > voucher.nilai_diskon) {
    const nilaiDiskon = (voucher.nilai_diskon / criterion1) * 100;
    const disc = (nilaiDiskon / 100) * (criterion2 ? criterion2 : criterion1);
    return disc;
  }

  return maxDiscountValue;
};

/**
 * Mengkalkulasikan produk yang dipilih oleh user dengan jumlah produk dan diskon dari voucher yang dipilih
 * TODO: refactor this function cause its look ugly
 * @param box jumlah produk dalam box
 * @param karton jumlah produk dalam karton
 * @param namaProduk id dari produk yang dipilih
 * @param kodeVoucher array kode_voucher dari voucher yang dipilih
 */
const getCalculation = ({ box, karton, namaProduk, pieces, kodeVoucher }) => {
  const localproduk = salesRequest.value.find(
    (produk) => produk.id === namaProduk
  );

  // mendapatkan info produk yang dipilih
  const produk = salesRequestStore.initialProducts.find(
    (product) => product.id === namaProduk
  );

  const getHarga = () => {
    const hargaPerPieces = produk.harga_jual * pieces;
    const hargaPerBox = produk.harga_jual * produk.konversi_2 * box;
    const hargaPerKarton =
      produk.harga_jual * produk.konversi_2 * produk.konversi_3 * karton;

    return hargaPerPieces + hargaPerBox + hargaPerKarton;
  };

  // set selected voucher as global key, value object
  selectedVouchers.value[localproduk ? localproduk.id : namaProduk] =
    kodeVoucher ? kodeVoucher : [];

  if (kodeVoucher?.length) {
    const getVoucher = kodeVoucher.map((kode) => {
      return voucher.allVoucher.find(
        (voucher) => voucher.kode_voucher === kode
      );
    });

    /**
     * mendapatkan info voucher yang dipilih
     * dan menambahkan setiap diskonnya
     * */
    const diskon = getVoucher
      .map((voucher) => ({
        vouchers: voucher.kode_voucher,
        disc1: voucher.persentase_diskon_1,
        disc2: voucher.persentase_diskon_2,
        disc3: voucher.persentase_diskon_3,
      }))
      .reduce((akumulasiDiskon, diskon) => {
        for (const key in diskon) {
          if (akumulasiDiskon.hasOwnProperty(key)) {
            if (typeof diskon[key] === "string") {
              akumulasiDiskon[key].push(diskon[key]);
            } else {
              akumulasiDiskon[key] += diskon[key];
            }
          } else {
            if (typeof diskon[key] === "string") {
              akumulasiDiskon[key] = [diskon[key]];
            } else {
              akumulasiDiskon[key] = diskon[key];
            }
          }
        }

        return akumulasiDiskon;
      }, {});

    const harga = getHarga();

    const subTotalDiskon = getVoucher.reduce((akumulasiDiskon, voucher) => {
      if (harga >= voucher.minimal_subtotal_pembelian) {
        const nilaiDiskon = discountWithNilaiDiskon(
          voucher,
          harga,
          akumulasiDiskon
        );
        return akumulasiDiskon - nilaiDiskon;
      }
    }, harga);

    /**
     * memisahkan voucher produk / voucher 2 dari voucher lainnya
     * dan membuat array of objek dengan kode voucher dan diskon
     * yang di dapat
     */

    const arrayOfVoucherObject = getVoucher.reduce((vouchers, voucher) => {
      let vouchersObject = vouchers.find(
          (val) => val.kode_voucher === voucher.kode_voucher
        ),
        nilaiDiskon = 0,
        diskon = 0;

      // get diskon berdasar total harga per produk
      if (harga >= voucher.minimal_subtotal_pembelian) {
        nilaiDiskon = discountWithNilaiDiskon(voucher, harga);
        diskon =
          voucher[
            `persentase_diskon_${
              voucher?.kode_voucher.split("-").splice(-1)[0]
            }`
          ];
      }

      if (!vouchersObject) {
        vouchers.push({
          id: voucher.id,
          kode: voucher?.kode_voucher,
          nilai_diskon: 0,
          diskon,
        });
      }

      return vouchers;
    }, []);

    console.log("array of object :", arrayOfVoucherObject);

    // const discount2 = (subTotalDiskon / 100) * harga;
    const discount2 = harga - subTotalDiskon;
    const discount3 = (diskon.disc3 / 100) * (harga - discount2);
    const finalPrice = harga - (discount2 + discount3);
    const diskonPrice = discount2 + discount3;
    const totalDisc = diskon.disc1 + diskon.disc2 + diskon.disc3;

    selectedVouchers2.value[localproduk ? localproduk.id : namaProduk] =
      discount2;

    return {
      ...produk,
      ...diskon,
      vouchersDetail: arrayOfVoucherObject,
      harga_jual: produk.harga_jual,
      uom3: pieces,
      uom2: box,
      uom1: karton,
      totalDisc,
      diskonPrice: 0,
      totalHarga: harga,
      jumlahHarga: harga,
    };
  } else {
    selectedVouchers2.value[localproduk ? localproduk.id : namaProduk] = 0;
    return {
      ...produk,
      vouchers: [],
      vouchersDetail: [],
      disc1: 0,
      disc2: 0,
      disc3: 0,
      uom3: pieces,
      uom2: box,
      uom1: karton,
      totalDisc: 0,
      diskonPrice: 0,
      totalHarga: getHarga(),
      jumlahHarga: getHarga(),
    };
  }
};

const getFreeProduct = (vouchers) => {
  return vouchers
    .map((vou) => {
      const voucherStore = voucher.allVoucher.find(
        (voucher) => voucher.kode_voucher === vou
      );
      return voucherStore.free_produk.map((free) => ({
        kode_voucher: voucherStore.kode_voucher,
        ...free,
      }));
    })
    .filter((voucher) => voucher.length !== 0)
    .flat();
};

const restructureFreeProduct = () => {
  const newFreeProduct = salesRequest.value
    .map((produk) => {
      return getFreeProduct(produk.vouchers);
    })
    .filter((produk) => produk.length !== 0)
    .flat()
    .map((produk, idx) => ({
      no: idx + 1,
      ...produk,
    }));

  freeProducts.value = newFreeProduct;
};

const tambahProduk = handleSubmit((values) => {
  if (salesRequest.value.some((produk) => produk.id === values.namaProduk)) {
    const produk = salesRequest.value.find(
      (produk) => produk.id === values.namaProduk
    );

    tableRowIndex.value = salesRequest.value.findIndex(
      (produk) => produk.id === values.namaProduk
    );
    const { uom1: karton, uom2: box, uom3: pieces } = produk;
    const kodeVoucher = values.kodeVoucher
      ? produk.vouchers.concat(values.kodeVoucher)
      : produk.vouchers;
    const valuesAfter = {
      ...values,
      box: box + values.box,
      karton: karton + values.karton,
      pieces: pieces + values.pieces,
      kodeVoucher: kodeVoucher,
    };

    editprodukBeforeForm(valuesAfter);
  } else {
    const tableData = getCalculation({ ...values });
    // const voucherFreeProducts = getFreeProduct(values.kodeVoucher);

    salesRequest.value.push(tableData);
    // voucherFreeProducts && freeProducts.value.push(voucherFreeProducts);

    restructureFreeProduct();
  }

  tableKey.value = tableKey.value + 1;
  closeModal();
});

const editprodukBeforeForm = (values) => {
  const tableData = getCalculation({ ...values });
  salesRequest.value[tableRowIndex.value] = tableData;

  restructureFreeProduct();

  tableKey.value++;
  closeModal();
};

const editProduk = handleSubmit((values) => editprodukBeforeForm(values));

const removeProduct = (val) => {
  selectedVouchers.value[salesRequest.value[val.rowIndex].id] = [];
  selectedVouchers2.value[salesRequest.value[val.rowIndex].id] = 0;
  salesRequest.value.splice(val.rowIndex, 1);
  restructureFreeProduct();
  tableKey.value = tableKey.value + 1;
};

const openTambahModal = () => {
  isEdit.value = false;
  resetForm();
  nextTick(() => {
    modal.value.show();
  });
};

const openRegularVoucherModal = async () => {
  await voucher.getAllVoucher();

  getRegularVoucher();
  nextTick(() => listVoucher.value.show());
};

const resettingVoucher = async (tipeVoucher) => {
  await voucher.getAllVoucher();

  availableVoucher.value = [];
  openTambahModal();
};

const openEditModal = (val) => {
  isEdit.value = true;
  principalId.value = val.value.principalId;
  tableRowIndex.value = val.rowIndex;

  namaProduk.value = val.value.namaProduk;
  pieces.value = val.value.pieces;
  box.value = val.value.box;
  karton.value = val.value.karton;
  kodeVoucher.value = val.value.kodeVoucher;

  nextTick(() => {
    modal.value.show();
  });
};

const resetFormModal = () => {
  availableVoucher.value = [];
  resetForm();
};

const closeModal = () => {
  resetFormModal();
  modal.value.hide();
};

/**
 * mendapatkan semua resources sales request
 * seperti piutang, voucher, initial produk yang akan
 * direquest oleh sales
 */
const getResources = async () => {
  if (!principalStore.principalProduct.products.length) {
    await principalStore.getPrincipalProducts();
  }

  if (!piutang.listPiutang.length) {
    await piutang.getPiutang(
      kunjungan.activeKunjungan.kunjungan.user_id,
      kunjungan.activeKunjungan.kunjungan.customer_id
    );
  }

  if (!voucher.allVoucher.length) await voucher.getAllVoucher();

  if (!salesRequestStore.initialProducts.length)
    await salesRequestStore.getSalesRequest();

  salesRequest.value = [...salesRequestStore.initialProducts];
  tableKey.value = tableKey.value + 1;
};

/**
 * Mendapatkan produk principal
 * TODO: produk principal ikut berubah sesuai principal pada modal edit seperti perilaku modal tambah
 */
function getprincipalProducts() {
  if (!isEdit.value) namaProduk.value = 0;
  principalProducts.value = salesRequestStore.initialProducts.filter(
    (product) => product.id_principal === principalId.value
  );
}

/**
 * Mendapatkan produk voucher berdasar produk yang dipilih
 * TODO: produk voucher ikut berubah sesuai produk pada modal edit seperti perilaku modal tambah
 */
const getVouchers = (isRegularVoucher = false) => {
  let produkVoucher = [];
  let vouchers = null;
  availableVoucher.value = [];

  if (!isEdit.value) kodeVoucher.value = null;

  if (isRegularVoucher) {
    console.log("sales request getVoucher : ", salesRequest.value);
    const currentPrincipalIds = salesRequest.value
      .map((produk) => produk.id_principal)
      .reduce((finals, current) => {
        const currId = finals.find((final) => final === current);

        if (!currId) finals.push(current);
        return finals;
      }, []);

    console.log("principal ids : ", currentPrincipalIds);
    vouchers = currentPrincipalIds
      .map((id) => {
        return voucher.voucher1.filter((val) => val.id_principal === id);
      })
      .flat()
      .filter((voucher) => voucher);

    console.log("voucher after reduce : ", vouchers);
  } else {
    vouchers = voucher.voucher2.filter(
      (voucher) => voucher.id_produk === namaProduk.value
    );
  }

  const voucher_3 = voucher.voucher3.filter(
    (voucher) =>
      voucher.id_product === namaProduk.value &&
      voucher.tipe_voucher === (isRegularVoucher ? 1 : 0)
  );

  console.log("voucher 3 : ", voucher_3);

  // const voucher_2 = salesRequestStore.initialProducts.find(
  //   (produk) => produk.id === namaProduk.value
  // ).produk_vouchers;

  const voucherTemp = [...vouchers, ...voucher_3].map((voucher, idx) => ({
    no: idx + 1,
    ...voucher,
  }));

  if (!isRegularVoucher) {
    const produk = salesRequest.value.find(
      (produk) => produk.id === namaProduk.value
    );

    if (produk) {
      produkVoucher = voucherTemp.filter((voucherList) => {
        if (
          produk.vouchers.some(
            (kodeVoucher) => kodeVoucher === voucherList.kode_voucher
          )
        ) {
          return voucherList;
        }
      });
    }

    const selectedVoucherRef = Object.keys(selectedVouchers.value)
      .map((key) => {
        if (selectedVouchers.value[key]) {
          return selectedVouchers.value[key];
        }
      })
      .flat();

    const filteredVoucher = voucherTemp.filter((voucherList) => {
      if (
        !selectedVoucherRef.some(
          (selected) => selected === voucherList.kode_voucher
        )
      ) {
        return voucherList;
      }
    });

    const concatingVoucher = isEdit.value
      ? produkVoucher.concat(filteredVoucher)
      : filteredVoucher;
    availableVoucher.value = [...concatingVoucher].sort((a, b) => a.no - b.no);
  } else {
    availableVoucher.value = [...voucherTemp].sort((a, b) => a.no - b.no);
  }

  selectKey.value++;
};

const getProductVouchers = () => namaProduk.value && getVouchers();

const getRegularVoucher = () => getVouchers(true);

const submitOrder = async () => {
  if (
    Object.keys(headerFields)
      .map((key) => headerFields[key])
      .some((value) => value === "")
  ) {
    const fieldKosong = Object.keys(headerFields)
      .map((key) => {
        if (!headerFields[key]) return key.split("_").join(" ");
        else return null;
      })
      .filter((value) => value !== null);

    alert.setMessage(`Field : ${fieldKosong.join(", ")} Kosong`, "danger");
  } else if (!salesRequest.value.length) {
    alert.setMessage(`List Order Kosong`, "danger");
  } else if (
    !salesRequest.value.every(
      (produk) => produk.id_principal === salesRequest.value[0].id_principal
    )
  ) {
    alert.setMessage(
      "Anda memilih lebih dari satu principal, cukup pilih satu principal per faktur",
      "danger"
    );
  } else {
    const voucherRegular = multiSelectRegularVoucher.value.map(
      (kodeVoucher) => {
        let v = voucher.allVoucher.find(
            (val) => val.kode_voucher === kodeVoucher
          ),
          nilaiDiskon = 0,
          diskon = 0;

        if (subTotal.value >= v.minimal_total_pembelian) {
          nilaiDiskon = discountWithNilaiDiskon(v, subTotal.value);
          diskon =
            v[`persentase_diskon_${kodeVoucher.split("-").splice(-1)[0]}`];
        }

        return {
          id: v.id,
          kode_voucher: kodeVoucher,
          nilai_diskon: 0,
          diskon: diskon,
        };
      }
    );

    const request = {
      id_plafon: kunjungan.activeKunjungan.kunjungan.id_plafon,
      no_sales_order: headerFields.nota_order,
      tanggal_order: headerFields.tanggal_order,
      nama_sales: sales.salesUser.nama,
      subtotal_penjualan: parseFloat(subTotal.value - diskon1Price.value),
      subtotal_diskon: parseFloat(nilaiTotalDiskon.value),
      total_penjualan: parseFloat(total.value),
      tanggal_jatuh_tempo: tanggalJatuhTempo.value,
      // voucher regular
      kode_vouchers: voucherRegular,
      products: salesRequest.value.map((produk) => ({
        id_produk: produk.id,
        disc2: produk.disc2,
        disc3: produk.disc3,
        vouchers: produk.vouchersDetail,
        pieces_order: produk.uom3,
        box_order: produk.uom2,
        karton_order: produk.uom1,
        subtotalorder: produk.jumlahHarga,
      })),
    };

    submitLoading.value = true;

    try {
      await fetchWithAuth("POST", `${apiUrl}/api/sales/sales-request`, request);

      alert.setMessage(
        `Berhasil request produk dengan no order: ${headerFields.nota_order}`,
        "success"
      );

      dashboard.getDashboardInfo(sessionDisk.getSession("authUser").id_user);

      headerFields.nota_order = "";
      headerFields.tanggal_order = "";

      salesRequest.value = salesRequestStore.initialProducts;
      freeProducts.value = [];

      selectedVouchers.value = {};
      selectedVouchers2.value = {};

      tableKey.value++;
      selectKey.value++;
    } catch (error) {
      alert.setMessage(error, "danger");
    }

    console.log("request : ", request);

    submitLoading.value = false;
  }
};

const checkCurrencyMinus = (value) => {
  return value < 1 ? 0 : parseCurrency(value);
};

watch(principalId, () => getprincipalProducts());

watch(namaProduk, () => getProductVouchers());

watch(kunjungan.activeKunjungan.kunjungan, () => {
  piutang.$reset();
  voucher.$reset();
  salesRequest.$reset();

  getResources();
});

onMounted(() => {
  getResources();
});
</script>

<template>
  <FlexBox full flex-col class="lg:tw-pl-6 tw-pl-2">
    <SlideRightX
      class="tw-w-full tw-z-20"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.1"
      :delay-out="0.1"
      :initial-x="-40"
      :x="40">
      <Card dense no-subheader class="tw-pb-10">
        <template #header>Form Sales Request Order</template>
        <template #content>
          <FlexBox flex-col>
            <FlexBox it-center class="px-4 tw-flex-col lg:tw-flex-row">
              <FlexBox flex-col gap="small">
                <span class="tw-font-semibold">Sales</span>
                <BFormInput
                  class="lg:tw-w-[270px] tw-w-full"
                  disabled
                  :model-value="sales.salesUser.nama" />
              </FlexBox>
              <FlexBox flex-col gap="small">
                <span class="tw-font-semibold">Customer</span>
                <BFormInput
                  class="lg:tw-w-[270px] tw-w-full"
                  :title="kunjungan.activeKunjungan.kunjungan.nama_customer"
                  disabled
                  :model-value="
                    kunjungan.activeKunjungan.kunjungan.nama_customer
                  " />
              </FlexBox>
              <FlexBox flex-col gap="small">
                <span class="tw-font-semibold">Nota Order</span>
                <BFormInput
                  v-model="headerFields.nota_order"
                  class="lg:tw-w-[270px] tw-w-full" />
              </FlexBox>
            </FlexBox>
            <FlexBox it-center class="px-4 tw-flex-col lg:tw-flex-row">
              <FlexBox flex-col gap="small">
                <span class="tw-font-semibold">Tanggal Order</span>
                <div
                  class="lg:tw-w-[270px] tw-w-full tw-border tw-border-slate-300 tw-rounded-sm">
                  <VueDatePicker
                    v-model="headerFields.tanggal_order"
                    :enable-time-picker="false"
                    placeholder="mm/dd/yyyy"
                    :teleport="true"
                    auto-apply />
                </div>
              </FlexBox>
              <FlexBox flex-col gap="small">
                <span class="tw-font-semibold">Tanggal Jatuh Tempo</span>
                <div
                  class="lg:tw-w-[270px] tw-w-full tw-border tw-border-slate-300 tw-rounded-sm">
                  <VueDatePicker
                    v-model="tanggalJatuhTempo"
                    :enable-time-picker="false"
                    placeholder="mm/dd/yyyy"
                    :teleport="true"
                    auto-apply />
                </div>
              </FlexBox>
            </FlexBox>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="tw-w-full"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.2"
      :delay-out="0.2"
      :initial-x="-40"
      :x="40">
      <Card no-subheader class="tw-pb-8">
        <template #header>Info Sisa Plafon dan Piutang</template>
        <template #content>
          <div class="tw-w-full lg:tw-w-[60%]">
            <Table
              classic
              :key="piutang.tableKey"
              :loading="piutang.loading"
              :columns="sisaPlafonColumns"
              :table-data="piutang.listPiutang"
              hide-footer
              hide-toolbar />
          </div>
        </template>
      </Card>
    </SlideRightX>
    <SlideRightX
      class="tw-w-full"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.3"
      :delay-out="0.3"
      :initial-x="-40"
      :x="40">
      <FlexBox full jus-end>
        <Button
          :trigger="resettingVoucher"
          class="tw-bg-blue-600 tw-border-none tw-w-40 tw-h-10">
          <i class="mdi mdi-plus tw-text-xl tw-mr-2"></i>
          Tambah Produk
        </Button>
        <BButton
          @click="lewatiModal.show()"
          class="tw-bg-red-500 tw-border-none tw-w-64 tw-h-10">
          <i class="mdi mdi-block-helper tw-mr-2"></i>
          Lewati Sales Request
        </BButton>
      </FlexBox>
    </SlideRightX>
    <SlideRightX
      class="tw-w-full"
      :duration-enter="0.6"
      :duration-leave="0.6"
      :delay-in="0.4"
      :delay-out="0.4"
      :initial-x="-40"
      :x="40">
      <Card dense no-subheader class="tw-pb-10">
        <template #header>List Order</template>
        <template #content>
          <FlexBox full jus-end class="tw-flex-col lg:tw-flex-row tw-px-4">
            <!-- modal untuk tambah atau edit -->
            <Modal id="modal" @modal-closed="resetFormModal" ref="modal">
              <Card dense no-subheader no-main-center class="tw-p-4">
                <template #header>
                  <span class="tw-text-black">
                    {{ isEdit ? "Edit" : "Tambah" }} Produk
                  </span>
                </template>
                <template #content>
                  <FlexBox full>
                    <BForm
                      novalidate
                      class="tw-w-full tw-flex tw-flex-col tw-gap-6">
                      <FlexBox full flex-col gap="small">
                        <span class="tw-font-semibold">Principal</span>
                        <SelectInput
                          :disabled="isEdit"
                          :search="true"
                          placeholder="Pilih Principal"
                          :style="[{ height: '45px' }]"
                          :options="principal.principals"
                          v-model="principalId"
                          text-field="nama"
                          value-field="id" />
                      </FlexBox>
                      <BFormGroup
                        id="input-group-1"
                        label="Nama Produk:"
                        label-for="input-1"
                        v-bind="namaProdukProps">
                        <SelectInput
                          :disabled="isEdit"
                          placeholder="Pilih Produk"
                          text-field="nama"
                          :search="true"
                          value-field="id"
                          size="md"
                          :options="principalProducts"
                          v-model="namaProduk" />
                      </BFormGroup>
                      <TextField
                        group-id="input-group-2"
                        label-for="input-2"
                        :config-props="piecesProps"
                        v-model="pieces"
                        type="number"
                        label="Jml UOM 3 / Pieces"
                        placeholder="Masukkan Jumlah dalam Pieces" />
                      <TextField
                        group-id="input-group-3"
                        label-for="input-3"
                        :config-props="boxProps"
                        v-model="box"
                        type="number"
                        label="Jml UOM 2 / Box"
                        placeholder="Masukkan Jumlah dalam box" />
                      <TextField
                        group-id="input-group-4"
                        label-for="input-4"
                        :config-props="kartonProps"
                        v-model="karton"
                        type="number"
                        label="Jml UOM 1 / Karton"
                        placeholder="Masukkan Jumlah dalam Karton" />
                      <MultipleSelect
                        :key="selectKey"
                        label="Kode Voucher"
                        placeholder="Pilih Kode Voucher"
                        :options="availableVoucher"
                        v-model="kodeVoucher"
                        :text-field="voucher.allVoucher ? 'nama_voucher' : ''"
                        :value-field="voucher.allVoucher ? 'kode_voucher' : ''"
                        fieldname="kodeVoucher"
                        :max-selected-displayed="3"
                        size="md"
                        :search="true"
                        :errors="errors" />
                      <FlexBox full jus-end>
                        <BButton
                          @click="closeModal"
                          class="tw-bg-red-600 tw-border-none">
                          Cancel
                        </BButton>
                        <BButton
                          @click="isEdit ? editProduk() : tambahProduk()"
                          type="submit"
                          class="tw-bg-green-500 tw-border-none">
                          {{ isEdit ? "Update" : "Submit" }}
                        </BButton>
                      </FlexBox>
                    </BForm>
                  </FlexBox>
                </template>
              </Card>
            </Modal>
            <Modal
              id="lewati-modal"
              @modal-closed="resetLewatiTextArea"
              ref="lewatiModal">
              <Card no-subheader no-main-center class="tw-pb-5">
                <template #header>
                  <span class="tw-text-xl tw-text-black">
                    Keterangan / Alasan Tidak Order
                  </span>
                </template>
                <template #content>
                  <FlexBox full flex-col it-end gap="extra large">
                    <BFormTextarea
                      id="textarea"
                      v-model="keteranganTidakOrder"
                      placeholder="Masukkan Alasan"
                      rows="8" />
                    <FlexBox>
                      <BButton
                        class="tw-bg-red-500"
                        @click="lewatiModal.hide()">
                        Cancel
                      </BButton>
                      <BButton class="tw-bg-green-500">Submit</BButton>
                    </FlexBox>
                  </FlexBox>
                </template>
              </Card>
            </Modal>
            <Modal id="listVoucher" ref="listVoucher" centered>
              <Card no-subheader no-header class="tw-py-5">
                <template #content>
                  <FlexBox full flex-col jus-center>
                    <span class="tw-text-xl tw-font-black">
                      Pilih Regular Voucher
                    </span>
                    <BForm
                      novalidate
                      class="tw-w-full tw-flex tw-flex-col tw-gap-6">
                      <MultipleSelect
                        :key="selectKey"
                        placeholder="Pilih Kode Voucher"
                        :options="availableVoucher"
                        v-model="multiSelectRegularVoucher"
                        :text-field="voucher.allVoucher ? 'nama_voucher' : ''"
                        :value-field="voucher.allVoucher ? 'kode_voucher' : ''"
                        :max-selected-displayed="4"
                        size="md"
                        :search="true" />
                    </BForm>
                  </FlexBox>
                </template>
              </Card>
            </Modal>
          </FlexBox>
          <FlexBox full>
            <Table
              :loading="salesRequestStore.loading"
              :key="tableKey"
              :columns="listOrderColumns"
              hide-footer
              hide-toolbar
              :table-data="salesRequest"
              classic
              @open-row-modal="(val) => openEditModal(val)"
              @remove-row="(val) => removeProduct(val)" />
          </FlexBox>
          <FlexBox full jus-start it-center class="tw-pl-4">
            <Button
              :trigger="openRegularVoucherModal"
              class="tw-flex tw-gap-2 tw-w-40 tw-h-9">
              <i class="mdi mdi-plus" />
              Voucher Reguler
            </Button>
            <FlexBox
              class="tw-border tw-border-slate-400 tw-cursor-default tw-select-none tw-border-dashed tw-rounded-md tw-py-1 tw-px-4"
              v-for="voucherVal in voucherRegularSelected"
              :key="voucherVal?.kode_voucher"
              it-center
              gap="small">
              <i class="mdi mdi-ticket tw-text-yellow-500" />
              <span class="tw-text-slate-500 tw-text-xs tw-capitalize">
                {{ voucherVal?.nama_voucher }}
              </span>
            </FlexBox>
          </FlexBox>
          <FlexBox gap="small" it-end flex-col full class="tw-px-4">
            <table>
              <!-- <tr>
                <td>Sub Total (Before Discount)</td>
                <td class="tw-text-center">:</td>
                <td class="tw-text-end">
                  Rp. {{ checkCurrencyMinus(subTotalBeforeDiscount) }}
                </td>
              </tr>
              <tr>
                <td>Diskon Produk</td>
                <td class="tw-text-center">:</td>
                <td class="tw-text-end">
                  Rp. {{ checkCurrencyMinus(diskon2Price.toFixed(0)) }}
                </td>
              </tr>
              <tr>
                <td>Diskon Reguler</td>
                <td class="tw-text-center">:</td>
                <td class="tw-text-end">
                  Rp. {{ checkCurrencyMinus(diskon1Price.toFixed(0)) }}
                </td>
              </tr> -->
              <tr>
                <td>Sub Total</td>
                <td class="tw-text-center">:</td>
                <td class="tw-text-end">
                  Rp.
                  {{ checkCurrencyMinus(subTotal - diskon1Price.toFixed(0)) }}
                </td>
              </tr>
              <!-- <tr>
                <td>Diskon 3</td>
                <td class="tw-text-center">:</td>
                <td>
                  <div
                    :class="[
                      'tw-flex tw-flex-row tw-items-center',
                      subTotal == 0 ? 'tw-w-4 tw-gap-1' : 'tw-w-40 tw-gap-2',
                    ]"
                  >
                    <span>Rp.</span>
                    <span v-if="subTotal == 0">0</span>
                    <BFormInput v-model="potonganSales" v-else />
                  </div>
                </td>
              </tr> -->
              <tr>
                <td>PPN 11%</td>
                <td class="tw-text-center">:</td>
                <td class="tw-text-end">
                  Rp. {{ checkCurrencyMinus(pajak.toFixed(0)) }}
                </td>
              </tr>
              <tr class="tw-font-extrabold">
                <td>Total</td>
                <td class="tw-text-center tw-w-16">:</td>
                <td class="tw-text-end">Rp. {{ checkCurrencyMinus(total) }}</td>
              </tr>
            </table>
          </FlexBox>
          <FlexBox full jus-end class="tw-px-4">
            <Button
              v-if="!freeProducts.length"
              :trigger="submitOrder"
              class="tw-bg-green-500 tw-border-none tw-w-28 tw-h-9">
              <i class="mdi mdi-check tw-mr-2"></i>
              Submit
            </Button>
          </FlexBox>
        </template>
      </Card>
    </SlideRightX>
    <Card v-if="freeProducts.length" no-subheader class="tw-pb-8">
      <template #header>List Free Produk</template>
      <template #content>
        <FlexBox full flex-col it-end>
          <Table
            :key="tableKey"
            :columns="listFreeProductsColumns"
            :table-data="freeProducts"
            hide-footer
            hide-toolbar />
          <FlexBox full>
            <span class="tw-text-sm tw-text-blue-500">
              {{ `* Tergantung ketersediaan stock produk` }}
            </span>
          </FlexBox>
          <Button :trigger="submitOrder" class="tw-bg-green-500">
            <i class="mdi mdi-check tw-mr-2"></i>
            Submit
          </Button>
        </FlexBox>
      </template>
    </Card>
  </FlexBox>
</template>
