from apps import native_db
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

class global_table(native_db.Model):
    __tablename__ = 'global_table'
    
    id = Column(Integer, primary_key=True)
    key_column = Column(String(255))
    value_column = Column(String(60))