from apps.models.ProdukHargaJual import ProdukHargaJual as ProdukHargaJualModel
from sqlalchemy import delete, insert
from apps.conn2 import db
from apps.handler import handle_error_rollback
from apps.exceptions import ValidationException
class ProdukHargaJualServices:
    @staticmethod
    def _dedupe_by_keys(rows, keys=('id_produk', 'id_tipe_harga'), keep='last'):
        """
        Hapus duplikat berdasarkan kombinasi keys.
        keep = 'first' atau 'last' menentukan baris mana yang dipertahankan.
        """
        if not rows:
            return []

        print("==== deduping harga jual ====\n", f"keys: {keys} \n keep: {keep} \n total_rows: {len(rows)} \n rows: {rows}")
        if keep == 'first':
            seen = set()
            out = []
            for r in rows:
                k = tuple(r.get(k) for k in keys)
                if k in seen:
                    continue
                seen.add(k)
                out.append(r)
            return out
        else:  # keep last
            seen = set()
            out_rev = []
            for r in reversed(rows):
                k = tuple(r.get(k) for k in keys)
                if k in seen:
                    continue
                seen.add(k)
                print("==== keeping harga jual ====\n", r)
                out_rev.append(r)

            return list(reversed(out_rev))

    # @handle_error_rollback
    def insertdelete_produk_hargajual(self, data):
        # Logic to upsert product UOM data

        try:
            data = list(data or [])
            if not data:
                raise ValidationException("Data tidak boleh kosong")
            # print("==== incoming harga jual ====\n", data)
            # Menghapus data lama berdasarkan id_produk
            ids_produk = sorted({r.get('id_produk') for r in data if r.get('id_produk') not in (None, "", "NULL")})
            delete_stmt = delete(ProdukHargaJualModel).where(
                ProdukHargaJualModel.id_produk.in_(ids_produk)
            )
            deduped = self._dedupe_by_keys(data, keys=set(['id_produk']), keep='last')
            # print("==== deduped harga jual ====\n", deduped)

            db.session.execute(delete_stmt)

            if deduped:
              for i, r in enumerate(deduped, start=1):
                    new_hargajual = ProdukHargaJualModel()
                    new_hargajual.set(r)
                    db.session.add(new_hargajual)
                    try:
                        db.session.flush()
                    except Exception as inner_err:
                        db.session.rollback()
                        print("==== inner_err harga jual ====\n", str(inner_err))
                        raise ValidationException(f"Kesalahan format data pada baris ke-{i} pastikan format nya benar")
              db.session.commit()

            return {"inserted": len(deduped), "deleted_for_products": len(ids_produk)}
        except ValidationException as e:
            db.session.rollback()
            raise
            # raise e