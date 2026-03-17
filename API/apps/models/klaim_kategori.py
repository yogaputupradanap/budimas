from apps import native_db
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship


class klaim_kategori(native_db.Model):
    __tablename__ = 'klaim_kategori'

    # Tambahkan parameter 'name' sesuai dengan nama kolom di database Anda
    id = Column(Integer, name='id_kategori_klaim', primary_key=True) 
    nama = Column(String(200), nullable=False)
    deskripsi = Column(Text, nullable=True)
    