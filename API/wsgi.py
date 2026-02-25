# wsgi.py
from app import app # Asumsikan objek Flask Anda bernama 'app' di 'app.py'
from waitress import serve

if __name__ == "__main__":
    # Waitress akan berjalan di port internal yang hanya didengar oleh Nginx
    print("Starting Waitress server on port 8000...")
    serve(app, host='127.0.0.1', port=8001)