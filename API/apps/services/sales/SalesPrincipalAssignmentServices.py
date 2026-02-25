from sqlalchemy import delete, insert
from apps.conn2 import db
from apps.exceptions import ValidationException
from apps.models.SalesPrincipalAssignment import SalesPrincipalAssignment
class SalesPrincipalAssignmentServices:
    
    def insertdelete_sales_principal_assignment(self, data):
        try:
            delete_stmt = delete(SalesPrincipalAssignment).where(
                SalesPrincipalAssignment.id_sales.in_([r['id_sales'] for r in data])
            )
            db.session.execute(delete_stmt)
            for i, r in enumerate(data, start=1):
                new_assignment = SalesPrincipalAssignment()
                new_assignment.set(r)
                db.session.add(new_assignment)
                try:
                    db.session.flush()
                except Exception as inner_err:
                    db.session.rollback()
                    print("==== inner_err sales principal assignment ====\n", str(inner_err))
                    raise ValidationException(f"Kesalahan format data pada baris ke-{i} pastikan format nya benar")
            db.session.commit()
            return {"inserted": len(data), "deleted_for_users": len({r['id_sales'] for r in data})}
        except ValidationException as e:
            db.session.rollback()
            raise