from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from apps import native_db
from  .  import  BaseModel

class JurnalDetailModel(native_db.Model): # Ubah ke native_db.Model
    __tablename__ = "jurnal_detail"

    # Definisikan Primary Key sesuai dengan kenyataan di database
    id_jurnal_detail = Column(Integer, primary_key=True, autoincrement=True)
    
    # Kolom lainnya tetap sama
    id_jurnal = Column(Integer, ForeignKey("jurnal.id_jurnal", ondelete="CASCADE"))
    kode_jurnal = Column(String, nullable=False)
    nama_akun = Column(String, nullable=False)
    keterangan = Column(String)
    debit = Column(DECIMAL(18, 2), default=0)
    kredit = Column(DECIMAL(18, 2), default=0)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer)
    id_mal_detail = Column(Integer, ForeignKey("jurnal_mal_detail.id_mal_detail", ondelete="SET NULL"), nullable=True)

    # Relasi
    jurnal = relationship("JurnalModel", back_populates="details")
    # relasi ke tabel jurnal_mal_detail (many-to-one)
    jurnal_mal_detail = relationship("JurnalMalDetailModel", back_populates="jurnal_details")
