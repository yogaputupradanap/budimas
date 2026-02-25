<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Auth;
use App\Models\User;
use App\Models\Model;
use App\Models\Cabang as CabangModel;
use App\Services\OlahCabang as OlahCabangService;
use App\Services\OlahUser as OlahUserService;
use App\Services\UserAuthProvider;
use App\Services\OpsiWilayah;
use App\Models\Wilayah;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\Facades\Redirect;



class TestController extends Controller
{
    // function test(Request $request){
    //     $validation = $request->validate([
    //         'username' => 'required',
    //         'password' => 'required',
    //     ]);

    //     if (Auth::attempt($validation)) {
    //         // ddd(Auth::check());
    //         // ddd(Auth::user());
    //         // ddd(route('2.dashboard.index'));
    //         // return redirect()->intended(route('5.dashboard.index'));
    //     }
    // }

    function test(){
        return response()->json(count((new User)->getListByJabatanSales()));
    }
    // function test(Request $request){
    //     return Redirect::intended("http://budimas.test:8012/");
    //     // ddd($request->username);
    // }

    // function test(){
    //     // $where = [
    //     //         'id' => '2'
    //     // ];
    //     // $data= [
    //     //     'id'      => '2',
    //     //     'telepon' => '081212341234'
    //     // ];

    //     // Http::withToken('A')->asForm()
    //     // ->put('https://api-swgriortza-et.a.run.app/api/base/users', $data);


    //     // $a = Http::withToken('A')
    //     // ->get('https://api-swgriortza-et.a.run.app/api/base/users?q={"where":{"id":"2"}}')->object()->response;
        

    //     // $user = new User;
    //     // echo $user->session->tokens;
    //     // $a = $user->getTest1();
    //     // echo "<br>".$a->response;

    //     // $b = $user->where(["a" => "b", "c" => "d"])->where;
    //     // $b = $user->where(["a" => "b"])->where;
    //     // $b = $user->where(["a" => "b", "c" => "d"])->where;
    //     // $b = $user->where(["a" => "b", "c" => "d"])->where;
    //     // $b = $user->where(["a" => "b"])->endpointQuery()->where;
    //     // $b = $user->endpointQuery()->where;

    //     // $user->update([
    //     //     'id' => '2'
    //     // ], [
    //     //     'telepon' => '081212341234'
    //     // ]);

    //     // $b = $user->getListWhere([
    //     //     'id' => '2'
    //     // ]);
    //     // var_dump($b);

    //     $provinsi = new OpsiWilayah;
    //     ddd($provinsi->getProvinsi());

    //     // $cabang = new CabangModel;
    //     // ddd($cabang->getList());

    //     // $user = new userModel;
    //     // $cabang = new CabangModel;
    //     // $cabang = new OlahCabangService;
    //     // ddd($user->where([['username','=','adminkoor1'], ['password','=','test']])->select()->get());
    //     // ddd($user->whereOr([['username','=','adminkoor1'], ['password','=','test']])->select()->get());
    //     // var_dump($user->where([['username','=','adminkoor1'], ['password','=','test']])
    //     //     ->whereOr(['username','!=','adminit1'])
    //     //     ->orderBy('username ASC, id DESC')
    //     //     ->select()->get());

    //     // var_dump($user->where(['id','=','22'])->update([
    //     //     'age'               => 24,
    //     //     'alamat_wp'         => null,
    //     //     'budget_return'     => null,
    //     //     'email'             => 'aerial@mail.com',
    //     //     'first_name'        => 'Aerial Lafaytte',
    //     //     'id'                => 22,
    //     //     'id_cabang'         => 1,
    //     //     'id_jabatan'        => 4,
    //     //     'is_canvas'         => true,
    //     //     'is_to'             => false,
    //     //     'nama_wp'           => 'Aer',
    //     //     'no_rekening'       => 6654321,
    //     //     'npwp'              => 9231241232,
    //     //     'password'          => 'test',
    //     //     'target_penjualan'  => 2000000,
    //     //     'telepon'           => '087719147801',
    //     //     'tokens'            => null,
    //     //     'username'          => 'Aerial',
    //     // ])->get());
        
    //     // var_dump($user->orderBy('username ASC')->limit(1)->select()->get());
    //     // var_dump($user->token(md5('AuthBudimasHorus'))->where(['id','=', Session::get(Auth::getName())])->select()->first());

    //     // $uce =  new UserAuthProvider;
    //     // var_dump(Auth::user());
    //     // var_dump(Auth::check());
    //     // var_dump(Session::all());
    //     // var_dump(Session::get(Auth::getName()));
    //     // var_dump($uce->find(Session::get(Auth::getName())));
    //     // var_dump(Auth::user()->first()->id_jabatan);
    //     // var_dump($user->select()->get());
    //     // var_dump($cabang->select()->get());
    //     $func = 'demolisher';
    //     // var_dump(Model::$func());

    //     // Auth::logout();

    //     // $user = new OlahUserService;
    //     // ddd($user);
        
    //     // ddd(Auth::user());
    //     // Http::withToken('MJiZ369jGs2tZUy7fsnaCX3hkxc95bgMuCCTVDuFv5h6J5silZBDrmld0h4Z')
    //     //     ->asForm()
    //     //     ->put('http://127.0.0.1:5000/api/base/users?where={"id":"=30"}', [
    //     //     'nama' => ''
    //     // ]);

    //     // $user = new UserModel;


    //     // var_dump(md5('AuthBudimasHorus'));
    //     // var_dump($user->token(md5('AuthBudimasHorus'))->select()->get());

    //     // $user->insert([
    //     //     'username' => 'admintest1',
    //     //     'password' => 'test'
    //     // ]);

    //     // var_dump($user->select('/api/extra/getLastInsertedId/users')->get());
        
    //     // ddd($user->select("/api/extra/getUserLoginData/adminit1/test")->get());

    //     // echo "<br>".$b;
    // }

}
