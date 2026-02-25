from apps import native_db
from sqlalchemy import Integer, Column, String, SmallInteger, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

class stock_transfer(native_db.Model):
    __tablename__ = 'stock_transfer'

    id = Column(Integer, primary_key=True)
    nota_stock_transfer = Column(String(80))
    id_cabang_awal = Column(Integer)
    id_cabang_tujuan = Column(Integer)
    id_armada = Column(Integer, ForeignKey('armada.id'))
    nama_cabang_awal = Column(String(100))
    nama_cabang_tujuan = Column(String(100))
    status = Column(SmallInteger)
    pengambilan_oleh = Column(String(100))
    tanggal_ambil = Column(Date)
    tanggal_diterima = Column(Date)
    created_at = Column(Date)

    stock_transfer_detail = relationship('stock_transfer_detail', backref = 'stock_transfer', lazy = True)
