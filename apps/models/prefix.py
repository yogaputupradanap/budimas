from apps import native_db
from sqlalchemy import Column, Integer, String, Boolean, DateTime

class Prefix(native_db.Model):
    __tablename__ = 'prefix'

    id = Column(Integer, primary_key=True, autoincrement=True)
    no_faktur_pajak = Column(String(20), nullable=False)  # Faktur berupa string
    sudah_digunakan = Column(Boolean, nullable=False, default=False)  # Boolean
    tanggal_digunakan = Column(DateTime, nullable=True)  # Tanggal jika sudah digunakan
    id_perusahaan = Column(Integer, nullable=True)  # ID perusahaan wajib diisi
    faktur_id = Column(Integer, nullable=True)
