# routes/roteiro_routes.py

import os
from functools import wraps
from flask import Blueprint, request, jsonify
from src.services.roteiro_service import ServiceRoteiroPadrao

# Criando o Blueprint para Roteiros
roteiro_bp = Blueprint('roteiro_bp', __name__)

# 1. Instanciamos o service uma única vez para reaproveitar
roteiro_service = ServiceRoteiroPadrao()

# 2. Carregamos o token uma única vez na inicialização do módulo
API_TOKEN = os.getenv('API_TOKEN')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_header = request.headers.get('Authorization')

        if not token_header:
            return jsonify({'error': 'Token de autenticação ausente!'}), 401

        # Lida com ou sem o prefixo "Bearer "
        if token_header.startswith("Bearer "):
            token = token_header.split(" ")[1]
        else:
            token = token_header

        if token != API_TOKEN:
            return jsonify({'error': 'Token inválido!'}), 403

        return f(*args, **kwargs)

    return decorated


@roteiro_bp.route('/roteiros', methods=['GET'])
@token_required
def get_roteiros():
    response, status_code = roteiro_service.listaRoteiros()
    return jsonify(response), status_code


@roteiro_bp.route('/roteiros', methods=['POST'])
@token_required
def post_novo_roteiro():
    # 3. silent=True evita que o Flask quebre a API se não vier um JSON válido
    dados = request.get_json(silent=True) or {}

    response, status_code = roteiro_service.inclusaoRoteiro(dados)
    return jsonify(response), status_code


@roteiro_bp.route('/roteiros/<int:cod_roteiro>', methods=['PUT'])
@token_required
def put_editar_roteiro(cod_roteiro):
    dados = request.get_json(silent=True) or {}

    response, status_code = roteiro_service.editarRoteiro(cod_roteiro, dados)
    return jsonify(response), status_code


@roteiro_bp.route('/roteiros/<int:cod_roteiro>', methods=['DELETE'])
@token_required
def delete_excluir_roteiro(cod_roteiro):
    response, status_code = roteiro_service.excluirRoteiro(cod_roteiro)
    return jsonify(response), status_code