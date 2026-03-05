from apps import native_db
from sqlalchemy import Column, Integer, ForeignKey, Date, String, Float, Text
from sqlalchemy.orm import relationship

class canvas_order_detail(native_db.Model):
    __tablename__ = 'canvas_order_detail'

    id = Column(Integer, primary_key=True)
    id_canvas_order = Column(Integer, ForeignKey('canvas_order.id'))
    id_produk = Column(Integer, ForeignKey('produk.id'))
    pcs_order = Column(Integer)
    box_order = Column(Integer)
    carton_order = Column(Integer)
    harga = Column(Float)
    subtotal = Column(Float)
    diskon = Column(Float)
    total = Column(Float)

    # Relationships
    canvas_order = relationship('canvas_order', backref='canvas_order_detail', lazy=True)
    produk = relationship('produk', backref='canvas_order_detail', lazy=True)