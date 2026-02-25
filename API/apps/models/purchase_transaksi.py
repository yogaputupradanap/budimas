from apps import native_db
from sqlalchemy import Integer, String, Float, Column, SmallInteger, Date, ForeignKey, Text
from sqlalchemy.orm import relationship

class purchase_transaksi(native_db.Model):
    __tablename__ = "purchase_transaksi"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    no_transaksi = Column(String(100))
    subtotal = Column(Float)
    potongan = Column(Float)
    biaya_lainnya = Column(Float)
    total = Column(Float)
    status_pembayaran = Column(SmallInteger)
    proses_id_berjalan = Column(SmallInteger)
    batch = Column(SmallInteger)
    keterangan = Column(String(100))
    jatuh_tempo = Column(Date)

    tagihan_details = relationship("purchase_tagihan_detail", backref="tagihan_detail_transaksi")
    purchase_transaksi_detail = relationship('purchase_transaksi_detail', backref=__tablename__, lazy=True)
    purchase_transaksi_detail_jumlah = relationship('purchase_transaksi_detail_jumlah', backref=__tablename__, lazy=True)