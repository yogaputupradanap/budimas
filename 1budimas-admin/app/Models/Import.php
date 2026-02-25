<?php

namespace App\Models;

use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Session;

class Import extends Model
{
    /**
     * Setting Up Intial API Endpoint.
     */

    public $endpoint;
    public $fileName;
    public $fileContent;
    public function __construct($table)
    {
        parent::__construct();
        $this->endpoint = "/api/extra/create/bulk/$table";
    }

    function getNamaKolom($opsi)
    {
        $kolom = null;
        switch ($opsi) {
            case 1:
                $kolom = [
                    ['id', '(int)'],
                    ['nama', '(str[50])'],
                    ['alamat', '(str[50])'],
                    ['telepon', '(str[15])'],
                    ['npwp', '(str[25])'],
                    ['id_wilayah1', '(int)', 'https://docs.google.com/spreadsheets/d/1pe23Vib7lbxLfOqn8KKBGLhXTiA58x_ASZkJFPCB-kY/edit?usp=sharing'],
                    ['id_wilayah2', '(int)', 'https://docs.google.com/spreadsheets/d/1E7urZAPh3l8nJuseUA9ZyYYLNerVK4KYwuQJQ3WD2i0/edit?usp=sharing'],
                    ['id_wilayah3', '(int)', 'https://docs.google.com/spreadsheets/d/19URxte_qAVvajF1u-ncRODbE7mMCqHnTHw-gigJm4vg/edit?usp=sharing'],
                    ['id_wilayah4', '(int)', 'https://docs.google.com/spreadsheets/d/1azGMJOz-KGknw8Y7mtefrFGK64HtuQCicOSZnVhecVA/edit?usp=sharing'],
                    ['kode', '(str[255])'],
                ];
                break;
            case 2:
                $kolom = [
                    ['id', '(int)'],
                    ['nama', '(str[50])'],
                    ['alamat', '(str[50])'],
                    ['telepon', '(str[13])'],
                    ['npwp', '(str[25])'],
                    ['id_wilayah1', '(int)', 'https://docs.google.com/spreadsheets/d/1pe23Vib7lbxLfOqn8KKBGLhXTiA58x_ASZkJFPCB-kY/edit?usp=sharing'],
                    ['id_wilayah2', '(int)', 'https://docs.google.com/spreadsheets/d/1E7urZAPh3l8nJuseUA9ZyYYLNerVK4KYwuQJQ3WD2i0/edit?usp=sharing'],
                    ['id_wilayah3', '(int)', 'https://docs.google.com/spreadsheets/d/19URxte_qAVvajF1u-ncRODbE7mMCqHnTHw-gigJm4vg/edit?usp=sharing'],
                    ['id_wilayah4', '(int)', 'https://docs.google.com/spreadsheets/d/1azGMJOz-KGknw8Y7mtefrFGK64HtuQCicOSZnVhecVA/edit?usp=sharing'],
                    ['kode', '(str[255])'],
                ];
                break;
            case 3:
                $kolom = [
                    ['id', '(int)'],
                    ['nama', '(str[50])'],
                    ['alamat', '(str[50])'],
                    ['telepon', '(str[13])'],
                    ['npwp', '(str[25])'],
                    ['id_wilayah1', '(int)', 'https://docs.google.com/spreadsheets/d/1pe23Vib7lbxLfOqn8KKBGLhXTiA58x_ASZkJFPCB-kY/edit?usp=sharing'],
                    ['id_wilayah2', '(int)', 'https://docs.google.com/spreadsheets/d/1E7urZAPh3l8nJuseUA9ZyYYLNerVK4KYwuQJQ3WD2i0/edit?usp=sharing'],
                    ['id_wilayah3', '(int)', 'https://docs.google.com/spreadsheets/d/19URxte_qAVvajF1u-ncRODbE7mMCqHnTHw-gigJm4vg/edit?usp=sharing'],
                    ['id_wilayah4', '(int)', 'https://docs.google.com/spreadsheets/d/1azGMJOz-KGknw8Y7mtefrFGK64HtuQCicOSZnVhecVA/edit?usp=sharing'],
                    ['no_rekening', '(str[20])'],
                    ['pic', '(str[50])'],
                    ['id_perusahaan', '(int)', 'https://docs.google.com/spreadsheets/d/1y2scsECTvcf7QrEbQRmydDu--3mCY-4zHXdR6wuxjLQ/edit?usp=sharing'],
                    ['kode', '(str[100])'],
                ];
                break;
            case 4:
                $kolom = [
                    ['id', '(int)'],
                    ['nama', '(str[25])'],
                    ['kode', '(str[10])']
                ];
                break;
            case 5:
                $kolom = [
                    ['id', '(int)'],
                    ['kode', '(str[30])'],
                    ['nama', '(str[50])'],
                    ['alamat', '(str[60])'],
                    ['telepon', '(str[15])'],
                    ['telepon2', '(str[15])'],
                    ['npwp', '(str[25])'],
                    ['id_wilayah1', '(int)', 'https://docs.google.com/spreadsheets/d/1pe23Vib7lbxLfOqn8KKBGLhXTiA58x_ASZkJFPCB-kY/edit?usp=sharing'],
                    ['id_wilayah2', '(int)', 'https://docs.google.com/spreadsheets/d/1E7urZAPh3l8nJuseUA9ZyYYLNerVK4KYwuQJQ3WD2i0/edit?usp=sharing'],
                    ['id_wilayah3', '(int)', 'https://docs.google.com/spreadsheets/d/19URxte_qAVvajF1u-ncRODbE7mMCqHnTHw-gigJm4vg/edit?usp=sharing'],
                    ['id_wilayah4', '(int)', 'https://docs.google.com/spreadsheets/d/1azGMJOz-KGknw8Y7mtefrFGK64HtuQCicOSZnVhecVA/edit?usp=sharing'],
                    ['id_tipe', '(int)'],
                    ['id_cabang', '(int)', 'https://docs.google.com/spreadsheets/d/1M6hpgwS3GqXnELsLuT2r0UpFCrjBJI_LfxeEdWMuhBM/edit?usp=sharing'],
                    ['id_rute', '(int)', 'https://docs.google.com/spreadsheets/d/1NGjgbRyxcifzcElfiZv_EpI6sGbmdw87wn7pjRXG1h0/edit?usp=sharing'],
                    ['id_tipe_harga', '(int)'],
                    ['email', '(str[50])'],
                    ['nama_wajib_pajak', '(str[50])'],
                    ['alamat_wajib_pajak', '(str[100])'],
                    ['is_ppn', '(0=non active, 1=active)'],
                    ['no_rekening', '(str[20])'],
                    ['pic', '(str[20])'],
                    ['longitude', '(str[25])'],
                    ['latitude', '(str[25])']
                ];
                break;
            case 6:
                $kolom = [
                    ['id', '(int)'],
                    ['nama', '(str[25])']
                ];
                break;
            case 7:
                $kolom = [
                    ['id', '(int)'],
                    ['nama', '(str[25])']
                ];
                break;
            case 8:
                $kolom = [
                    ['id', '(int)'],
                    ['id_principal', '(int)', 'https://docs.google.com/spreadsheets/d/1Ao8BUGFH6FbEe2kzZLAU5AR_jTHZQ8FOR7_45jlwN0E/edit?usp=sharing'],
                    ['id_kategori', '(int)', 'https://docs.google.com/spreadsheets/d/1FFsG9htI9UvgCI0UtJGOdDC0yUEOvtgl9p1irxbr7c4/edit?usp=sharing'],
                    ['id_brand', '(int)', 'https://docs.google.com/spreadsheets/d/1o7sd6p36lAONKFGt6lWv39OTtZg46atEQI3TT1-sT0s/edit?usp=sharing'],
                    ['id_status', '(1=aktif,0=non aktif)'],
                    ['kode_sku', '(str[25])'],
                    ['kode_ean', '(str[25])'],
                    ['nama', '(str[50])'],
                    ['harga_beli', '(int)'],
                    ['harga_jual', '(int)'],
                    ['keterangan', '(str[50])'],
                    ['kubikasiperbox', '(int)'],
                    ['kubikasiperkarton', '(int)'],
                    ['isiperbox', '(int)'],
                    ['isiperkarton', '(int)'],
                    ['satuan', '(str[30])'],
                    ['kubikasiperpieces', '(int)'],
                    ['ppn', '(1 atau 0)'],
                    ['kode', '(str[25])'],
                    ['nama', '(str[50])'],
                    ['level', '(int)'],
                    ['packing_satuan', '(str[25])'],
                    ['set_default_storage', '(boolean)'],
                    ['faktor_konversi', '(int)'],
                    ['id_tipe_harga', '(int)'],
                    ['harga', '(int)']
                ];
                break;
            case 9:
                $kolom = [
                    ['id', '(int)'],
                    ['id_cabang', '(int)', 'https://docs.google.com/spreadsheets/d/1l_O7VP9zv4bKcFMRzXBCFlg4QkZzPKzZ8-Z-kon6utE/edit?usp=sharing'],
                    ['id_tipe', '(int)', 'https://docs.google.com/spreadsheets/d/1IyKF8tzD-jpbyD7SsTjdZwS87Mmt4sb7n4ac2XB3Qv8/edit?usp=sharing'],
                    ['nama', '(str[50])'],
                    ['no_pelat', '(str[50])'],
                    ['kubikasi', '(int)'],
                    ['tanggal_stnk', '(YYYY-MM-DD)'],
                    ['tanggal_uji', '(YYYY-MM-DD)'],
                    ['keterangan', '(str[25])'],
                    ['id_status', '(1=aktif,2=non aktif)'],
                ];
                break;
            case 10:
                $kolom = [
                    ['id', '(int)'],
                    ['id_customer', '(int)', 'https://docs.google.com/spreadsheets/d/1d-g6-YQMYDBGj4dlcZhfJIw0-iuSUGqjHdJb-VxMUsc/edit?usp=sharing'],
                    ['id_principal', '(int)', 'https://docs.google.com/spreadsheets/d/1Ao8BUGFH6FbEe2kzZLAU5AR_jTHZQ8FOR7_45jlwN0E/edit?usp=sharing'],
                    ['id_sales', '(int)'],
                    ['id_user', '(int)'],
                    ['limit_bon', '(float)'],
                    ['id_tipe_harga', '(int)', 'https://docs.google.com/spreadsheets/d/1WV4TkyYvLdQIZWCZZQa9HOP7bqz5KkqORse4mZRPZb0/edit?usp=sharing'],
                    ['top', '(int)'],
                    ['lock_order', '(0=unlocked,1=locked)'],
                    ['sisa_bon', '(float)'],
                    ['id_hari', '(integer)'],
                    ['id_minggu', '(integer)'],
                    ['id_status', '(0=non active,1=active)'],
                    ['id_tipe_kunjungan', '(1=terjadwal,2=tidak terjadwal,3=pengganti)'],
                ];
                break;
            case 11:
                $kolom = [
                    ['id', '(int)'],
                    ['nama', '(str[50])'],
                    ['nik', '(str[25])'],
                    ['id_cabang', '(str[25])'],
                    ['tanggal_lahir', '(YYYY-MM-DD)'],
                    ['username', '(str[25])'],
                    ['password', '(str[200])'],
                    ['email', '(str[100])'],
                    ['alamat', '(str[100])'],
                    ['telepon', '(str[13])'],
                    ['id_tipe', '(smallint)'],
                    ['id_wilayah1', '(int)', 'https://docs.google.com/spreadsheets/d/1pe23Vib7lbxLfOqn8KKBGLhXTiA58x_ASZkJFPCB-kY/edit?usp=sharing'],
                    ['id_wilayah2', '(int)', 'https://docs.google.com/spreadsheets/d/1E7urZAPh3l8nJuseUA9ZyYYLNerVK4KYwuQJQ3WD2i0/edit?usp=sharing'],
                    ['id_principal', '(int)'],
                ];
                break;
            case 12:
                $kolom = [
                    ['id', '(int)'],
                    ['nama', '(str[50])'],
                    ['email', '(str[100])'],
                    ['telepon', '(str[13])'],
                    ['no_rekening', '(str[25])'],
                    ['id_jabatan', '(int)'],
                    ['id_cabang', '(int)'],
                    ['username', '(str[25])'],
                    ['password', '(str[200])'],
                    ['alamat', '(str[100])'],
                    ['nik', '(str[25])'],
                    ['tanggal_lahir', '(YYYY-MM-DD)'],
                ];
                break;
        }

        return $kolom;
    }

    public function attach($fileName, $fileContent)
    {
        $this->fileName = $fileName;
        $this->fileContent = $fileContent;
        return $this;
    }

    public function upload()
    {
        return parent::attach($this->fileName, $this->fileContent);
    }

    public function check()
    {
        if (empty($this->fileName) || empty($this->fileContent)) {
            return false;
        }

        $header = fgetcsv($this->fileContent);
        if ($header === false || count($header) < 2) {
            Log::error("Invalid CSV file: missing required columns");
            return false;
        }

        rewind($this->fileContent);

        return true;
    }


}
