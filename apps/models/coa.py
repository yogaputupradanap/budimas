from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from apps import native_db
from  .  import  BaseModel


class CoaModel(native_db.Model): 
    __tablename__ = "coa"

    # Sekarang id_coa menjadi satu-satunya primary key
    id_coa = Column(Integer, primary_key=True, autoincrement=True)
    id_kategori = Column(Integer, ForeignKey("coa_category.id_category", ondelete="SET NULL"))
    id_perusahaan = Column(Integer, nullable=False)
    nomor_akun = Column(String)
    nama_akun = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer)
    parent_id = Column(Integer, ForeignKey("coa.id_coa"), nullable=True)
    principal_id = Column(Integer, ForeignKey("principal.id"), nullable=True)

    kategori = relationship("CoaCategoryModel", back_populates="coa_list")