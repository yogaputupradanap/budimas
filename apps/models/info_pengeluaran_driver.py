from apps import native_db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

class info_pengeluaran_driver(native_db.Model):
    __tablename__ = 'info_pengeluaran_driver'
    
    id = Column(Integer, primary_key=True)
    id_driver = Column(Integer, ForeignKey('driver.id'))
    tujuan = Column(String(100))
    km_berangkat = Column(Float)
    helper = Column(String(100))
    km_pulang = Column(Float)
    km_isi_bbm = Column(Float)
    isi_bbm_liter = Column(Float)
    isi_bbm_rupiah = Column(Float)
    uang_saku = Column(Float)
    tanggal = Column(Date)
    
    pengeluaran_driver = relationship('pengeluaran_driver', backref=__tablename__, lazy=True)