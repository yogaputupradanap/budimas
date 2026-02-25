from apps import native_db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

class FakturDetailModel(native_db.Model):
    __tablename__ = 'faktur_detail'
    
    id = Column(Integer, primary_key=True)
    id_faktur = Column(Integer)
    id_sales_order = Column(Integer)
    id_principal = Column(Integer)
    subtotal_diskon = Column(Float)
    subtotal= Column(Float)
    pajak = Column(Float)
    draft_total = Column(Float)
    total = Column(Float)


