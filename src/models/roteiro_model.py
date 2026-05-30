# models/roteiro_model.py

from src.connection import db_config


class RoteiroPadrao:
    
    def __init__(self):
        pass

    def cadastrarRoteiro(self, descricao_roteiro):
        # cod_roteiro é SERIAL, o banco gera automaticamente
        query = """
            INSERT INTO roteiro_padrao (descricao_roteiro)
            VALUES (%s) RETURNING cod_roteiro;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (descricao_roteiro,))
                conn.commit()
                return cursor.fetchone()[0] # Retorna o ID gerado
        except Exception as e:
            conn.rollback() 
            raise e
        finally:
            conn.close() 

    def buscarTodosRoteiros(self):
        query = "SELECT cod_roteiro, descricao_roteiro FROM roteiro_padrao ORDER BY cod_roteiro ASC;"
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            conn.close()

    def editarRoteiro(self, cod_roteiro, descricao_roteiro):
        query = """
            UPDATE roteiro_padrao 
            SET descricao_roteiro = %s 
            WHERE cod_roteiro = %s;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (descricao_roteiro, cod_roteiro))
                conn.commit()
                return cursor.rowcount > 0 
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def excluirRoteiro(self, cod_roteiro):
        query = "DELETE FROM roteiro_padrao WHERE cod_roteiro = %s;"
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_roteiro,))
                conn.commit()
                return cursor.rowcount > 0 
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()