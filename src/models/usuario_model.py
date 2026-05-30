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

        # Traduz a string recebida da API para o formato inteiro esperado pelo banco (1 ou 0)
        # O 'in' garante que se vier 'ativo', '1', ou True, ele salva 1.
        status_db = 1 if str(status).lower() in ['ativo', '1', 'true'] else 0

        query = """
            INSERT INTO usuario (nome_usuario, login, senha, contato, status) 
            VALUES (%s, %s, %s, %s, %s) RETURNING cod_usuario;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Agora passamos o status_db convertido
                cursor.execute(query, (nome_usuario, login, senha_criptografada, contato, status_db))
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
        # Traduz o status para o banco
        status_db = 1 if str(status).lower() in ['ativo', '1', 'true'] else 0

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
                    cursor.execute(query, (nome_usuario, login, senha_criptografada, contato, status_db, cod_usuario))
                else:
                    # Atualiza os dados, mantendo a senha antiga
                    query = """
                        UPDATE usuario 
                        SET nome_usuario = %s, login = %s, contato = %s, status = %s 
                        WHERE cod_usuario = %s;
                    """
                    cursor.execute(query, (nome_usuario, login, contato, status_db, cod_usuario))

                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()


    def buscarUsuarios(self):
        # O CASE WHEN faz com que o banco de dados já devolva a string 'ativo' ou 'inativo'
        # ao invés de devolver os números 1 ou 0.
        query = """
            SELECT cod_usuario, 
                   nome_usuario, 
                   login, 
                   contato, 
                   CASE WHEN status = 1 THEN 'ativo' ELSE 'inativo' END as status
            FROM usuario;
        """
        conn = db_config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            conn.close()

            
    def buscarUsuarioPorLogin(self, login):
            """Busca o usuário no banco pelo login para realizar a autenticação."""
            query = """
                SELECT cod_usuario, nome_usuario, senha, status 
                FROM usuario 
                WHERE login = %s;
            """
            conn = db_config.get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, (login,))
                    # Retorna a tupla (cod_usuario, nome_usuario, senha_hash, status) ou None
                    return cursor.fetchone()
            finally:
                conn.close()