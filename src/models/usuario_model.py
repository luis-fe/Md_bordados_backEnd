# models/usuario_model.py

import bcrypt
from src.connection import db_config


class Usuario:

    def __init__(self):
        pass

    # --- NOVOS MÉTODOS DE SEGURANÇA ---

    def _criptografar_senha(self, senha_plana):
        """Recebe a senha em texto plano e retorna o hash criptografado."""
        # O bcrypt exige que a senha seja convertida para bytes
        bytes_senha = senha_plana.encode('utf-8')
        salt = bcrypt.gensalt()
        hash_senha = bcrypt.hashpw(bytes_senha, salt)
        # Decodifica de volta para string para salvar no banco de dados (VARCHAR)
        return hash_senha.decode('utf-8')

    def verificar_senha(self, senha_plana, senha_hash):
        """Verifica se a senha digitada no login bate com o hash do banco."""
        bytes_senha = senha_plana.encode('utf-8')
        bytes_hash = senha_hash.encode('utf-8')
        return bcrypt.checkpw(bytes_senha, bytes_hash)

    # --- MÉTODOS DE BANCO DE DADOS ATUALIZADOS ---

    def cadastrarUsuario(self, nome_usuario, senha):
        senha_criptografada = self._criptografar_senha(senha)

        # Atualizado para inserir a senha no banco
        query = """
            INSERT INTO usuario (nome_usuario, senha) 
            VALUES (%s, %s) RETURNING cod_usuario;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (nome_usuario, senha_criptografada))
                conn.commit()
                return cursor.fetchone()[0]  # Retorna o ID (cod_usuario) gerado
        except Exception as e:
            conn.rollback()  # Em caso de erro, desfaz a transação
            raise e
        finally:
            conn.close()  # Garante que a conexão será fechada

    def editarUsuario(self, cod_usuario, nome_usuario, nova_senha=None):
        """
        Atualiza o nome do usuário. Se uma nova_senha for passada,
        ela também será criptografada e atualizada.
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                if nova_senha:
                    senha_criptografada = self._criptografar_senha(nova_senha)
                    query = """
                        UPDATE usuario 
                        SET nome_usuario = %s, senha = %s 
                        WHERE cod_usuario = %s;
                    """
                    cursor.execute(query, (nome_usuario, senha_criptografada, cod_usuario))
                else:
                    # Se não passou senha nova, atualiza apenas o nome
                    query = """
                        UPDATE usuario 
                        SET nome_usuario = %s 
                        WHERE cod_usuario = %s;
                    """
                    cursor.execute(query, (nome_usuario, cod_usuario))

                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def buscarUsuarios(self):
        # É uma boa prática NÃO retornar as senhas (mesmo em hash) numa listagem geral
        query = "SELECT cod_usuario, nome_usuario FROM usuario;"
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            conn.close()