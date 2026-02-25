from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from apps import native_db
from  .  import  BaseModel

class CoaCategoryModel(BaseModel):
    __tablename__ = "coa_category"

    id_category = Column(Integer, primary_key=True, autoincrement=True)
    nama_kategori = Column(String, nullable=False)

    coa_list = relationship("CoaModel", back_populates="kategori", lazy=True)
