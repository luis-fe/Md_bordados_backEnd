# db_config.py
import psycopg2
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def get_db_connection():
    """
    Cria e retorna uma conexão com o banco de dados PostgreSQL.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("db_host", "localhost"),
            database=os.getenv("db_name", "nome_do_seu_banco"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("db_password", "sua_senha"),
            port=os.getenv("db_port", "5432")
        )
        return conn
    except psycopg2.Error as e:
        print(f"Erro fatal: Não foi possível conectar ao banco de dados.\nDetalhes: {e}")
        raise e