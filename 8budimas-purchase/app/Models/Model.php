<?php

namespace App\Models;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Http;

use function PHPSTORM_META\type;

/**
 * This is Custom Base Modeling Class.
 * This Containing Logic to Supply HTTP Request for Accessing API.
 * This Also Provide Returning Mechanism of Requested Result.
 *
 * Many Functions used in this class is extend from laravel HTTP Client Functions.
 * For Official Documentation about Laravel HTTP Request, go to this link.
 * @link https://laravel.com/docs/7.x/http-client
 */
class Model
{
    //    protected static $baseURL = 'http://192.168.0.198:5001';  // Base URL dari API (Local)
    // protected static $baseURL = 'https://api-swgriortza-et.a.run.app';  // Base Url dari API
    //protected static $baseURL = 'https://api-purchase-189463082311.asia-southeast2.run.app';  // Base Url dari API
    protected static $baseURL = 'https://127.0.0.1:5000';  // Base Url dari API
    // protected static $baseURL = 'https://192.168.0.103:5000';

    public static function getBaseURL()
    {
        return self::$baseURL;
    }

    protected $token = null;  // Auth Token

    public $endpoint = null;  // Endpoint URL

    public $response = null;  // Response dari Request

    protected $where = '';  // Klausa Tambahan Where

    protected $whereOr = '';  // Klausa Tambahan WhereOr

    protected $orderBy = '';  // Klausa Tambahan OrderBy

    protected $limit = '';  // Klausa Tambahan Limit

    protected $returning = '';  // Klausa Tambahan Returning *Khusus untuk Insert Saja!!

    protected $query = '';  // Query untuk Klausa Tambahan e.g. Where, Order

    /**
     * By Default, Token will be Added when a Class Has been Instantiated.
     * Once User Has Login, Token Will be Fetched from Users Table.
     */
    public function __construct()
    {
        if (Auth::check()) {
            $this->token(Auth::user()->token);
        }
    }

    /**
     * Setting Up Auth Token for Making Request.
     * @param token is used for authentication.
     */
    public function url($endpoint)
    {
        $this->endpoint = $endpoint;
        return $this;
    }

    /**
     * Setting Up Auth Token for Making Request.
     * @param token is used for authentication.
     */
    public function token($token)
    {
        $this->token = $token;
        return $this;
    }

    /**
     * Counting Requested Response Result.
     * @return int numbers of counted response.
     */
    
    public function count()
    {
        return count($this->response->result);
    }

    /**
     * Getting Status of Requested Response.
     * @return int HTTP code of Request Status.
     */
    public function status()
    {
        return $this->response->status;
    }

    /**
     * Getting Result of Requested Response.
     * @return array of Requested Response.
     */
    public function get()
    {
        if (is_object($this->response) && property_exists($this->response, 'result')) {
            return $this->response->result;
        } else {
            // Tangani kasus ketika $this->response tidak valid
            return null;
        }
    }

    /**
     * Getting Response of Result and Status.
     * @return Illuminate\Http\JsonResponse Response and Status Code.
     */
    public function response()
    {
        if (is_object($this->response) && property_exists($this->response, 'result')) {
            
            // Ambil status dan pastikan tipenya Integer
            $statusCode = $this->status();
            
            // Jika $statusCode berisi 'success', Laravel akan error. 
            // Kita paksa jadi 200 jika bukan angka murni.
            if (!is_numeric($statusCode)) {
                $statusCode = 200; 
            }

            return response()->json($this->get(), (int) $statusCode);
            
        } else {
            return response()->json(['error' => 'Invalid response from API'], 500);
        }
    }

    /**
     * Getting Result of Requested Response.
     * (Only the First Element)
     *
     * @return mix of Requested Response.
     */
    public function first()
    {
        $result = $this->response->result;
        return !empty($result) ? $result[0] : $result;
    }

    /**
     * Builder of Query Additional Clauses.
     *
     * This Will Combine All Query Additional Clause
     * from Each Builder Result.
     * E.g Where, WhereOr, OrderBy.
     *
     * @uses This will be Implemented Directly
     *       when Selecting, Updating, or Deleting.
     */
    public function builder()
    {
        if ($this->where != '') {
            $this->query .= '?where={' . $this->where . '}';
        }

        if ($this->whereOr != '') {
            $this->query .= $this->query != ''
                ? '&whereOr={' . $this->whereOr . '}'
                : '?whereOr={' . $this->whereOr . '}';
        }

        if ($this->orderBy != '') {
            $this->query .= $this->query != ''
                ? '&orderBy={"fields":"' . $this->orderBy . '"}'
                : '?orderBy={"fields":"' . $this->orderBy . '"}';
        }

        if ($this->limit != '') {
            $this->query .= $this->query != ''
                ? '&limit={"numbers":"' . $this->limit . '"}'
                : '?limit={"numbers":"' . $this->limit . '"}';
        }

        if ($this->returning != '') {
            $this->query .= $this->query != ''
                ? '&returning={"fields":"' . $this->returning . '"}'
                : '?returning={"fields":"' . $this->returning . '"}';
        }

        return $this;
    }

