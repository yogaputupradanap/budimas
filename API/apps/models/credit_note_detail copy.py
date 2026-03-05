from apps import native_db
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class CreditNoteDetail(native_db.Model):
    __tablename__ = 'credit_note_detail'

    id_cn_detail = Column(Integer, primary_key=True)
    id_cn = Column(Integer, ForeignKey('credit_note.id_cn', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    id_retur_request_detail = Column(Integer, nullable=False)
    nominal_cn = Column(Float, nullable=False)
    tanggal = Column(DateTime, nullable=False)
    subtotal = Column(Float, nullable=False)