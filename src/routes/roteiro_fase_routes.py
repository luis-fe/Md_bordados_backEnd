# routes/roteiro_fase_routes.py

import os
from functools import wraps
from flask import Blueprint, request, jsonify
from src.services.roteiro_fase_service import ServiceRoteiroFase

# Criando o Blueprint para as Fases do Roteiro
roteiro_fase_bp = Blueprint('roteiro_fase_bp', __name__)


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


@roteiro_fase_bp.route('/roteiros/<int:cod_roteiro>/fases', methods=['GET'])
@token_required
def getFasesDoRoteiro(cod_roteiro):
    service = ServiceRoteiroFase()
    response, status_code = service.listaFasesRoteiro(cod_roteiro)

    return jsonify(response), status_code


@roteiro_fase_bp.route('/roteiros/fases', methods=['POST'])
@token_required
def post_novaFaseNoRoteiro():
    dados = request.get_json()

    service = ServiceRoteiroFase()
    response, status_code = service.inclusaoRoteiroFase(dados)

    return jsonify(response), status_code


@roteiro_fase_bp.route('/roteiros/<int:cod_roteiro>/fases/<int:cod_fase>', methods=['PUT'])
@token_required
def put_editarFaseDoRoteiro(cod_roteiro, cod_fase):
    dados = request.get_json()

    service = ServiceRoteiroFase()
    response, status_code = service.editarRoteiroFase(cod_roteiro, cod_fase, dados)

    return jsonify(response), status_code


@roteiro_fase_bp.route('/roteiros/<int:cod_roteiro>/fases/<int:cod_fase>', methods=['DELETE'])
@token_required
def delete_excluirFaseDoRoteiro(cod_roteiro, cod_fase):
    service = ServiceRoteiroFase()
    response, status_code = service.excluirRoteiroFase(cod_roteiro, cod_fase)

    return jsonify(response), status_code