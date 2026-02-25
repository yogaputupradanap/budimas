import  sqlalchemy
import os

# |---------------------------------------------------------------------------------
# | CONNECTION CONFIGURATIONS
# |---------------------------------------------------------------------------------
# |
def init_connection_engine():
    db_config = {
    # |-----------------------------------------------------------------------------
    # | [START cloud_sql_mysql_sqlalchemy_limit]
    # |-----------------------------------------
    # | Pool size is the maximum number of permanent connections to keep.
    # |
        "pool_size": 2,
    # |   
    # | Temporarily exceeds the set pool_size if no connections are available.
    # |-----------------------------------------------------------------------------       
        "max_overflow": 1,
    # |
    # | The total number of concurrent connections for your application will be
    # | a total of pool_size and max_overflow.
    # |---------------------------------------
    # | [END cloud_sql_mysql_sqlalchemy_limit]
    # |-----------------------------------------------------------------------------

    # |-----------------------------------------------------------------------------
    # | [START cloud_sql_mysql_sqlalchemy_backoff]
    # |-------------------------------------------
    # | SQLAlchemy automatically uses delays between failed connection attempts,
    # | but provides no arguments for configuration.
    #
    # |
    # |-----------------------------------------
    # | [END cloud_sql_mysql_sqlalchemy_backoff]
    # |-----------------------------------------------------------------------------

    # |-----------------------------------------------------------------------------
    # | [START cloud_sql_mysql_sqlalchemy_timeout]
    # |-------------------------------------------
    # | `pool_timeout` is the maximum number of seconds to wait when retrieving a
    # | new connection from the pool. After the specified amount of time, an
    # | exception will be thrown.
    # |-----------------------------------------------------------------------------
        "pool_timeout": 30,  # 30 seconds
    # |
    # |-----------------------------------------
    # | [END cloud_sql_mysql_sqlalchemy_timeout]
    # |-----------------------------------------------------------------------------

    # |-----------------------------------------------------------------------------
    # | [START cloud_sql_mysql_sqlalchemy_lifetime]
    # |--------------------------------------------
    # | 'pool_recycle' is the maximum number of seconds a connection can persist.
    # | Connections that live longer than the specified amount of time will be
    # | reestablished.
    # |-----------------------------------------------------------------------------
        "pool_recycle": 45,  # 30 minutes
    # |
    # |-----------------------------------------
    # | [END cloud_sql_mysql_sqlalchemy_timeout]
    # |-----------------------------------------------------------------------------
    }

    # |-----------------------------------------------------------------------------
    # | Settings SSH Connection Certifications.
    # |-----------------------------------------------------------------------------
    # if os.environ.get("DB_HOST"):
    #     if os.environ.get("DB_ROOT_CERT"):
    #         return init_tcp_sslcerts_connection_engine(db_config)

    # return init_unix_connection_engine(db_config)
    return init_tcp_connection_engine(db_config)

def init_tcp_connection_engine(db_config):
    # |-----------------------------------------------------------------------------
    # | [START cloud_sql_mysql_sqlalchemy_create_tcp]
    # |-----------------------------------------------------------------------------

    # |-----------------------------------------------------------------------------
    # | Remember - storing secrets in plaintext is potentially unsafe. 
    # | Consider using something like 
    # | https://cloud.google.com/secret-manager/docs/overview 
    # | to help keep secrets secret.
    # |-----------------------------------------------------------------------------
    # db_user = os.environ["root"]
    # db_pass = os.environ["123456789"]
    # db_name = os.environ["larissa"]
    # db_host = os.environ["127.0.0.1"]
    # |
    # |-----------------------------------------------------------------------------

    # |-----------------------------------------------------------------------------
    # | Extract port from db_host if present,
    # | otherwise use DB_PORT environment variable.
    # |-----------------------------------------------------------------------------
    # host_args = db_host.split(":")
    # if len(host_args) == 1:
    #     db_hostname = db_host
    #     db_port     = os.environ["3306"]
    # elif len(host_args) == 2:
    #     db_hostname, db_port = host_args[0], int(host_args[1])
    # |
    # |-----------------------------------------------------------------------------
    
    # |-----------------------------------------------------------------------------
    # | Setting Pool Conncetions Engine.
    # |-----------------------------------------------------------------------------
    INSTANCE_UNIX_SOCKET = os.environ.get("INSTANCE_UNIX_SOCKET")
    username = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASS", "")
    host = os.environ.get("DB_HOST", "127.0.0.1")
    port = os.environ.get("DB_PORT", "5432")
    database = os.environ.get("DB_NAME", "budimas-dev")
    # connection_string = f"postgresql+pg8000://postgres:HorusBudimas@/postgres?unix_sock={INSTANCE_UNIX_SOCKET}/.s.PGSQL.5432"
    connection_string = f"postgresql+pg8000://{username}:{password}@{host}:{port}/{database}"
    pool = sqlalchemy.create_engine(connection_string, **db_config)

    # |-----------------------------------------------------------------------------
    # | [END cloud_sql_mysql_sqlalchemy_create_tcp]
    # |-----------------------------------------------------------------------------

    return pool

# |---------------------------------------------------------------------------------
# | CONNECTION
# |---------------------------------------------------------------------------------
db = init_connection_engine()