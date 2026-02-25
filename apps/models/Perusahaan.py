from  .  import  BaseModel
from  apps.conn2  import  db
from  flask       import  Flask, request
from  apps.query  import  DB
from sqlalchemy.orm import relationship


class Perusahaan(BaseModel):
    __tablename__ = "perusahaan"

    nama         = BaseModel.string(50)
    alamat       = BaseModel.string(100)
    telepon      = BaseModel.string(13)
    npwp         = BaseModel.string(25)

    id_wilayah1  = BaseModel.integer()     # int4
    id_wilayah2  = BaseModel.integer()     # int4
    id_wilayah3  = BaseModel.bigInteger()     # int4
    id_wilayah4  = BaseModel.bigInteger()     # int4

    no_prefix    = BaseModel.string(20)
    kode         = db.Column(db.String)
    rekening_perusahaan = relationship("RekeningPerusahaan", back_populates="perusahaan")    # varchar tanpa panjang

    base_query = f"""
        SELECT
          perusahaan.id,
          perusahaan.kode,
          perusahaan.nama,
          perusahaan.alamat,
          perusahaan.telepon,
          perusahaan.npwp,
          perusahaan.id_wilayah1,
          perusahaan.id_wilayah2,
          perusahaan.id_wilayah3,
          perusahaan.id_wilayah4

        FROM perusahaan
        """

    def __repr__(self):
        return f"<Perusahaan id={self.id} nama={self.nama}>"
    
    @classmethod
    def all(cls):
        try:
          result = DB(request).setRawQuery(cls.base_query).execute().fetchall().get()
          return result
        except Exception as e:
          return {"error": str(e)}, 500

      