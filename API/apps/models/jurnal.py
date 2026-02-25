from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from apps import native_db
from  .  import  BaseModel

class JurnalModel(native_db.Model):
    __tablename__ = "jurnal"

    id_jurnal = Column(Integer, primary_key=True, autoincrement=True)
    id_jurnal_mal = Column(
        Integer,
        ForeignKey("jurnal_mal.id_jurnal_mal", ondelete="SET NULL"),
        nullable=True
    )
    id_perusahaan = Column(Integer, nullable=False)
    id_cabang = Column(Integer)
    tanggal = Column(DateTime, nullable=False)
    keterangan = Column(String)

    # relasi ke detail jurnal (one-to-many)
    details = relationship("JurnalDetailModel", back_populates="jurnal", cascade="all, delete-orphan")
    # Relasi many-to-one ke JurnalMalModel
    jurnal_mal = relationship("JurnalMalModel", back_populates="jurnal_list")
