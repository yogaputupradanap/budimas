from apps import native_db
from sqlalchemy import Column, Integer, Float, ForeignKey, Date, Text
from  .  import  BaseModel
class pengeluaran_driver(BaseModel):
    __tablename__ = 'pengeluaran_driver'
    
    id = Column(Integer, primary_key=True)
    id_tipe = Column(Integer, ForeignKey('tipe_pengeluaran.id'))
    tanggal = Column(Date)
    nominal = Column(Float)
    keterangan = Column(Text)
    id_faktur = Column(Integer, ForeignKey('faktur.id'))
    id_info = Column(Integer, ForeignKey('info_pengeluaran_driver.id'))
    