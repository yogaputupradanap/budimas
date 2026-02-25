import os
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "budimas-dev")

connection_string = (
    f"postgresql+pg8000://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("🔌 Connecting to DB...")
print("HOST:", DB_HOST)
print("PORT:", DB_PORT)
print("DB:", DB_NAME)

engine = sqlalchemy.create_engine(connection_string)

try:
    with engine.connect() as conn:
        result = conn.execute(
            sqlalchemy.text("select current_database(), current_user")
        ).fetchone()

    print("✅ CONNECTED SUCCESS")
    print("DATABASE :", result[0])
    print("USER     :", result[1])

except Exception as e:
    print("🛑 CONNECTION FAILED")
    print(str(e))
