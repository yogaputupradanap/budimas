from apps import native_db
from sqlalchemy import Column, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

class wilayah4(native_db.Model):
    __tablename__ = 'wilayah4'

    id = Column(BigInteger, primary_key=True)
    id_wilayah3 = Column(BigInteger, ForeignKey('wilayah3.id'))
    nama = Column(String(50))
    
    cabang = relationship('cabang', backref='wilayah4', lazy=True)
    principal = relationship('principal', backref='wilayah4', lazy=True)