import { reduce } from "./compose";

const GENERATE_DATA_COUNT = 1000;

function generateDummmy(columnList) {
  let generateDummyList = [];

  for (let i = 0; i < GENERATE_DATA_COUNT; i++) {
    let newObject = reduce(columnList)((acc, curr, idx) => {
      acc[curr] = `Test ${curr} ${idx}.${i}`;
      return acc;
    });

    generateDummyList.push(newObject);
  }

  return generateDummyList;
}

export const voucherDummy = generateDummmy([
  "row_num",
  "kode_principal",
  "principal",
  "kode_voucher",
  "tanggal_berlaku",
  "tanggal_berakhir",
  "limit_diskon",
]);
