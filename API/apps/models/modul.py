from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from apps import native_db
from  .  import  BaseModel

class ModulModel(BaseModel):
    __tablename__ = "modul"

    id_modul = Column(Integer, primary_key=True, autoincrement=True)
    nama_modul = Column(String, nullable=False)

    source_list = relationship("SourceModulModel", back_populates="modul", cascade="all, delete-orphan")
    jurnal_detail_list = relationship("JurnalMalDetailModel", back_populates="modul")

