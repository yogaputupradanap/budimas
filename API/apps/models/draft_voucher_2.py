from apps import native_db
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from  .  import  BaseModel
class draft_voucher_2(BaseModel):
    __tablename__ = 'draft_voucher_2'
    
    id = Column(Integer, primary_key=True)
    id_detail_sales = Column(Integer, ForeignKey('sales_order_detail.id'))
    id_voucher = Column(Integer)
    status_klaim = Column(Integer)
    tanggal_klaim_faktur = Column(Date)
    tanggal_klaim_ke_principal = Column(Date)
    kode_voucher = Column(String(65))
    jumlah_diskon = Column(Float)
    discount = Column(Float)