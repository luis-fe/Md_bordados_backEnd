# routes/op_routes.py

import os
from functools import wraps
from flask import Blueprint, request, jsonify
from src.services.op_service import ServiceOrdemProducao

# Criando o Blueprint para Ordem de Producao (OP)
op_bp = Blueprint('op_bp', __name__)


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


@op_bp.route('/ops', methods=['GET'])
@token_required
def getOps():
    service = ServiceOrdemProducao()
    response, status_code = service.listaOPs()

    return jsonify(response), status_code


@op_bp.route('/ops/<string:cod_op>', methods=['GET'])
@token_required
def getOpPorId(cod_op):
    service = ServiceOrdemProducao()
    response, status_code = service.buscaOP(cod_op)

    return jsonify(response), status_code


@op_bp.route('/ops', methods=['POST'])
@token_required
def post_novaOp():
    dados = request.get_json()

    service = ServiceOrdemProducao()
    response, status_code = service.inclusaoOP(dados)

    return jsonify(response)


@op_bp.route('/ops/<string:cod_op>', methods=['PUT'])
@token_required
def put_editarOp(cod_op):
    dados = request.get_json()

    service = ServiceOrdemProducao()
    response, status_code = service.editarOP(cod_op, dados)

    return jsonify(response), status_code


@op_bp.route('/ops/<string:cod_op>', methods=['DELETE'])
@token_required
def delete_excluirOp(cod_op):
    service = ServiceOrdemProducao()
    response, status_code = service.excluirOP(cod_op)

    return jsonify(response), status_code