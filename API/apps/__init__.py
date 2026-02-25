from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
native_db = db

# ⬇️ PINDAHKAN KE SINI (MODULE LEVEL)
from apps.models import *

def create_app():
    app = Flask(__name__)

    CORS(app, supports_credentials=True)

    from apps.conn2 import init_connection
    init_connection(app)

    # ⬇️ DEBUG RELATIONSHIP
    with app.app_context():
        for mapper in db.Model.registry.mappers:
            for rel in mapper.relationships:
                if rel.key == "perusahaan":
                    print("🚨 RELASI SALAH ADA DI:", mapper.class_)
                    print("➡️ TARGET:", rel.entity)

    # Register blueprint
    from apps.routes.auth import auth
    from apps.routes.base import base as base_blueprint
    from apps.routes.extra import extra as extra_blueprint

    app.register_blueprint(auth)
    app.register_blueprint(base_blueprint)
    app.register_blueprint(extra_blueprint)

    return app
