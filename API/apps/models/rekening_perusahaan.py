from apps import native_db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from . import BaseModel

class RekeningPerusahaan(BaseModel):
    __tablename__ = "rekening_perusahaan"

    # SOLUSI UTAMA: Map atribut 'id' (warisan BaseModel) ke kolom fisik 'id_rekening_perusahaan'
    # Ini akan menghentikan error "column rekening_perusahaan.id does not exist"
    id = Column("id_rekening_perusahaan", Integer, primary_key=True, autoincrement=True)
    
    # Buat alias agar kode lama yang memanggil 'id_rekening_perusahaan' tidak rusak
    @property
    def id_rekening_perusahaan(self):
        return self.id

    @id_rekening_perusahaan.setter
    def id_rekening_perusahaan(self, value):
        self.id = value

    nama_bank = Column(String)
    nomor_rekening = Column(String)
    nama_pemilik = Column(String)
    is_aktif = Column(Boolean, default=True)
    id_cabang = Column(Integer)
    id_perusahaan = Column(Integer, ForeignKey("perusahaan.id"))

    # Menegaskan kembali primary key untuk mapper
    __mapper_args__ = {
        'primary_key': [id]
    }

    # Relationships
    mutasi_bank = relationship("MutasiBank", back_populates="rekening")
    accounting_entries = relationship("AccountingEntryModel", back_populates="rekening")
    perusahaan = relationship("Perusahaan", back_populates="rekening_perusahaan")