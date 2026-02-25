from apps import native_db
from sqlalchemy import Column, Integer, Float, ForeignKey, Date, String, Text, DateTime

class pajak(native_db.Model):
  __tablename__ = 'pajak'

  id = Column(Integer, primary_key=True)
  id_faktur = Column(Integer, ForeignKey('faktur.id'))
  id_perusahaan = Column(Integer, ForeignKey('perusahaan.id'))
  id_cabang = Column(Integer, ForeignKey('cabang.id'))
  no_faktur = Column(String(100))
  nsfp = Column(Integer)
  nama_fakturist = Column(String(100))
  tanggal_faktur = Column(Date)
  subtotal_penjualan = Column(Float)
  total_penjualan = Column(Float)
  subtotal_diskon = Column(Float)
  dpp = Column(Float)
  pajak = Column(Float)
  keterangan_pajak = Column(Text)
  tanggal_import_pajak = Column(DateTime)
  tanggal_export_pajak = Column(DateTime)
  export_pajak = Column(Integer)
  tanggal_lapor = Column(DateTime)
  status_faktur_pajak = Column(Integer)