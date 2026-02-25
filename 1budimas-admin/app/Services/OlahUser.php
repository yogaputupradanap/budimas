<?php

namespace App\Services;

use App\Models\User;
use App\Models\UserAkses;
use App\Models\Cabang;
use App\Models\Jabatan;
use App\Models\JabatanAkses;
use App\Services\Service;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Str;

/**
 * Service Class untuk Mengolah Data User.
 * Tabel User Memiliki Relasi dengan Tabel
 * Cabang dan Jabatan.
 * 
 * Untuk mengetahui Fungsi yang Digunakan
 * dalam Memanipulasi Data.
 * @see Model App\Models.
 * 
 * Penyisipan Data Menggunakan Function.
 * @method setData().
 * @see Service App\Services.
 */
class OlahUser extends Service
{   
    /**
     * Mendapatkan Semua Data dari Tabel User.
     * @return object (N) Banyak Baris dari Tabel User.
     */
    function getAll() {
        return (new User)->all();
    }

    /**
     * Mendapatkan Data dari Tabel User Berdasarkan Id.
     * @param id Id (User).
     * @return object (1) Baris dari Tabel User.
     */ 
    function getDataById($id) {
        return (new User)->retrieveById($id);
    }

    /**
     * Mendapatkan Semua Data dari Tabel Cabang.
     * @return object (N) Banyak Baris dari Tabel Cabang.
     */
    function getCabangList() {
        return (new Cabang)->all();
    }

    /**
     * Mendapatkan Semua Data dari Tabel Jabatan.
     * @return object (N) Banyak Baris dari Tabel Jabatan.
     */
    function getJabatanList() {
        return (new Jabatan)->all();
    }

    /**
     * Mendapatkan Semua Data Default Fitur User dari Tabel JabatanAkses.
     * @param id Id (Jabatan).
     * @return object (N) Banyak Baris dari Tabel JabatanAkses.
     */
    function getDefaultFitur($id){
        return (new JabatanAkses)->getDefaultFiturListByIdJabatan($id);
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel UserAkses.
     * @param data|array [<id_user>, <id_fitur>].
     * @example insertUserFitur([2, 101]).
     * @return bool.
     */
    function insertUserFitur($data) {
        return (new UserAkses)->insert([
            'id_user'  => $data[0],
            'id_fitur' => $data[1]
        ])->check();
    }

    /**
     * Delete User Akses Berdasarkan Id User.
     * @param id Id (User).
     * @return bool.
     */
    function deleteUserFitur($id) {
        return (new UserAkses)->deleteUserFiturByIdUser($id);
    }

    /**
     * Memasukkan Data Baru ke dalam Tabel User.
     * Saat Memasukkan Data User Baru, Data Fitur
     * Default juga Akan Dimasukkan Berdasarkan
     * Id User menggunakan @method `insertUserFitur`.
     * 
     * @param this->data Illuminate\Http\Request
     *        Data User Baru yang Akan Dimasukkan.
     * @return bool.
     */
    function insert() {;
        // Memasukkan data User Baru dan Mengembalikan Id
        // dari Hasil Insert.
        $insertUser = (new User)
        ->token(Auth::user()->getRememberToken())
        ->returning('id')->insert([
            'nama'          => $this->data->nama,
            'id_cabang'     => $this->data->idCabang,
            'id_jabatan'    => $this->data->idJabatan,
            'id_perusahaan' => $this->data->idPerusahaan,
            'username'      => $this->data->username,
            'password'      => $this->data->password,
            'nik'           => $this->data->nik,
            'email'         => $this->data->email,
            'telepon'       => $this->data->telepon,
            'tanggal_lahir' => $this->data->tanggalLahir,
            'alamat'        => $this->data->alamat,
            'tokens'        => Str::random(60)
        ]);

        // Mendapatkan Id User dari Hasil Returning.
        $userId = $insertUser->first()->id;

        // Jika Insert User Berhasil, Masukkan Default Fitur ke User Akses.
        if ($insertUser->check() && !empty($userId)) {
            $nFitur = $this->getDefaultFitur($this->data->idJabatan);
            foreach ($nFitur as $fitur) {
                $this->insertUserFitur([$user->id, $fitur->id_fitur]);
            }
        }

        // NOTE : Seharusnya mengecek Keberhasilan dari Input User Fitur
        // Juga. Namun, ini Belum ditambahkan.
        return $insertUser->check();
    }


    /**
     * Menyunting Data Berdasarkan Id dari Tabel User.
     * Apabila Jabatan Berubah, Reset User Akses
     * (Insert Default Fitur Baru dan Delete Fitur Lama).
     * 
     * @param id Id (User).
     * @param this->data Illuminate\Http\Request
     *        Data User yang Akan Disunting.
     * @return bool.
     */
    function updateById($id) {
        $updateUser = (new User)->token(Auth::user()->getRememberToken())
        ->id($id)->update([
            'nama'          => $this->data->nama,
            'id_cabang'     => $this->data->idCabang,
            'id_jabatan'    => $this->data->idJabatan,
            'id_perusahaan' => $this->data->idPerusahaan,
            'username'      => $this->data->username,
            'password'      => $this->data->password,
            'nik'           => $this->data->nik,
            'email'         => $this->data->email,
            'telepon'       => $this->data->telepon,
            'tanggal_lahir' => $this->data->tanggalLahir,
            'alamat'        => $this->data->alamat
        ]);

        // Cek Perubahan Jabatan.
        if(!empty($this->data->idJabatanEx)) {
            if ($this->data->idJabatanEx != $this->data->idJabatan 
                && $updateUser->status() == 200) {
                $this->deleteUserFitur($id);

                $nFitur = $this->getDefaultFitur($this->data->idJabatan);
                foreach ($nFitur as $fitur) { 
                    $this->insertUserFitur([$id, $fitur->id_fitur]); 
                }
            }
        }

        return $updateUser->check();
    }

    /**
     * Menghapus Data Berdasarkan Id dari Tabel Armada.
     * Saat Mengahapus Data User, Data Fitur
     * juga Akan Dihapus Berdasarkan Id User 
     * menggunakan @method `deleteUserFitur`.
     * 
     * @param id Id (Armada).
     * @return bool.
     */
    function deleteById($id) {
        $deleteFitur = $this->deleteUserFitur($id);
        $deleteUser  = (new User)->token($this->token)->id($id)
                       ->delete()->check();

        return $deleteFitur && $deleteUser ? true : false;
    }
}