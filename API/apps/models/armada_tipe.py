from apps import native_db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class armada_tipe(native_db.Model):
    __tablename__ = 'armada_tipe'
    
    id = Column(Integer, primary_key=True)
    nama = Column(String(50))
    
    armada = relationship('armada', backref='armada_tipe', lazy=True)