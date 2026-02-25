from    apps.conn    import  db
from    apps.helper  import  *
from    flask        import  Flask, abort
from    sqlalchemy   import  bindparam, text
import  json


app = Flask(__name__)

class DB():
    '''
        Custom Class Helper for Query Building.
        @param `request` Set the "request" if using 
                         Additional Query Clause 
                         Modifier.
    '''

    def __init__(self, request=None) :
        '''
            Setting Initial Variables and Form Data.
        '''
        self.table     = None  # Table Name.
        self.result    = None  # Object Result of Database Request Execution.
        self.response  = None  # Formatted Object Response of Returned Result.
        self.query     = ""    # Query Container.
        
        if (request) : # if Any `Form Data Request` Sent.
            self.setData(request)       # Set Data 
            self.setAdditionalClause()  # Set Additional Query Clause.


    def setData(self, request) :
        '''
            Assigning Form Data.
        '''
        self.data      = request.form                   # Data (From Form Request).
        self.where     = request.args.get('where')      # `Where` Data (From Query Param).
        self.whereOr   = request.args.get('whereOr')    # `WhereOr` Data (From Query Param).
        self.orderBy   = request.args.get('orderBy')    # `OrderBy` Data (From Query Param).
        self.limit     = request.args.get('limit')      # `Limit` Data (From Query Param).
        self.returning = request.args.get('returning')  # `Returning` Data (From Query Param).
    

    def setAdditionalClause(self) :
        '''
            Building Query Additional Clauses.
            @methods `Where`, `WhereOr`, `OrderBy`, `Limit`, `Returning`.
        '''

        # Formatting `WhereOr` Data with `OR` Conjunction 
        # and Adding it to Query.
        if  self.whereOr :
            self.whereOr = json.loads(self.whereOr)
            if self.query != "" : 
                self.query += " OR "
            for key, value in self.whereOr.items() :
                self.query += key + value
                if key != list(self.whereOr)[-1] : 
                    self.query += " OR "

        # Formatting `Where` Data with `AND` Conjunction 
        # and Adding it to Query.
        if  self.where :
            self.where = json.loads(self.where)
            if self.query != "" : 
                self.query += " AND "
            for key, value in self.where.items() :
                self.query += key + value
                if key != list(self.where)[-1] : 
                    self.query += " AND "

        # Adding `Where` Clause to Query.
        if  self.where or self.whereOr : 
            self.query = f" WHERE {self.query}"

        # Adding `Order By` Clause to Query.
        if  self.orderBy : 
            self.orderBy = json.loads(self.orderBy)
            self.query += f" ORDER BY {self.orderBy['fields']}"

        # Add `Limit` Clause to Query.
        if  self.limit :
            self.limit = json.loads(self.limit)
            self.query += f" LIMIT {self.limit['numbers']}"

        # Adding `Returning` Clause to Query (INSERT ONLY !!!).
        if  self.returning : 
            self.returning = json.loads(self.returning)
            self.query += f" RETURNING {self.returning['fields']}"

    
    def setTable(self, name) :
        '''
            Setting Table Name.
            @param `name` Name of Table want to be Modify.
            @return `self`
        '''
        self.table = name
        return self
    
    
    def select(self) :
        '''
            Building Query with 'Select' Format.
            @return `self`
        '''
        self.query  = f"SELECT * FROM {self.table} {self.query}"
        return self


    def insert(self) :
        '''
            Building Query with 'Insert' Format.
            @return `self`
        '''

        # Formating `Fields` and `Values` Data for Insert.
        fields = ""
        values = ""

        for key, value in self.data.items(): 
            fields += f"{key}, " if key != list(self.data)[-1] else key
            value = 'NULL' if value == "" or value == None else f"'{value}'" 
            values += f"{value}, " if key != list(self.data)[-1] else value
        
        fields = f"({fields})"
        values = f"({values})"

        # Building Insert Query and Success Message.
        self.query    = f"INSERT INTO {self.table} {fields} VALUES {values} {self.query}"
        self.response = {"messege" : "Data Successfully Added"}

        return self
    

    def update(self) :
        '''
            Building Query with 'Update' Format.
            @return `self`
        '''

        # Formating `Set` Data for Update.
        sets  = ""

        for key, value in self.data.items(): 
            value = 'NULL' if value == "" or value == None else f"'{value}'"
            sets += f"{key} = {value}, " if key != list(self.data)[-1] else f"{key} = {value}"

        sets   = f" SET {sets}"
        
        # Building Update Query and Success Message.
        self.query    = f"UPDATE {self.table} {sets} {self.query}"
        self.response = {"messege" : "Data Successfully Updated"}

        return self
    

    def delete(self) :
        '''
            Building Query with 'Delete' Format.
            @return `self`
        '''
        self.query    = f"DELETE FROM {self.table} {self.query}"
        self.response = {"messege" : "Data Successfully Deleted"}

        return self
    
    
    def setRawQuery(self, query) :
        '''
            Building Query with Raw String.
            @return `self`
        '''
        self.query   = f"{query} {self.query}"
        return self

    
    def bindparams(self, param) :
        '''
            Setting Parameters Binding for
            Query.
            @use SQLAlchmy `text`, `bindparams`.
            @return `self`
        '''
        bindings = []
        for key, value in param.items():
            if(isinstance(value, (list, tuple))):
                bindings.append(bindparam(key, value, expanding=True))
            else:
                bindings.append(bindparam(key, value))

        self.query = text(self.query).bindparams(*bindings)
        return self
        

    def execute(self) :
        '''
            Executing Query.
            @use Flask DB Connection.
            @use module `conn`.
            @return `self`
        '''
        try :
            with db.connect() as conn:
                self.result = conn.execute(self.query)
            return self
        
        except Exception as e :
            return abort(500, description=str(e))
            

    def fetchall(self) :
        '''
            Fetching All Data.\n
            Set Result to (N) Object Response.
            @use `SQLAlchemy` `fetchall`.
            @return `self` 
        '''
        if self.result : 
            self.result = self.result.fetchall()

            if len(list(self.result)) == 0 : 
                self.result = None

        return self


    def fetchone(self) :
        '''
            Fetching one Data.\n
            Set Result to (1) Object Response.
            @use `SQLAlchemy` `fetchone`.
            @return `self` 
        '''
        if self.result : 
            self.result = self.result.fetchone()
            
            if len(list(self.result)) == 0 : 
                self.result = None

        return self


    def get(self, fields=None) : 
        '''
            Get Respon Result.
            Response can be an Object of Message or Data.
            @return `response` Formatted Object Response of Returned Result.
        '''
        try :
            if not fields :
                # Response untuk Select.
                if not self.response :
                    return set(self.result)
                
                # Response untuk Insert, Update, Delete.
                elif self.result and self.response :
                    # Response untuk Insert Retruning.
                    if self.returning :
                        self.fetchall()
                        return set(self.result)
                    else :
                        return set(self.response)
                    
        except Exception as e :
            return abort(500, description=str(e))