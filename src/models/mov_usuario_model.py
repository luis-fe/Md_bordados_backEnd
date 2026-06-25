from src.connection import db_config

class MovUsuario:
    
    def __init__(self):
        pass

    def cadastrarMovUsuario(self, cod_usuario, cod_fase):
        # O 'ON CONFLICT DO NOTHING' barra a duplicação direto no banco de dados.
        query = """
            INSERT INTO mov_usuario (cod_usuario, cod_fase)
            VALUES (%s, %s)
            ON CONFLICT (cod_usuario, cod_fase) DO NOTHING;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_usuario, cod_fase))
                conn.commit()
                # Retorna True se inseriu um novo, ou False se já existia (ignorado pelo conflito)
                return cursor.rowcount > 0 
        except Exception as e:
            conn.rollback() 
            raise e
        finally:
            conn.close() 

    def buscarTodasMovUsuarios(self):
        query = """
            SELECT m.cod_usuario, u.nome_usuario, m.cod_fase, f.descricao_fase 
            FROM mov_usuario m
            INNER JOIN usuario u ON m.cod_usuario = u.cod_usuario
            INNER JOIN fase f ON m.cod_fase = f.cod_fase
            ORDER BY u.nome_usuario ASC;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            conn.close()

    def excluirMovUsuario(self, cod_usuario, cod_fase):
        # A exclusão agora exige a combinação das duas chaves
        query = """
            DELETE FROM mov_usuario 
            WHERE cod_usuario = %s AND cod_fase = %s;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_usuario, cod_fase))
                conn.commit()
                # Retorna True se deletou alguma linha
                return cursor.rowcount > 0 
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()