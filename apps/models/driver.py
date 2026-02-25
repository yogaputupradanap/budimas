from apps import native_db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class driver(native_db.Model):
    __tablename__ = 'driver'
    
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id'))
    id_armada = Column(Integer, ForeignKey('armada.id'))
    id_wilayah1 = Column(Integer, ForeignKey('wilayah1.id'))
    id_wilayah2 = Column(Integer, ForeignKey('wilayah2.id'))
    
    info_pengeluaran_driver = relationship('info_pengeluaran_driver', backref=__tablename__, lazy=True)