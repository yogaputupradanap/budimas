from apps import native_db
from sqlalchemy import Integer, String, Float, Column, Date, ForeignKey
from sqlalchemy.orm import relationship
from  .  import  BaseModel
 
class purchase_tagihan(BaseModel):
    __tablename__ = "purchase_tagihan"

    id = Column(Integer, primary_key=True)
    jatuh_tempo = Column(Date)
    total = Column(Float)
    nominal_pembayaran = Column(Float)
    status_pembayaran = Column(Integer)
    tipe_setoran = Column(String(50))
    keterangan = Column(String(100))
    tanggal_bayar = Column(Date)
    no_tagihan = Column(String(100))
    
    details = relationship("purchase_tagihan_detail", backref="tagihan_detail")