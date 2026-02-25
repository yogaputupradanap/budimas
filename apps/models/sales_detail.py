
from apps import native_db
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from  .  import  BaseModel

class SalesDetail(BaseModel):
    __tablename__ = "sales_detail"

    id = Column(Integer, primary_key=True)
    id_sales = Column(Integer, ForeignKey("sales.id_sales"))
    kode_sales = Column(String)