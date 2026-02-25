<?php

namespace App\Services;

use App\Models\Armada;
use App\Services\ImportData;
use App\Models\Cabang;
use App\Models\Customer;
use App\Models\CustomerTipe;
use App\Models\Import;
use App\Models\Perusahaan;
use App\Models\Plafon;
use App\Models\Principal;
use App\Models\Produk;
use App\Models\ProdukBrand;
use App\Models\ProdukKategori;
use App\Models\ProdukSatuan;
use App\Models\Sales;
use App\Models\User;
use App\Models\Wilayah;
use App\Services\Service;
use Illuminate\Support\Collection;

class ExportData extends Service
{
    protected $file_content;
    protected $file_name;
    var $importDataServices;

    public function __construct()
    {
        $this->importDataServices = new ImportData();
    }

    /**
     * Mendapatkan Data dan Nama File saat Unduh Hasil Export.
     *
     * @param object|$this->data {
     *      @key int `opsi` dari Table yang Dipilih.
     * }
     *
     * @return array.
     */
    public function getAll() {

        $today = date('Ymd');
        $table = $this->importDataServices->getTableFromOpsi((int) $this->data->opsi || 1);
        switch ($this->data->opsi) {
            case 1:
                $this->file_content = (new Cabang)->all();
                $this->file_name    = 'data-cabang-' . $today . '.csv';
            break;
            case 2:
                $this->file_content = (new Perusahaan)->all();
                $this->file_name    = 'data-perusahaan-' . $today . '.csv';
            break;
            case 3:
                $this->file_content = (new Principal)->allBase();
                $this->file_name    = 'data-principal-' . $today . '.csv';
            break;
            case 4:
                $this->file_content = (new CustomerTipe)->all();
                $this->file_name    = 'data-customer_tipe-' . $today . '.csv';
            break;

            case 5:
                $this->file_content = (new ProdukBrand)->all();
                $this->file_name    = 'data-produk_brand-' . $today . '.csv';
            break;
            case 6:
                $this->file_content = (new ProdukKategori)->all();
                $this->file_name    = 'data-produk_kategori-' . $today . '.csv';
            break;
            case 7:
                $this->file_content = (new ProdukSatuan)->all();
                $this->file_name    = 'data-produk_satuan-' . $today . '.csv';
            break;
            case 8:
                $this->file_content = (new Produk)->all();
                $this->file_name    = 'data-produk-' . $today . '.csv';
            case 9:
                $this->file_content = (new Armada)->all();
                $this->file_name    = 'data-armada-' . $today . '.csv';
            break;
            case 10:
                $this->file_content = (new Plafon)->ExportCsv();
                $this->file_name    = 'data-plafon-' . $today . '.csv';
            break;
            case 11:
                $this->file_content = (new Sales)->ExportCsv();
                $this->file_name    = 'data-sales-' . $today . '.csv';
                break;
            case 12:
                $this->file_content = (new User)->ExportCsv();
                $this->file_name    = 'data-user-' . $today . '.csv';
                break;
        }
        $header_col = (new Import($table))->getNamaKolom($this->data->opsi);
        $header = [];
        foreach ($header_col as $col) {
            $header[] = is_array($col) ? $col[0] : $col;
        }
        sort($header);

        if($this->file_content) {
            $header = headings($this->file_content);
        }

        return [
            'header'    => $header,
            'data'      => $this->file_content,
            'file_name' => $this->file_name
        ];
    }
}
