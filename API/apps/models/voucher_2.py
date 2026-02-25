from apps import native_db
from sqlalchemy import Column, Integer, String, Text, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
class voucher_2(native_db.Model):
    __tablename__ = 'voucher_2'

    id = Column(Integer, primary_key=True)
    id_principal = Column(Integer, ForeignKey('principal.id'))
    id_produk = Column(Integer, ForeignKey('produk.id'))
    id_tipe_customer = Column(Integer, ForeignKey('tipe_toko_customer.id'))
    nama_voucher = Column(String(50))
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
    syarat_ketentuan = Column(Text)
    syarat_wajib = Column(Text)
    kategori_voucher = Column(Integer)
    nominal_diskon = Column(Float)
    level_uom = Column(Integer)
    minimal_jumlah_produk = Column(Integer)
    is_reguler = Column(Integer)
    
    
    voucher_2_produk = relationship('voucher_2_produk', backref=__tablename__, lazy=True)
    voucher_2_cabang = relationship('voucher_2_cabang', backref=__tablename__, lazy=True)