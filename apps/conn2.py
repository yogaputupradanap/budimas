from flask import abort
import os
# Jangan buat SQLAlchemy() baru di sini! 
# Import dari apps untuk memastikan instance yang sama
from apps import db, native_db 

def set_database_URI():
    username = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASS", "")
    host = os.environ.get("DB_HOST", "127.0.0.1")
    port = os.environ.get("DB_PORT", "5432")
    database = os.environ.get("DB_NAME", "budimas-dev")
    
    # Menggunakan pg8000 atau psycopg2 sesuai driver yang terinstall
    connection_string = f"postgresql+pg8000://{username}:{password}@{host}:{port}/{database}"
    return connection_string
    
def init_connection(app):
    try:
        app.config.update({
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SQLALCHEMY_DATABASE_URI': set_database_URI(),
            'SQLALCHEMY_ENGINE_OPTIONS': {
                'max_overflow': 5,
                'pool_size': 25,
                'pool_timeout': 30,
                'pool_recycle': 1800
            }
        })
        # Inisialisasi app menggunakan instance db tunggal
        db.init_app(app)
    except Exception as e:
        print(f"Error Database Connection: {e}")