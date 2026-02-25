from apps import native_db
from sqlalchemy import Column, Integer, String, Text, Float, Date, ForeignKey

class voucher_1(native_db.Model):
    __tablename__ = 'voucher_1'
    
    id = Column(Integer, primary_key=True)
    id_principal = Column(Integer, ForeignKey('principal.id'))
    id_tipe_customer = Column(Integer, ForeignKey('tipe_toko_customer.id'))
    nama_voucher = Column(String(100))
    keterangan = Column(Text)
    persentase_diskon_1 = Column(Float)
    nilai_diskon = Column(Integer)
    minimal_total_pembelian = Column(Integer)
    tanggal_mulai = Column(Date)
    tanggal_kadaluarsa = Column(Date)
    budget_diskon = Column(Float)
    current_budget_diskon = Column(Float)
    status_voucher = Column(Integer)
    promo = Column(Text)
    syarat_ketentuan = Column(Text)
    syarat_wajib = Column(Text)
    minimal_subtotal_pembelian = Column(Float)
    persentase_diskon_2 = Column(Float)
    persentase_diskon_3 = Column(Float)
    pic_voucher = Column(String(255))
    kode_voucher = Column(String(80))