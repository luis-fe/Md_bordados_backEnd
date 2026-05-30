# services/tamanho_service.py

from src.models.tamanho_model import Tamanho


class ServiceTamanho:
    def __init__(self):
        self.tamanho_model = Tamanho()

    def listaTamanhos(self):
        try:
            tamanhos_db = self.tamanho_model.buscarTodosTamanhos()

            # Formata a tupla retornada pelo psycopg2 para uma lista de dicionários
            tamanhos_lista = []
            for row in tamanhos_db:
                tamanhos_lista.append({
                    "cod_tamanho": row[0],
                    "descricao_tamanho": row[1],
                    "sequenciaTamanho": row[2]
                })

            return {"status": "success", "data": tamanhos_lista}, 200

        except Exception as e:
            return {"status": "error", "message": f"Erro ao listar tamanhos: {str(e)}"}, 500

    def inclusaoTamanho(self, dados):
        # Validação básica: código do tamanho é a chave primária e, portanto, obrigatório
        if not dados or not dados.get('cod_tamanho'):
            return {"status": "error", "message": "O código do tamanho (cod_tamanho) é obrigatório."}, 400

        try:
            novo_cod = self.tamanho_model.cadastrarTamanho(
                cod_tamanho=dados.get('cod_tamanho'),
                descricao_tamanho=dados.get('descricao_tamanho'),
                sequencia_tamanho=dados.get('sequenciaTamanho')
            )

            return {"status": "success", "message": "Tamanho cadastrado com sucesso", "cod_tamanho": novo_cod}, 201

        except Exception as e:
            # Captura erros como violação de chave primária (tamanho já existe)
            return {"status": "error", "message": f"Erro ao cadastrar tamanho: {str(e)}"}, 500

    def editarTamanho(self, cod_tamanho, dados):
        if not dados:
            return {"status": "error", "message": "Nenhum dado fornecido para atualização."}, 400

        try:
            sucesso = self.tamanho_model.editarTamanho(
                cod_tamanho=cod_tamanho,
                descricao_tamanho=dados.get('descricao_tamanho'),
                sequencia_tamanho=dados.get('sequenciaTamanho')
            )

            if sucesso:
                return {"status": "success", "message": "Tamanho atualizado com sucesso."}, 200
            else:
                return {"status": "error", "message": "Tamanho não encontrado para edição."}, 404

        except Exception as e:
            return {"status": "error", "message": f"Erro ao atualizar tamanho: {str(e)}"}, 500

    def excluirTamanho(self, cod_tamanho):
        try:
            sucesso = self.tamanho_model.excluirTamanho(cod_tamanho=cod_tamanho)

            if sucesso:
                return {"status": "success", "message": "Tamanho excluído com sucesso."}, 200
            else:
                return {"status": "error", "message": "Tamanho não encontrado para exclusão."}, 404

        except Exception as e:
            # Muito útil para capturar o erro de ON DELETE RESTRICT (quando o tamanho já está em uso na grade_op)
            return {"status": "error", "message": f"Erro ao excluir tamanho. Ele pode estar em uso por uma Ordem de Produção: {str(e)}"}, 500