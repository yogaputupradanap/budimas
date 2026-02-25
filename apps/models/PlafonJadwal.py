from  apps.query   import  DB
from  apps.helper  import  *
from  flask        import  request
from apps.models.BaseModel import BaseModel

class PlafonJadwal(BaseModel) :
    __tablename__ = 'plafon_jadwal'

    id_plafon    = BaseModel.foreign('plafon.id')
    id_tipe_kunjungan = BaseModel.integer()
    id_hari     = BaseModel.integer()
    id_minggu   = BaseModel.integer()
    id_status  = BaseModel.smallInteger()
    
    def all() :
        """
        """
        return DB(request).setRawQuery("""
                                   
            SELECT      plafon_jadwal  .*,
                        plafon         .kode  AS  kode,
                        users          .nama  AS  nama_user,
                        customer       .nama  AS  nama_customer,
                        principal      .nama  AS  nama_principal
                                    
            FROM        plafon_jadwal
                                    
            LEFT JOIN   plafon 
                ON      plafon         .id            = 
                        plafon_jadwal  .id_plafon
                                    
            LEFT JOIN   customer 
                ON      customer       .id            = 
                        plafon         .id_customer
                                    
            LEFT JOIN   principal 
                ON      principal      .id            = 
                        plafon         .id_principal
                                    
            LEFT JOIN   users 
                ON      users          .id
                        plafon         .id_user       = 
                                    
        """).execute().fetchall().get()
    
    def set(self, data=None):
        if (data) :
                self.id                  = data.get('plafon_jadwal_id')
                self.id_plafon           = data.get('id_plafon')
                self.id_tipe_kunjungan   = data.get('id_tipe_kunjungan')
                self.id_hari             = data.get('id_hari')
                self.id_minggu           = data.get('id_minggu')
                self.id_status          = data.get('id_status')
        return  self