from apps import native_db
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

class status(native_db.Model):
    __tablename__ = 'status'
    
    id = Column(Integer, primary_key=True)
    code = Column(Integer)
    status = Column(String(20))
    
    armada = relationship('armada', backref='status', lazy=True)
    