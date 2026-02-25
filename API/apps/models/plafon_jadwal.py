from sqlalchemy import Column, Integer, ForeignKey
from apps import native_db
from sqlalchemy.orm import relationship

class plafon_jadwal(native_db.Model):
    __tablename__ = "plafon_jadwal"
    
    id = Column(Integer, primary_key=True)
    id_plafon = Column(Integer, ForeignKey('plafon.id'))
    id_tipe_kunjungan = Column(Integer)
    id_hari = Column(Integer)
    id_minggu = Column(Integer)
    id_status = Column(Integer)
    
    sales_kunjungan = relationship("sales_kunjungan", backref="plafon_jadwal", lazy=True)