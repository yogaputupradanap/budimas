# apps/lib/encryption.py
import json
import os
from functools import wraps
from flask import jsonify
import base64


def get_encryption_enabled():
    # jika lokal ubah ke 'development'
    env = 'production'
    return env == 'production'


def simple_encrypt(text, key):
    """Enkripsi sederhana menggunakan XOR - hanya untuk demo"""
    key_bytes = key.encode('utf-8')
    text_bytes = text.encode('utf-8')
    encrypted = bytearray()

    for i in range(len(text_bytes)):
        encrypted.append(text_bytes[i] ^ key_bytes[i % len(key_bytes)])

    return base64.b64encode(encrypted).decode('utf-8')


def encrypt_response(func):
    """Decorator untuk mengenkripsi response"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Panggil fungsi asli
        response = func(*args, **kwargs)

        # Jika bukan di production, return response asli
        if not get_encryption_enabled():
            return response

        try:
            # Ambil data dari response (bisa berupa tuple atau dict)
            if isinstance(response, tuple):
                data = response[0]
                status_code = response[1] if len(response) > 1 else 200
                headers = response[2] if len(response) > 2 else {}
            else:
                data = response
                status_code = 200
                headers = {}

            # Convert data ke JSON
            json_data = json.dumps(data)

            # Enkripsi sederhana
            key = os.environ.get('API_ENCRYPTION_KEY', '02f8e272aa13d26f48b992c43a2d333b')
            encrypted_data = simple_encrypt(json_data, key)

            # Format response
            encrypted_response = {
                "encrypted": True,
                "data": encrypted_data
            }

            # Return dengan format yang sama
            if isinstance(response, tuple):
                if len(response) > 2:
                    return jsonify(encrypted_response), status_code, headers
                elif len(response) > 1:
                    return jsonify(encrypted_response), status_code

            return jsonify(encrypted_response)

        except Exception as e:
            print(f"Encryption error: {str(e)}")
            # Fallback ke data asli
            return response

    return wrapper