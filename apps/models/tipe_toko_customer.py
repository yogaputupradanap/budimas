from apps import native_db
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

class tipe_toko_customer(native_db.Model):
    __tablename__ = 'tipe_toko_customer'
    
    id = Column(Integer, primary_key=True)
    tipe_toko = Column(String(30))
    
    voucher_1 = relationship('voucher_1', backref='tipe_toko_customer', lazy=True)
    voucher_2 = relationship('voucher_2', backref='tipe_toko_customer', lazy=True)