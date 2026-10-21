import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# Carrega as configurações do ficheiro .env.
load_dotenv()

# Lê as informações necessárias para encontrar a base de dados.
db_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME"),
)

# Cria o objeto que gere as ligações ao PostgreSQL.
engine = create_engine(
    db_url,
    pool_pre_ping=True,
)

# Esta função verifica se conseguimos comunicar com a base de dados.
def testar_ligacao():
    with engine.connect() as connection:
        resultado = connection.execute(text("SELECT 1"))
        return resultado.scalar_one()