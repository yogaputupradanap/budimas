from sqlalchemy import Column, Integer, Time, Date, SmallInteger, ForeignKey
from apps import native_db
class sales_kunjungan(native_db.Model):
    __tablename__ = "sales_kunjungan"
    
    id = Column(Integer, primary_key=True)
    id_plafon = Column(Integer, ForeignKey('plafon.id'))
    id_plafon_jadwal = Column(Integer, ForeignKey('plafon_jadwal.id'))
    tanggal = Column(Date)
    waktu_mulai = Column(Time)
    waktu_selesai = Column(Time)
    status = Column(SmallInteger)