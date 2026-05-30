# services/usuario_service.py

from src.models.usuario_model import Usuario


class ServiceUsuario:
    def __init__(self):
        self.usuario_model = Usuario()

    def listaUsuarios(self):
        try:
            usuarios_db = self.usuario_model.buscarUsuarios()

            # Formata a tupla retornada pelo psycopg2 para uma lista de dicionários
            usuarios_lista = []
            for row in usuarios_db:
                usuarios_lista.append({
                    "id": row[0],
                    "nome_usuario": row[1],
                    "login": row[2],
                    "contato": row[3],
                    "status": row[4]
                })

            return {"status": "success", "data": usuarios_lista}, 200

        except Exception as e:
            return {"status": "error", "message": f"Erro ao listar usuários: {str(e)}"}, 500

    def inclusaoUsuario(self, dados):
        # Validação básica: nome, login e senha são obrigatórios para criar um usuário
        if not dados or not dados.get('nome_usuario') or not dados.get('login') or not dados.get('senha'):
            return {"status": "error", "message": "Nome, login e senha são campos obrigatórios."}, 400

        try:
            # Se o status não for enviado no JSON, assume 'ativo' como padrão
            status_usuario = dados.get('status', 'ativo')

            novo_id = self.usuario_model.cadastrarUsuario(
                nome_usuario=dados.get('nome_usuario'),
                login=dados.get('login'),
                senha=dados.get('senha'),
                contato=dados.get('contato'),
                status=status_usuario
            )

            return {"status": "success", "message": "Usuário cadastrado com sucesso", "id": novo_id}, 201

        except Exception as e:
            # Captura erros como violação de constraint (ex: login já existe no banco)
            return {"status": "error", "message": f"Erro ao cadastrar usuário: {str(e)}"}, 500

    def editarUsuario(self, id_usuario, dados):
        if not dados:
            return {"status": "error", "message": "Nenhum dado fornecido para atualização."}, 400

        # Para editar, precisamos garantir que os campos obrigatórios da edição estão presentes
        if not dados.get('nome_usuario') or not dados.get('login') or not dados.get('status'):
            return {"status": "error", "message": "Nome, login e status são obrigatórios para a edição."}, 400

        try:
            # Pega a nova senha apenas se ela tiver sido enviada no JSON
            nova_senha = dados.get('senha')
            if nova_senha and nova_senha.strip() == "":
                nova_senha = None  # Evita salvar uma senha em branco se o front-end mandar uma string vazia

            sucesso = self.usuario_model.editarUsuario(
                cod_usuario=id_usuario,
                nome_usuario=dados.get('nome_usuario'),
                login=dados.get('login'),
                contato=dados.get('contato'),
                status=dados.get('status'),
                nova_senha=nova_senha
            )

            if sucesso:
                return {"status": "success", "message": "Usuário atualizado com sucesso."}, 200
            else:
                return {"status": "error", "message": "Usuário não encontrado."}, 404

        except Exception as e:
            return {"status": "error", "message": f"Erro ao atualizar usuário: {str(e)}"}, 500
        

        
    def autenticarUsuario(self, dados):
        if not dados or not dados.get('login') or not dados.get('senha'):
            return {"status": "error", "message": "Login e senha são obrigatórios."}, 400

        login = dados.get('login')
        senha_plana = dados.get('senha')

        try:
            # 1. Busca o usuário no banco
            usuario_db = self.usuario_model.buscarUsuarioPorLogin(login)

            # Se não encontrou o usuário, retorna erro genérico (boa prática de segurança)
            if not usuario_db:
                return {"status": "error", "message": "Usuário ou senha incorretos."}, 401

            cod_usuario, nome_usuario, senha_hash, status_db = usuario_db

            # 2. Verifica se o usuário está ativo (1 = ativo)
            if status_db != 1:
                return {"status": "error", "message": "Usuário inativo ou bloqueado."}, 403

            # 3. Verifica se a senha confere
            senha_valida = self.usuario_model.verificar_senha(senha_plana, senha_hash)

            if senha_valida:
                return {
                    "status": "success", 
                    "message": "Autenticação realizada com sucesso.",
                    "data": {
                        "id": cod_usuario,
                        "nome": nome_usuario,
                        "login": login
                    }
                }, 200
            else:
                return {"status": "error", "message": "Usuário ou senha incorretos."}, 401

        except Exception as e:
            return {"status": "error", "message": f"Erro durante a autenticação: {str(e)}"}, 500