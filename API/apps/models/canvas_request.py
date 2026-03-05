from apps import native_db
from sqlalchemy import Column, Integer, Date, ForeignKey, Float
from sqlalchemy.orm import relationship

class canvas_request(native_db.Model):
    __tablename__ = 'canvas_request'
    
    id = Column(Integer, primary_key=True)
    id_sales = Column(Integer, ForeignKey('sales.id'))
    tanggal_request = Column(Date)
    plafon_limit = Column(Float)
    total_request = Column(Float)
    status = Column(Integer)

    sales = relationship('sales', backref='canvas_request', lazy=True)