from apps import native_db
from sqlalchemy import Integer, String, Float, Column, Date, ForeignKey
from sqlalchemy.orm import relationship
from  .  import  BaseModel

class purchase_tagihan_detail(BaseModel):
    __tablename__ = "purchase_tagihan_detail"
    
    id = Column(Integer, primary_key=True)
    transaksi_id = Column(Integer, ForeignKey('purchase_transaksi.id'))
    tagihan_id = Column(Integer, ForeignKey('purchase_tagihan.id'))
    subtotal = Column(Float)
    