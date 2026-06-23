# services/grade_op_service.py

from src.models.grade_op_model import GradeOp


class ServiceGradeOp:
    def __init__(self):
        self.grade_model = GradeOp()

    def listaGradeDaOP(self, cod_op):
        try:
            grade_db = self.grade_model.buscarGradePorOP(cod_op)

            grade_lista = []
            for row in grade_db:
                grade_lista.append({
                    "cod_op": row[0],
                    "cod_tamanho": row[1],
                    "descricao_tamanho": row[2],
                    "cor": row[3],
                    "quantidade_qual_1": row[4],
                    "quantidade_qual_2": row[5],
                    "quantidade_cancelada": row[6]
                })

            return {"status": "success", "data": grade_lista}, 200

        except Exception as e:
            return {"status": "error", "message": f"Erro ao listar a grade da OP: {str(e)}"}, 500

    def inclusaoGradeOp(self, dados):
        if not dados or not dados.get('cod_op') or not dados.get('cod_tamanho'):
            return {"status": "error", "message": "Os campos cod_op e cod_tamanho são obrigatórios."}, 400

        try:
            # Garante o fallback do banco se o campo 'cor' não for enviado
            cor_definida = dados.get('cor', 'Sem Cor')
            if not cor_definida:
                cor_definida = 'Sem Cor'

            sucesso = self.grade_model.cadastrarGradeOp(
                cod_op=dados.get('cod_op'),
                cod_tamanho=dados.get('cod_tamanho'),
                cor=cor_definida,
                quantidade_qual_1=dados.get('quantidade_qual_1', 0),
                quantidade_qual_2=dados.get('quantidade_qual_2', 0),
                quantidade_cancelada=dados.get('quantidade_cancelada', 0)
            )

            if sucesso:
                return {"status": "success", "message": "Item adicionado à grade com sucesso."}, 201
            else:
                return {"status": "error", "message": "Não foi possível adicionar o item à grade."}, 400

        except Exception as e:
            if "duplicate key" in str(e).lower() or "unique constraint" in str(e).lower():
                return {"status": "error", "message": "Este tamanho e cor já estão lançados para esta OP."}, 409
            return {"status": "error", "message": f"Erro ao cadastrar grade: {str(e)}"}, 500

    def editarGradeOp(self, cod_op, cod_tamanho, cor, dados):
        if not dados:
            return {"status": "error", "message": "Dados de quantidades não informados."}, 400

        try:
            sucesso = self.grade_model.editarGradeOp(
                cod_op=cod_op,
                cod_tamanho=cod_tamanho,
                cor=cor,
                quantidade_qual_1=dados.get('quantidade_qual_1', 0),
                quantidade_qual_2=dados.get('quantidade_qual_2', 0),
                quantidade_cancelada=dados.get('quantidade_cancelada', 0)
            )

            if sucesso:
                return {"status": "success", "message": "Quantidades da grade atualizadas com sucesso."}, 200
            else:
                return {"status": "error", "message": "Item da grade não encontrado para edição."}, 404

        except Exception as e:
            return {"status": "error", "message": f"Erro ao atualizar grade: {str(e)}"}, 500

    def excluirLinhaGrade(self, cod_op, cod_tamanho, cor):
        try:
            sucesso = self.grade_model.excluirLinhaGrade(cod_op=cod_op, cod_tamanho=cod_tamanho, cor=cor)

            if sucesso:
                return {"status": "success", "message": "Item removido da grade com sucesso."}, 200
            else:
                return {"status": "error", "message": "Item da grade não encontrado para exclusão."}, 404

        except Exception as e:
            return {"status": "error", "message": f"Erro ao excluir item da grade: {str(e)}"}, 500