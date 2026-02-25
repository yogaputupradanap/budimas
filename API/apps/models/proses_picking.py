from apps import native_db
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from  .  import  BaseModel
class proses_picking(BaseModel):
    __tablename__ = "proses_picking"
    
    id = Column(Integer, primary_key=True)
    id_order_detail = Column(Integer, ForeignKey('sales_order_detail.id'))
    id_produk = Column(Integer, ForeignKey('produk.id'))
    nama_barang = Column(String(100))
    jumlah_dipesan = Column(String(60))
    jumlah_booked = Column(String(60))
    jumlah_diterima = Column(String(60))
    date_picked = Column(Date)
    pickers = Column(String(60))
    date_on_delivery = Column(Date)
    id_armada = Column(Integer)
    id_driver = Column(Integer)
    date_delivered = Column(Date)
    receiver = Column(String(60))
    jumlah_picked = Column(Integer)
    delivering_date = Column(Date)