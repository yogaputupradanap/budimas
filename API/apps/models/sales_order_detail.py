from sqlalchemy import Column, Integer, String, Text, Float, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from apps import native_db

class sales_order_detail(native_db.Model):
    __tablename__ = 'sales_order_detail'

    id = Column(Integer, primary_key=True)
    hargaorder = Column(Float)
    subtotaldelivered = Column(Integer)
    is_bonus = Column(Integer)
    estimasi_kubikasi = Column(Float)
    id_sales_order = Column(Integer, ForeignKey('sales_order.id'))
    id_produk = Column(Integer)
    pieces_order = Column(Integer)
    box_order = Column(Integer)
    karton_order = Column(Integer)
    pieces_booked = Column(Integer)
    box_booked = Column(Integer)
    karton_booked = Column(Integer)
    pieces_picked = Column(Integer)
    box_picked = Column(Integer)
    karton_picked = Column(Integer)
    pieces_shipped = Column(Integer)
    box_shipped = Column(Integer)
    karton_shipped = Column(Integer)
    pieces_delivered = Column(Integer)
    box_delivered = Column(Integer)
    karton_delivered = Column(Integer)
    vouchers = Column(ARRAY(String))
    subtotalorder = Column(Float)
    pieces_retur = Column(Integer)
    box_retur = Column(Integer)
    karton_retur = Column(Integer)
    keterangan_retur = Column(Text)
    total_nilai_discount = Column(Float)
    
    draft_voucher_2 = relationship('draft_voucher_2', backref='draft_voucher_2', lazy=True)
    proses_picking = relationship('proses_picking', backref='sales_order_detail', lazy=True)