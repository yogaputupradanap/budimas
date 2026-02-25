import * as XLSX from "xlsx";
export function parseFakturExcel(excel) {
  const wb = XLSX.read(excel, { type: "array", cellDates: true });
  const rows = wb.Sheets[wb.SheetNames[0]];
  const data = XLSX.utils.sheet_to_json(rows, {
    defval: null,      
    raw: true,         
    blankrows: false,
  });
  // ambil kolom nomor faktur pajak dan buang yang null/undefined
  const no_faktur_arr = data.map(r => r['Referensi']).filter(n => n).map(String);

  return {data, no_faktur_arr};
}