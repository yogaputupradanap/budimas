from apps import native_db
from sqlalchemy import Column, Integer, String, Text, Float, Date, ForeignKey


class voucher_2_cabang(native_db.Model):
    __tablename__ = 'voucher_2_cabang'
    
    id = Column(Integer, primary_key=True)
    id_voucher = Column(Integer, ForeignKey('voucher_2.id'))
    id_cabang = Column(Integer, ForeignKey('cabang.id'))