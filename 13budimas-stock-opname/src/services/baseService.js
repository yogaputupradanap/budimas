export class baseService {
  constructor() {
    this.serviceName = "";
  }
  deduplication(
    sourceData,
    columns = [],
    {
      keyId1 = "id_stock_transfer",
      keyId2 = "id_stock_transfer",
      sumKeys = ["jumlah", "jumlah_diterima", "jumlah_picked"],
      appendKeys = [],
    } = {}
  ) {
    const removeDuplicate = (acc, val) => {
      const checkExistingValue = acc.find((i) => i[keyId1] === val[keyId2]);

      if (!checkExistingValue) {
        acc.push(val);
      } else {
        sumKeys.length &&
          sumKeys.forEach((item) => {
            checkExistingValue[item] += val[item];
          });
        appendKeys.length &&
          appendKeys.forEach((item) => {
            if (checkExistingValue[item]) {
              const isArray = Array.isArray(checkExistingValue[item]);
              const value = isArray
                ? checkExistingValue[item].concat(val[item])
                : [checkExistingValue[item]];

              checkExistingValue[item] = value;
            }
          });
      }
      return acc;
    };

    const selectColumn = (acc, val) => {
      const select = columns.reduce((objects, object) => {
        objects[object] = val[object];
        return objects;
      }, {});

      acc.push(select);
      return acc;
    };

    const data = sourceData.reduce(removeDuplicate, []);
    const selectedColums =
      columns.length > 0 ? data.reduce(selectColumn, []) : data;

    return selectedColums;
  }
  setServiceName(serviceName) {
    this.serviceName = serviceName;
  }
  throwError(error) {
    const message = `error while do some operation on ${this.serviceName} service with -> ${error}`;
    throw message;
  }
}
