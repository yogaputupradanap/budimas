from sqlalchemy import Column, Integer, String, Date, Float, Text, ForeignKey, DateTime
from apps import native_db
from  .  import  BaseModel

class pengeluaran_kasir(BaseModel):
    __tablename__ = 'pengeluaran_kasir'

    id = Column(Integer, primary_key=True)
    id_cabang = Column(Integer, ForeignKey('cabang.id'), nullable=False)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    no_pengeluaran = Column(String(50), nullable=False)
    keterangan_pengeluaran = Column(Text)
    pic = Column(String(100), nullable=False)
    tanggal_pengajuan = Column(DateTime, nullable=False)
    tanggal_acc = Column(DateTime)
    tanggal_diberikan = Column(DateTime)
    jumlah_pengeluaran = Column(Float, nullable=False)
    status_pengeluaran = Column(Integer, nullable=False) # 0 : diajukan 1 : disetujui 2 : ditolak 3 : diberikan
    jumlah_acc = Column(Float, nullable=True, default=0.0)
    id_perusahaan = Column(Integer)