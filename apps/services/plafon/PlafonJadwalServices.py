from apps.exceptions import ValidationException
from apps.models.PlafonJadwal import PlafonJadwal as PlafonJadwalModel
from sqlalchemy import delete
from apps.conn2 import db
class PlafonJadwalServices:
    def insertdelete_plafon_jadwal(self, data):
        # Implementasi logika insert/delete plafon jadwal di sini
        try:
            data = list(data or [])
            if not data:
                raise ValidationException("Data tidak boleh kosong")
            
            ids_plafon = sorted({r.get('id_plafon') for r in data if r.get('id_plafon') not in (None, "", "NULL")})
            delete_stmt = delete(PlafonJadwalModel).where(
                PlafonJadwalModel.id_plafon.in_(ids_plafon)
            )

            db.session.execute(delete_stmt)

            for i, r in enumerate(data, start=1):
                new_jadwal = PlafonJadwalModel()
                new_jadwal.set(dict(r, id_tipe_kunjungan=1))
                db.session.add(new_jadwal)
                try:
                    db.session.flush()
                except Exception as inner_err:
                    db.session.rollback()
                    print("==== inner_err plafon jadwal ====\n", str(inner_err))
                    raise ValidationException(f"Kesalahan format data pada baris ke-{i} pastikan format nya benar")
            db.session.commit()
            return {"inserted": len(data), "deleted_for_plafon": len({r['id_plafon'] for r in data})}
        except Exception as e:
            raise e