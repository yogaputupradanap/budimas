from  apps.query   import  DB
from  apps.helper  import  *
from  flask        import  request


class Fitur() :
    
    def get_list_tersedia_by_user() : 
        """
        """
        return DB(request).setRawQuery("""
                                   
            SELECT      * 
                                                                    
            FROM        fitur
                                                            
            WHERE       NOT EXISTS (
                                    
                SELECT  id_fitur
                                    
                FROM    users_akses
                                    
                WHERE   id_user                 = 
                        :id
                                    
                AND     fitur        .id        = 
                        users_akses  .id_fitur
                                    
            )
                                                                
            ORDER BY    nama
        
        """).bindparams({
            
            'id' : request.args.get('id')

        }).execute().fetchall().get()

        
    def get_list_tersedia_by_jabatan() :
        """
        """
        return DB(request).setRawQuery("""
                                                       
            SELECT  * 
                                    
            FROM    fitur
                                    
            WHERE NOT EXISTS (
                                    
                SELECT  id_fitur 
                
                FROM    jabatan_akses

                WHERE   id_jabatan                = 
                        :id
                                    
                AND     fitur          .id        = 
                        jabatan_akses  .id_fitur
            )
                                    
            ORDER BY nama
            
        """).bindparams({

            'id' : request.args.get('id')

        }).execute().fetchall().get()
