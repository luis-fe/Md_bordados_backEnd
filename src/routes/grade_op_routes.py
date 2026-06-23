# routes/grade_op_routes.py

import os
from functools import wraps
from flask import Blueprint, request, jsonify
from src.services.grade_op_service import ServiceGradeOp

# Criando o Blueprint para a Grade da OP
grade_op_bp = Blueprint('grade_op_bp', __name__)


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


@grade_op_bp.route('/ops/<string:cod_op>/grade', methods=['GET'])
@token_required
def getGradeDaOP(cod_op):
    service = ServiceGradeOp()
    response, status_code = service.listaGradeDaOP(cod_op)
    return jsonify(response), status_code


@grade_op_bp.route('/ops/grade', methods=['POST'])
@token_required
def post_novaLinhaGrade():
    dados = request.get_json()
    service = ServiceGradeOp()
    response, status_code = service.inclusaoGradeOp(dados)
    return jsonify(response)


@grade_op_bp.route('/ops/<string:cod_op>/grade/<string:cod_tamanho>/<string:cor>', methods=['PUT'])
@token_required
def put_editarLinhaGrade(cod_op, cod_tamanho, cor):
    dados = request.get_json()
    service = ServiceGradeOp()
    response, status_code = service.editarGradeOp(cod_op, cod_tamanho, cor, dados)
    return jsonify(response), status_code


@grade_op_bp.route('/ops/<string:cod_op>/grade/<string:cod_tamanho>/<string:cor>', methods=['DELETE'])
@token_required
def delete_excluirLinhaGrade(cod_op, cod_tamanho, cor):
    service = ServiceGradeOp()
    response, status_code = service.excluirLinhaGrade(cod_op, cod_tamanho, cor)
    return jsonify(response), status_code