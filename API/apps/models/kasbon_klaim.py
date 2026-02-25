from apps import native_db
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime

class kasbon_klaim(native_db.Model):
    __tablename__ = 'kasbon_klaim'
    
    id_kasbon_klaim = Column(Integer, primary_key=True, autoincrement=True)
    kode_kasbon_klaim = Column(String(100), nullable=False, unique=True, index=True)
    tanggal_pengajuan = Column(DateTime, nullable=False, default=datetime.utcnow)
    nominal_kasbon_diajukan = Column(Numeric(20), nullable=True, default=0)
    nominal_kasbon_disetujui = Column(Numeric(20), nullable=True, default=0)
    total_kasbon_terpakai = Column(Numeric(20), nullable=True, default=0)
    keterangan = Column(Text, nullable=True)
    status_kasbon = Column(Integer, nullable=False, default=0, index=True)
    id_user_pengaju = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    id_user_approval = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)
    id_principal = Column(Integer, ForeignKey('principal.id'), nullable=False, index=True)
    tipe_kasbon = Column(Integer, nullable=True)
    
    # --- Relationships ---
    details = relationship("kasbon_klaim_detail", back_populates="kasbon_klaim_header", cascade="all, delete-orphan")
    user_pengaju = relationship("users", foreign_keys=[id_user_pengaju])
    user_approval = relationship("users", foreign_keys=[id_user_approval])
    principal = relationship("principal", foreign_keys=[id_principal])

