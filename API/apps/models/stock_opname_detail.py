from apps import native_db
from sqlalchemy import Integer, Column, ForeignKey, Text,BigInteger, Float

class stock_opname_detail(native_db.Model):
    __tablename__ = 'stock_opname_detail'

    id_stock_opname_detail = Column(Integer, primary_key=True)
    id_stock_opname = Column(Integer, ForeignKey('stock_opname.id_stock_opname'))
    id_produk = Column(Integer, ForeignKey('produk.id'))
    uom_3 = Column(Integer)
    uom_2 = Column(Integer)
    uom_1 = Column(Integer)
    stok = Column(Integer)
    stok_sistem = Column(Integer)
    harga = Column(Float)
    bad_stock = Column(Integer)
    subtotal = Column(Float)
    subtotal_selisih = Column(Float)
    ket_produk = Column(Text)
