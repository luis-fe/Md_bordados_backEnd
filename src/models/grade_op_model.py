# models/grade_op_model.py

from src.connection import db_config


class GradeOp:

    def __init__(self):
        pass

    def cadastrarGradeOp(self, cod_op, cod_tamanho, cor, quantidade_qual_1=0, quantidade_qual_2=0, quantidade_cancelada=0):
        query = """
            INSERT INTO grade_op (cod_op, cod_tamanho, cor, quantidade_qual_1, quantidade_qual_2, quantidade_cancelada)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_op, cod_tamanho, cor, quantidade_qual_1, quantidade_qual_2, quantidade_cancelada))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(e)
            conn.rollback()
            raise e
        finally:
            conn.close()

    def buscarGradePorOP(self, cod_op):
        # Busca toda a grade da OP trazendo a descrição e a sequência correta do tamanho para o grid
        query = """
            SELECT 
                g.cod_op, 
                g.cod_tamanho, 
                t.descricao_tamanho,
                g.cor, 
                g.quantidade_qual_1, 
                g.quantidade_qual_2, 
                g.quantidade_cancelada,
                t."sequenciaTamanho"
            FROM grade_op g
            INNER JOIN tamanho t ON g.cod_tamanho = t.cod_tamanho
            WHERE g.cod_op = %s
            ORDER BY g.cor ASC, t."sequenciaTamanho" ASC;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_op,))
                return cursor.fetchall()
        finally:
            conn.close()

    def buscarLinhaGrade(self, cod_op, cod_tamanho, cor):
        query = """
            SELECT cod_op, cod_tamanho, cor, quantidade_qual_1, quantidade_qual_2, quantidade_cancelada
            FROM grade_op
            WHERE cod_op = %s AND cod_tamanho = %s AND cor = %s;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_op, cod_tamanho, cor))
                return cursor.fetchone()
        finally:
            conn.close()

    def editarGradeOp(self, cod_op, cod_tamanho, cor, quantidade_qual_1, quantidade_qual_2, quantidade_cancelada):
        query = """
            UPDATE grade_op 
            SET quantidade_qual_1 = %s, 
                quantidade_qual_2 = %s, 
                quantidade_cancelada = %s
            WHERE cod_op = %s AND cod_tamanho = %s AND cor = %s;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (quantidade_qual_1, quantidade_qual_2, quantidade_cancelada, cod_op, cod_tamanho, cor))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def excluirLinhaGrade(self, cod_op, cod_tamanho, cor):
        query = """
            DELETE FROM grade_op 
            WHERE cod_op = %s AND cod_tamanho = %s AND cor = %s;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_op, cod_tamanho, cor))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()