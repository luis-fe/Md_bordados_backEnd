# routes/cliente_routes.py

from flask import Blueprint, request, jsonify
from services.cliente_service import ServiceCliente

# Criando o Blueprint para Clientes
cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/clientes', methods=['GET'])
def getCliente():
    # Instancia o service (não precisa mais passar a conexão)
    service = ServiceCliente()
    
    # Chama o método que já devolve o dicionário e o código HTTP (ex: 200, 500)
    response, status_code = service.listaClientes()
    
    # Retorna o JSON pronto para o front-end
    return jsonify(response), status_code


@cliente_bp.route('/clientes', methods=['POST'])
def post_novoCliente():
    # Captura o JSON enviado no corpo da requisição (front-end -> back-end)
    dados = request.get_json()
    
    service = ServiceCliente()
    response, status_code = service.inclusaoCliente(dados)
    
    return jsonify(response), status_code


@cliente_bp.route('/clientes/<string:id_cliente>', methods=['PUT'])
def put_editarCliente(id_cliente):
    # O id_cliente vem da URL. Os dados a serem atualizados vêm do corpo (JSON)
    dados = request.get_json()
    
    service = ServiceCliente()
    response, status_code = service.editarCliente(id_cliente, dados)
    
    return jsonify(response), status_code