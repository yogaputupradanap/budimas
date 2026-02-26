@extends('layouts.main')
@section('content')
    @include('partials.breadcrumb')
    <!-- ============================================================== -->
    <!-- Content Container  -->
    <!-- ============================================================== -->
    <div class="container-fluid">
        <div class="row m-md-1">
            <div class="col-md-12">
                <form action="{{ route('profile.update') }}" method="post" class="form-horizontal">
                    <div class="card form">
                        <div class="card-header">
                            <span class="card-title">Edit {{ $content->name }}</span>
                        </div>
                        <div class="card-body card-bar-menu">
                            <div class="btn-group" role="group">
                                <a class="btn btn-primary" type="button" onclick="submitConfirmation(event, this)">
                                    <i class="mdi mdi-pencil"></i>Edit
                                </a>
                                <a class="btn btn-danger" onclick="window.history.back()">
                                    <i class="mdi mdi-step-backward"></i>Kembali
                                </a>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="row m-md-2">
                                <div class="col-md-6 px-md-3">
                                    @csrf
                                    <input type="hidden" name="idJabatanEx" value="{{ $user->id_jabatan }}" disabled>
                                    <div class="input-group">
                                        <div class="form-group w-100">
                                            <label>Nama</label>
                                            <input type="text" name="nama" value="{{ $user->nama }}"
                                                class="form-control-modal" maxlength="50"
                                                placeholder="Masukkan Nama Lengkap User (Max 50 Karakter)" required>
                                        </div>
                                    </div>
                                    <div class="input-group">
                                        <div class="form-group w-100">
                                            <label>Cabang</label>
                                            <div>
                                                <select class="select2 shadow-none" name="idCabang" disabled>
                                                    <option value="" selected disabled> Pilih Cabang </option>
                                                    @foreach ($nCabang as $cabang)
                                                        <option value="{{ $cabang->id }}"
                                                            {{ $cabang->id == $user->id_cabang ? 'selected' : '' }}>
                                                            {{ $cabang->nama }}
                                                        </option>
                                                    @endforeach
                                                </select>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="input-group">
                                        <div class="form-group w-100">
                                            <label>Jabatan</label>
                                            <div>
                                                <select class="select2 shadow-none" name="idJabatan" disabled>
                                                    <option value="" selected disabled> Pilih Jabatan </option>
                                                    @foreach ($nJabatan as $jabatan)
                                                        <option value="{{ $jabatan->id }}"
                                                            {{ $jabatan->id == $user->id_jabatan ? 'selected' : '' }}>
                                                            {{ $jabatan->nama }}
                                                        </option>
                                                    @endforeach
                                                </select>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="input-group">
                                        <div class="form-group w-100">
                                            <label>Username</label>
                                            <input type="text" name="username" value="{{ $user->username }}"
                                                class="form-control-modal" placeholder="Masukkan Username Untuk Login"
                                                required>
                                        </div>
                                    </div>
                                    <div class="input-group">
                                        <div class="form-group w-100">
                                            <label>Password</label>
                                            <input type="password" name="password" value=""
                                                class="form-control-modal password active form-control-md"
                                                placeholder="Masukkan Password Untuk Login">
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6 px-md-3">
                                    <div class="input-group">
                                        <div class="form-group w-100">
                                            <label>NIK</label>
                                            <input type="number" name="nik" value="{{ $user->nik }}"
                                                class="form-control-modal" maxlength="25"
                                                placeholder="Masukkan Nomor Induk User (Max 25 Karakter)" disabled>
                                        </div>
                                    </div>
                                    <div class="input-group">
                                        <div class="form-group w-100">
                                            <label>E-mail</label>
                                            <input type="email" name="email" value="{{ $user->email }}"
                                                class="form-control-modal"
                                                placeholder="Masukkan E-mail User (Max 100 Karakter) e.g. user@mail.com">
                                        </div>
                                    </div>
                                    <div class="input-group">
                                        <div class="form-group w-100">
                                            <label>Telepon</label>
                                            <input type="number" name="telepon" value="{{ $user->telepon }}"
                                                class="form-control-modal" maxlength="13"
                                                placeholder="Masukkan Telepon User (Max 13 Karater) e.g. 081212341234">
                                        </div>
                                    </div>
                                    <div class="input-group">
                                        <div class="form-group w-100">
                                            <label>Tanggal Lahir</label>
                                            <input type="text" name="tanggalLahir" value="{{ $user->tanggal_lahir }}"
                                                class="datepicker form-control-modal"
                                                placeholder="Masukkan Tanggal Lahir (yyyy-mm-dd) e.g. 2000-08-31">
                                        </div>
                                    </div>
                                    <div class="input-group">
                                        <div class="form-group w-100">
                                            <label>Alamat</label>
                                            <textarea type="text" name="alamat" class="form-control-modal" maxlength="100"
                                                placeholder="Masukkan Alamat User (Max 100 Karater)">{{ $user->alamat }}</textarea>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
    <!-- ============================================================== -->
    <!-- End Content Container  -->
    <!-- ============================================================== -->
@endsection
