# models/usuario_model.py

from connection import db_config

class Usuario:
    
    def __init__(self):
        pass

    def cadastrarUsuario(self, nome_usuario):
        query = """
            INSERT INTO usuario (nome_usuario) 
            VALUES (%s) RETURNING cod_usuario;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (nome_usuario,))
                conn.commit()
                return cursor.fetchone()[0] # Retorna o ID (cod_usuario) gerado
        except Exception as e:
            conn.rollback() # Em caso de erro, desfaz a transação
            raise e
        finally:
            conn.close() # Garante que a conexão será fechada

    def editarUsuario(self, cod_usuario, nome_usuario):
        query = """
            UPDATE usuario 
            SET nome_usuario = %s 
            WHERE cod_usuario = %s;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (nome_usuario, cod_usuario))
                conn.commit()
                return cursor.rowcount > 0 # Retorna True se o usuário foi encontrado e editado
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    # Adicionei este método extra caso precise listar os usuários no front-end depois
    def buscarUsuarios(self):
        query = "SELECT cod_usuario, nome_usuario FROM usuario;"
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            conn.close()