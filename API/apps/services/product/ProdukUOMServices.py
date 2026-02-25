from apps.models.ProdukUOM import ProdukUOM as ProdukUOMModel
from sqlalchemy import delete, insert
from apps.conn2 import db
from apps.handler import handle_error_rollback
from apps.exceptions import ValidationException
class ProdukUOMServices:
    # @handle_error_rollback
    def insertdelete_produk_uom(self, data):
        # Logic to upsert product UOM data
        try:
            delete_stmt = delete(ProdukUOMModel).where(
                ProdukUOMModel.id_produk.in_([r['id_produk'] for r in data])
            )
            db.session.execute(delete_stmt)
            for i, r in enumerate(data, start=1):
                new_uom = ProdukUOMModel()
                new_uom.set(r)
                db.session.add(new_uom)
                try:
                    db.session.flush()
                except Exception as inner_err:
                    db.session.rollback()
                    print("==== inner_err harga jual ====\n", str(inner_err))
                    raise ValidationException(f"Kesalahan format data pada baris ke-{i} pastikan format nya benar")
            db.session.commit()
            return {"inserted": len(data), "deleted_for_products": len({r['id_produk'] for r in data})}
        except ValidationException as e:
            db.session.rollback()
            raise

        