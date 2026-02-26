/*
 |--------------------------------------------------------------------------
 | Alert.
 |--------------------------------------------------------------------------
 |
 | Global Alert Functions & Configurations Collection.
 |
 */
/**
 * Class of Alert Collections Utilizing 
 * SweetAlert Lib.
 * 
 * @requires SweetAlert2 `swal`.
 */
class Alerts {
    /** Firing Swal Alert dengan Opsi Untuk Notifikasi. */
	notice(icon, title, text) {
		Swal.fire({
			icon  : icon,
			text  : text,
			title : title,
			timer : 1500,
			showConfirmButton : false
		}); 
    }
    /** Firing Swal Alert dengan Opsi Untuk Konfirmasi. */
	confirmation(icon, title, text) {
		return Swal.fire({
            icon               : icon,
            text               : text,
			title              : title,
            confirmButtonText  : 'Lanjut',
            confirmButtonColor : '#4CAF50',
            showCancelButton   : true,
            cancelButtonText   : 'Batal',
            cancelButtonColor  : '#3085D6',
		}); 
    }
    /** Menampilkan Session Alert (Jika Ada) */ 
    session() {
        switch (parseInt($('#session-alert').val())) {
          case 1 : this.success1(); break;
          case 2 : this.success2(); break;
          case 3 : this.success3(); break;
          case 4 : this.error();    break;
        }
    }
	/** Menampilkan Alert Sukses Insert. */
    success1() {
      	this.notice('success','Berhasil','Data Berhasil Ditambah.');
    }
    /** Menampilkan Alert Sukses Update. */
    success2() {
		this.notice('success','Berhasil','Data Berhasil Diubah.');
    }
    /** Menampilkan Alert Sukses Delete. */
    success3() {
		this.notice('success','Berhasil','Data Berhasil Dihapus.');
    }
    /** Menampilkan Pesan Error/Gagal. */
    error() {
        this.notice('error','Kesalahan','Silahkan Coba Kembali!');
    }
    /** Menampilkan Pesan Pembatalan Aksi. */
    cancel() {
        this.notice('warning','Batal','Aksi telah Dibatalkan!');
    }
    /** Menampilkan Pesan Peringatan Required Form Fill. */
    required1() {
        this.notice('warning','Required','Data Belum Lengakap!');
    }
    /** Menampilkan Pesan Peringatan Required Filter Form Fill. */
    required2() {
        this.notice('warning','Required','Isi Data Filter Terlebih Dahulu!');
    }
    /** Menampilkan Pesan Peringatan Exist Form Fill. */
    exist() {
        this.notice('warning','Data Sudah Ada','Untuk Input Ulang, Hapus Data Terlebih Dahulu');
    }
    /** Menampilkan Konfirmasi Submit Form. */
    submit() {
        return this.confirmation('question','Yakin untuk Submit?','Pastikan Inputan Telah Sesuai!');
    }
    /** Menampilkan Konfirmasi Delete Form. */
    delete() {
        return this.confirmation('warning','Yakin untuk Hapus?','Data yang Dihapus, Tidak Dapat Dikembalikan!');
    }
}

// Instantiate Alert Class.
Alert = () => { return new Alerts(); }

// Run Session Alert.
$(document).ready(function(){
    Alert().session();
});
