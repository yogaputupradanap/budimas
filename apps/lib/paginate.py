from apps.lib.helper import to_array_string
from apps.handler import nonServerErrorException
from apps.lib.query import DB
import json
import ast

class Paginate():

    def __init__(self, request = None, query = '', bindParams = None):

        self.query = query
        self.tableJoin = ''
        self.columns = None
        self.filterColumns = None
        self.clause = None
        self.groupBy = None
        self.string_clause = ''
        self.string_group_by = ''
        self.request = request
        self.bindParams = bindParams

        self.__setColumns()
        self.__setClause()
        self.__setGroupBy()

    def __validateSelectQuery(self, query):
        disallowed_keywords = ['UPDATE', 'DELETE', 'INSERT', 'DROP', 'ALTER']
        query_upper = query.upper()

        for keyword in disallowed_keywords:
            if keyword in query_upper:
                raise nonServerErrorException(f"Disallowed operation in query: {keyword}")

        return True

    def __boolean(self, value):
        return {'true': True, 'false': False}.get(value, False)

    def __buildQuery(self):
        string_column = ', '.join(self.columns) if self.columns else '*'

        if self.clause:
            clause = [f"{key} {value}" for key, value in self.clause.items()]
            self.string_clause = ' AND '.join(clause)

        if self.groupBy:
            string_group_by = ", ".join(self.groupBy)
            self.string_group_by = f"group by {string_group_by}"

        self.query = f"{string_column} from {self.tableJoin}"

    def __setGroupBy(self):
        group_by = self.request.args.get("group_by") if self.request else None

        if group_by:
            self.__validateSelectQuery(group_by)

            string_array = to_array_string(group_by)
            array_columns = json.loads(string_array)
            self.groupBy = array_columns

        return self

    # colmn value example : ['customer'], ['customer.nama', 'user.id as id_user']
    def __setColumns(self):
        columns = self.request.args.get('columns')

        if columns :
            self.__validateSelectQuery(columns)

            string_array = to_array_string(columns)
            array_columns = json.loads(string_array)
            self.columns = array_columns

            self.filterColumns = [f"{col.split('as')[0]}" for col in array_columns]

        return self

    # clause value example : {'customer': 'sumber sehat', 'user.id': 1}
    def __setClause(self):
        clause = self.request.args.get('clause')

        if clause :
            self.__validateSelectQuery(clause)

            dict_clause = ast.literal_eval(clause)
            self.clause = dict_clause

        return self

    # table value example : 'customer', 'user join customer on user.id = customer.id_user'
    def setTable(self, table):
        join = self.request.args.get('join')
        on = self.request.args.get('on')

        self.__validateSelectQuery(table)

        self.tableJoin = table

        def joinHelper(column: str):
            column_array = column.split(' ')
            column_length = len(column_array)

            if column_length > 1 :
                return column
            else:
                return f"join {column}"

        if join and on:
            queries = f"{join} {on}"

            self.__validateSelectQuery(queries)

            ext_string = to_array_string(join)
            array_exts = json.loads(ext_string)

            clause_string = to_array_string(on)
            array_clause = json.loads(clause_string)

            join_table = [joinHelper(ext) for ext in array_exts]
            with_on = [f'{val} {array_clause[idx]}' for idx, val in enumerate(join_table)]

            mixed_table = ' '.join(with_on)
            self.tableJoin = f"{table} {mixed_table}"

        return self

    def __getRequest(self):
        page = int(self.request.args.get("page", 0)) + 1
        limit = int(self.request.args.get("limit", 5))

        order = self.request.args.get("order", 'asc')
        field = self.request.args.get("field", 'id')

        filters = self.request.args.get('filters', '')
        no_paginate = self.request.args.get('no-paginate', 'false')

        no_paginate_bool = self.__boolean(no_paginate)
        queries = f"{page} {limit} {order} {field} {filters}"

        self.__validateSelectQuery(queries)

        return page, limit, order, field, filters, no_paginate_bool

    def __getClauseFiltersQuery(self, filters):
        check_filtering = filters and self.columns
        filters_query, clause = '', ''

        if check_filtering :
            array_clause = [f"cast({column_name} as text) ILIKE '%{filters}%'" for column_name in self.filterColumns]
            string_clause = " OR ".join(array_clause) if len(array_clause) > 1 else ''.join(array_clause)
            filters_query = f"WHERE ({string_clause})"

        clause = f"where {self.string_clause}" if not len(filters_query) else f"AND {self.string_clause}"
        clause_query = clause if len(self.string_clause) else ''

        return filters_query, clause_query

    def __getQuery(self, filters):
        self.__buildQuery()
        clause_query, filters_query = self.__getClauseFiltersQuery(filters)

        self.query = f"{self.query} {clause_query} {filters_query}"

        return self

    def getAll(self):
        __, __, __, __, filters, __ = self.__getRequest()
        self.__getQuery(filters)
        query = f"select {self.query} {self.string_group_by}"

        return DB().setRawQuery(query).execute().fetchall().get()

    def paginate(self):
        check_build = self.query == ''
        page, limit, order, field, filters, no_paginate = self.__getRequest()

        offset = (page - 1) * limit
        sort = f"{field or 'nama'} {order or ''}"

        clause_query, filters_query = self.__getClauseFiltersQuery(filters)
        if check_build:
            self.__getQuery(filters)

        summarized_query = f"""WITH summarized_data AS 
        ({'select' if check_build else ''}
        {self.query} {clause_query or ''} {self.string_group_by})
        """
        
        indexed_page_query = (
            f"""
                {summarized_query},
                numbered_data AS (
                    select
                    ROW_NUMBER() OVER (ORDER BY {sort}) AS row_num,
                    *
                    FROM summarized_data 
                )
                SELECT *
                FROM numbered_data
                {
                    f"WHERE row_num > {offset} AND row_num <= {page * limit};"
                    if not no_paginate else ''
                }
            """
        )

        size_query = f"""
            {summarized_query}
            select count({field}) as total from summarized_data
        """

        page = DB().setRawQuery(indexed_page_query)
        page_size = DB().setRawQuery(size_query if check_build else self.query)

        page_result = (
            page.bindparams(self.bindParams).execute().fetchall().get()
            if
            not check_build and self.bindParams != None
            else
            page.execute().fetchall().get()
        )
        
        page_size_result = (
            page_size.execute().fetchone().result["total"]
            if
            check_build
            else (
                len(page_size.execute().fetchall().get())
                if 
                self.bindParams == None
                else
                len(
                    page_size
                    .bindparams(self.bindParams)
                    .execute()
                    .fetchall()
                    .get()
                )
            )
        )

        return {"pages": page_result, "total_data": page_size_result}