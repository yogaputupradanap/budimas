import json
from functools import wraps
from flask import Flask, jsonify, request, abort
from flask_httpauth import HTTPTokenAuth
from sqlalchemy import or_, desc
from werkzeug.exceptions import HTTPException
from apps.conn import db # Pastikan path koneksi db Anda benar

# Inisialisasi Auth
token_auth = HTTPTokenAuth()

class nonServerErrorException(Exception):
    def __init__(self, code=500, message=''):
        super().__init__(message)
        self.status_code = code

@token_auth.verify_token
def verify_token(token):
    with db.connect() as conn:
        result = conn.execute(
            f"SELECT tokens FROM users WHERE tokens='{token}'"
        ).fetchone()
        
    return True if result else abort(403)

def handle_exception(e):
    """Global Error Handler untuk Flask app"""
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    
    return jsonify(
        result=[{"message": str(e)}],
        status=code
    ), code

def handle_error(func):
    """Decorator untuk membungkus fungsi route agar aman dari crash"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except nonServerErrorException as e:
            return jsonify({"error": str(e)}), e.status_code
        except Exception as e:
            print(f"==== Error caught by handle_error ====\n{str(e)}")
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    return wrapper

def handle_error_rollback(func):
    """Decorator khusus untuk fungsi yang melakukan manipulasi DB (Insert/Update/Delete)"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Cek jika argumen pertama (self) punya session untuk di-rollback
            if args and hasattr(args[0], 'db') and hasattr(args[0].db, 'session'):
                args[0].db.session.rollback()
            
            print(f"==== Rollback Error ====\n{str(e)}")
            return jsonify({"error": "Database Error", "message": str(e)}), 500
    return wrapper

def handle_response_data(data):
    """Format response standard API"""
    if data is None:
        return jsonify({
            "data": None,
            "data_exists": False,
            "status_code": 404,
            "status_message": "Not Found"
        }), 404 # Mengirimkan status code HTTP 404
    
    return jsonify({
        "data": data,
        "data_exists": True,
        "status_code": 200,
        "status_message": "OK"
    }), 200

def handle_response_datatable(data):
    """Logika Server-side Processing untuk DataTables (dari List)"""
    draw = int(request.args.get('draw', 0))
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))
    search_value = request.args.get('search[value]', '')
    
    order_column = int(request.args.get('order[0][column]', 0))
    order_dir = request.args.get('order[0][dir]', 'asc')

    # Filter
    filtered_data = [item for item in data if search_value.lower() in str(item).lower()]

    # Sort
    if filtered_data and isinstance(filtered_data[0], dict):
        column_name = request.args.get(f'columns[{order_column}][data]')
        if column_name:
            filtered_data.sort(
                key=lambda x: str(x.get(column_name, '')).lower(),
                reverse=(order_dir == 'desc')
            )

    # Paginate
    paginated_data = filtered_data[start:start + length]

    return jsonify({
        'data': paginated_data,
        'draw': draw,
        'recordsTotal': len(data),
        'recordsFiltered': len(filtered_data)
    })