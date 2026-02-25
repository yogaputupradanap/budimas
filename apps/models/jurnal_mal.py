from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declared_attr # Tambahkan declared_attr

from apps import native_db
from . import BaseModel

class JurnalMalModel(BaseModel):
    __tablename__ = "jurnal_mal"

    # FIX: Paksa SQLAlchemy mengabaikan kolom 'id' dari BaseModel
    @declared_attr
    def id(cls):
        return None

    id_jurnal_mal = Column(Integer, primary_key=True, autoincrement=True)
    id_perusahaan = Column(Integer, nullable=False)
    id_fitur_mal = Column(Integer, ForeignKey("fitur_mal.id_fitur_mal", ondelete="SET NULL"))
    main_coa_id = Column(Integer, ForeignKey("coa.id_coa", ondelete="SET NULL"))
    nama_mal = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    created_by = Column(Integer)

    fitur = relationship("FiturMalModel", back_populates="jurnal_list")
    detail_list = relationship(
        "JurnalMalDetailModel",
        back_populates="jurnal",
        cascade="all, delete-orphan"
    )

    jurnal_list = relationship("JurnalModel", back_populates="jurnal_mal")