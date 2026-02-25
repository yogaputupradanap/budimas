<?php

use App\Models\UserAkses;
use Illuminate\Support\Facades\Auth;

/**
 * @return user
 */
function user()
{
    return Auth::user()->first();
}

/**
 * Mendapatkan List Akses Fitur dari User.
 *
 * @return object|array dari users_akses model.
 */
function userFitur()
{
    return (new userAkses)->getListByIdUser(user()->id);
}

/**
 * Check Fitur yang akan diakses oleh User.
 *
 * @param id Fitur ID.
 * @param userFitur List Akses Fitur dari User.
 * @return boolean
 */
function fitur($userFitur, $id)
{
    $check = false;
    $i = 0;
    while ($i < count($userFitur) && !$check) {
        if ($userFitur[$i]->id_fitur == $id) {
            $check = true;
        }
        $i++;
    }

    return $check;
}

/**
 * Check Modul yang akan diakses oleh User.
 *
 * @param userFitur List Akses Fitur dari User.
 * @return boolean
 */
function modul($userFitur)
{
    $check = false;
    if (!empty($userFitur)) {
        $i = 0;
        while ($i < count($userFitur) && !$check) {
            if (
                $userFitur[$i]->id_fitur > 100 &&
                $userFitur[$i]->id_fitur < 200
            ) {
                $check = true;
            } else if (empty($userFitur[$i]->id_fitur)) {
                $check = false;
            }
            $i++;
        }
        return $check;
    }
}

/**
 * @param jabatan int|array id_jabatan from user.
 * @return boolean
 */
function jabatan($jabatan)
{
    if (!Auth::check()) {
        return false;
    }

    if (is_array($jabatan)) {
        $check = false;
        foreach ($jabatan as $value) {
            if ($value == Auth::user()->first()->id_jabatan && $check == false) {
                $check = true;
            }
        }
        return $check == true ? true : false;
    } else {
        return $jabatan == Auth::user()->first()->id_jabatan ? true : false;
    }
}

/**
 * Formatting month number to month name.
 *
 * @param id Month number.
 * @return string|null Month name in Indonesia.
 */
function bulan($id)
{
    switch ($id) {
        case 1:
            return 'Januari';
            break;
        case 2:
            return 'Februari';
            break;
        case 3:
            return 'Maret';
            break;
        case 4:
            return 'April';
            break;
        case 5:
            return 'Mei';
            break;
        case 6:
            return 'Juni';
            break;
        case 7:
            return 'Juli';
            break;
        case 8:
            return 'Agustus';
            break;
        case 9:
            return 'September';
            break;
        case 10:
            return 'Oktober';
            break;
        case 11:
            return 'November';
            break;
        case 12:
            return 'Desember';
            break;
        default:
            break;
    }
}

/**
 * Formatting day number to day name.
 *
 * @param id Day number.
 * @return string|null Day name in Indonesia.
 */
function hari($id)
{
    switch ($id) {
        case 1:
            return 'Minggu';
            break;
        case 2:
            return 'Senin';
            break;
        case 3:
            return 'Selasa';
            break;
        case 4:
            return 'Rabu';
            break;
        case 5:
            return 'Kamis';
            break;
        case 6:
            return 'Jumat';
            break;
        case 7:
            return 'Sabtu';
            break;

        default:
            break;
    }
}

/**
 * Formatting Jadwal Minggu.
 *
 * @param id Week number.
 * @return string|null.
 */
function minggu($id)
{
    switch ($id) {
        case 1:
            return '1';
            break;
        case 2:
            return '2';
            break;
        case 3:
            return '3';
            break;
        case 4:
            return '4';
            break;
        case 5:
            return '1 dan 2';
            break;
        case 6:
            return '1 dan 3';
            break;
        case 7:
            return '1 dan 4';
            break;
        case 8:
            return '2 dan 3';
            break;
        case 9:
            return '2 dan 4';
            break;
        case 10:
            return '3 dan 4';
            break;
        case 11:
            return 'Semua';
            break;
        default:
            break;
    }
}

/**
 * Get Status of Items.
 *
 * @param id Status ID.
 * @param btn If true, show with button class for view.
 * @return string|null Status.
 */
function status($id, $btn = false)
{
    switch ($id) {
        case 1:
            return $btn == true
                ? '<span class="btn btn-sm btn-info pills def-point">Aktif</span>'
                : 'Aktif';
            break;
        case 2:
            return $btn == true
                ? '<span class="btn btn-sm btn-danger pills def-point text-nowrap">Non Aktif</span>'
                : 'Non Aktif';
            break;
        default:
            break;
    }
}

/**
 * Get Tipe Kunjungan Pada Olah Plafon.
 *
 * @param id Tipe Kunjungan ID.
 * @return string|null Name of Selected Tipe Kunjungan.
 */
function tipe_kunjungan($id)
{
    switch ($id) {
        case 1:
            return 'Terjadwal';
            break;
        case 2:
            return 'Tidak Terjadwal';
            break;
        case 3:
            return 'Spesial/Pengganti';
            break;
        default:
            break;
    }
}

