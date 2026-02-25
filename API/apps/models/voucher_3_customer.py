from apps import native_db
from sqlalchemy import Column, Integer, ForeignKey


class voucher_3_customer(native_db.Model):
    __tablename__ = 'voucher_3_customer'
    
    id = Column(Integer, primary_key=True)
    id_voucher = Column(Integer, ForeignKey('voucher_3.id'))
    id_customer = Column(Integer, ForeignKey('customer.id'))