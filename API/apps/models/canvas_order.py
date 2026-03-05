from apps import native_db
from sqlalchemy import Column, Integer, ForeignKey, Date, String, Float, Text
from sqlalchemy.orm import relationship

class canvas_order(native_db.Model):
    __tablename__ = 'canvas_order'
    
    id = Column(Integer, primary_key=True)
    id_canvas_request = Column(Integer, ForeignKey('canvas_request.id', ondelete='CASCADE'))
    nama_customer = Column(String(255))
    tanggal_order = Column(Date)
    tanggal_faktur = Column(Date)
    total_order = Column(Float)
    sub_total_order = Column(Float)
    id_voucher_2 = Column(Integer, ForeignKey('voucher_2.id'), nullable=True)
    id_voucher_3 = Column(Integer, ForeignKey('voucher_3.id'), nullable=True)
    total_diskon = Column(Float)
    alamat = Column(Text)
    status_order = Column(Integer)

    # Relationships
    canvas_request = relationship('canvas_request', backref='orders', lazy=True)
    voucher_2 = relationship('voucher_2', backref='orders', lazy=True)
    voucher_3 = relationship('voucher_3', backref='orders', lazy=True)