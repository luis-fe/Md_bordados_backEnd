# services/op_service.py

from src.models.op_model import OrdemProducao

class ServiceOrdemProducao:
    def __init__(self):
        self.op_model = OrdemProducao()

    def format_op_row(self, row):
        """Helper para formatar a tupla do banco em um dicionário."""
        return {
            "cod_op": row[0],
            "id_op_cliente": row[1],
            "descricao_op": row[2],
            "valor_unitario": float(row[3]) if row[3] else 0.0,
            "data_previsao": row[4].strftime('%Y-%m-%d') if row[4] else None,
            "data_criacao": row[5].strftime('%Y-%m-%d %H:%M:%S') if row[5] else None,
            "status_op": row[6],
            "cliente": {
                "id": row[7],
                "razao_social": row[8]
            },
            "roteiro": {
                "cod_roteiro": row[9],
                "descricao_roteiro": row[10]
            },
            "usuario": {
                "cod_usuario": row[11],
                "nome_usuario": row[12]
            },
            # Nova linha mapeando a coluna gerada pelo GROUP BY do banco
            "qtde_pecas": int(row[13]) if row[13] else 0
        }

    def listaOPs(self):
        try:
            ops_db = self.op_model.buscarTodasOPs()
            ops_lista = [self.format_op_row(row) for row in ops_db]

            return {"status": "success", "data": ops_lista}, 200

        except Exception as e:
            return {"status": "error", "message": f"Erro ao listar Ordens de Produção: {str(e)}"}, 500

    def buscaOP(self, cod_op):
        try:
            op_db = self.op_model.buscarOPPorId(cod_op)
            if op_db:
                return {"status": "success", "data": self.format_op_row(op_db)}, 200
            else:
                return {"status": "error", "message": "Ordem de Produção não encontrada."}, 404
        except Exception as e:
            return {"status": "error", "message": f"Erro ao buscar OP: {str(e)}"}, 500

    def inclusaoOP(self, dados):
        campos_obrigatorios = ['cod_op', 'cod_cliente', 'cod_roteiro', 'usuario_geracao']
        if not dados or not all(campo in dados for campo in campos_obrigatorios):
            return {"status": "error", "message": "Os campos cod_op, cod_cliente, cod_roteiro e usuario_geracao são obrigatórios."}, 400

        try:
            nova_op = self.op_model.cadastrarOP(
                cod_op=dados.get('cod_op'),
                cod_cliente=dados.get('cod_cliente'),
                descricao_op=dados.get('descricao_op', ''),
                cod_roteiro=dados.get('cod_roteiro'),
                valor_unitario=dados.get('valor_unitario', 0.0),
                data_previsao=dados.get('data_previsao'),
                usuario_geracao=dados.get('usuario_geracao'),
                status_op=dados.get('status_op', 'Criada')
            )

            return {"status": "success", "message": "Ordem de Produção gerada com sucesso", "cod_op": nova_op}, 201

        except Exception as e:
            if "unique constraint" in str(e).lower() and "cod_op" in str(e).lower():
                return {"status": "error", "message": "Já existe uma OP com este código."}, 409
            return {"status": "error", "message": f"Erro ao gerar OP: {str(e)}"}, 500

    def editarOP(self, cod_op, dados):
        if not dados:
            return {"status": "error", "message": "Dados não informados para atualização."}, 400

        try:
            sucesso = self.op_model.editarOP(
                cod_op=cod_op,
                descricao_op=dados.get('descricao_op', ''),
                cod_roteiro=dados.get('cod_roteiro'),
                valor_unitario=dados.get('valor_unitario', 0.0),
                data_previsao=dados.get('data_previsao'),
                status_op=dados.get('status_op', 'Criada')
            )

            if sucesso:
                return {"status": "success", "message": "Ordem de Produção atualizada com sucesso."}, 200
            else:
                return {"status": "error", "message": "OP não encontrada para edição."}, 404

        except Exception as e:
            return {"status": "error", "message": f"Erro ao atualizar OP: {str(e)}"}, 500

    def excluirOP(self, cod_op):
        try:
            sucesso = self.op_model.excluirOP(cod_op=cod_op)

            if sucesso:
                return {"status": "success", "message": "Ordem de Produção excluída com sucesso."}, 200
            else:
                return {"status": "error", "message": "OP não encontrada para exclusão."}, 404

        except Exception as e:
            # Captura erro caso a OP já tenha movimentos (grade_op, mov_fase) devido ao ON DELETE CASCADE/RESTRICT
            return {"status": "error", "message": f"Erro ao excluir OP. Ela pode conter movimentações vinculadas: {str(e)}"}, 500