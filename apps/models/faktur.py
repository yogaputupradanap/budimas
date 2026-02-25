from apps import native_db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from  .  import  BaseModel
class faktur(native_db.Model):
    __tablename__ = 'faktur'
    
    id = Column(Integer, primary_key=True)
    id_sales_order = Column(Integer, ForeignKey('sales_order.id'))
    no_faktur = Column(String(100))
    nama_fakturist = Column(String(100))
    no_seri = Column(String(100))
    status_faktur = Column(Integer)
    jenis_faktur = Column(String(100))
    subtotal_penjualan = Column(Float)
    subtotal_diskon = Column(Float)
    total_penjualan = Column(Float)
    total_dana_diterima = Column(Float)
    no_faktur_pajak = Column(String(100))
    status_faktur_pajak = Column(Integer)
    perubahan_ke = Column(Integer)
    pajak = Column(Float)
    tanggal_retur_pengajuan = Column(Date)
    dpp = Column(Float)
    draft_total_penjualan = Column(Float)
    nominal_retur = Column(Float)
    id_order_batch = Column(Integer, ForeignKey('order_batch.id'))
    
    pengeluaran_driver = relationship('pengeluaran_driver', backref=__tablename__, lazy=True)
    order_batch = relationship('OrderBatchModel', back_populates="faktur")