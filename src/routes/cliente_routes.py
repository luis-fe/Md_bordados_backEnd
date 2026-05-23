# routes/cliente_routes.py

import os
from functools import wraps
from flask import Blueprint, request, jsonify
from src.services.cliente_service import ServiceCliente

# Criando o Blueprint para Clientes
cliente_bp = Blueprint('cliente_bp', __name__)


def token_required(f):
    """
    Decorator para proteger as rotas exigindo um token no Header da requisição.
    O token esperado deve estar definido na variável de ambiente 'API_TOKEN'.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        # Captura o token enviado no header (ex: Authorization: Bearer <seu_token>)
        token_header = request.headers.get('Authorization')

        # Pega o token verdadeiro da variável de ambiente
        # Certifique-se de ter um arquivo .env ou a variável exportada no seu SO
        env_token = os.getenv('API_TOKEN')

        if not token_header:
            return jsonify({'error': 'Token de autenticação ausente!'}), 401

        # Se você estiver usando o padrão "Bearer meu-token-123"
        # Precisamos remover a palavra "Bearer " para comparar apenas o token
        if token_header.startswith("Bearer "):
            token = token_header.split(" ")[1]
        else:
            token = token_header

        # Compara o token enviado com o token do ambiente
        if token != env_token:
            return jsonify({'error': 'Token inválido!'}), 403

        # Se passar na verificação, executa a rota normalmente
        return f(*args, **kwargs)

    return decorated


@cliente_bp.route('/clientes', methods=['GET'])
@token_required  # <--- Adicionando a proteção aqui
def getCliente():
    # Instancia o service (não precisa mais passar a conexão)
    service = ServiceCliente()

    # Chama o método que já devolve o dicionário e o código HTTP (ex: 200, 500)
    response, status_code = service.listaClientes()

    # Retorna o JSON pronto para o front-end
    return jsonify(response), status_code


@cliente_bp.route('/clientes', methods=['POST'])
@token_required  # <--- Adicionando a proteção aqui
def post_novoCliente():
    # Captura o JSON enviado no corpo da requisição (front-end -> back-end)
    dados = request.get_json()

    service = ServiceCliente()
    response, status_code = service.inclusaoCliente(dados)

    return jsonify(response), status_code


@cliente_bp.route('/clientes/<string:id_cliente>', methods=['PUT'])
@token_required  # <--- Adicionando a proteção aqui
def put_editarCliente(id_cliente):
    # O id_cliente vem da URL. Os dados a serem atualizados vêm do corpo (JSON)
    dados = request.get_json()

    service = ServiceCliente()
    response, status_code = service.editarCliente(id_cliente, dados)

    return jsonify(response), status_code