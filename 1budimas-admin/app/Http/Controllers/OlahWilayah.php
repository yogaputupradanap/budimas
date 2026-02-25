<?php

namespace App\Http\Controllers;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\Wilayah;

class OlahWilayah extends Controller {

    /**
     * Mendapatkan Semua Data untuk Option.
     * 
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @param integer|$data->opsi Request Pilihan Wilayah.
     * @param integer|$data->id Reqest Id Wilayah.
     * @return Illuminate\Http\JsonResponse Data Berformat Opsi.
     */
    public function showOptionData(Request $data) {
        switch ($data->opsi) {
            case 1 : return option((new Wilayah)->getProvinsi(), ['nama']);                break;
            case 2 : return option((new Wilayah)->getKabupatenKota($data->id), ['nama']);  break;
            case 3 : return option((new Wilayah)->getKecamatan($data->id), ['nama']);      break;
            case 4 : return option((new Wilayah)->getKelurahan($data->id), ['nama']);      break;
        }
    }
}
