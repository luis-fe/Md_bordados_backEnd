# models/cliente_model.py

from connection import db_config


class Cliente:
    
    # O __init__ não precisa mais receber a conexão, 
    # o próprio model vai gerenciar isso a cada método.
    def __init__(self):
        pass

    def cadastrarCliente(self, cnpj_cpf, razao_social, descricao, responsavel, email, contato):
        query = """
            INSERT INTO clientes (cnpj_cpf, razao_social, descricao_cliente, nome_responsavel, email, contato)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
        """
        conn = db_config.get_db_connection()
        try:
            # O 'with' fecha o cursor automaticamente ao terminar
            with conn.cursor() as cursor:
                cursor.execute(query, (cnpj_cpf, razao_social, descricao, responsavel, email, contato))
                conn.commit()
                return cursor.fetchone()[0] # Retorna o UUID gerado
        except Exception as e:
            conn.rollback() # Em caso de erro, desfaz a transação
            raise e
        finally:
            conn.close() # Garante que a conexão com o banco será fechada

    def buscarClientes(self):
        query = "SELECT id, cnpj_cpf, razao_social, email, contato FROM clientes;"
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            conn.close()

    def editarCliente(self, id_cliente, razao_social, email, contato):
        query = """
            UPDATE clientes 
            SET razao_social = %s, email = %s, contato = %s 
            WHERE id = %s;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (razao_social, email, contato, id_cliente))
                conn.commit()
                return cursor.rowcount > 0 # Retorna True se editou alguma linha
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()