    /**
     * Demolisher of Query Additional Clauses.
     *
     * This Will Clean Up Query Builder Cache
     * before it is Used Again.
     *
     * @uses This will be Implemented Directly
     *       after Selecting, Updating, or Deleting.
     */
    public function demolisher()
    {
        $this->where = '';
        $this->whereOr = '';
        $this->orderBy = '';
        $this->limit = '';
        $this->returning = '';
        $this->query = '';

        return $this;
    }

    /**
     * Builder of Where Clause
     *
     * @param array $array of Where Parameters.
     * @example where(["id", "=", "1"])
     * @example Nested Where
     *          >>> where([["id_cabang", "=", "1"], ["status", "!=", "2"]])
     */
public function where($array)
{
    // Pastikan input tidak kosong
    if (empty($array)) return $this;

    // Cek apakah ini Nested Array (Array di dalam Array)
    // Contoh: [['status', '=', '1'], ['level', '=', 'admin']]
    if (isset($array[0]) && is_array($array[0])) { 
        foreach ($array as $i) {
            // Pastikan sub-array memiliki minimal 3 elemen (key, operator, value)
            if (count($i) >= 3) {
                $this->buildWhereString($i[0], $i[1], $i[2]);
            }
        }
    } else {
        // Ini untuk Single Array (Array 1 dimensi)
        // Contoh: ['username', '=', 'admin']
        if (count($array) >= 3) {
            $this->buildWhereString($array[0], $array[1], $array[2]);
        }
    }

    return $this;
}

// Helper function untuk merapikan string
private function buildWhereString($column, $operator, $value)
{
    $formatted = '"' . $column . '":"' . $operator . " '" . $value . "'\"";
    
    if ($this->where == '') {
        $this->where = $formatted;
    } else {
        $this->where .= ',' . $formatted;
    }
}
    /**
     * Builder of WhereOr Clause
     *
     * @param array $array of WhereOr Parameters.
     * @example whereOr(["id", "=", "1"])
     * @example Nested Where
     *          >>> whereOr([["id_cabang", "=", "1"], ["status", "!=", "2"]])
     */
    public function whereOr($array)
    {
        if (is_array($array[0])) {  // If WhereOr is Nested
            foreach ($array as $i) {
                $this->whereOr .= $this->whereOr == '' ||
                    $array == array_key_first($array) ||
                    $array == array_key_last($array)
                    ? '"' . $i[0] . '":"' . $i[1] . ' ' . "'" . $i[2] . "'" . '"'
                    : ',"' . $i[0] . '":"' . $i[1] . ' ' . "'" . $i[2] . "'" . '"';
            }
        } else {
            $this->whereOr .= $this->whereOr == ''
                ? '"' . $array[0] . '":"' . $array[1] . ' ' . "'" . $array[2] . "'" . '"'
                : ',"' . $array[0] . '":"' . $array[1] . ' ' . "'" . $array[2] . "'" . '"';
        }

        return $this;
    }

    /**
     * Builder of OrderBy Clause.
     * Applied to Select Request Only.
     *
     * @param value Fields with The Order.
     * @example orderBy('id DESC, name DESC')
     */
    public function orderBy($value)
    {
        $this->orderBy .= $this->orderBy == '' ? $value : ',' . $value;
        return $this;
    }

    /**
     * Builder of Returning Clause.
     * Applied to Insert Request Only.
     *
     * @param value Fields of Expected Data Returned,
     *        Use * for All Fields.
     * @example returning('id, username') || returning('*')
     */
    public function returning($value)
    {
        $this->returning .= $this->returning == '' ? $value : ',' . $value;
        return $this;
    }

    /**
     * Builder of Limit Clause.
     * Applied to Select Request Only.
     *
     * @param value int Value of Expected Limitation.
     */
    public function limit($value)
    {
        $this->limit = $value;
        return $this;
    }

    /**
     * Requesting HTTP GET for Selecting Data via API Call.
     *
     * @param extra|null Fill if Using Custom/Extra API.
     * @param method If Use Method POST, Fill the Param with `post`.
     * @param array $data Data Used to Filter.
     * @return mix Fetched data From API Call.
     */
    public function select($extra = null, $method = 'get', $data = [])
{
    $endpoint = $extra == null ? $this->endpoint : $extra;

    // --- TAMBAHKAN LOGIC INI ---
    // Jika property 'where' tidak kosong, masukkan ke dalam array $data
    if (!empty($this->where)) {
        $data['where'] = '{' . $this->where . '}';
    }
    // ---------------------------

    if (count($data) > 0) { 
        $this->builder()->response = Http::withOptions(['verify' => false])
            ->withToken($this->token)
            ->asForm()
            // Kirim $data sebagai query parameter atau body
            ->{$method}(self::$baseURL . $endpoint . $this->query, $data)
            ->object();
    } else { 
        $this->builder()->response = Http::withOptions(['verify' => false])
            ->withToken($this->token)
            ->{$method}(self::$baseURL . $endpoint . $this->query)
            ->object();
    }

    $this->demolisher();
    return $this;
}

