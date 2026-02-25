from apps import native_db
from sqlalchemy import Column, Integer, String, Text, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

class voucher_3(native_db.Model):
    __tablename__ = 'voucher_3'

    id = Column(Integer, primary_key=True)
    id_customer = Column(Integer, ForeignKey('customer.id'))
    nama_voucher = Column(String(40))
    keterangan = Column(Text)
    persentase_diskon_1 = Column(Float)
    nilai_diskon = Column(Integer)
    minimal_subtotal_pembelian = Column(Integer)
    tanggal_mulai = Column(Date)
    tanggal_kadaluarsa = Column(Date)
    budget_diskon = Column(Integer)
    current_budget_diskon = Column(Float)
    status_voucher = Column(Integer)
    persentase_diskon_2 = Column(Float)
    persentase_diskon_3 = Column(Float)
    minimal_total_pembelian = Column(Float)
    pic_voucher = Column(String(255))
    kode_voucher = Column(String(80))
    id_produk = Column(Integer, ForeignKey('produk.id'))
    id_principal = Column(Integer, ForeignKey('principal.id'))
    tipe_voucher = Column(Integer)
    syarat_ketentuan = Column(Text)
    syarat_wajib = Column(Text)
    kategori_voucher = Column(Integer)
    nominal_diskon = Column(Float)
    is_reguler = Column(Integer)
    
    voucher_3_produk = relationship('voucher_3_produk', backref=__tablename__, lazy=True)
    voucher_3_cabang = relationship('voucher_3_cabang', backref=__tablename__, lazy=True)