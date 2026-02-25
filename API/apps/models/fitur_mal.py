from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from apps import native_db

from  .  import  BaseModel
class FiturMalModel(BaseModel):
    __tablename__ = "fitur_mal"

    id_fitur_mal = Column(Integer, primary_key=True, autoincrement=True)
    nama_fitur_mal = Column(String, nullable=False)

    jurnal_list = relationship("JurnalMalModel", back_populates="fitur")


