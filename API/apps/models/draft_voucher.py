from apps import native_db
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Time
from sqlalchemy.orm import relationship
from  .  import  BaseModel
class draft_voucher(BaseModel):
    __tablename__ = 'draft_voucher'
    
    id = Column(Integer, primary_key=True)
    id_sales_order = Column(Integer, ForeignKey('sales_order.id'))
    id_voucher = Column(Integer)
    status_klaim = Column(Integer)
    discount = Column(Float)
    tanggal_klaim_faktur = Column(Date)
    tanggal_klaim_principal = Column(Date)
    kode_voucher = Column(String(70))
    jumlah_diskon = Column(Float)
    id_sales_order_detail = Column(Integer)
    tipe_voucher = Column(Integer)
    status_promo = Column(Integer)
    waktu_klaim_faktur = Column(Time)
    waktu_klaim_ke_principal = Column(Time)
    
    draft_voucher_detail = relationship('draft_voucher_detail', backref = 'draft_voucher', lazy = True)