from apps import native_db
from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

class canvas_request_detail(native_db.Model):
    __tablename__ = 'canvas_request_detail'
    
    id = Column(Integer, primary_key=True)
    id_canvas = Column(Integer, ForeignKey('canvas_request.id' , ondelete='CASCADE'))
    id_produk = Column(Integer, ForeignKey('produk.id'))
    qty_request = Column(Float)
    qty_approve = Column(Float)
    status = Column(Integer)

    canvas_request = relationship('canvas_request', backref='canvas_request_detail', lazy=True)
    produk = relationship('produk', backref='canvas_request_detail', lazy=True)