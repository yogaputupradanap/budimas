from apps import native_db
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

class wilayah3(native_db.Model):
    __tablename__ = 'wilayah3'

    id = Column(BigInteger, primary_key=True)
    id_wilayah2 = Column(Integer, ForeignKey('wilayah2.id'))
    nama = Column(String(50))
    
    cabang = relationship('cabang', backref='wilayah3', lazy=True)
    principal = relationship('principal', backref='wilayah3', lazy=True)
    wilayah4 = relationship('wilayah4', backref='wilayah3', lazy=True)
