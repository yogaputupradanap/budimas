from apps import native_db
from sqlalchemy import Integer, String, Float, Column, Date, ForeignKey
from sqlalchemy.orm import relationship

class purchase_transaksi_detail_jumlah(native_db.Model):
    __tablename__ = "purchase_transaksi_detail_jumlah"

    id = Column(Integer, primary_key=True)
    transaksi_id = Column(Integer, ForeignKey('purchase_transaksi.id'))
    jumlah = Column(Integer)
    subtotal = Column(Float)
    order_detail_jumlah_id = Column(Integer)
    transaksi_detail_id = Column(Integer)