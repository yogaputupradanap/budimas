from apps import native_db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, SMALLINT

class ProdukUom(native_db.Model):
    __tablename__ = 'produk_uom'

    id = Column(Integer, primary_key=True)
    kode = Column(String)
    nama = Column(String)
    level = Column(Integer)
    packing_satuan = Column(String)
    packing_tinggi = Column(Float)
    packing_panjang = Column(Float)
    packing_lebar = Column(Float)
    berat_satuan = Column(String)
    berat_bersih = Column(Float)
    berat_kotor = Column(Float)
    set_default_sales = Column(Integer)
    set_default_storage = Column(Integer)
    id_produk = Column(Integer)
    faktor_konversi = Column(Float)