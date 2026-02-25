from apps import native_db
from sqlalchemy import Column, Integer, ForeignKey


class voucher_3_cabang(native_db.Model):
    __tablename__ = 'voucher_3_cabang'
    
    id = Column(Integer, primary_key=True)
    id_voucher = Column(Integer, ForeignKey('voucher_3.id'))
    id_cabang = Column(Integer, ForeignKey('cabang.id'))