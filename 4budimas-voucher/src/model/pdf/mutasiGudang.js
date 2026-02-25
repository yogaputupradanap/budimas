import { parseCurrency } from "@/src/lib/utils";
import { format } from "date-fns";

export function definition(datas) {
  const listStockTransfer = datas.listStockTransfer.map((val) => {
    const mapProduk = (list, key, currency) => {
      return list.map((val) => ({
        text: currency ? parseCurrency(val[key]) : val[key],
        style: "tableBodySubheader",
      }));
    };

    const reduceHarga = (acc, val) => {
      acc += val.jumlah_harga;
      return acc;
    };

    const tanggal = format(new Date(val.created_at), "dd/MM/yyyy");
    const stockTransfer = {
      layout: "lightHorizontalLines",
      margin: [0, 10, 0, 0],
      table: {
        widths: ["10%", "30%", "8%", "8%", "8%", "10%", "13%", "15%"],
        body: [
          [
            { text: "Stok", style: "tableHeader" },
            { text: "Nama", style: "tableHeader" },
            { text: "UOM1", style: "tableHeader" },
            { text: "UOM2", style: "tableHeader" },
            { text: "UOM3", style: "tableHeader" },
            { text: "Jumlah", style: "tableHeader" },
            { text: "Harga", style: "tableHeader" },
            { text: "Jumlah Harga", style: "tableHeader" },
          ],
          [
            {
              stack: [
                {
                  text: " ",
                  style: "tableBodyHeader",
                },
                ...mapProduk(val.listProduk, "kode_sku"),
              ],
            },
            {
              stack: [
                {
                  text: `${tanggal} - DEPO${val.id_cabang_tujuan} - DEPO ${val.nama_cabang_tujuan}`,
                  style: "tableBodyHeader",
                },
                ...mapProduk(val.listProduk, "nama_produk"),
              ],
            },
            {
              stack: [
                { text: " ", style: "tableBodyHeader" },
                ...mapProduk(val.listProduk, "pieces"),
              ],
            },
            {
              stack: [
                { text: " ", style: "tableBodyHeader" },
                ...mapProduk(val.listProduk, "box"),
              ],
            },
            {
              stack: [
                { text: " ", style: "tableBodyHeader" },
                ...mapProduk(val.listProduk, "carton"),
              ],
            },
            {
              stack: [
                { text: " ", style: "tableBodyHeader" },
                ...mapProduk(val.listProduk, "jumlah_picked"),
              ],
            },
            {
              stack: [
                { text: " ", style: "tableBodyHeader" },
                ...mapProduk(val.listProduk, "harga", true),
              ],
            },
            {
              stack: [
                { text: " ", style: "tableBodyHeader" },
                ...mapProduk(val.listProduk, "jumlah_harga", true),
                { text: "----------------------" },
                {
                  text: parseCurrency(val.listProduk.reduce(reduceHarga, 0)),
                  fontSize: 6,
                  bold: true
                },
              ],
            },
          ],
        ],
      },
    };

    return stockTransfer;
  });

  const date = format(new Date(), "dd/MM/yyyy");
  const time = format(new Date(), "p")
  const tanggal = `${date}, ${time}`

  const startDate = format(
    new Date(datas.listStockTransfer[0]?.created_at),
    "dd/MM/yyyy"
  );
  const endDate = format(
    new Date(datas.listStockTransfer.at(-1)?.created_at),
    "dd/MM/yyyy"
  );

  const periode = `${startDate} - ${endDate}`;

  const dd = {
    pageMargins: [20, 20, 20, 20],
    footer: function (currentPage, pageSize) {
      return {
        text: `Page ${currentPage} of ${pageSize}`,
        fontSize: 6,
        alignment: "right",
        margin: [0, 0, 20, 0],
      };
    },
    content: [
      {
        width: "auto",
        text: `MUTASI GUDANG`,
        alignment: "center",
      },
      {
        canvas: [
          {
            type: "line",
            x1: 205,
            y1: 3,
            x2: 350,
            y2: 3,
            lineWidth: 1,
          },
        ],
      },
      {
        margin: [0, 10, 0, 0],
        columns: [
          {
            text: `PT. BUDIMAS MAKMUR MULIA*\nPeriode: ${periode} -UnClose-`,
            style: "subheader",
          },
          {
            text: `${datas.user.nama}\n${tanggal}`,
            style: "subheader",
            alignment: "right",
          },
        ],
      },
      ...listStockTransfer,
    ],
    styles: {
      header: {
        fontSize: 16,
        bold: true,
        margin: [0, 0, 0, 10],
      },
      subheader: {
        fontSize: 10,
        margin: [0, 10, 0, 5],
      },
      tableHeader: {
        bold: true,
        fontSize: 7,
        fillColor: "#eeeeee",
        alignment: "left",
      },
      tableRow: {
        fontSize: 8,
      },
      tableExample: {
        margin: [0, 10, 0, 10],
      },
      tableBodyHeader: {
        fontSize: 7,
        bold: true,
        fillColor: "#eeeeee",
      },
      tableBodySubheader: {
        fontSize: 6,
        margin: [0, 2, 0, 0],
      },
    },
    defaultStyle: {
      alignment: "justify",
    },
  };

  return dd;
}

// parameter 'datas' interface
const _ = {
  user: "user store interface",
  listStockTransfer: [
    {
      kode_cabang: "string",
      id_cabang_tujuan: "number",
      nama_cabang_tujuan: "string",
      listProduk: [
        {
          kode_sku: "string",
          nama_produk: "string",
          uom_1: "number",
          uom_2: "number",
          uom_3: "number",
          jumlah: "number",
          harga: "number",
          jumlah_harga: "number",
        },
      ],
    },
  ],
};
