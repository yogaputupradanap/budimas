from sqlalchemy import Column, Integer, Date, Float
from apps import native_db

class setoran_customer(native_db.Model):
    __tablename__ = 'setoran_customer'

    id = Column(Integer, primary_key=True)
    id_sales = Column(Integer)
    id_sales_order = Column(Integer)
    jumlah_setoran = Column(Float)
    tipe_setoran = Column(Integer)  # 1: Setoran Tunai, 2: Setoran Non Tunai
    tanggal_input = Column(Date)
    is_rekap = Column(Integer)