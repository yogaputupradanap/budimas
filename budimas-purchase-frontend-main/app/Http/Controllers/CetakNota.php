<?php

namespace App\Http\Controllers;
use Illuminate\Http\Request;
use Elibyy\TCPDF\Facades\TCPDF;
use PDF;
use App\Models\{
    Cabang, Stok, Inventori,
    ProdukSatuan,
    PurchaseRequestLogProses,
    PurchaseRequest,
    PurchaseRequestDetail,
    PurchaseOrder,
    PurchaseOrderDetail,
    PurchasePenerimaanBarang,
    PurchaseTagihan,
    PurchaseTagihanPelunasan,
};

class CetakNota extends Controller {
    /**
     * 
     */
    public function purchaseFaktur(Request $data) {
        
        // 1. LOAD TCPDF CLASS
        $pdf = new TCPDF();
        $pdf::SetTitle('FAKTUR PURCHASE ORDER - PT. BUDIMAS MAKMUR MULIA');
        $pdf::AddPage();

        // 2. LOAD DATA
        $purchaseOrder       = (new PurchaseOrder)->getDataById($data->idOrder);
        $purchaseOrderDetail = (new purchaseOrderDetail)->getListByIdRequest($data->idOrder);

        $noFaktur          = $purchaseOrder->no_faktur         ?? '';
        $kodeRequest       = $purchaseOrder->kode_request      ?? '';
        $namaPrincipal     = $purchaseOrder->nama_principal    ?? '';
        $namaCabang        = $purchaseOrder->nama_cabang       ?? '';
        $namaUser          = $purchaseOrder->nama_user         ?? '';
        $tanggal           = $purchaseOrder->tanggal           ?? '';
        $waktu             = $purchaseOrder->waktu             ?? '';
        $noBatch           = $purchaseOrder->no_batch_faktur   ?? '';
        $subtotalTransaksi = $purchaseOrder->subtotal          ?? 0;
        $totalTransaksi    = $purchaseOrder->total             ?? 0;
        $potongan          = $purchaseOrder->potongan          ?? 0;
        $biayaLainnya      = $purchaseOrder->biaya_lainnya     ?? 0;
        $statusPembayaran  = $purchaseOrder->status_pembayaran ?? '';
        $waktuTransaksi    = $tanggal.' '.$waktu;

        if($statusPembayaran == 1) {
            $statusPembayaran = 'Belum Lunas';
        } else if ($statusPembayaran == 2) {
            $statusPembayaran = 'Lunas';
        }

        // 3. CREATING LAYOUT
        $header = '
        <style>
            .th2 {
                border-collapse : collapse;
                width           : 100%;
                font-size       : 9px;
            }
            .th2 > th, .th2 > td  {
                border-bottom : 1px solid #000;
                border-top    : 1px solid #000;
                padding       : 8px;
                text-align    : left;
            }
        </style>

        <table>
            <tr>
                <td style="color:#01579b; font-weight:bold; font-size:12pt;">PT. BUDIMAS MAKMUR MULIA</td>
                <td style="font-size:10pt; text-align:right;">Faktur Purchase Order</td>
            </tr>
            <tr style="font-weight:bold;">
                <td style="color:#1976d2; font-size:10pt;">Distribution and Manufacturing Co.</td>
                <td style="text-align:right; font-size:10pt;">'.$noFaktur.'</td>
            </tr>
        </table>

        <!-- Spacing -->
        <table><tr><td></td></tr></table>';

        $subHeader = '
        <table class="th2" cellpadding="2.5">
            <tr>
                <!-- kiri -->
                <td width="15%">No. Batch</td>
                <td width="3%">:</td>
                <td width="32%">'.$noBatch.'</td>

                <!-- kanan -->
                <td width="15%">Kode Request</td>
                <td width="3%">:</td>
                <td width="32%">'.$kodeRequest.'</td>
                
            </tr>
            <tr>
                <!-- kiri -->
                <td>Principal</td>
                <td>:</td>
                <td>'.$namaPrincipal.'</td>

                <!-- kanan -->
                <td width="15%">Waktu Transaksi</td>
                <td width="3%">:</td>
                <td width="32%">'.$waktuTransaksi.'</td>
            </tr>
            <tr>
                <!-- kiri -->
                <td>Cabang</td>
                <td>:</td>
                <td>'.$namaCabang.'</td>

                <!-- kanan -->
                <td width="15%">User (PIC)</td>
                <td width="3%">:</td>
                <td width="32%">'.$namaUser.'</td>
            </tr>
        </table>
        
        <!-- Spacing -->
        <table><tr><td></td></tr><tr><td></td></tr></table>';
        
        $body='
        <table border="0.5" style="font-size:9pt;" cellpadding="4">
            <thead>
                <tr style="text-align: center">
                    <th width="20%"><b>Kode Produk</b></th>
                    <th width="25%"><b>Nama Produk</b></th>
                    <th width="15%"><b>Jumlah</b></th>
                    <th width="20%"><b>Harga Beli</b></th>
                    <th width="20%"><b>Subtotal</b></th>
                </tr>
            </thead>
            <tbody>';
        
        foreach ($purchaseOrderDetail as $item) {
            $kodeProduk      = $item->kode_produk       ?? '';
            $namaProduk      = $item->nama_produk       ?? '';
            $jumlah          = $item->jumlah_order      ?? 0;
            $hargaBeliProduk = $item->harga_beli_produk ?? 0;
            $subtotal        = $item->subtotal          ?? 0;

            $body .= '
                <tr style="text-align: center">
                    <td width="20%">'.$kodeProduk.'</td>
                    <td width="25%">'.$namaProduk.'</td>
                    <td width="15%">'.$jumlah.'</td>
                    <td width="20%">'.currency($hargaBeliProduk, true).'</td>
                    <td width="20%">'.currency($subtotal, true).'</td>
                </tr>
            ';
        }

        $body.='
                <tr>
                    <td width="80%" colspan="3">Sub Total Transaksi</td>
                    <td width="20%" style="text-align: center">'.currency($subtotalTransaksi, true).'</td>
                </tr>
                <tr>
                    <td width="80%" colspan="3">Potongan</td>
                    <td width="20%" style="text-align: center">'.currency($potongan, true).'</td>
                </tr>
                <tr>
                    <td width="80%" colspan="3">Biaya Lainnya</td>
                    <td width="20%" style="text-align: center">'.currency($biayaLainnya, true).'</td>
                </tr>
                <tr>
                    <td width="80%" colspan="3"><b>Total Transaksi</b></td>
                    <td width="20%" style="text-align: center"><b>'.currency($totalTransaksi, true).'</b></td>
                </tr>
                <tr>
                    <td width="80%" colspan="3">Status Pembayaran</td>
                    <td width="20%" style="text-align: center"><b>'.$statusPembayaran.'</b></td>
                </tr>
            </tbody>
        </table>';
        
        $html = $header.$subHeader.$body;
        $pdf::writeHTML($html, true, false, true, false, '');
        $pdf::lastPage();

        $pdf::Output('hello_world.pdf');
    }

