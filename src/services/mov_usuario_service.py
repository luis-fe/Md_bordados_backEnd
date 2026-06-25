import logging
from src.models.mov_usuario_model import MovUsuario

# Configuração básica de logger (ideal para produção)
logger = logging.getLogger(__name__)

class ServiceMovUsuario:
    def __init__(self):
        self.mov_usuario_model = MovUsuario()

    def listaMovUsuarios(self):
        try:
            mov_db = self.mov_usuario_model.buscarTodasMovUsuarios()

            # Construção da lista de forma mais limpa (List Comprehension)
            mov_lista = [
                {
                    "cod_mov_usuario": row[0],
                    "cod_usuario": row[1],
                    "nome_usuario": row[2],
                    "cod_fase": row[3],
                    "descricao_fase": row[4]
                }
                for row in mov_db
            ]

            return {"status": "success", "data": mov_lista}, 200

        except Exception as e:
            logger.error(f"Erro ao listar autorizações de movimentação: {e}")
            # Mensagem genérica para o usuário, erro real no log do servidor
            return {"status": "error", "message": "Erro interno ao listar autorizações."}, 500

    def inclusaoMovUsuario(self, dados):
        # Validação mais segura contra o valor '0'
        if not dados or dados.get('cod_usuario') is None or dados.get('cod_fase') is None:
            return {"status": "error", "message": "Os campos cod_usuario e cod_fase são obrigatórios."}, 400

        try:
            novo_cod = self.mov_usuario_model.cadastrarMovUsuario(
                cod_usuario=dados.get('cod_usuario'),
                cod_fase=dados.get('cod_fase')
            )

            return {"status": "success", "message": "Autorização cadastrada com sucesso", "cod_mov_usuario": novo_cod}, 201

        except Exception as e:
            logger.error(f"Erro na inclusão de MovUsuario: {e}")
            # Você pode manter o detalhe se for estritamente necessário para debug no front, 
            # mas em produção, prefira mensagens genéricas.
            return {"status": "error", "message": f"Erro ao cadastrar autorização. Verifique se o usuário e a fase existem: {str(e)}"}, 500

    def editarMovUsuario(self, cod_mov_usuario, dados):
        if not dados or dados.get('cod_usuario') is None or dados.get('cod_fase') is None:
            return {"status": "error", "message": "Os campos cod_usuario e cod_fase são obrigatórios para atualização."}, 400

        try:
            sucesso = self.mov_usuario_model.editarMovUsuario(
                cod_mov_usuario=cod_mov_usuario,
                cod_usuario=dados.get('cod_usuario'),
                cod_fase=dados.get('cod_fase')
            )

            if sucesso:
                return {"status": "success", "message": "Autorização atualizada com sucesso."}, 200
            else:
                return {"status": "error", "message": "Autorização não encontrada para edição."}, 404

        except Exception as e:
            logger.error(f"Erro na edição de MovUsuario ({cod_mov_usuario}): {e}")
            return {"status": "error", "message": f"Erro ao atualizar autorização: {str(e)}"}, 500

    def excluirMovUsuario(self, cod_mov_usuario):
        try:
            sucesso = self.mov_usuario_model.excluirMovUsuario(cod_mov_usuario=cod_mov_usuario)

            if sucesso:
                return {"status": "success", "message": "Autorização excluída com sucesso."}, 200
            else:
                return {"status": "error", "message": "Autorização não encontrada para exclusão."}, 404

        except Exception as e:
            logger.error(f"Erro na exclusão de MovUsuario ({cod_mov_usuario}): {e}")
            return {"status": "error", "message": f"Erro ao excluir autorização: {str(e)}"}, 500