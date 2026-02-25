from sqlalchemy import Column, Integer, String, Date, Float, Text, ForeignKey, DateTime
from apps import native_db
from  .  import  BaseModel
class lph(BaseModel):
    __tablename__ = 'lph'

    id = Column(Integer, primary_key=True)
    id_sales = Column(Integer)
    id_user = Column(Integer)
    kode_lph = Column(String(50))
    tanggal_lph = Column(DateTime)
    jumlah_ditagih = Column(Float)
    batch_cetak = Column(Integer)
    is_cp = Column(Integer)  # 0: tidak, 1: ya
    tanggal_dicetak = Column(DateTime)
    total_retur = Column(Float)
