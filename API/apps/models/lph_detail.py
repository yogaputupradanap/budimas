from sqlalchemy import Column, Integer, String, Date, Float, Text, ForeignKey, DateTime
from apps import native_db
from  .  import  BaseModel
class lph_detail(BaseModel):
    __tablename__ = 'lph_detail'

    id = Column(Integer, primary_key=True)
    id_lph = Column(Integer, ForeignKey('lph.id'))
    id_faktur = Column(Integer, ForeignKey('faktur.id'))
    jumlah_tagihan = Column(Float)
    nominal_retur = Column(Float)
    kode_cn = Column(String)
