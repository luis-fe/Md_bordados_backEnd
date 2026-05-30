# models/tamanho_model.py

from src.connection import db_config


class Tamanho:
    
    def __init__(self):
        # O __init__ segue o padrão sem receber conexão direta.
        pass

    def cadastrarTamanho(self, cod_tamanho, descricao_tamanho, sequencia_tamanho):
        # Nota: "sequenciaTamanho" precisa de aspas duplas na query devido ao CamelCase no PostgreSQL
        query = """
            INSERT INTO tamanho (cod_tamanho, descricao_tamanho, "sequenciaTamanho")
            VALUES (%s, %s, %s) RETURNING cod_tamanho;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_tamanho, descricao_tamanho, sequencia_tamanho))
                conn.commit()
                return cursor.fetchone()[0] # Retorna o cod_tamanho cadastrado
        except Exception as e:
            conn.rollback() # Desfaz a transação em caso de erro
            raise e
        finally:
            conn.close() # Garante o fechamento da conexão

    def buscarTodosTamanhos(self):
        query = """
            SELECT cod_tamanho, descricao_tamanho, "sequenciaTamanho" 
            FROM tamanho 
            ORDER BY "sequenciaTamanho" ASC;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall() # Retorna a lista de tuplas com os tamanhos
        finally:
            conn.close()


    def verificarSequenciaExiste(self, sequencia, cod_tamanho_ignorar=None):
        query = 'SELECT cod_tamanho FROM tamanho WHERE "sequenciaTamanho" = %s'
        params = [sequencia]
        
        # Se for uma edição, precisamos ignorar o código do próprio tamanho que estamos editando
        if cod_tamanho_ignorar:
            query += " AND cod_tamanho != %s"
            params.append(cod_tamanho_ignorar)
            
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                # Retorna True se encontrou alguém usando essa sequência
                return cursor.fetchone() is not None 
        finally:
            conn.close()

    def editarTamanho(self, cod_tamanho, descricao_tamanho, sequencia_tamanho):
        query = """
            UPDATE tamanho 
            SET descricao_tamanho = %s, "sequenciaTamanho" = %s 
            WHERE cod_tamanho = %s;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (descricao_tamanho, sequencia_tamanho, cod_tamanho))
                conn.commit()
                return cursor.rowcount > 0 # Retorna True se alterou alguma linha
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def excluirTamanho(self, cod_tamanho):
        query = "DELETE FROM tamanho WHERE cod_tamanho = %s;"
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_tamanho,))
                conn.commit()
                return cursor.rowcount > 0 # Retorna True se deletou com sucesso
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()