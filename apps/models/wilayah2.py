from apps import native_db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class wilayah2(native_db.Model):
    __tablename__ = 'wilayah2'

    id = Column(Integer, primary_key=True)
    id_wilayah1 = Column(Integer, ForeignKey('wilayah1.id'))
    nama = Column(String(50))
    
    cabang = relationship('cabang', backref='wilayah2', lazy=True)
    principal = relationship('principal', backref='wilayah2', lazy=True)
    wilayah3 = relationship('wilayah3', backref='wilayah2', lazy=True)
    driver = relationship('driver', backref='wilayah2', lazy=True)