from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import BaseModel

class CreditNoteDetail(BaseModel):
    __tablename__ = 'credit_note_detail'

    id_cn_detail = Column(Integer, primary_key=True)
    id_cn = Column(
        Integer,
        ForeignKey('credit_note.id_cn', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    )

    id_retur_request_detail = Column(Integer, nullable=False)
    nominal_cn = Column(Float, nullable=False)
    tanggal = Column(DateTime, nullable=False)
    subtotal = Column(Float, nullable=False)

    # many details -> one CreditNote
    credit_note = relationship(
        "CreditNote",
        back_populates="details"
    )
