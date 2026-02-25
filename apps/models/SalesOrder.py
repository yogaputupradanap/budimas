from apps import native_db
from sqlalchemy import Integer, String, Float, Column, SmallInteger, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from  .  import  BaseModel

class sales_order(BaseModel):
    __tablename__ = "sales_order"
    
    id = Column(Integer, primary_key=True)
    id_plafon = Column(Integer, ForeignKey('plafon.id'))
    tanggal_order = Column(Date)
    tanggal_faktur = Column(Date)
    tanggal_terkirim = Column(Date)
    tanggal_jatuh_tempo = Column(Date)
    nama_sales = Column(String(100))
    pic_customer = Column(String(100))
    total_kubikasi = Column(Integer)
    status_order = Column(SmallInteger)
    total_order = Column(Float)
    no_order = Column(String(100))
    no_tagihan = Column(String(80))
    no_faktur = Column(String(100))
    keterangan = Column(Text)
    
    sales_order_detail = relationship('sales_order_detail', backref = 'sales_order', lazy = True)
    faktur = relationship('faktur', backref = 'sales_order', lazy = True)
    draft_voucher = relationship('draft_voucher', backref = 'sales_order', lazy = True)
    setoran = relationship('setoran', backref = 'sales_order', lazy = True)