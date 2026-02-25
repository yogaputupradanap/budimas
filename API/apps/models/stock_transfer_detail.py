from apps import native_db
from sqlalchemy import Integer, Column, ForeignKey, Text

class stock_transfer_detail(native_db.Model):
    __tablename__ = 'stock_transfer_detail'

    id = Column(Integer, primary_key=True)
    id_stock_transfer = Column(Integer, ForeignKey('stock_transfer.id'))
    id_principal = Column(Integer, ForeignKey('principal.id'))
    id_produk = Column(Integer, ForeignKey('produk.id'))
    jumlah = Column(Integer)
    jumlah_diterima = Column(Integer)
    jumlah_picked = Column(Integer)
    jumlah_ditolak = Column(Integer)
    keterangan = Column(Text)
