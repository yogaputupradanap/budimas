from apps import native_db
from sqlalchemy import Column, Integer, Float, ForeignKey
from  .  import  BaseModel
class draft_voucher_detail(BaseModel):
    __tablename__ = 'draft_voucher_detail'
    
    id = Column(Integer, primary_key=True)
    id_draft_voucher = Column(Integer, ForeignKey('draft_voucher.id'))
    id_produk = Column(Integer, ForeignKey('produk.id'))
    discount = Column(Integer)
    nilai_discount = Column(Float)