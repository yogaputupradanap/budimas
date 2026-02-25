// import pdfMake from "pdfmake/build/pdfmake";
// import pdfFonts from "pdfmake/build/vfs_fonts";
// pdfMake.vfs = pdfFonts.pdfMake.vfs;

export function useGeneratePdf(defFunc, sourceData, filename) {
  const docDefinition = defFunc(sourceData);
  pdfMake.createPdf(docDefinition).download(filename);
}
