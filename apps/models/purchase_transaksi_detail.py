from apps import native_db
from sqlalchemy import Integer, String, Float, Column, Date, ForeignKey
from sqlalchemy.orm import relationship

class purchase_transaksi_detail(native_db.Model):
    __tablename__ = "purchase_transaksi_detail"

    id = Column(Integer, primary_key=True)
    transaksi_id = Column(Integer, ForeignKey('purchase_transaksi.id'))
    tanggal_expired = Column(Date)
    subtotal = Column(Float)
    batch_number = Column(String(50))
    order_detail_id = Column(Integer)