/**
 * Formatting numbers to currency.
 *
 * @param value int numbers.
 * @param rupiah boolean, True will also add Rp. prefix.
 * @return string Numbers formatted into currency.
 */
function currency($value, $rupiah = false)
{
    if (!empty($value)) {
        $value = number_format($value, 0, ',', '.');
        $value = $rupiah ? 'Rp. ' . $value : $value;
    }

    return $value;
}

function sha256($text)
{
    return hash('sha256', $text);
}

function headings($data)
{
    return array_keys(get_object_vars($data[0]));
}

function stringDateFormater($date)
{
    if (!empty($date)) {
        return date('Y-m-d', strtotime($date));
    }
}

function selected($selected, $value)
{
    return $selected == $value ? 'selected' : '';
}

// function formatTableData($data){}

/**
 * Format Option Data.
 * Option Data Formater untuk Komponen Select2.
 *
 * @param collections[object] Collection Data yang Ingin Diformat.
 * @param keys[array] Key dari Data yang Ingin Ditampilkan
 *                    Pada Option Text.
 * @param full[bool] Jika true, Makan akan Return Collections
 *                   (Data Sebelum Diformat Option).
 *
 *
 * @example option((new Model)->all(), ['name'])
 *          option((new Model)->all(), ['name','code'])
 *          option((new Model)->all(), ['name','code'], true)
 *
 * @todo Digunakan di Controller pada Saat Memformat Data
 *       untuk Dikirim ke Tampilan/View.
 */
function option($collections, $keys, $full = false)
{
    $collections = !is_array($collections) ? array($collections) : $collections;

    $options = collect($collections)->map(function ($item) use ($keys) {
        $text = '';

        if (count($keys) == 1) {
            foreach ($keys as $key) {
                $text = $item->{$key};
            }
        } else {
            foreach ($keys as $key) {
                $text .= '[' . $item->{$key} . ']';
            }
        }

        $result = [
            'id' => $item->id,
            'text' => $text
        ];

        // Hanya tambahkan id_user jika properti tersebut ada
        if (isset($item->id_user)) {
            $result['id_user'] = $item->id_user;
        }

        if (isset($item->id_sales)) {
            $result['id_sales'] = $item->id_sales;
        }

        if (isset($item->id_cabang)) {
            $result['id_cabang'] = $item->id_cabang;
        }
        if (isset($item->id_principal)) {
            $result['id_principal'] = $item->id_principal;
        }

        return (object) $result;
    });

    return $full ? [
        'collections' => $collections,
        'options' => $options
    ] : $options;
}

function nStatus()
{
    return [
        ['id' => 1, 'text' => 'Aktif'],
        ['id' => 2, 'text' => 'Non Aktif'],
    ];
}

function nIsppn()
{
    return [
        ['id' => 1, 'text' => 'Tidak'],
        ['id' => 2, 'text' => 'Ya'],
    ];
}

function nBulan()
{
    return [
        ['id' => 1, 'text' => 'Januari'],
        ['id' => 2, 'text' => 'Februari'],
        ['id' => 3, 'text' => 'Maret'],
        ['id' => 4, 'text' => 'April'],
        ['id' => 5, 'text' => 'Mei'],
        ['id' => 6, 'text' => 'Juni'],
        ['id' => 7, 'text' => 'Juli'],
        ['id' => 8, 'text' => 'Agustus'],
        ['id' => 9, 'text' => 'September'],
        ['id' => 10, 'text' => 'Oktober'],
        ['id' => 11, 'text' => 'November'],
        ['id' => 12, 'text' => 'Desember'],
    ];
}

function nMinggu()
{
    return [
        ['id' => 1, 'text' => '1'],
        ['id' => 2, 'text' => '2'],
        ['id' => 3, 'text' => '3'],
        ['id' => 4, 'text' => '4'],
        ['id' => 5, 'text' => '1 dan 2'],
        ['id' => 6, 'text' => '1 dan 3'],
        ['id' => 7, 'text' => '1 dan 4'],
        ['id' => 8, 'text' => '2 dan 3'],
        ['id' => 9, 'text' => '2 dan 4'],
        ['id' => 10, 'text' => '3 dan 4'],
        ['id' => 11, 'text' => 'Semua'],
    ];
}

function nHari()
{
    return [
        ['id' => 1, 'text' => 'Minggu'],
        ['id' => 2, 'text' => 'Senin'],
        ['id' => 3, 'text' => 'Selasa'],
        ['id' => 4, 'text' => 'Rabu'],
        ['id' => 5, 'text' => 'Kamis'],
        ['id' => 6, 'text' => 'Jumat'],
        ['id' => 7, 'text' => 'Sabtu'],
    ];
}

function nTipeKunjungan()
{
    return [
        ['id' => 1, 'text' => 'Terjadwal'],
        ['id' => 2, 'text' => 'Tidak Terjadwal'],
        ['id' => 3, 'text' => 'Spesial/Pengganti'],
    ];
}

function nLevelSatuan()
{
    return [
        ['id' => 1, 'text' => 1],
        ['id' => 2, 'text' => 2],
        ['id' => 3, 'text' => 3],
    ];
}
