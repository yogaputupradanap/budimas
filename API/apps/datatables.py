from flask import request
from sqlalchemy import text
from typing import List, Dict, Any


class DictMapper:
    def __init__(self, data):
        self.data = data

    def to_dict(self):
        return self

    def add_col(self, func, col_name):
        for item in self.data:
            item[col_name] = func(item)
        return self

    def get(self):
        return self.data


class DataTables:
    def __init__(self, db):
        self.db = db

    def execute_raw_query(self, query: str, params: Dict = None) -> List[Dict]:
        """
        Eksekusi raw SQL query dan return hasilnya sebagai list of dict
        """
        result = self.db.session.execute(text(query), params or {})
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result]

    def handle(self, base_query: str, transformer=None) -> Dict:
        """
        Handle datatables dengan raw SQL query

        Parameters:
        base_query: Query SQL dasar
        transformer: Fungsi untuk transform hasil query (optional)
        """
        # Ambil parameter datatables
        draw = int(request.args.get('draw', 0))
        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        search_value = request.args.get('search[value]', '').strip()
        order_column = request.args.get('order[0][column]')
        order_dir = request.args.get('order[0][dir]', 'asc')

        params = {}

        # Query untuk total records
        count_query = f"SELECT COUNT(*) as count FROM ({base_query}) as base_query"
        total_records = self.db.session.execute(text(count_query), params).scalar()

        # Tambahkan pencarian jika ada
        search_query = base_query
        if search_value:
            # Ambil semua kolom dari query dasar
            columns_query = f"SELECT * FROM ({base_query}) as cols LIMIT 1"
            sample_row = self.db.session.execute(text(columns_query)).keys()

            search_conditions = []
            for column in sample_row:
                search_conditions.append(f"CAST({column} as TEXT) ILIKE :search")

            search_query = f"""
                SELECT * FROM ({base_query}) as base_query 
                WHERE {' OR '.join(search_conditions)}
            """
            params['search'] = f"%{search_value}%"

        # Query untuk filtered records
        filtered_count_query = f"SELECT COUNT(*) as count FROM ({search_query}) as search_query"
        filtered_records = self.db.session.execute(text(filtered_count_query), params).scalar()

        # Tambahkan ordering
        if order_column and order_column.isdigit():
            column_name = request.args.get(f'columns[{order_column}][data]')
            if column_name:
                search_query = f"""
                    SELECT * FROM ({search_query}) as ordered_query 
                    ORDER BY {column_name} {order_dir}
                """

        # Tambahkan pagination
        final_query = f"""
            SELECT * FROM ({search_query}) as paginated_query 
            LIMIT {length} OFFSET {start}
        """

        # Eksekusi query final
        data = self.execute_raw_query(final_query, params)

        # Transform data jika ada transformer
        if transformer:
            data = transformer(data)

        return {
            'data': data,
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records
        }