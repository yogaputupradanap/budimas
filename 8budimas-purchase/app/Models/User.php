<?php

namespace App\Models;

use Illuminate\Contracts\Auth\Authenticatable;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Str;

class User extends Model implements Authenticatable
{
    private $id;  // User's Identifier which Used to Recall User's Data.
    private $username;  // Logged Username which Used to Check User Validity.
    private $password;  // Logged Password which Used to Check User Validity.

    /**
     * Setting Up Intial API Endpoint
     */
    public function __construct()
    {
        $this->endpoint = '/api/base/users';
    }

    /*
     * |--------------------------------------------------------------------------
     * | Auth Functions
     * |--------------------------------------------------------------------------
     * |
     */
    public function init()
    {
        $this->token(Auth::user()->getRememberToken());
        return $this;
    }

    /**
     * Fetch User By Credentials Paramaters.
     *
     * @param array $credentials containing Login Data
     * @return Illuminate\Contracts\Auth\Authenticatable
     */
    public function fetchUserByCredentials(array $credentials)
    {
        // 1. Ambil Token
        $data = [
            'username' => $credentials['username'], 
            'password' => $credentials['password']
        ];
        $tokensResponse = $this->select('/api/extra/getUserToken', 'get', $data);

        if ($tokensResponse->status() != 200 || empty($tokensResponse->first())) {
            return null; 
        }

        $tokens = $tokensResponse->first()->tokens;

        if (empty($tokens)) {
            return null;
        }

        // 2. Ambil Data User berdasarkan token
        // DEBUG: Pastikan method where() tidak menghasilkan URL query string "?where=..." 
        // Jika API kamu bermasalah dengan kata 'where', coba kirim sebagai parameter biasa
        $user = $this->token($tokens)->where([
            'username' => $credentials['username'] // Gunakan format key-value jika didukung
        ])->select();

        // 3. Validasi hasil (Gunakan method count() yang kita perbaiki di awal chat)
        if ($user && $user->count() > 0) {
            $userData = $user->first();
            $this->id = $userData->id;
            $this->username = $userData->username;
            // Jangan lupa simpan token jika diperlukan untuk session berikutnya
            $this->tokens = $tokens; 
            
            return $this; 
        }

        return null;
    }

    /**
     * Getting User's Authentication Unique Identifier (Used to be an `id` Field).
     *
     * @inheritDoc @see \Illuminate\Contracts\Auth\Authenticatable::getAuthIdentifierName()
     * @see App\Services\UserAuthProvider::retrieveById()
     */
    public function getAuthIdentifierName()
    {
        return 'id';
    }

    /**
     * Getting User's Authentication Unique Identifier.
     * The Value of Field Will be Saved in Session Drive and
     * Will be Used Once User Request to Fetch Data Again (recall).
     *
     * @inheritDoc @see \Illuminate\Contracts\Auth\Authenticatable::getAuthIdentifier()
     */
    public function getAuthIdentifier()
    {
        return !empty($this->{$this->getAuthIdentifierName()})
            ? $this->{$this->getAuthIdentifierName()}
            : $this->first()->{$this->getAuthIdentifierName()};
    }

    /**
     * Getting Fetched User Name.
     *
     * @see App\Services\UserAuthProvider::validateCredentials()
     */
    public function getAuthUsername()
    {
        return $this->username;
    }

    /**
     * Getting Fetched User Password.
     *
     * @inheritDoc @see \Illuminate\Contracts\Auth\Authenticatable::getAuthPassword()
     * @see App\Services\UserAuthProvider::validateCredentials()
     */
    public function getAuthPassword()
    {
        return $this->password;
    }

    /**
     * Get the Token Value.
     *
     * @inheritDoc @see \Illuminate\Contracts\Auth\Authenticatable::getRememberToken()
     */
    public function getRememberToken()
    {
        if (!empty($this->getRememberTokenName())) {
            return $this->first()->{$this->getRememberTokenName()};
        }
    }

    /**
     * Set the Token Value.
     *
     * @inheritDoc @see \Illuminate\Contracts\Auth\Authenticatable::getRememberToken()
     */
    public function setRememberToken($value)
    {
        if (!empty($this->getRememberTokenName())) {
            return $this->{$this->getRememberTokenName()} = $value;
        }
    }

