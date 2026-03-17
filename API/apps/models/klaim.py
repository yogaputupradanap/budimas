from apps import native_db
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

# Import class secara eksplisit dari file User.py
# Pastikan path import sesuai dengan struktur folder Anda
try:
    from apps.models.User import User  # Class di User.py bernama 'User'
    from apps.models.klaim_kategori import klaim_kategori
except ImportError:
    # Fallback string jika import gagal (Harus persis nama Class-nya)
    User = "User" 
    klaim_kategori = "klaim_kategori"

class klaim(native_db.Model):
    __tablename__ = 'klaim'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_voucher = Column(Integer, nullable=False, index=True)
    
    # Gunakan nama tabel 'klaim_kategori' dan kolom 'id'
    id_kategori_klaim = Column(Integer, ForeignKey('klaim_kategori.id_kategori_klaim'), nullable=False, index=True)
    
    # ForeignKey merujuk ke nama tabel 'users' (lowercase)
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
    
    # --- RELATIONSHIPS ---
    
    # PERBAIKAN: Gunakan "User" (sesuai class User) bukan "Users"
    user_admin = relationship("User", backref="klaim_records", lazy=True)
    
    # Pastikan klaim_kategori sudah benar
    kategori_klaim = relationship("klaim_kategori", backref="klaim_items", lazy=True)

    def __repr__(self):
        return f"<Klaim {self.nomor_klaim}>"