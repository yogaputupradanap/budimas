from apps import native_db
from sqlalchemy import Integer, Column, ForeignKey, Text, Date, Time,BigInteger, Float

class stock_opname(native_db.Model):
    __tablename__ = 'stock_opname'

    id_stock_opname = Column(Integer, primary_key=True)
    id_cabang = Column(Integer, ForeignKey('cabang.id'))
    id_principal = Column(Integer, ForeignKey('principal.id'))
    kode_so = Column(Text)
    total = Column(Float)
    ket_so = Column(Text)
    tanggal_so = Column(Date)
    status_so = Column(Text)
    waktu_verifikasi = Column(Time)
    id_user_input = Column(Integer, ForeignKey('users.id'))
    id_verifikator = Column(Integer, ForeignKey('users.id'))
    total_selisih = Column(Float)