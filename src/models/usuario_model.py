# models/usuario_model.py

import bcrypt
from src.connection import db_config


class Usuario:

    def __init__(self):
        pass

    # --- MÉTODOS DE SEGURANÇA ---

    def _criptografar_senha(self, senha_plana):
        """Recebe a senha em texto plano e retorna o hash criptografado."""
        bytes_senha = senha_plana.encode('utf-8')
        salt = bcrypt.gensalt()
        hash_senha = bcrypt.hashpw(bytes_senha, salt)
        return hash_senha.decode('utf-8')

    def verificar_senha(self, senha_plana, senha_hash):
        """Verifica se a senha digitada no login bate com o hash do banco."""
        bytes_senha = senha_plana.encode('utf-8')
        bytes_hash = senha_hash.encode('utf-8')
        return bcrypt.checkpw(bytes_senha, bytes_hash)

    # --- MÉTODOS DE BANCO DE DADOS ATUALIZADOS ---

    def cadastrarUsuario(self, nome_usuario, login, senha, contato, status="ativo"):
        senha_criptografada = self._criptografar_senha(senha)

        # Adicionados: login, contato e status
        query = """
            INSERT INTO usuario (nome_usuario, login, senha, contato, status) 
            VALUES (%s, %s, %s, %s, %s) RETURNING cod_usuario;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (nome_usuario, login, senha_criptografada, contato, status))
                conn.commit()
                return cursor.fetchone()[0]  # Retorna o ID gerado
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def editarUsuario(self, cod_usuario, nome_usuario, login, contato, status, nova_senha=None):
        """
        Atualiza os dados do usuário. Se uma nova_senha for passada, ela também será atualizada.
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                if nova_senha:
                    senha_criptografada = self._criptografar_senha(nova_senha)
                    query = """
                        UPDATE usuario 
                        SET nome_usuario = %s, login = %s, senha = %s, contato = %s, status = %s 
                        WHERE cod_usuario = %s;
                    """
                    cursor.execute(query, (nome_usuario, login, senha_criptografada, contato, status, cod_usuario))
                else:
                    # Atualiza os dados, mantendo a senha antiga
                    query = """
                        UPDATE usuario 
                        SET nome_usuario = %s, login = %s, contato = %s, status = %s 
                        WHERE cod_usuario = %s;
                    """
                    cursor.execute(query, (nome_usuario, login, contato, status, cod_usuario))

                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def buscarUsuarios(self):
        # A listagem agora traz os novos campos, mas continua protegendo a senha
        query = "SELECT cod_usuario, nome_usuario, login, contato, status FROM usuario;"
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            conn.close()