from . import BaseModel

class SalesTipe(BaseModel):
  __tablename__ = 'sales_tipe'

  nama = BaseModel.string(25)

  def __repr__(self):
      return f"data('{self.id}')"