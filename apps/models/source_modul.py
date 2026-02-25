from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declared_attr

from apps import native_db
from . import BaseModel

class SourceModulModel(BaseModel):
    __tablename__ = "source_modul"

    # Perbaikan: Kita map kolom 'id' dari BaseModel ke 'id_source_data' di DB
    # agar SQLAlchemy tidak mencari kolom bernama 'id'
    id_source_data = Column(Integer, primary_key=True, autoincrement=True)
    
    # Tambahkan ini jika BaseModel Anda memaksa kolom 'id' ada:
    @declared_attr
    def id(cls):
        return None  # Ini akan menghapus definisi 'id' dari BaseModel untuk model ini

    id_modul = Column(Integer, ForeignKey("modul.id_modul", ondelete="CASCADE"))
    nama_tabel = Column(String)
    nama_kolom_db = Column(String)
    nama_kolom_view = Column(String)

    modul = relationship("ModulModel", back_populates="source_list")
    jurnal_detail_list = relationship("JurnalMalDetailModel", back_populates="source_modul")