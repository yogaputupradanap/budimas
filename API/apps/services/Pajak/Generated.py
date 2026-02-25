from apps.handler import handle_error_rollback
from apps.models.prefix import Prefix
from flask import jsonify
from apps.services.BaseServices import BaseServices

class Generated(BaseServices):
    def __init__(self):
        super().__init__()
        
    @handle_error_rollback
    def GenerateNoFaktur(self):
        try:
            id_perusahaan = int(self.req("id_perusahaan"))
            prefix = self.req("prefix")
            from_num = int(self.req("from"))
            to_num = int(self.req("to"))
            
            if from_num > to_num:
                return jsonify({"message": "Range angka tidak valid."}), 400

            faktur_baru = []
            
            for num in range(from_num, to_num + 1):
                no_faktur_pajak = f"{prefix}{str(num).zfill(8)}" 

                no_faktur_terdaftar = self.db.session.query(Prefix).filter(
                    (Prefix.no_faktur_pajak == no_faktur_pajak) &
                    (Prefix.id_perusahaan == id_perusahaan)
                ).first()

                if no_faktur_terdaftar:
                    return jsonify({
                        "message": f"Nomor faktur {no_faktur_pajak} sudah terdaftar.",
                    }), 400

                pajak = Prefix(
                    id_perusahaan=id_perusahaan,
                    no_faktur_pajak=no_faktur_pajak,
                    sudah_digunakan=False,
                    tanggal_digunakan=None
                )
                self.add(pajak)
                faktur_baru.append({"no_faktur_pajak": no_faktur_pajak})

            self.commit()

            return jsonify({
                "message": "Nomor faktur berhasil digenerate.",
                "numbers": faktur_baru
            }), 200

        except Exception as e:
            self.db.session.rollback()
            return jsonify({"message": "Terjadi kesalahan!", "error": str(e)}), 500

        