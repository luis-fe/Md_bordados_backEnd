# services/roteiro_fase_service.py

from src.models.roteiro_fase_model import RoteiroFase


class ServiceRoteiroFase:
    def __init__(self):
        self.roteiro_fase_model = RoteiroFase()

    def listaFasesRoteiro(self, cod_roteiro):
        try:
            fases_db = self.roteiro_fase_model.buscarFasesDoRoteiro(cod_roteiro)

            fases_lista = []
            for row in fases_db:
                fases_lista.append({
                    "cod_roteiro": row[0],
                    "cod_fase": row[1],
                    "descricao_fase": row[2],
                    "sequencia": row[3],
                    "fase_simultanea": row[4]
                })

            return {"status": "success", "data": fases_lista}, 200

        except Exception as e:
            return {"status": "error", "message": f"Erro ao listar as fases do roteiro: {str(e)}"}, 500

    def inclusaoRoteiroFase(self, dados):
        if not dados or not dados.get('cod_roteiro') or not dados.get('cod_fase') or not dados.get('sequencia'):
            return {"status": "error", "message": "Os campos cod_roteiro, cod_fase e sequencia são obrigatórios."}, 400

        try:
            sucesso = self.roteiro_fase_model.cadastrarRoteiroFase(
                cod_roteiro=dados.get('cod_roteiro'),
                cod_fase=dados.get('cod_fase'),
                sequencia=dados.get('sequencia'),
                fase_simultanea=dados.get('fase_simultanea')
            )

            if sucesso:
                return {"status": "success", "message": "Fase vinculada ao roteiro com sucesso."}, 201
            else:
                return {"status": "error", "message": "Não foi possível vincular a fase ao roteiro."}, 400

        except Exception as e:
            # Tratamento caso tente inserir uma duplicidade na chave composta (cod_roteiro, cod_fase)
            if "duplicate key" in str(e).lower() or "unique constraint" in str(e).lower():
                return {"status": "error", "message": "Esta fase já está vinculada a este roteiro."}, 409
            return {"status": "error", "message": f"Erro ao cadastrar fase no roteiro: {str(e)}"}, 500

    def editarRoteiroFase(self, cod_roteiro, cod_fase, dados):
        if not dados or not dados.get('sequencia'):
            return {"status": "error", "message": "A sequência é obrigatória para atualização."}, 400

        try:
            sucesso = self.roteiro_fase_model.editarRoteiroFase(
                cod_roteiro=cod_roteiro,
                cod_fase=cod_fase,
                sequencia=dados.get('sequencia'),
                fase_simultanea=dados.get('fase_simultanea')
            )

            if sucesso:
                return {"status": "success", "message": "Fase do roteiro atualizada com sucesso."}, 200
            else:
                return {"status": "error", "message": "Vínculo de fase e roteiro não encontrado para edição."}, 404

        except Exception as e:
            return {"status": "error", "message": f"Erro ao atualizar fase do roteiro: {str(e)}"}, 500

    def excluirRoteiroFase(self, cod_roteiro, cod_fase):
        try:
            sucesso = self.roteiro_fase_model.excluirRoteiroFase(cod_roteiro=cod_roteiro, cod_fase=cod_fase)

            if sucesso:
                return {"status": "success", "message": "Fase removida do roteiro com sucesso."}, 200
            else:
                return {"status": "error", "message": "Vínculo de fase e roteiro não encontrado para exclusão."}, 404

        except Exception as e:
            return {"status": "error", "message": f"Erro ao excluir fase do roteiro: {str(e)}"}, 500