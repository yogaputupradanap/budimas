from  apps.handler import  *
from  apps.helper  import  *
from  apps.widget  import  *
from  sqlalchemy   import  desc
from  .            import  Base
from  apps.models  import  Principal


class PrincipalService(Base) :

    def __init__(self) :
        super().__init__()


    @handle_error
    def fetch_option(self) :
        with self.db.session.begin() :
            return (
                Principal.query.with_entities(
                    Principal  .id,
                    Principal  .nama  .label('text'),
                )
                .all()
            )
    
    
    @handle_error
    def daftar_option(self) :
        return Mapper(self.fetch_option()).to_dict().get()
    

    
    