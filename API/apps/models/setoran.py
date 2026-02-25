from sqlalchemy import Column, Integer, String, Date, Float, Text, ForeignKey, Numeric
from apps import native_db
from  .  import  BaseModel

class setoran(BaseModel):
    __tablename__ = 'setoran'

    id = Column(Integer, primary_key=True)
    id_sales_order = Column(Integer, ForeignKey('sales_order.id'))
    draft_tanggal_input = Column(Date)
    draft_jumlah_setor = Column(Float)
    draft_tipe_setor = Column(Integer)
    keterangan = Column(Text)
    nama_pj = Column(String(60))
    jumlah_setoran = Column(Integer)
    tipe_setoran = Column(Integer)
    tanggal_setoran_diterima = Column(Date)
    keterangan_kasir = Column(Text)
    nama_kasir = Column(String(60))
    status_audit = Column(Integer)
    nama_auditor = Column(String(60))
    metode_pembayaran = Column(String(60))
    bukti_transfer = Column(String(255))
    status_setoran = Column(Integer)
    biaya_lainnya = Column(Float())
    ket_biaya_lainnya = Column(Text)
    setoran_bersih = Column(Float)
    max_biaya_lainnya = Column(Numeric, default=2900)
    id_setoran_customer = Column(Integer)
    pj_setoran = Column(Integer) # 1 = sales , 2 = admin gudang
    id_order_batch = Column(Integer)