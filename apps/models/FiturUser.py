from  apps.query   import  DB
from  apps.helper  import  *
from  flask        import  request


class FiturUser() :
    
    def all() : 
        """
        """
        return DB(request).setRawQuery("""
                                   
            SELECT      users_akses  .*, 
                        fitur        .nama  AS  nama_fitur
                                    
            FROM        users_akses
                                    
            LEFT JOIN   fitur 
                ON      fitur        .id        = 
                        users_akses  .id_fitur
                                    
        """).execute().fetchall().get()
    
    
    def get_list_by_distinct_user() : 
        """
        """
        return DB(request).setRawQuery("""
                                   
            SELECT      DISTINCT (id_user)  AS  id, 
                        users    .nama, 
                        users    .nik, 
                        jabatan  .nama      AS  nama_jabatan
                                    
            FROM        users_akses 
                                    
            JOIN        users 
                ON      users        .id          = 
                        users_akses  .id_user
                                    
            JOIN        jabatan 
                ON      jabatan      .id          = 
                        users        .id_jabatan
                                    
        """).execute().fetchall().get()