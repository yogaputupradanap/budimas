from apps import native_db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class wilayah1(native_db.Model):
    __tablename__ = 'wilayah1'

    id = Column(Integer, primary_key=True)
    nama = Column(String(25))

    cabang = relationship('cabang', backref='wilayah1', lazy=True)
    principal = relationship('principal', backref='wilayah1', lazy=True)
    wilayah2 = relationship('wilayah2', backref='wilayah1', lazy=True)
    driver = relationship('driver', backref='wilayah1', lazy=True)