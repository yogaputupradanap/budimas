from apps import native_db
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship


class klaim_detail(native_db.Model):
    __tablename__ = 'klaim_detail'

    id = Column(Integer, primary_key=True)
    id_klaim = Column(Integer, ForeignKey('klaim.id'), nullable=False)
    id_draft_voucher = Column(Integer, ForeignKey('draft_voucher.id'), nullable=False)
    dpp = Column(Integer, nullable=False)
    ppn = Column(Integer, nullable=False)
    pph = Column(Integer, nullable=False)

    klaim = relationship('klaim', backref='klaim', lazy=True)
    draft_voucher = relationship('draft_voucher', backref='draft_voucher', lazy=True)