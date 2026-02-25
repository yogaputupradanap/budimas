from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declared_attr # Tambahkan declared_attr

from apps import native_db
from . import BaseModel

class JurnalMalDetailModel(BaseModel):
    __tablename__ = "jurnal_mal_detail"

    # FIX: Paksa SQLAlchemy mengabaikan kolom 'id' dari BaseModel
    @declared_attr
    def id(cls):
        return None

    id_mal_detail = Column(Integer, primary_key=True, autoincrement=True)
    id_jurnal_mal = Column(Integer, ForeignKey("jurnal_mal.id_jurnal_mal", ondelete="CASCADE"))
    id_modul = Column(Integer, ForeignKey("modul.id_modul", ondelete="SET NULL"))
    id_source_data = Column(Integer, ForeignKey("source_modul.id_source_data", ondelete="SET NULL"))
    id_coa = Column(Integer)
    type = Column(Integer)
    urutan = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime)

    jurnal = relationship("JurnalMalModel", back_populates="detail_list")
    modul = relationship("ModulModel", back_populates="jurnal_detail_list")
    source_modul = relationship("SourceModulModel", back_populates="jurnal_detail_list")
    jurnal_details = relationship("JurnalDetailModel", back_populates="jurnal_mal_detail")