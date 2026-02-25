from apps import native_db
from sqlalchemy import Column, Integer, String, Text, Float, Date, ForeignKey


class voucher_1_produk(native_db.Model):
    __tablename__ = 'voucher_1_produk'

    id = Column(Integer, primary_key=True)
    id_voucher = Column(Integer, ForeignKey('voucher_1.id'))
    id_produk = Column(Integer, ForeignKey('produk.id'))