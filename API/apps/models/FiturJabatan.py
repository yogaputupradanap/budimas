from  apps.query   import  DB
from  apps.helper  import  *
from  flask        import  request


class FiturJabatan() :
    
    def all() : 
        """
        """
        return DB(request).setRawQuery("""

            SELECT      jabatan_akses  .*, 
                        fitur          .nama  AS  nama_fitur
                                    
            FROM        jabatan_akses
                                    
            LEFT JOIN   fitur 
                ON      fitur          .id          = 
                        jabatan_akses  .id_fitur
                                    
            WHERE       jabatan_akses  .id_jabatan  = 
                        :id
            
            ORDER       BY jabatan_akses.id
            
        """).bindparams({

            'id' : request.args.get('id')

        }).execute().fetchall().get()