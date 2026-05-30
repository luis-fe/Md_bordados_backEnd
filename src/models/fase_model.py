# models/fase_model.py

from src.connection import db_config


class Fase:
    
    def __init__(self):
        pass

    def cadastrarFase(self, descricao_fase, fase_finalizacao):
        # O cod_fase é SERIAL, então não enviamos no INSERT. O RETURNING devolve o ID gerado.
        query = """
            INSERT INTO fase (descricao_fase, fase_finalizacao)
            VALUES (%s, %s) RETURNING cod_fase;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (descricao_fase, fase_finalizacao))
                conn.commit()
                return cursor.fetchone()[0] # Retorna o cod_fase gerado automaticamente
        except Exception as e:
            conn.rollback() 
            raise e
        finally:
            conn.close() 

    def buscarTodasFases(self):
        query = "SELECT cod_fase, descricao_fase, fase_finalizacao FROM fase ORDER BY cod_fase ASC;"
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            conn.close()

    def editarFase(self, cod_fase, descricao_fase, fase_finalizacao):
        query = """
            UPDATE fase 
            SET descricao_fase = %s, fase_finalizacao = %s 
            WHERE cod_fase = %s;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (descricao_fase, fase_finalizacao, cod_fase))
                conn.commit()
                return cursor.rowcount > 0 
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def excluirFase(self, cod_fase):
        query = "DELETE FROM fase WHERE cod_fase = %s;"
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_fase,))
                conn.commit()
                return cursor.rowcount > 0 
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()