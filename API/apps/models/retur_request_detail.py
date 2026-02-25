from apps import native_db
from sqlalchemy import Column, Integer, ForeignKey, Float, Text

class ReturRequestDetail(native_db.Model):
    __tablename__ = 'retur_request_detail'

    id_request_detail = Column(Integer, primary_key=True)
    id_request = Column(Integer, ForeignKey('retur_request.id_request'))
    id_sales_order_detail = Column(Integer, ForeignKey('sales_order_detail.id'))
    id_produk = Column(Integer, ForeignKey('produk.id'))

    pieces_diajukan = Column(Integer)
    box_diajukan = Column(Integer)
    karton_diajukan = Column(Integer)
    alasan_retur = Column(Text)

    harga_satuan = Column(Float)
    subtotal_retur = Column(Float)
    diskon_retur = Column(Float)
    dpp_retur = Column(Float)
    ppn_retur = Column(Float)
    total_retur = Column(Float)
    pieces_retur = Column(Integer)
    box_retur = Column(Integer)
    karton_retur = Column(  Integer)
    pieces_good_diajukan = Column(Integer)
    box_good_diajukan = Column(Integer)
    karton_good_diajukan = Column(Integer)
