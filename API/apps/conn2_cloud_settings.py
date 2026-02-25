from    flask_sqlalchemy  import  SQLAlchemy
from    flask             import  abort
import  os, sqlalchemy

db = SQLAlchemy()

def set_database_URI():
    try:
        db_user = os.environ["DB_USER"]
        db_pass = os.environ["DB_PASS"]
        db_name = os.environ["DB_NAME"]
        unix_socket_path = os.environ["INSTANCE_UNIX_SOCKET"]

        uri = sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,
            password=db_pass,
            host="localhost",
            database=db_name,
            query={"unix_sock": f"{unix_socket_path}/.s.PGSQL.5432"}
        )

        return str(uri)  # Convert the URL object to a string

    except Exception as e:
        abort(500, description=str(e))

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

        db = SQLAlchemy(app)
        return db

    except Exception as e:
        abort(500, description=str(e))