# routes/tamanho_routes.py

import os
from functools import wraps
from flask import Blueprint, request, jsonify
from src.services.tamanho_service import ServiceTamanho

# Criando o Blueprint para Tamanhos
tamanho_bp = Blueprint('tamanho_bp', __name__)

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
        env_token = os.getenv('API_TOKEN')

        if not token_header:
            return jsonify({'error': 'Token de autenticação ausente!'}), 401

        # Remove a palavra "Bearer " para comparar apenas o token
        if token_header.startswith("Bearer "):
            token = token_header.split(" ")[1]
        else:
            token = token_header

        # Compara o token enviado com o token do ambiente
        if token != env_token:
            return jsonify({'error': 'Token inválido!'}), 403

        return f(*args, **kwargs)

    return decorated


@tamanho_bp.route('/tamanhos', methods=['GET'])
@token_required
def getTamanhos():
    service = ServiceTamanho()
    response, status_code = service.listaTamanhos()
    
    return jsonify(response), status_code


@tamanho_bp.route('/tamanhos', methods=['POST'])
@token_required
def post_novoTamanho():
    dados = request.get_json()

    service = ServiceTamanho()
    response, status_code = service.inclusaoTamanho(dados)

    return jsonify(response), status_code


# Aqui usamos <string:cod_tamanho> pois a chave primária no banco é VARCHAR(10)
@tamanho_bp.route('/tamanhos/<string:cod_tamanho>', methods=['PUT'])
@token_required
def put_editarTamanho(cod_tamanho):
    dados = request.get_json()

    service = ServiceTamanho()
    response, status_code = service.editarTamanho(cod_tamanho, dados)

    return jsonify(response), status_code


@tamanho_bp.route('/tamanhos/<string:cod_tamanho>', methods=['DELETE'])
@token_required
def delete_excluirTamanho(cod_tamanho):
    service = ServiceTamanho()
    response, status_code = service.excluirTamanho(cod_tamanho)

    return jsonify(response), status_code