from apps import native_db
from sqlalchemy import Column, Integer, ForeignKey


class voucher_3_produk(native_db.Model):
    __tablename__ = 'voucher_3_produk'
    
    id = Column(Integer, primary_key=True)
    id_voucher = Column(Integer, ForeignKey('voucher_3.id'))
    id_produk = Column(Integer, ForeignKey('produk.id'))