
from apps import native_db
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from  .  import  BaseModel

class MutasiBank(BaseModel):
    __tablename__ = "mutasi_bank"

    id = Column("id_mutasi", Integer, primary_key=True)
    id_rekening_perusahaan = Column(Integer, ForeignKey("rekening_perusahaan.id_rekening_perusahaan"))
    tanggal_mutasi = Column(Date)
    nominal_mutasi = Column(Float)
    tipe = Column(Integer)
    id_customer = Column(Integer)
    id_setoran = Column(Integer)
    keterangan = Column(String)
    tanggal_upload = Column(DateTime)
    cabang_mutasi = Column(Integer)
    saldo_akhir = Column(Float)
    id_sales = Column(Integer)
    id_user = Column(Integer)
    kode_mutasi = Column(String)
    sisa = Column(Float)
    status_mutasi = Column(Integer, default=1)

    rekening = relationship("RekeningPerusahaan", back_populates="mutasi_bank")
    
    @property
    def id_mutasi(self):
        return self.id

    @id_mutasi.setter
    def id_mutasi(self, value):
        self.id = value