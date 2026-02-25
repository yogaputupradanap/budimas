<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Cabang;
use App\Models\Jabatan;
use App\Models\User;
use Illuminate\Http\Request;

class Profile extends Controller
{
    public function index()
    {
        return view('contents.profile', [
            'user' => (new User)->init()->find(user()->id),
            'nCabang' => (new Cabang)->all(),
            'nJabatan' => (new Jabatan)->all(),
            'content' => (object) [
                'name' => 'Profile',
                'breadcrumb' => ['Profile', 'Edit Profile']
            ]
        ]);
    }

    // public function update(Request $request) {
    //     $update = $this->service->setData($request)->updateById(user()->id);
    //     return $update
    //         ? redirect()->route($this->route.'edit')->with('status', 2)
    //         : redirect()->route($this->route.'edit')->with('status', 4);
    // }

    public function update(Request $request)
    {
        // Get the authenticated user's ID
        $userId = user()->id;

        // Format the data to match the expected structure
        $formattedData = (object) [
            'id' => $userId,
            'nama' => $request->nama,
            'idCabang' => $request->idCabang,
            'idJabatan' => $request->idJabatan,
            'username' => $request->username,
            'password' => $request->password,
            'nik' => $request->nik,
            'email' => $request->email,
            'telepon' => $request->telepon,
            'tanggalLahir' => $request->tanggalLahir,
            'alamat' => $request->alamat
        ];

        $user = new User();
        $user->init();  // Initialize with token
        $result = $user->updateById($formattedData)->response();

        if ($result->status() == 200) {
            return redirect()->route('profile.index')->with('status', 2);
        } else {
            return redirect()->route('profile.index')->with('status', 4);
        }
    }
}
