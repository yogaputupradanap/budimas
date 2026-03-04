from apps import native_db
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from  .  import  BaseModel
class users(BaseModel):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    nama = Column(String(40))
    email = Column(String(100))
    tokens = Column(String(60))
    telepon = Column(String(13))
    no_rekening = Column(String(25))
    npwp = Column(String(25))
    nama_wp = Column(String(50))
    alamat_wp = Column(String(50))
    id_jabatan = Column(Integer)
    id_cabang = Column(Integer)
    username = Column(String(25))
    password = Column(String(200))
    nik = Column(String(25))
    alamat = Column(String(100))
    tanggal_lahir = Column(Date)
    
    driver = relationship('driver', backref='users', lazy=True)