    /**
     * 
     */
    public function purchaseRiwayatPelunasan(Request $data) {
        
        // 1. LOAD TCPDF CLASS
        $pdf = new TCPDF();
        $pdf::SetTitle('FAKTUR PURCHASE ORDER - PT. BUDIMAS MAKMUR MULIA');
        $pdf::AddPage();

        // 2. LOAD DATA
        $purchaseOrder            = (new PurchaseOrder)->getDataById($data->idOrder);
        $purchaseOrderDetail      = (new purchaseOrderDetail)->getListByIdRequest($data->idOrder);
        $purchaseTagihanPelunasan = (new purchaseTagihanPelunasan)->getListByIdOrder($data->idOrder);

        $noFaktur          = $purchaseOrder->no_faktur           ?? '';
        $kodeRequest       = $purchaseOrder->kode_request        ?? '';
        $namaPrincipal     = $purchaseOrder->nama_principal      ?? '';
        $namaCabang        = $purchaseOrder->nama_cabang         ?? '';
        $namaUser          = $purchaseOrder->nama_user           ?? '';
        $tanggal           = $purchaseOrder->tanggal             ?? '';
        $waktu             = $purchaseOrder->waktu               ?? '';
        $noBatch           = $purchaseOrder->no_batch_faktur     ?? '';
        $subtotalTransaksi = $purchaseOrder->subtotal            ?? 0;
        $totalTransaksi    = $purchaseOrder->total               ?? 0;
        $totalDiaudit      = $purchaseOrder->nominal_total_audit ?? 0;
        $potongan          = $purchaseOrder->potongan            ?? 0;
        $biayaLainnya      = $purchaseOrder->biaya_lainnya       ?? 0;
        $statusPembayaran  = $purchaseOrder->status_pembayaran   ?? '';
        $waktuTransaksi    = $tanggal.' '.$waktu;

        if($statusPembayaran == 1) {
            $statusPembayaran = 'Belum Lunas';
        } else if ($statusPembayaran == 2) {
            $statusPembayaran = 'Lunas';
        }

        // Latest Pelunasan
        // Index Terakhir dari `$purchaseTagihanPelunasan` atau Record Pelunasan Terakhir
        $lp                                  = !empty($purchaseTagihanPelunasan)
                                               ? max(array_keys($purchaseTagihanPelunasan)) : 0;
        $noAngsuranTagihanTerakhir           = $purchaseTagihanPelunasan[$lp]->no_angsuran            ?? '';
        $namaUserTagihanTerakhir             = $purchaseTagihanPelunasan[$lp]->nama_user1             ?? '';
        $nominalPembayaranTagihanTerakhir    = $purchaseTagihanPelunasan[$lp]->nominal_pembayaran     ?? 0;
        $nominalTotalTerbayarTagihanTerakhir = $purchaseTagihanPelunasan[$lp]->nominal_total_terbayar ?? 0;
        $nominalTotalSisaTagihanTerakhir     = $purchaseTagihanPelunasan[$lp]->nominal_total_sisa     ?? 0;
        $tanggalTagihanTerakhir              = $purchaseTagihanPelunasan[$lp]->tanggal                ?? '';
        $waktuTagihanTerakhir                = $purchaseTagihanPelunasan[$lp]->waktu                  ?? '';
        $waktuTagihanTerakhir                = $tanggalTagihanTerakhir.' '.$waktuTagihanTerakhir;

        // 3. CREATING LAYOUT
        $header = '
        <style>
            .th2 {
                border-collapse : collapse;
                width           : 100%;
                font-size       : 9px;
            }
            .th2 > th, .th2 > td  {
                border-bottom : 1px solid #000;
                border-top    : 1px solid #000;
                padding       : 8px;
                text-align    : left;
            }
        </style>

        <table>
            <tr>
                <td style="color:#01579b; font-weight:bold; font-size:12pt;">PT. BUDIMAS MAKMUR MULIA</td>
                <td style="font-size:10pt; text-align:right;">Pelunasan Tagihan Purchase</td>
            </tr>
            <tr style="font-weight:bold;">
                <td style="color:#1976d2; font-size:10pt;">Distribution and Manufacturing Co.</td>
                <td style="text-align:right; font-size:10pt;">'.$noFaktur.'</td>
            </tr>
        </table>

        <!-- Spacing -->
        <table><tr><td></td></tr></table>';

        $subHeader = '
        <table class="th2" cellpadding="2.5">
            <tr>
                <!-- kiri -->
                <td width="15%">No. Batch</td>
                <td width="3%">:</td>
                <td width="32%">'.$noBatch.'</td>

                <!-- kanan -->
                <td width="15%">Kode Request</td>
                <td width="3%">:</td>
                <td width="32%">'.$kodeRequest.'</td>
                
            </tr>
            <tr>
                <!-- kiri -->
                <td>Principal</td>
                <td>:</td>
                <td>'.$namaPrincipal.'</td>

                <!-- kanan -->
                <td width="15%">Waktu Transaksi</td>
                <td width="3%">:</td>
                <td width="32%">'.$waktuTransaksi.'</td>
            </tr>
            <tr>
                <!-- kiri -->
                <td>Cabang</td>
                <td>:</td>
                <td>'.$namaCabang.'</td>

                <!-- kanan -->
                <td width="15%">User (PIC)</td>
                <td width="3%">:</td>
                <td width="32%">'.$namaUser.'</td>
            </tr>
        </table>
        
        <!-- Spacing -->
        <table><tr><td></td></tr><tr><td></td></tr></table>';
        
        $body = '
        <table border="0.5" style="font-size:9pt;" cellpadding="4">
            <thead>
                <tr>
                    <th colspan="2" style="font-size:10pt;"><b>Informasi Tagihan</b></th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td width="65%">Total Transaksi</td>
                    <td width="35%" style="text-align: center">'.currency($totalTransaksi, true).'</td>
                </tr>
                <tr>
                    <td width="65%"><b>Total Transaksi Diaudit</b></td>
                    <td width="35%" style="text-align: center"><b>'.currency($totalDiaudit, true).'</b></td>
                </tr>
                <tr>
                    <td width="65%">Status Pembayaran</td>
                    <td width="35%" style="text-align: center"><b>'.$statusPembayaran.'</b></td>
                </tr>
            </tbody>
        </table>

        <!-- Spacing -->
        <table><tr><td></td></tr></table>';

        $body .= '
        <table border="0.5" style="font-size:9pt;" cellpadding="4">
            <thead>
                <tr>
                    <th colspan="2" style="font-size:10pt;"><b>Informasi Pembayaran Angsuran Terakhir</b></th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td width="65%">No. Angsuran</td>
                    <td width="35%" style="text-align: center">'.$noAngsuranTagihanTerakhir.'</td>
                </tr>
                <tr>
                    <td width="65%">User Finance (PIC)</td>
                    <td width="35%" style="text-align: center">'.$namaUserTagihanTerakhir.'</td>
                </tr>
                <tr>
                    <td width="65%">Waktu Pembayaran</td>
                    <td width="35%" style="text-align: center">'.$waktuTagihanTerakhir.'</td>
                </tr>
                <tr>
                    <td width="65%">Nominal Pembayaran</td>
                    <td width="35%" style="text-align: center">'.currency($nominalPembayaranTagihanTerakhir, true).'</td>
                </tr>
                <tr>
                    <td width="65%">Nominal Total Angsuran Dibayar</td>
                    <td width="35%" style="text-align: center">'.currency($nominalTotalTerbayarTagihanTerakhir, true).'</td>
                </tr>
                <tr>
                    <td width="65%"><b>Nominal Total Sisa Angsuran</b></td>
                    <td width="35%" style="text-align: center"><b>'.currency($nominalTotalSisaTagihanTerakhir, true).'</b></td>
                </tr>
            </tbody>
        </table>
        
        <!-- Spacing -->
        <table><tr><td></td></tr></table>';

        $body .= '
        <table border="0.5" style="font-size:9pt;" cellpadding="4">
            <thead>
                <tr>
                    <th colspan="5" style="font-size:10pt;"><b>Informasi Riwayat Pembayaran Angsuran</b></th>
                </tr>
                <tr style="text-align: center">
                    <th width="15%"><b>No. Angsuran</b></th>
                    <th width="20%"><b>Waktu</b></th>
                    <th width="25%"><b>User Finance (PIC)</b></th>
                    <th width="20%"><b>Pembayaran</b></th>
                    <th width="20%"><b>Total Pelunasan</b></th>
                </tr>
            </thead>
            <tbody>';
        
        if(!empty($purchaseTagihanPelunasan) && count($purchaseTagihanPelunasan)>1) {
            for ($i=0; $i<count($purchaseTagihanPelunasan); $i++) {
                $item = $purchaseTagihanPelunasan;
                if ($i > 0 && $i < max(array_keys($purchaseTagihanPelunasan))) {
                    $noAngsuran           = $item[$i]->no_angsuran            ?? '';
                    $namaUser             = $item[$i]->nama_user1             ?? '';
                    $nominalPembayaran    = $item[$i]->nominal_pembayaran     ?? 0;
                    $nominalTotalTerbayar = $item[$i]->nominal_total_terbayar ?? 0;
                    $nominalTotalSisa     = $item[$i]->nominal_total_sisa     ?? 0;
                    $tanggal              = $item[$i]->tanggal                ?? '';
                    $waktu                = $item[$i]->waktu                  ?? '';
                    $waktu                = $tanggal.' '.$waktu;
    
                    $body .= '
                        <tr style="text-align: center">
                            <td width="15%">'.$noAngsuran.'</td>
                            <td width="20%">'.$waktu.'</td>
                            <td width="25%">'.$namaUser.'</td>
                            <td width="20%">'.currency($nominalPembayaran, true).'</td>
                            <td width="20%">'.currency($nominalTotalTerbayar, true).'</td>
                        </tr>
                    ';
                }
            }
        } else {
            $body .= '
                <tr style="text-align: center">
                    <td colspan="5"><em>Riwayat Pembayaran Angsuran Belum Tersedia untuk Transaksi Ini</em></td>
                </tr>
            ';
        }
        
        $body.='
            </tbody>
        </table>';
        
        $html = $header.$subHeader.$body;
        $pdf::writeHTML($html, true, false, true, false, '');
        $pdf::lastPage();

        $pdf::Output('hello_world.pdf');
    }
}
