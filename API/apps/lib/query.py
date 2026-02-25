from apps import native_db
from .helper import *
from flask import abort, current_app
from sqlalchemy import bindparam, text
import json
class DB:
    """
    Custom Class Helper for Query Building.
    @param `request` Set the "request" if using
    Additional Query Clause
    Modifier.
    """

    def __init__(self, request=None):
        """
        Setting Initial Variables and Form Data.
        """
        self.db = native_db.session 
        self.table = None  # Table Name.
        self.result = None  # Object Result of Database Request Execution.
        self.response = None  # Formatted Object Response of Returned Result.
        self.query = ""  # Query Container.
        self.dbSession = None
        self.dbTransaction = None


        if request:  # if Any `Form Data Request` Sent.
            self.setData(request)  # Set Data
            self.setAdditionalClause()  # Set Additional Query Clause.

    def setData(self, request):

        json_data = request.get_json(silent=True)

        if json_data:
            self.data = json_data
        else:
            self.data = request.form.to_dict()

        # 🔥 INI YANG PENTING
        self.where = request.args.to_dict()

        self.orderBy = request.args.get("orderBy")
        self.limit = request.args.get("limit")
        self.returning = request.args.get("returning")

        return self

    def setAdditionalClause(self):

        if self.where:
            parts = []

            for key, value in self.where.items():
                if str(value).isdigit():
                    parts.append(f"{key} = {value}")
                else:
                    parts.append(f"{key} = '{value}'")

            self.query += " WHERE " + " AND ".join(parts)

        if self.orderBy:
            self.query += f" ORDER BY {self.orderBy}"

        if self.limit:
            self.query += f" LIMIT {self.limit}"

        return self

    def setTable(self, name):
        """
        Setting Table Name.
        @param `name` Name of Table want to be Modify.
        @return `self`
        """
        self.table = name
        return self

    def select(self):
        """
        Building Query with 'Select' Format.
        @return `self`
        """
        self.query = f"SELECT * FROM {self.table} {self.query}"
        return self

    def insert(self):
        """
        Building Query with 'Insert' Format.
        @return `self`
        """

        # Formating `Fields` and `Values` Data for Insert.
        fields = ""
        values = ""

        for key, value in self.data.items():
            fields += f"{key}, " if key != list(self.data)[-1] else key
            value = "NULL" if value == "" or value == None else f"'{value}'"
            values += f"{value}, " if key != list(self.data)[-1] else value

        fields = f"({fields})"
        values = f"({values})"

        # Building Insert Query and Success Message.
        self.query = f"INSERT INTO {self.table} {fields} VALUES {values} {self.query}"
        self.response = {"messege": "Data Successfully Added"}

        return self

    def update(self):
        """
        Building Query with 'Update' Format.
        @return `self`
        """

        set_parts = []

        for key, value in self.data.items():
            if value is None or value == "":
                set_parts.append(f"{key} = NULL")
            elif isinstance(value, bool):
                set_parts.append(f"{key} = {'TRUE' if value else 'FALSE'}")
            else:
                set_parts.append(f"{key} = '{value}'")

        set_clause = "SET " + ", ".join(set_parts)
            

        # 🔥 RESET QUERY (PENTING)
        self.query = f"UPDATE {self.table} {set_clause}"

        self.response = {"messege": "Data Successfully Updated"}

        return self

    def delete(self):
        """
        Building Query with 'Delete' Format.
        @return `self`
        """
        self.query = f"DELETE FROM {self.table} {self.query}"
        self.response = {"messege": "Data Successfully Deleted"}

        return self

    def setRawQuery(self, query):
        """
        Building Query with Raw String.
        @return `self`
        """
        self.query = f"{query} {self.query}"
        return self

    def bindparams(self, param):
        """
        Setting Parameters Binding for
        Query.
        @use SQLAlchmy `text`, `bindparams`.
        @return `self`
        """
        self.query = text(self.query).bindparams(
            *[bindparam(key, value) for key, value in param.items()]
        )

        return self

    def bindparams_v2(self, params, expanding_keys=None):
        """
           Bind parameters to a SQLAlchemy text query with optional support for expanding parameters.

           This method allows binding normal parameters as well as expanding parameters
           (useful for SQL `IN` clauses). If a key is listed in `expanding_keys`,
           its value will be bound with `expanding=True`.

           Args:
               params (dict):
                   Dictionary of parameters to bind into the query.
                   Example: {"id": 123, "ids": [1, 2, 3]}.
               expanding_keys (list, optional):
                   List of keys from `params` that should use `expanding=True`.
                   This is typically used for binding lists to an `IN` clause.
                   Defaults to an empty list.

           Returns:
               self: The current instance with the query updated to include bound parameters.

           Example:
               >>> params = {"id": 1, "ids": [1, 2, 3]}
               >>> query = "SELECT * FROM users WHERE id = :id OR id IN :ids"
               >>> obj.query = query
               >>> obj.bindparams_v2(params, expanding_keys=["ids"])
               <obj with bound query>

           Notes:
               - Requires `sqlalchemy.text` and `sqlalchemy.bindparam`.
               - Expanding parameters are only supported in SQLAlchemy >= 1.2.
           """
        expanding_keys = expanding_keys or []
        bp_list = []

        for key, value in params.items():
            if key in expanding_keys:
                bp_list.append(bindparam(key, value, expanding=True))
            else:
                bp_list.append(bindparam(key, value))

        self.query = text(self.query).bindparams(*bp_list)
        return self

    def execute(self, data_insert=None):
        """
        Executing Query.
        @use Flask DB Connection.
        @use module `conn`.
        @return `self`
        """ 
        try:
            self.result = (
                self.db.execute(self.query)
                if not data_insert
                else self.db.execute(self.query, data_insert)
            )
            
            return self

        except Exception as e:
            raise e
        
    def setRawQueryDt(self, query): 
        self.query = query
        return self

    def fetchall(self):
        """
        Fetching All Data.\n
        Set Result to (N) Object Response.
        @use `SQLAlchemy` `fetchall`.
        @return `self`
        """
        if self.result:
            self.result = self.result.fetchall()

            if len(list(self.result)) == 0:
                self.result = None

        return self

    def fetchone(self):
        """
        Fetching one Data.\n
        Set Result to (1) Object Response.
        @use `SQLAlchemy` `fetchone`.
        @return `self`
        """
        # print(f"self result fetchone : {self.result}")
        if self.result:
            try:
                fetched_result = self.result.fetchone()
                if fetched_result:
                    self.result = dict(fetched_result)
                else:
                    self.result = {}
            except Exception as e:
                print('some weird python error:', e)
        else:
            self.result = {}
            
        return self

    def get(self, fields=None):
        try:
            serialized_result = self._serialize(self.result)

            if not self.response:
                return {
                    "result": serialized_result,
                    "status": "success"
                }

            if self.response:
                if self.returning:
                    return {
                        "result": serialized_result,
                        "status": "success"
                    }
                else:
                    return {
                        "result": self.response,
                        "status": "success"
                    }

            return {
                "result": [],
                "status": "empty"
            }

        except Exception as e:
            return {
                "result": [],
                "message": str(e),
                "status": "error"
            }, 500


    def ends_with_brackets(value):
        """
        Check if the given value ends with '[' and ']'.

        Args:
        value (str): The string to check.

        Returns:
        bool: True if the value ends with '[' and ']', False otherwise.
        """
        return value.startswith('[') and value.endswith(']')

    def to_array_string(value):
        is_array_string = ends_with_brackets(str(value))
        new_value = value if is_array_string else f"[{value}]"

        return new_value

    def _serialize(self, data):
        """
        Convert SQLAlchemy Row / list[Row] into JSON-serializable objects
        """
        if data is None:
            return []

        # List of rows
        if isinstance(data, list):
            return [dict(row._mapping) for row in data]

        # Single row
        if hasattr(data, "_mapping"):
            return dict(data._mapping)

        # Already serializable
        return data
