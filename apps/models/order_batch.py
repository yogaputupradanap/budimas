from apps import native_db
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from  .  import  BaseModel

class OrderBatchModel(BaseModel):
    __tablename__ = 'order_batch'

    id = Column(Integer, primary_key=True)
    id_sales = Column(Integer,  nullable=False)
    id_customer = Column(Integer, ForeignKey('customer.id'), nullable=False)
    tanggal_submit = Column(DateTime, default=func.now())
    status = Column(Integer, nullable=False)

    customer = relationship("Customer", back_populates="order_batches")
    faktur = relationship("faktur", back_populates="order_batch")

