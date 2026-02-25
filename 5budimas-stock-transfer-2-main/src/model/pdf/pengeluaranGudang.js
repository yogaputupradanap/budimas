import { format } from "date-fns";

export function definition(datas) {
  const mapProduk = (list, key, indexed) => {
    return list.map((val, idx) => ({
      text: indexed ? `${idx + 1}. ${val[key]}` : val[key],
      style: "tableBodySubheader",
    }));
  };
  const tanggal = format(new Date(), "dd-MM-yyyy");

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
        text: `BUKTI PENGELUARAN GUDANG ${datas.nama_cabang_awal.toUpperCase()} KE DEPO`,
        alignment: "center",
      },
      {
        canvas: [
          {
            type: "rect",
            x: 137,
            y: 14,
            w: 300,
            h: 25,
            lineWidth: 1,
            lineColor: "#000000",
            dash: { length: 4 },
          },
        ],
        margin: [-10, -35, 0, 0],
      },
      {
        margin: [0, 10, 0, 0],
        columns: [
          {
            text: `NOMOR : \nSALES : DEPO ${datas.nama_cabang_tujuan}`,
            style: "subheader",
          },
          {
            text: tanggal,
            style: "subheader",
            alignment: "right",
          },
        ],
      },
      {
        margin: [0, 10, 0, 0],
        table: {
          widths: ["15%", "*", "8%", "8%", "8%", "8%"],
          body: [
            [
              { text: "Kode", style: "tableHeader" },
              { text: "Barang", style: "tableHeader" },
              { text: "Jumlah", style: "tableHeader" },
              { text: "UOM3", style: "tableHeader" },
              { text: "UOM2", style: "tableHeader" },
              { text: "UOM1", style: "tableHeader" },
            ],
            [
              {
                stack: [...mapProduk(datas.listProduk, "kode_sku", true)],
              },
              {
                stack: [...mapProduk(datas.listProduk, "nama_produk")],
              },
              {
                stack: [...mapProduk(datas.listProduk, "jumlah_picked")],
              },
              {
                stack: [...mapProduk(datas.listProduk, "carton")],
              },
              {
                stack: [...mapProduk(datas.listProduk, "box")],
              },
              {
                stack: [...mapProduk(datas.listProduk, "pieces")],
              },
            ],
          ],
        },
      },
      {
        margin: [0, 50, 0, 0],
        columns: [
          {
            columns: [
              {
                stack: [
                  {
                    text: "GUDANG",
                    style: "subheader",
                    margin: [30, 0, 0, 0],
                  },
                  {
                    text: "(........................................)",
                    style: "subheader",
                    margin: [0, 35, 0, 0],
                  },
                ],
              },
              {
                stack: [
                  {
                    text: "ADMIN",
                    style: "subheader",
                    margin: [34, 0, 0, 0],
                  },
                  {
                    text: "(........................................)",
                    style: "subheader",
                    margin: [0, 35, 0, 0],
                  },
                ],
              },
            ],
          },
          {
            stack: [
              {
                text: "SALES",
                style: "subheader",
                alignment: "right",
                margin: [0, 0, 30, 0],
              },
              {
                text: "(........................................)",
                style: "subheader",
                alignment: "right",
                margin: [0, 35, 0, 0],
              },
            ],
          },
        ],
      },
    ],
    styles: {
      header: {
        fontSize: 16,
        bold: true,
        margin: [0, 0, 0, 10],
      },
      subheader: {
        fontSize: 8,
        margin: [0, 10, 0, 5],
      },
      tableHeader: {
        bold: true,
        fontSize: 8,
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
        fontSize: 8,
        bold: true,
        fillColor: "#eeeeee",
      },
      tableBodySubheader: {
        fontSize: 7,
        margin: [0, 2, 0, 0],
        alignment: "left",
      },
    },
    defaultStyle: {
      alignment: "justify",
    },
  };

  return dd;
}
