from apps import native_db
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship

class ReturRequest(native_db.Model):
    __tablename__ = 'retur_request'

    id_request = Column(Integer, primary_key=True)
    id_sales_order = Column(Integer, ForeignKey('sales_order.id'))
    kode_request = Column(String)
    id_sales = Column(Integer, ForeignKey('users.id'))
    id_customer = Column(Integer, ForeignKey('customer.id'))
    id_principal = Column(Integer, ForeignKey('principal.id'))
    tanggal_request = Column(Date)
    status_request = Column(String)
    subtotal_retur = Column(Float)
    total_dpp_retur = Column(Float)
    total_ppn_retur = Column(Float)
    total_retur = Column(Float)
    tanggal_retur = Column(Date)
    kode_kpr = Column(String)
    no_cn = Column(String)
    total_diskon_retur = Column(Float)
