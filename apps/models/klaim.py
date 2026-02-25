from apps import native_db
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime


class klaim(native_db.Model):
    __tablename__ = 'klaim'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_voucher = Column(Integer, nullable=False, index=True)
    id_kategori_klaim = Column(Integer, ForeignKey('klaim_kategori.id'), nullable=False, index=True)
    id_user_adm_klaim = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    nomor_klaim = Column(String(100), nullable=False, unique=True, index=True)
    kode_voucher = Column(String(50), nullable=False, index=True) 
    total_dpp = Column(Numeric(15, 2), nullable=False, default=0.00)
    total_ppn = Column(Numeric(15, 2), nullable=False, default=0.00)
    total_pph = Column(Numeric(15, 2), nullable=False, default=0.00)
    total_klaim_diajukan = Column(Numeric(15, 2), nullable=False, default=0.00)
    total_klaim_diterima = Column(Numeric(15, 2), nullable=True, default=0.00)
    tanggal_pengajuan_klaim = Column(DateTime, nullable=False, default=datetime.utcnow)
    tanggal_penerimaan_klaim = Column(DateTime, nullable=True)
    status = Column(Integer, nullable=False, default=0, index=True)
    
    
    # Relationships
    user_admin = relationship("users", backref="users", lazy=True)
    kategori_klaim = relationship("klaim_kategori", backref="klaim_kategori", lazy=True)