    /**
     * Requesting HTTP PUT for Updating Data via API Call.
     *
     * @param array $data Data Want to be Updated.
     * @return mix HTTP Status Messages.
     * @example update(["username" => "user test"])
     * @todo In Order Not to Update Whole Table Rows,
     *       Don't Forget Applying Where Function.
     */
    public function update($data)
    {
        $this->builder()->response = Http::withOptions([
					'verify' => false, // <--- TAMBAHKAN INI
				])->withToken($this->token)
            ->asForm()
            ->put(self::$baseURL . $this->endpoint . $this->query, $data)
            ->object();

        $this->demolisher();
        return $this;
    }

    /**
     * Requesting HTTP POST for Inserting Data via API Call.
     *
     * @param array $data Data Want to be Inserted.
     * @return mix HTTP Status Messages || Fetched data From API Call.
     * @example insert(["username" => "user test", ...])
     */
    public function insert($data)
    {
        $this->builder();
        $response = Http::withOptions([
					'verify' => false, // <--- TAMBAHKAN INI
				])->withToken($this->token)
            ->asForm()
            ->post(self::$baseURL . $this->endpoint . $this->query, $data);

        if ($response->successful()) {
            $this->response = $response->object();
        } else {
            // Tangani error di sini
            $this->response = null;
            // Mungkin tambahkan logging atau pesan error
        }

        $this->demolisher();
        return $this;
    }

    /**
     * Requesting HTTP POST for Sending File via API Call.
     *
     * @param string $fileName The Name of File Want to be Sent.
     * @param string $fileContent The Content of File Want to be Sent.
     * @return mix HTTP Status Messages || Fetched data From API Call.
     */
    public function attach($fileName, $fileContent)
    {
        $response = Http::withOptions([
					'verify' => false, // <--- TAMBAHKAN INI
				])->withToken($this->token)
            ->attach('file', $fileContent, $fileName)
            ->post(self::$baseURL . $this->endpoint);

        if ($response->failed()) {
            $errorData = $response->json('error') ?? ['error'=>'Unknown error'];

            $errorMessage = json_encode($errorData);
            throw new \Exception($errorMessage);
        }

        $this->response = $response->object();

        $this->demolisher();
        return $this;
    }

    /**
     * Requesting HTTP DELETE for Deleting Data via API Call.
     *
     * @return mix HTTP Status Messages.
     * @todo In Order Not to Update Whole Table Rows,
     *       Don't Forget Applying Where Function.
     */
    public function delete()
    {
        $this->builder()->response = Http::withOptions([
					'verify' => false, // <--- TAMBAHKAN INI
				])->withToken($this->token)
            ->delete(self::$baseURL . $this->endpoint . $this->query)
            ->object();

        $this->demolisher();
        return $this;
    }

    /**
     * Fetch All Rows From a Table
     */
    function all()
    {
        return $this->orderBy('id')->select()->get();
    }

    /**
     * Fetch a Row From a Table By Id
     */
    function find($id)
    {
        return $this->where(['id', '=', $id])->select()->first();
    }

    /**
     * Set Where Id Query Parameter
     * @param id String of id from a Table
     */
    function id($id)
    {
        $this->where(['id', '=', $id]);
        return $this;
    }

    /**
     * Set Custom Where Query Parameter
     * @param id String of id from a Table
     * @param field String of field from a Table
     */
    function id_custom($id, $field)
    {
        $this->where([$field, '=', $id]);
        return $this;
    }

    function filter($data)
    {
        foreach ($data as $key => $value) {
            if (!empty($value)) {
                if ($key == 'nama') {
                    // %25 Adalah Encoding untuk Special Character %
                    $this->where(['nama', ' ILIKE', '%25' . $data['nama'] . '%25']);
                } else {
                    $this->where([$key, '=', $value]);
                }
            }
        }

        return $this;
    }

    public function get1()
    {
        return $this->response->data ?? [];
    }

    public function first1()
    {
        $result = $this->get1();
        return !empty($result) ? $result[0] : null;
    }

    public function count1()
    {
        return $this->response->recordsTotal ?? 0;
    }

    public function filteredCount()
    {
        return $this->response->recordsFiltered ?? 0;
    }

    public function getDraw()
    {
        return $this->response->draw ?? 0;
    }

    public function select1($extra = null, $method = 'get', $data = [])
    {
        $endpoint = $extra == null ? $this->endpoint : $extra;

        if (count($data) > 0) {  // WITH RESPONSE BODY DATA
            $this->builder()->response = Http::withOptions([
					'verify' => false, // <--- TAMBAHKAN INI
				])->withToken($this->token)
                ->asForm()
                ->{$method}(self::$baseURL . $endpoint . $this->query, $data)
                ->object();
        } else {  // NO RESPONSE BODY DATA
            $this->builder()->response = Http::withOptions([
					'verify' => false, // <--- TAMBAHKAN INI
				])->withToken($this->token)
                ->{$method}(self::$baseURL . $endpoint . $this->query)
                ->object();
        }

        $this->demolisher();
        return $this;
    }
}
