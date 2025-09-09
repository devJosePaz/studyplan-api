import psycopg
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

conn = psycopg.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="127.0.0.1",  # se for outro container no mesmo compose: "db"
    port=os.getenv("POSTGRES_PORT")
)

print("Conexão OK:", conn.info)
conn.close()
