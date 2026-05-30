# routes/fase_routes.py

import os
from functools import wraps
from flask import Blueprint, request, jsonify
from src.services.fase_service import ServiceFase

# Criando o Blueprint para Fases
fase_bp = Blueprint('fase_bp', __name__)

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


@fase_bp.route('/fases', methods=['GET'])
@token_required
def getFases():
    service = ServiceFase()
    response, status_code = service.listaFases()
    
    return jsonify(response), status_code


@fase_bp.route('/fases', methods=['POST'])
@token_required
def post_novaFase():
    dados = request.get_json()

    service = ServiceFase()
    response, status_code = service.inclusaoFase(dados)

    return jsonify(response), status_code


# Chave primária é um inteiro (SERIAL)
@fase_bp.route('/fases/<int:cod_fase>', methods=['PUT'])
@token_required
def put_editarFase(cod_fase):
    dados = request.get_json()

    service = ServiceFase()
    response, status_code = service.editarFase(cod_fase, dados)

    return jsonify(response), status_code


@fase_bp.route('/fases/<int:cod_fase>', methods=['DELETE'])
@token_required
def delete_excluirFase(cod_fase):
    service = ServiceFase()
    response, status_code = service.excluirFase(cod_fase)

    return jsonify(response), status_code