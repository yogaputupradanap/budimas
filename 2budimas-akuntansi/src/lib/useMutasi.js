import Papa from "papaparse";
import {getDateNow} from "@/src/lib/utils";

const useMutasi = () => {

    const handleCsvBCA = (file) => {
        return new Promise((resolve, reject) => {
            Papa.parse(file, {
                header: false,
                skipEmptyLines: true,
                complete: (results) => {
                    try {
                        const data = results.data;
                        const transactions = [];
                        let summary = {};

                        // Ambil header transaksi (cari baris yang sesuai)
                        const headerIndex = data.findIndex(
                            row =>
                                row[0]?.trim() === "Tanggal Transaksi" &&
                                row[1]?.trim() === "Keterangan" &&
                                row[2]?.trim() === "Cabang" &&
                                row[3]?.trim() === "Jumlah" &&
                                row[4]?.trim() === "Saldo"
                        );

                        if (headerIndex === -1) {
                            reject(new Error("Format CSV tidak sesuai. Pastikan file CSV mengikuti format yang benar."));
                            return;
                        }

                        for (const row of data) {
                            const values = row.map(v => v.trim());

                            if (values[0] && (/^\d{2}\/\d{2}\/\d{4}$/.test(values[0]) || values[0].toLowerCase() === 'pend')) {
                                let jumlahStr = values[3]?.replace(/,/g, '') || '';
                                transactions.push({
                                    tanggal: values[0].toLowerCase() === 'pend' ? getDateNow() : values[0],
                                    keterangan: values[1],
                                    cabang_mutasi: values[2],
                                    jumlah: parseFloat(jumlahStr.replace(/\s*(CR|DB)\s*/g, '')),
                                    tipe: (() => {
                                        const match = jumlahStr.match(/\b(CR|DB)\b/)?.[0] || '';
                                        if (match?.toUpperCase() === 'CR') return 'DB';
                                        if (match?.toUpperCase() === 'DB') return 'CR';
                                        return '';
                                    })(),
                                    kredit: jumlahStr.includes('DB') ? parseFloat(jumlahStr.replace(/CR/g, '').replace(/,/g, '')) : 0,
                                    debit: jumlahStr.includes('CR') ? parseFloat(jumlahStr.replace(/DB/g, '').replace(/,/g, '')) : 0,
                                    saldo: parseFloat(values[4]?.replace(/,/g, '') || '')
                                });
                            }

                            if (values[0]?.includes('Saldo Awal')) {
                                summary.saldo_awal = values[0].match(/[-\d.,]+$/)?.[0]?.replace(/,/g, '');
                            } else if (values[0]?.includes('Mutasi Kredit')) {
                                summary.mutasi_debet = values[0].match(/[-\d.,]+$/)?.[0]?.replace(/,/g, '');
                            } else if (values[0]?.includes('Mutasi Debet')) {
                                summary.mutasi_kredit = values[0].match(/[-\d.,]+$/)?.[0]?.replace(/,/g, '');
                            } else if (values[0]?.includes('Saldo Akhir')) {
                                summary.saldo_akhir = values[0].match(/[-\d.,]+$/)?.[0]?.replace(/,/g, '');
                            }
                        }

                        resolve({transactions, summary});

                    } catch (e) {
                        reject(new Error("Format CSV tidak sesuai. Pastikan file CSV mengikuti format yang benar."))
                    }
                },
                error: (err) => {
                    reject(err);
                }
            });
        });
    }

    const handleCsvMandiri = (file) => {
        return new Promise((resolve, reject) => {
            Papa.parse(file, {
                header: true,
                skipEmptyLines: true,
                complete: (results) => {
                    try {

                        const transactions = [];
                        let totalCredit = 0;
                        let totalDebit = 0;

                        const expectedColumns = ["PostDate", "Credit Amount", "Debit Amount", "Close Balance"];
                        const columns = results.meta.fields;

                        // cek apakah semua expectedColumns ada di dalam columns
                        const missing = expectedColumns.filter(col => !columns.includes(col));

                        if (missing.length > 0) {
                            reject(new Error(
                                `Format CSV tidak sesuai. Kolom yang kurang: ${missing.join(", ")}`
                            ));
                            return
                        }

                        const saldo_close_awal = parseFloat(results.data[0]["Close Balance"]);
                        const data_credit_temp = parseFloat(results.data[0]["Credit Amount"]) || 0;
                        const data_debit_temp = parseFloat(results.data[0]["Debit Amount"]) || 0;
                        const saldo_awal = data_credit_temp > 0 ? saldo_close_awal - data_credit_temp : saldo_close_awal + data_debit_temp;

                        for (const row of results.data) {
                            const postDate = new Date(row["PostDate"]);
                            const credit = parseFloat(row["Credit Amount"] || 0);
                            const debit = parseFloat(row["Debit Amount"] || 0);

                            transactions.push({
                                tanggal: getDateNow(postDate),
                                keterangan: row['AdditionalDesc'] || '-',
                                cabang_mutasi: 0,
                                jumlah: credit || debit,
                                tipe: credit > 0 ? 'CR' : 'DB',
                                kredit: credit,
                                debit: debit,
                                saldo: parseFloat(row["Close Balance"]),
                            });

                            totalCredit += credit;
                            totalDebit += debit;
                        }
                        const rounded = (num) => Math.round(num * 100) / 100;
                        const summary = {
                            saldo_awal: rounded(saldo_awal),
                            mutasi_kredit: totalCredit,
                            mutasi_debet: totalDebit,
                            saldo_akhir: parseFloat(results.data[results.data.length - 1]["Close Balance"]) || 0
                        };

                        resolve({transactions, summary});
                    } catch (error) {
                        reject(new Error("Format CSV tidak sesuai. Pastikan file CSV mengikuti format yang benar."));
                    }
                },
                error: (err) => reject(err),
            });
        });
    }

    const handleCsvBCADIFI = (file) => {
        return new Promise((resolve, reject) => {
            Papa.parse(file, {
                header: true,
                skipEmptyLines: true,
                complete: (results) => {
                    const transactions = [];
                    let totalCredit = 0;
                    let totalDebit = 0;

                    const columns = results.meta.fields;
                    const expectedColumns = ["Tanggal", "Mutasi", "Saldo", "Jenis Transaksi"];

                    // cek apakah semua expectedColumns ada di dalam columns
                    const missing = expectedColumns.filter(col => !columns.includes(col));

                    if (missing.length > 0) {
                        reject(new Error(
                            `Format CSV tidak sesuai. Kolom yang kurang: ${missing.join(", ")}`
                        ));
                    }

                    const saldo_close_awal = parseFloat(results.data[0]["Saldo"]);
                    const jumlah = parseFloat(results.data[0]["Mutasi"]) || 0;
                    const type_transaksi_awal = (() => {
                        const tipe = results.data[0]["Jenis Transaksi"];
                        if (tipe?.toUpperCase() === 'CR') return 'DB';
                        if (tipe?.toUpperCase() === 'DB') return 'CR';
                        return '';
                    })();
                    const saldo_awal = type_transaksi_awal === 'CR' ? saldo_close_awal + jumlah : saldo_close_awal - jumlah;

                    for (const row of results.data) {
                        const postDate = new Date(row["Tanggal"]);
                        const mutasi = parseFloat(row["Mutasi"] || 0);
                        const type_transaksi = (() => {
                            const tipe = row["Jenis Transaksi"];
                            if (tipe?.toUpperCase() === 'CR') return 'DB';
                            if (tipe?.toUpperCase() === 'DB') return 'CR';
                            return '';
                        })();

                        transactions.push({
                            tanggal: getDateNow(postDate),
                            keterangan: row['Keterangan'] || '-',
                            cabang_mutasi: row['Cabang'],
                            jumlah: mutasi,
                            tipe: type_transaksi,
                            kredit: type_transaksi === 'CR' ? mutasi : 0,
                            debit: type_transaksi === 'DB' ? mutasi : 0,
                            saldo: parseFloat(row["Saldo"]),
                        });

                        totalCredit += row["Jenis Transaksi"] === 'CR' ? mutasi : 0;
                        totalDebit += row["Jenis Transaksi"] === 'DB' ? mutasi : 0;
                    }
                    const rounded = (num) => Math.round(num * 100) / 100;
                    console.log("saldo_awal", saldo_awal);
                    console.log("rounded saldo awal", rounded(saldo_awal));
                    const summary = {
                        saldo_awal: rounded(saldo_awal),
                        mutasi_kredit: totalCredit,
                        mutasi_debet: totalDebit,
                        saldo_akhir: parseFloat(results.data[results.data.length - 1]["Saldo"]) || 0
                    };

                    resolve({transactions, summary});
                },
                error: (err) => reject(err),
            });
        });
    }

    return {
        handleCsvBCA,
        handleCsvMandiri,
        handleCsvBCADIFI
    };

}

export default useMutasi;