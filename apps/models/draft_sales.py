from apps import native_db
from sqlalchemy import Integer, String, Column, Date, ForeignKey

class draft_sales(native_db.Model):
    __tablename__ = 'draft_sales'

    id = Column(Integer, primary_key=True)
    no_sales_order = Column(String(50))
    no_faktur = Column(String(50))
    status_order = Column(String(20))
    keterangan = Column(String)
    tanggal_order = Column(Date)
    tanggal_faktur = Column(Date)
    tanggal_terkirim = Column(Date)
    tanggal_jatuh_tempo = Column(Date)
    nama_sales = Column(String(60))
    pic_customer = Column(String(100))
    id_plafon = Column(Integer, ForeignKey('plafon.id'))
    no_order = Column(String(100))