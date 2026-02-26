<?php

namespace App\Models;
use Illuminate\Support\Facades\Session;

class Import extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */
    public function __construct($table){
        parent::__construct();
        $this->endpoint = "/api/extra/create/bulk/$table";
    }

    function getNamaKolom($opsi){
        $kolom = null;
        switch ($opsi) {
            case 1:
                $kolom = [
                    ['nama', '(str[50])'], 
                    ['alamat', '(str[50])'], 
                    ['telepon', '(str[13])'],
                    ['npwp', '(str[25])'],
                    ['id_wilayah1', '(int)'],
                    ['id_wilayah2', '(int)'],
                    ['id_wilayah3', '(int)'],
                    ['id_wilayah4', '(int)']
                ];
            break;
            case 2:
                $kolom = [
                    ['nama', '(str[50])'], 
                    ['alamat', '(str[50])'], 
                    ['telepon', '(str[13])'],
                    ['npwp', '(str[25])'],
                    ['id_wilayah1', '(int)'],
                    ['id_wilayah2', '(int)'],
                    ['id_wilayah3', '(int)'],
                    ['id_wilayah4', '(int)']
                ];
            break;
            case 3:
                $kolom = [
                    ['nama', '(str[50])'], 
                    ['alamat', '(str[50])'], 
                    ['telepon', '(str[13])'],
                    ['npwp', '(str[25])'],
                    ['id_wilayah1', '(int)'],
                    ['id_wilayah2', '(int)'],
                    ['id_wilayah3', '(int)'],
                    ['id_wilayah4', '(int)'],
                    ['no_rekening', '(str[20])'],
                    ['pic', '(str[20])'],
                    ['id_perusahaan', '(int)']
                ];
            break;
            case 4:
                $kolom = [
                    ['nama', '(str[25])'],
                    ['kode', '(str[10])']
                ];
            break;
            case 5:
                $kolom = [
                    ['kode', '(str[30])'], 
                    ['nama', '(str[50])'], 
                    ['alamat', '(str[60])'], 
                    ['telepon', '(str[15])'],
                    ['telepon2', '(str[15])'],
                    ['npwp', '(str[25])'],
                    ['id_wilayah1', '(int)'],
                    ['id_wilayah2', '(int)'],
                    ['id_wilayah3', '(int)'],
                    ['id_wilayah4', '(int)'],
                    ['id_tipe', '(int)'],
                    ['id_cabang', '(int)'],
                    ['no_rekening', '(str[20])'],
                    ['pic', '(str[20])'],
                    ['longitude', '(str[25])'],
                    ['latitude', '(str[25])']
                ];
            break;
            case 6: 
                $kolom = [
                    ['nama', '(str[25])']
                ]; 
            break;
            case 7: 
                $kolom = [
                    ['nama', '(str[25])']
                ]; 
            break;
            case 8: 
                $kolom = [
                    ['nama', '(str[25])']
                ]; 
            break;
            case 9:
                $kolom = [
                    ['id_principal', '(int)'],
                    ['id_brand', '(int)'],
                    ['id_kategori', '(int)'],
                    ['id_status', '(int)'],
                    ['nama', '(str[50])'],
                    ['kode_sku', '(str[25])'],
                    ['harga_beli', '(int)'],
                    ['id_satuan', '(int)'],
                    ['isi_box', '(int)'],
                    ['kubikasi_satuan', '(int/dec)'],
                    ['kubikasi_box', '(int/dec)'],
                    ['keterangan', '(str[50])'],
                    ['kode_ean', '(str[25])']
                ];
            break;
        }

        return $kolom;
    }
}