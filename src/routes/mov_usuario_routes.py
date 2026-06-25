import os
from functools import wraps
from flask import Blueprint, request, jsonify
from src.services.mov_usuario_service import ServiceMovUsuario

# Criando o Blueprint para Movimentação de Usuários
mov_usuario_bp = Blueprint('mov_usuario_bp', __name__)

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


@mov_usuario_bp.route('/mov-usuarios', methods=['GET'])
@token_required
def getMovUsuarios():
    service = ServiceMovUsuario()
    response, status_code = service.listaMovUsuarios()
    
    return jsonify(response), status_code


@mov_usuario_bp.route('/mov-usuarios', methods=['POST'])
@token_required
def post_novaMovUsuario():
    dados = request.get_json()

    service = ServiceMovUsuario()
    response, status_code = service.inclusaoMovUsuario(dados)

    return jsonify(response), status_code


@mov_usuario_bp.route('/mov-usuarios/<int:cod_mov_usuario>', methods=['PUT'])
@token_required
def put_editarMovUsuario(cod_mov_usuario):
    dados = request.get_json()

    service = ServiceMovUsuario()
    response, status_code = service.editarMovUsuario(cod_mov_usuario, dados)

    return jsonify(response), status_code


@mov_usuario_bp.route('/mov-usuarios/<int:cod_mov_usuario>', methods=['DELETE'])
@token_required
def delete_excluirMovUsuario(cod_mov_usuario):
    service = ServiceMovUsuario()
    response, status_code = service.excluirMovUsuario(cod_mov_usuario)

    return jsonify(response), status_code