# routes/roteiro_routes.py

import os
from functools import wraps
from flask import Blueprint, request, jsonify
from src.services.roteiro_service import ServiceRoteiroPadrao

# Criando o Blueprint para Roteiros
roteiro_bp = Blueprint('roteiro_bp', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_header = request.headers.get('Authorization')
        env_token = os.getenv('API_TOKEN')

        if not token_header:
            return jsonify({'error': 'Token de autenticação ausente!'}), 401

        if token_header.startswith("Bearer "):
            token = token_header.split(" ")[1]
        else:
            token = token_header

        if token != env_token:
            return jsonify({'error': 'Token inválido!'}), 403

        return f(*args, **kwargs)

    return decorated


@roteiro_bp.route('/roteiros', methods=['GET'])
@token_required
def getRoteiros():
    service = ServiceRoteiroPadrao()
    response, status_code = service.listaRoteiros()
    
    return jsonify(response), status_code


@roteiro_bp.route('/roteiros', methods=['POST'])
@token_required
def post_novoRoteiro():
    dados = request.get_json()

    service = ServiceRoteiroPadrao()
    response, status_code = service.inclusaoRoteiro(dados)

    return jsonify(response), status_code


@roteiro_bp.route('/roteiros/<int:cod_roteiro>', methods=['PUT'])
@token_required
def put_editarRoteiro(cod_roteiro):
    dados = request.get_json()

    service = ServiceRoteiroPadrao()
    response, status_code = service.editarRoteiro(cod_roteiro, dados)

    return jsonify(response), status_code


@roteiro_bp.route('/roteiros/<int:cod_roteiro>', methods=['DELETE'])
@token_required
def delete_excluirRoteiro(cod_roteiro):
    service = ServiceRoteiroPadrao()
    response, status_code = service.excluirRoteiro(cod_roteiro)

    return jsonify(response), status_code