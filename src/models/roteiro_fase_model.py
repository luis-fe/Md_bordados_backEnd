# models/roteiro_fase_model.py

from src.connection import db_config


class RoteiroFase:

    def __init__(self):
        pass

    def cadastrarRoteiroFase(self, cod_roteiro, cod_fase, sequencia, fase_simultanea=None):
        query = """
            INSERT INTO roteiro_padrao_fase (cod_roteiro, cod_fase, sequencia, "faseSimultanea")
            VALUES (%s, %s, %s, %s);
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_roteiro, cod_fase, sequencia, fase_simultanea))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def buscarFasesDoRoteiro(self, cod_roteiro):
        # Utiliza INNER JOIN para buscar também a descrição da fase, facilitando a exibição no Front-end
        query = """
            SELECT 
                rpf.cod_roteiro, 
                rpf.cod_fase, 
                f.descricao_fase,
                rpf.sequencia, 
                rpf."faseSimultanea"
            FROM roteiro_padrao_fase rpf
            INNER JOIN fase f ON rpf.cod_fase = f.cod_fase
            WHERE rpf.cod_roteiro = %s
            ORDER BY rpf.sequencia ASC;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_roteiro,))
                return cursor.fetchall()
        finally:
            conn.close()

    def editarRoteiroFase(self, cod_roteiro, cod_fase, sequencia, fase_simultanea=None):
        # A chave primária composta é (cod_roteiro, cod_fase)
        query = """
            UPDATE roteiro_padrao_fase 
            SET sequencia = %s, 
                "faseSimultanea" = %s 
            WHERE cod_roteiro = %s AND cod_fase = %s;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (sequencia, fase_simultanea, cod_roteiro, cod_fase))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def excluirRoteiroFase(self, cod_roteiro, cod_fase):
        query = """
            DELETE FROM roteiro_padrao_fase 
            WHERE cod_roteiro = %s AND cod_fase = %s;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (cod_roteiro, cod_fase))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()