from src.connection import db_config

class MovUsuario:
    
    def __init__(self):
        pass

    def cadastrarMovUsuario(self, cod_usuario, cod_fase):
        query = """
            INSERT INTO mov_usuario (cod_usuario, cod_fase)
            VALUES (%s, %s) RETURNING cod_mov_usuario;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_usuario, cod_fase))
                conn.commit()
                return cursor.fetchone()[0] # Retorna o ID gerado
        except Exception as e:
            conn.rollback() 
            raise e
        finally:
            conn.close() 

    def buscarTodasMovUsuarios(self):
        # Faz um JOIN simples para trazer o nome do usuário e a descrição da fase, facilitando no front-end
        query = """
            SELECT m.cod_mov_usuario, m.cod_usuario, u.nome_usuario, m.cod_fase, f.descricao_fase 
            FROM mov_usuario m
            INNER JOIN usuario u ON m.cod_usuario = u.cod_usuario
            INNER JOIN fase f ON m.cod_fase = f.cod_fase
            ORDER BY m.cod_mov_usuario ASC;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            conn.close()

    def editarMovUsuario(self, cod_mov_usuario, cod_usuario, cod_fase):
        query = """
            UPDATE mov_usuario 
            SET cod_usuario = %s, cod_fase = %s 
            WHERE cod_mov_usuario = %s;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_usuario, cod_fase, cod_mov_usuario))
                conn.commit()
                return cursor.rowcount > 0 
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def excluirMovUsuario(self, cod_mov_usuario):
        query = "DELETE FROM mov_usuario WHERE cod_mov_usuario = %s;"
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_mov_usuario,))
                conn.commit()
                return cursor.rowcount > 0 
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()