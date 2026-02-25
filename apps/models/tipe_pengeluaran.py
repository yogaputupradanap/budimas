from apps import native_db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class tipe_pengeluaran(native_db.Model):
    __tablename__ = 'tipe_pengeluaran'
    
    id = Column(Integer, primary_key=True)
    tipe = Column(String(80))
    
    pengeluaran_driver = relationship('pengeluaran_driver', backref=__tablename__, lazy=True)