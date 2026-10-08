from pathlib import Path
import pymysql

ROOT = Path(__file__).resolve().parents[1]
SQL_FILE = ROOT / "database" / "001_create_schema.sql"

connection = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    autocommit=True,
    charset="utf8mb4",
    client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS,
)

try:
    with connection.cursor() as cursor:
        cursor.execute(SQL_FILE.read_text(encoding="utf-8"))
    print("Banco Flash configurado com sucesso.")
finally:
    connection.close()
