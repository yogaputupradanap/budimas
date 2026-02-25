from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from . import BaseModel

class CreditNote(BaseModel):
    __tablename__ = 'credit_note'

    id_cn = Column(Integer, primary_key=True)
    kode_cn = Column(String(50), nullable=False)
    id_customer = Column(Integer, nullable=False)
    id_principal = Column(Integer, nullable=False)
    tanggal = Column(DateTime, nullable=False)
    status_cn = Column(Integer, nullable=False)
    id_retur_request = Column(Integer, nullable=False)
    total_cn = Column(Float, default=0)
    id_faktur = Column(Integer)

    # one CreditNote -> many details
    details = relationship(
        "CreditNoteDetail",
        back_populates="credit_note",
        cascade="all, delete-orphan",
        lazy="select"
    )
