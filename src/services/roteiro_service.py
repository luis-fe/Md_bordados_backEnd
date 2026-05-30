# services/roteiro_service.py

from src.models.roteiro_model import RoteiroPadrao


class ServiceRoteiroPadrao:
    def __init__(self):
        self.roteiro_model = RoteiroPadrao()

    def listaRoteiros(self):
        try:
            roteiros_db = self.roteiro_model.buscarTodosRoteiros()

            roteiros_lista = []
            for row in roteiros_db:
                roteiros_lista.append({
                    "cod_roteiro": row[0],
                    "descricao_roteiro": row[1]
                })

            return {"status": "success", "data": roteiros_lista}, 200

        except Exception as e:
            return {"status": "error", "message": f"Erro ao listar roteiros padrão: {str(e)}"}, 500

    def inclusaoRoteiro(self, dados):
        if not dados or not dados.get('descricao_roteiro'):
            return {"status": "error", "message": "A descrição do roteiro é obrigatória."}, 400

        try:
            novo_cod = self.roteiro_model.cadastrarRoteiro(
                descricao_roteiro=dados.get('descricao_roteiro')
            )

            return {"status": "success", "message": "Roteiro cadastrado com sucesso", "cod_roteiro": novo_cod}, 201

        except Exception as e:
            return {"status": "error", "message": f"Erro ao cadastrar roteiro: {str(e)}"}, 500

    def editarRoteiro(self, cod_roteiro, dados):
        if not dados or not dados.get('descricao_roteiro'):
            return {"status": "error", "message": "A descrição do roteiro é obrigatória para atualização."}, 400

        try:
            sucesso = self.roteiro_model.editarRoteiro(
                cod_roteiro=cod_roteiro,
                descricao_roteiro=dados.get('descricao_roteiro')
            )

            if sucesso:
                return {"status": "success", "message": "Roteiro atualizado com sucesso."}, 200
            else:
                return {"status": "error", "message": "Roteiro não encontrado para edição."}, 404

        except Exception as e:
            return {"status": "error", "message": f"Erro ao atualizar roteiro: {str(e)}"}, 500

    def excluirRoteiro(self, cod_roteiro):
        try:
            sucesso = self.roteiro_model.excluirRoteiro(cod_roteiro=cod_roteiro)

            if sucesso:
                return {"status": "success", "message": "Roteiro excluído com sucesso."}, 200
            else:
                return {"status": "error", "message": "Roteiro não encontrado para exclusão."}, 404

        except Exception as e:
            # Captura exceções de restrição de chave estrangeira (ON DELETE RESTRICT em ordem_producao)
            return {"status": "error", "message": f"Erro ao excluir roteiro. Ele pode estar sendo utilizado em uma Ordem de Produção: {str(e)}"}, 500