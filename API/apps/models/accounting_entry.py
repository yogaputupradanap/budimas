from apps import native_db
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from . import BaseModel

class AccountingEntryModel(BaseModel):
    __tablename__ = "accounting_entry"

    # SOLUSI: Map atribut 'id' (dari BaseModel) ke kolom fisik 'id_mutasi_acc'
    id = Column("id_mutasi_acc", Integer, primary_key=True, autoincrement=True)
    
    # Buat properti agar pemanggilan .id_mutasi_acc tetap berfungsi
    @property
    def id_mutasi_acc(self):
        return self.id

    @id_mutasi_acc.setter
    def id_mutasi_acc(self, value):
        self.id = value

    id_rekening_perusahaan = Column(Integer, ForeignKey("rekening_perusahaan.id_rekening_perusahaan"), nullable=False)
    tanggal_transaksi = Column(Date, nullable=False)
    nominal = Column(Float, nullable=False)
    tipe = Column(Integer, nullable=False)
    kode_transaksi = Column(String, nullable=False)
    keterangan = Column(Text)
    id_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)

    # Tegaskan primary key untuk mapper
    __mapper_args__ = {
        'primary_key': [id]
    }

    rekening = relationship("RekeningPerusahaan", back_populates="accounting_entries") 