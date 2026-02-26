<?php

namespace App\Services;

use App\Models\Cabang;
use App\Models\Customer;
use App\Models\CustomerTipe;
use App\Models\Perusahaan;
use App\Models\Principal;
use App\Models\Produk;
use App\Models\ProdukBrand;
use App\Models\ProdukKategori;
use App\Models\ProdukSatuan;
use App\Models\Wilayah;
use App\Services\Service;  
use Illuminate\Support\Collection;

class ExportData extends Service
{ 
    protected $file_content;
    protected $file_name;

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
        switch ($this->data->opsi) {
            case 1: 
                $this->file_content = (new Cabang)->all(); 
                $this->file_name    = 'data-cabang.csv';
            break;
            case 2: 
                $this->file_content = (new Perusahaan)->all(); 
                $this->file_name    = 'data-perusahaan.csv';
            break;
            case 3: 
                $this->file_content = (new Principal)->all(); 
                $this->file_name    = 'data-principal.csv';
            break;
            case 4: 
                $this->file_content = (new CustomerTipe)->all(); 
                $this->file_name    = 'data-customer-tipe.csv';
            break;
            case 5: 
                $this->file_content = (new Customer)->all(); 
                $this->file_name    = 'data-customer.csv';
            break;
            case 6: 
                $this->file_content = (new ProdukBrand)->all(); 
                $this->file_name    = 'data-produk-brand.csv';
            break;
            case 7: 
                $this->file_content = (new ProdukKategori)->all(); 
                $this->file_name    = 'data-produk-kategori.csv';
            break;
            case 8: 
                $this->file_content = (new ProdukSatuan)->all(); 
                $this->file_name    = 'data-produk-satuan.csv';
            break;
            case 9: 
                $this->file_content = (new Produk)->all(); 
                $this->file_name    = 'data-produk.csv';
            break;
            case 10: 
                $this->file_content = (new Provinsi)->all(); 
                $this->file_name    = 'data-wilayah1.csv';
            break;
            case 11: 
                $this->file_content = (new KabupatenKota)->all(); 
                $this->file_name    = 'data-wilayah2.csv';
            break;
            case 12: 
                $this->file_content = (new Kecamatan)->all(); 
                $this->file_name    = 'data-wilayah3.csv';
            break;
            case 13: 
                $this->file_content = (new Kelurahan)->all(); 
                $this->file_name    = 'data-wilayah4.csv';
            break;
        }

        return [
            'header'    => headings($this->file_content),
            'data'      => $this->file_content,
            'file_name' => $this->file_name
        ];
    }
}