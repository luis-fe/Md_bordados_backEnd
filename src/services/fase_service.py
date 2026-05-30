# services/fase_service.py

from src.models.fase_model import Fase


class ServiceFase:
    def __init__(self):
        self.fase_model = Fase()

    def listaFases(self):
        try:
            fases_db = self.fase_model.buscarTodasFases()

            fases_lista = []
            for row in fases_db:
                fases_lista.append({
                    "cod_fase": row[0],
                    "descricao_fase": row[1],
                    "fase_finalizacao": row[2] # Retorna True ou False
                })

            return {"status": "success", "data": fases_lista}, 200

        except Exception as e:
            return {"status": "error", "message": f"Erro ao listar fases: {str(e)}"}, 500

    def inclusaoFase(self, dados):
        # Validação: Apenas a descrição é obrigatória, já que o ID é automático e a finalização tem default FALSE
        if not dados or not dados.get('descricao_fase'):
            return {"status": "error", "message": "A descrição da fase é obrigatória."}, 400

        try:
            # Captura a flag de finalização. Se o front enviar string 'true' ou '1', converte para bool.
            fase_final = dados.get('fase_finalizacao', False)
            if isinstance(fase_final, str):
                fase_final = fase_final.lower() in ['true', '1', 't', 'y', 'yes']

            novo_cod = self.fase_model.cadastrarFase(
                descricao_fase=dados.get('descricao_fase'),
                fase_finalizacao=fase_final
            )

            return {"status": "success", "message": "Fase cadastrada com sucesso", "cod_fase": novo_cod}, 201

        except Exception as e:
            return {"status": "error", "message": f"Erro ao cadastrar fase: {str(e)}"}, 500

    def editarFase(self, cod_fase, dados):
        if not dados or not dados.get('descricao_fase'):
            return {"status": "error", "message": "A descrição da fase é obrigatória para atualização."}, 400

        try:
            # Tratamento de conversão de booleano novamente
            fase_final = dados.get('fase_finalizacao', False)
            if isinstance(fase_final, str):
                fase_final = fase_final.lower() in ['true', '1', 't', 'y', 'yes']

            sucesso = self.fase_model.editarFase(
                cod_fase=cod_fase,
                descricao_fase=dados.get('descricao_fase'),
                fase_finalizacao=fase_final
            )

            if sucesso:
                return {"status": "success", "message": "Fase atualizada com sucesso."}, 200
            else:
                return {"status": "error", "message": "Fase não encontrada para edição."}, 404

        except Exception as e:
            return {"status": "error", "message": f"Erro ao atualizar fase: {str(e)}"}, 500

    def excluirFase(self, cod_fase):
        try:
            sucesso = self.fase_model.excluirFase(cod_fase=cod_fase)

            if sucesso:
                return {"status": "success", "message": "Fase excluída com sucesso."}, 200
            else:
                return {"status": "error", "message": "Fase não encontrada para exclusão."}, 404

        except Exception as e:
            # Trata o erro caso a fase já esteja sendo usada em `roteiro_padrao_fase` ou `mov_fase`
            return {"status": "error", "message": f"Erro ao excluir fase. Ela já pode estar em uso no sistema: {str(e)}"}, 500