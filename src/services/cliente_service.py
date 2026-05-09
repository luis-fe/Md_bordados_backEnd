# services/cliente_service.py

from src.models.cliente_model import Cliente

class ServiceCliente:
    def __init__(self):
        self.cliente_model = Cliente() # Não precisa mais receber conn

    def listaClientes(self):
        try:
            # Apenas chama o model, o model resolve a conexão
            clientes_db = self.cliente_model.buscarClientes()
            
            # Formata a tupla retornada pelo psycopg2 para uma lista de dicionários
            clientes_lista = []
            for row in clientes_db:
                clientes_lista.append({
                    "id": row[0],
                    "cnpj_cpf": row[1],
                    "razao_social": row[2],
                    "email": row[3],
                    "contato": row[4]
                })
            
            # Retorna os dados e o código HTTP 200 (OK)
            return {"status": "success", "data": clientes_lista}, 200
            
        except Exception as e:
            # Captura qualquer erro e retorna um status 500 (Internal Server Error)
            return {"status": "error", "message": f"Erro ao listar clientes: {str(e)}"}, 500

    def inclusaoCliente(self, dados):
        # Validação básica: garante que os campos obrigatórios foram enviados
        if not dados or not dados.get('cnpj_cpf') or not dados.get('razao_social'):
            return {"status": "error", "message": "CNPJ/CPF e Razão Social são obrigatórios."}, 400
        
        try:
            # Chama o model repassando os dados do dicionário (JSON recebido na rota)
            # Usamos o .get() para evitar erro caso o campo não tenha sido enviado (retorna None)
            novo_id = self.cliente_model.cadastrarCliente(
                cnpj_cpf=dados.get('cnpj_cpf'),
                razao_social=dados.get('razao_social'),
                descricao=dados.get('descricao_cliente'),
                responsavel=dados.get('nome_responsavel'),
                email=dados.get('email'),
                contato=dados.get('contato')
            )
            
            # Retorna sucesso e o código HTTP 201 (Created)
            return {"status": "success", "message": "Cliente cadastrado com sucesso", "id": novo_id}, 201
            
        except Exception as e:
            # Se for um erro de Unique Violation (CNPJ duplicado, por exemplo), o except captura aqui
            return {"status": "error", "message": f"Erro ao cadastrar cliente: {str(e)}"}, 500

    def editarCliente(self, id_cliente, dados):
        # Valida se algum dado foi enviado para atualização
        if not dados:
            return {"status": "error", "message": "Nenhum dado fornecido para atualização."}, 400

        try:
            # Chama o model para atualizar apenas os campos permitidos
            sucesso = self.cliente_model.editarCliente(
                id_cliente=id_cliente,
                razao_social=dados.get('razao_social'),
                email=dados.get('email'),
                contato=dados.get('contato')
            )
            
            # O model retorna True se a linha foi afetada, False se o ID não existe
            if sucesso:
                return {"status": "success", "message": "Cliente atualizado com sucesso."}, 200
            else:
                return {"status": "error", "message": "Cliente não encontrado."}, 404
                
        except Exception as e:
            return {"status": "error", "message": f"Erro ao atualizar cliente: {str(e)}"}, 500