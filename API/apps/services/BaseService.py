from . import MultiDict
from apps.handler import *
from apps.conn2 import db
from flask import request
from sqlalchemy import func, cast, Date, or_, desc, asc
from typing import List, Any, Dict, Tuple, Optional


class BaseService():

    def __init__(self):
        self.db = db
        self.data = MultiDict()
        self.set_data()

    @handle_error
    def set_data(self):
        if request.method == 'POST':
            if request.json: self.data.update(request.json)
        if request.form:
            self.data.update(request.form)
        if request.args:
            self.data.update(request.args)
        self.data.update({
            'tokens': request.headers['Authorization'].split(' ')[1] or None
        })

    def set_param(self):
        return {key: int(value) if value.isdigit() else value for key, value in self.data.items()}

    @handle_error
    def apply_filters(self, query, filters):
        """
        Method untuk menerapkan filter ke query

        Parameters:
        query: Query SQLAlchemy
        filters: List dict dengan format:
            [
                {
                    'field': Column yang akan difilter,
                    'param': Nama parameter di request.args,
                    'type': Tipe filter ('exact' atau 'date_range'),
                    'converter': Fungsi konversi (opsional, default str)
                }
            ]
        """
        for filter_config in filters:
            field = filter_config['field']
            param = filter_config['param']
            filter_type = filter_config.get('type', 'exact')
            converter = filter_config.get('converter', str)

            try:
                if filter_type == 'date_range':
                    start_date = request.args.get('start_date')
                    end_date = request.args.get('end_date')
                    if start_date and end_date:
                        query = query.filter(cast(field, Date).between(
                            cast(start_date, Date),
                            cast(end_date, Date)
                        ))
                else:
                    value = request.args.get(param)
                    if value:
                        query = query.filter(field == converter(value))

            except ValueError as e:
                raise Exception(f"Error konversi nilai untuk {param}: {str(e)}")

        return query

    def setup_datatables(self, searchable_columns: List = None, orderable_columns: Dict = None):
        """
        Setup konfigurasi datatables

        Parameters:
        searchable_columns: List kolom yang bisa dicari
        orderable_columns: Dict kolom yang bisa diurutkan dengan mapping ke model
        """
        self.searchable_columns = searchable_columns or []
        self.orderable_columns = orderable_columns or {}
        return self

    def apply_datatables_query(self, base_query: Any) -> Dict:
        """
        Terapkan query datatables (search, order, pagination)

        Parameters:
        base_query: Query dasar SQLAlchemy

        Returns:
        Dict dengan format response datatables
        """

        searchable_columns, orderable_columns = self._get_searchable_and_orderable_columns(base_query)
        self.searchable_columns = searchable_columns
        self.orderable_columns = orderable_columns
        # Ambil parameter datatables
        draw = int(self.data.get('draw', 0))
        start = int(self.data.get('start', 0))
        length = int(self.data.get('length', 10))
        search_value = self.data.get('search[value]', '').strip()
        order_column = self.data.get('order[0][column]')
        order_dir = self.data.get('order[0][dir]', 'asc')

        # Salin query untuk total records
        count_query = base_query
        total_records = self.db.session.query(func.count('*')).select_from(
            base_query.subquery()
        ).scalar()

        # Terapkan pencarian global
        if search_value and self.searchable_columns:
            search_filters = []
            for column in self.searchable_columns:
                search_filters.append(column.ilike(f'%{search_value}%'))
            base_query = base_query.filter(or_(*search_filters))

        # Hitung records setelah filter
        filtered_records = self.db.session.query(func.count('*')).select_from(
            base_query.subquery()
        ).scalar()

        # Terapkan pengurutan
        if order_column and order_column.isdigit():
            column_name = self.data.get(f'columns[{order_column}][data]')
            if column_name in self.orderable_columns:
                column = self.orderable_columns[column_name]
                base_query = base_query.order_by(
                    desc(column) if order_dir == 'desc' else asc(column)
                )
        else:
            # Default sort by id desc
            base_query = base_query.order_by(desc('id'))

        # Terapkan pagination
        base_query = base_query.offset(start).limit(length)

        return {
            'query': base_query,
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records
        }

    def handle_datatables_response(self, query_result: Any, transformer=None) -> Dict:
        """
        Handle response datatables
        """
        data = query_result['query'].all()
        if transformer:
            data = transformer(data)

        return {
            'data': data,
            'draw': query_result['draw'],
            'recordsTotal': query_result['recordsTotal'],
            'recordsFiltered': query_result['recordsFiltered']
        }

    def get_datatables(self, base_query: Any, transformer=None) -> Dict:
        """
        Method utama untuk handle datatables

        Parameters:
        base_query: Query dasar SQLAlchemy
        transformer: Fungsi untuk transform hasil query (optional)

        Returns:
        Dict response datatables
        """
        query_result = self.apply_datatables_query(base_query)
        return self.handle_datatables_response(query_result, transformer)

    def _get_searchable_and_orderable_columns(self, query):
        """Otomatis mendapatkan kolom yang bisa dicari dan diurutkan dari query"""
        searchable_columns = []
        orderable_columns = {}

        # Ambil semua kolom dari query
        for entity in query.column_descriptions:
            column = entity['expr']
            # Hanya kolom string yang bisa dicari
            if hasattr(column.type, 'python_type') and column.type.python_type == str:
                searchable_columns.append(column)

            # Semua kolom bisa diurutkan
            # Gunakan nama label jika ada, jika tidak gunakan nama kolom
            column_name = entity.get('name', column.key)
            orderable_columns[column_name] = column

        return searchable_columns, orderable_columns
