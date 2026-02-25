from apps import native_db
from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship

class kasbon_klaim_detail(native_db.Model):
    __tablename__ = 'kasbon_klaim_detail'
    
    id_kasbon_klaim_detail = Column(Integer, primary_key=True, autoincrement=True)
    id_kasbon_klaim = Column(Integer, ForeignKey('kasbon_klaim.id_kasbon_klaim'), nullable=False, index=True)
    id_klaim = Column(Integer, ForeignKey('klaim.id'), index=True)
    nominal_dijamin = Column(Numeric(20), nullable=True, default=0)
    
    kasbon_klaim_header = relationship("kasbon_klaim", back_populates="details")
    klaim_info = relationship("klaim")

