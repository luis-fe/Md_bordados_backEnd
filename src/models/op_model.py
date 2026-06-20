# models/op_model.py

from src.connection import db_config


class OrdemProducao:

    def __init__(self):
        pass

    def cadastrarOP(self, cod_op, cod_cliente, descricao_op, cod_roteiro, valor_unitario, data_previsao, usuario_geracao, status_op='Criada'):
        # id_op_cliente e data_criacao são gerados automaticamente pelo Banco (Trigger e Default)
        query = """
            INSERT INTO ordem_producao (
                cod_op, cod_cliente, descricao_op, cod_roteiro, 
                valor_unitario, data_previsao, usuario_geracao, status_op
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING cod_op;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (
                    cod_op, cod_cliente, descricao_op, cod_roteiro,
                    valor_unitario, data_previsao, usuario_geracao, status_op
                ))
                conn.commit()
                return cursor.fetchone()[0]
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def buscarTodasOPs(self):
        # Utiliza INNER JOIN para trazer os nomes em vez de apenas os IDs, facilitando o Front-end
        query = """
            SELECT 
                op.cod_op, op.id_op_cliente, op.descricao_op, 
                op.valor_unitario, op.data_previsao, op.data_criacao, op.status_op,
                c.id AS cod_cliente, c.razao_social, 
                r.cod_roteiro, r.descricao_roteiro, 
                u.cod_usuario, u.nome_usuario
            FROM ordem_producao op
            INNER JOIN clientes c ON op.cod_cliente = c.id
            INNER JOIN roteiro_padrao r ON op.cod_roteiro = r.cod_roteiro
            INNER JOIN usuario u ON op.usuario_geracao = u.cod_usuario
            ORDER BY op.data_criacao DESC;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            conn.close()

    def buscarOPPorId(self, cod_op):
        query = """
            SELECT 
                op.cod_op, op.id_op_cliente, op.descricao_op, 
                op.valor_unitario, op.data_previsao, op.data_criacao, op.status_op,
                c.id AS cod_cliente, c.razao_social, 
                r.cod_roteiro, r.descricao_roteiro, 
                u.cod_usuario, u.nome_usuario
            FROM ordem_producao op
            INNER JOIN clientes c ON op.cod_cliente = c.id
            INNER JOIN roteiro_padrao r ON op.cod_roteiro = r.cod_roteiro
            INNER JOIN usuario u ON op.usuario_geracao = u.cod_usuario
            WHERE op.cod_op = %s;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_op,))
                return cursor.fetchone()
        finally:
            conn.close()

    def editarOP(self, cod_op, descricao_op, cod_roteiro, valor_unitario, data_previsao, status_op):
        # Geralmente não se altera o cliente ou usuário gerador após criada, apenas dados de processo
        query = """
            UPDATE ordem_producao 
            SET descricao_op = %s, 
                cod_roteiro = %s, 
                valor_unitario = %s, 
                data_previsao = %s, 
                status_op = %s
            WHERE cod_op = %s;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (
                    descricao_op, cod_roteiro, valor_unitario, data_previsao, status_op, cod_op
                ))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def excluirOP(self, cod_op):
        query = "DELETE FROM ordem_producao WHERE cod_op = %s;"
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_op,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()