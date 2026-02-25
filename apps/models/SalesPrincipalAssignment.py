from  apps.query   import  DB
from  apps.helper  import  *
from  flask        import  request
from  apps.models.BaseModel import BaseModel

class SalesPrincipalAssignment(BaseModel) :
    __tablename__ = 'sales_principal_assignment'

    id_sales          = BaseModel.foreign('sales.id')
    id_principal     = BaseModel.foreign('principal.id')

    def all() :
        """
        """
        return DB(request).setRawQuery("""
                                   
            SELECT      sales_principal_assignment  .*,
                        users                       .nama  AS  nama_sales,
                        principal                   .nama  AS  nama_principal
                                    
            FROM        sales_principal_assignment
                                    
            LEFT JOIN   users 
                ON      users          .id            = 
                        sales_principal_assignment  .id_sales
                                    
            LEFT JOIN   principal 
                ON      principal      .id            = 
                        sales_principal_assignment  .id_principal
                                    
        """).execute().fetchall().get()
    
    def __repr__(self):
      return f"data('{self.id}')"

    def set(self, data=None):
        if (data) :
                self.id                  = data.get('sales_principal_assignment_id')
                self.id_sales           = data.get('id_sales')
                self.id_principal       = data.get('id_principal')
                self.status_aktif       = data.get('status_aktif')
        return  self