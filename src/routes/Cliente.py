from flask import Blueprint, jsonify, request
from functools import wraps
from src.models import Cliente
cliente_routes = Blueprint('cliente_routes', __name__) # Esse é o nome atribuido para o conjunto de rotas envolvendo usuario



def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token == 'Easy445277888':  # Verifica se o token é igual ao token fixo
            return f(*args, **kwargs)
        return jsonify({'message': 'Acesso negado'}), 401

    return decorated_function

@cliente_routes.route('/api/md_bordados/Clientes', methods=['GET'])
@token_required
def Clientes_jonh_field():
    consulta = Cliente.Cliente()
    consulta = consulta.get_clientes()

    # Obtém os nomes das colunas
    column_names = consulta.columns
    # Monta o dicionário com os cabeçalhos das colunas e os valores correspondentes
    consulta_data = []
    for index, row in consulta.iterrows():
        consulta_dict = {}
        for column_name in column_names:
            consulta_dict[column_name] = row[column_name]
        consulta_data.append(consulta_dict)
    return jsonify(consulta_data)


@cliente_routes.route('/api/md_bordados/NovoCliente', methods=['POST'])
@token_required
def NovoCliente():
    data = request.get_json()
    codCliente = data.get('codCliente')
    nomeCliente = data.get('nomeCliente', '-')
    cnpj_cpf =  data.get('cnpj_cpf', '-')
    situacao = data.get('situacao', '-')

    cliente = Cliente.Cliente(codCliente,nomeCliente,cnpj_cpf, situacao)
    consulta = cliente.post_cliente()

    # Obtém os nomes das colunas
    column_names = consulta.columns
    # Monta o dicionário com os cabeçalhos das colunas e os valores correspondentes
    consulta_data = []
    for index, row in consulta.iterrows():
        consulta_dict = {}
        for column_name in column_names:
            consulta_dict[column_name] = row[column_name]
        consulta_data.append(consulta_dict)
    return jsonify(consulta_data)


@cliente_routes.route('/api/md_bordados/AlterarCliente', methods=['PUT'])
@token_required
def AlterarCliente():
    data = request.get_json()
    codCliente = data.get('codCliente')
    nomeCliente = data.get('nomeCliente', '-')
    cnpj_cpf =  data.get('cnpj_cpf', '-')
    situacao = data.get('situacao', '-')

    cliente = Cliente.Cliente(codCliente,nomeCliente,cnpj_cpf, situacao)
    consulta = cliente.put_cliente()

    # Obtém os nomes das colunas
    column_names = consulta.columns
    # Monta o dicionário com os cabeçalhos das colunas e os valores correspondentes
    consulta_data = []
    for index, row in consulta.iterrows():
        consulta_dict = {}
        for column_name in column_names:
            consulta_dict[column_name] = row[column_name]
        consulta_data.append(consulta_dict)
    return jsonify(consulta_data)


@cliente_routes.route('/api/md_bordados/ExcluirCliente', methods=['PUT'])
@token_required
def ExcluirCliente():
    data = request.get_json()
    codCliente = data.get('codCliente')

    cliente = Cliente.Cliente(codCliente)
    consulta = cliente.delete_cliente_especifico()

    # Obtém os nomes das colunas
    column_names = consulta.columns
    # Monta o dicionário com os cabeçalhos das colunas e os valores correspondentes
    consulta_data = []
    for index, row in consulta.iterrows():
        consulta_dict = {}
        for column_name in column_names:
            consulta_dict[column_name] = row[column_name]
        consulta_data.append(consulta_dict)
    return jsonify(consulta_data)