    /**
     * Get the Column Name for the Token.
     *
     * @inheritDoc @see \Illuminate\Contracts\Auth\Authenticatable::getRememberTokenName()
     */
    public function getRememberTokenName()
    {
        return 'tokens';
    }

    /*
     * |--------------------------------------------------------------------------
     * | Others
     * |--------------------------------------------------------------------------
     * |
     * | All Users Other Functions Need Redeclare Token Functions!
     * |
     */

    function all()
    {
        return $this
            ->token(Auth::user()->getRememberToken())
            ->orderBy('id')
            ->select('/api/extra/getUser')
            ->get();
    }

    function find($id)
    {
        return $this
            ->token(Auth::user()->getRememberToken())
            ->where(['users.id', '=', $id])
            ->select('/api/extra/getUser')
            ->first();
    }

    function getListByJabatanSales()
    {
        return $this
            ->token(Auth::user()->getRememberToken())
            ->where(['id_jabatan', '=', '4'])
            ->select('/api/extra/getUser')
            ->get();
    }

    function getListByJabatanDriver()
    {
        return $this
            ->token(Auth::user()->getRememberToken())
            ->where(['id_jabatan', '=', '6'])
            ->select('/api/extra/getUser')
            ->get();
    }

    function getListByIdCabang($id)
    {
        return $this
            ->token(Auth::user()->getRememberToken())
            ->where(['id_cabang', '=', $id])
            ->select('/api/extra/getUser')
            ->get();
    }

    function getFilteredList($data)
    {
        $model = $this->token(Auth::user()->getRememberToken());

        if (!empty($data['id_jabatan'])) {
            $model = $model->where(['id_jabatan', '=', $data['id_jabatan']]);
        }
        if (!empty($data['nik'])) {
            $model = $model->whereOr(['nik', '=', $data['nik']]);
        }
        if (!empty($data['nama'])) {  // %25 Adalah Encoding untuk Special Character %
            $model = $model->whereOr(['nama', ' ILIKE', '%25' . $data['nama'] . '%25']);
        }

        return $model->orderBy('id')->select()->get();
    }

    /**
     * Insert Data Baru dan Mengembalikan Data Id.
     *
     * @method Override.
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\User Instance.
     */
    public function insert($data)
    {
        $this->token(Auth::user()->getRememberToken());
        if (!is_object($data)) {
            $data = (object) $data;
        }

        return parent::insert([
            'nama' => $data->nama,
            'id_cabang' => $data->idCabang,
            'id_jabatan' => $data->idJabatan,
            'username' => $data->username,
            'password' => bcrypt($data->password),
            'nik' => $data->nik,
            'email' => $data->email,
            'telepon' => $data->telepon,
            'tanggal_lahir' => $data->tanggalLahir,
            'alamat' => $data->alamat,
            'tokens' => Str::random(60)
        ])->first()->id;
    }

    /**
     * Update Data Berdasarkan Id.
     *
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\User Instance.
     */
    public function updateById($data)
    {
        // Siapkan array untuk data yang akan diupdate
        $updateData = [
            'nama' => $data->nama,
            'id_cabang' => $data->idCabang,
            'id_jabatan' => $data->idJabatan,
            'username' => $data->username,
            'nik' => $data->nik,
            'email' => $data->email,
            'telepon' => $data->telepon,
            'tanggal_lahir' => $data->tanggalLahir,
            'alamat' => $data->alamat
        ];

        // Hanya tambahkan password ke updateData jika password tidak kosong
        if (!empty($data->password)) {
            $updateData['password'] = bcrypt($data->password);
        }

        return $this
            ->token(Auth::user()->getRememberToken())
            ->id($data->id)
            ->update($updateData);
    }

    /**
     * Delete Data Berdasarkan Id.
     *
     * @param Illuminate\Http\Request|$data Requested HTTP Form Data.
     * @return App\Models\User Instance.
     */
    public function deleteById($data)
    {
        return $this
            ->token(Auth::user()->getRememberToken())
            ->id($data->id)
            ->delete();
    }
}
