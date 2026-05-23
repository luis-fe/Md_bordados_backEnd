# routes/usuario_routes.py

import os
from functools import wraps
from flask import Blueprint, request, jsonify
from src.services.usuario_service import ServiceUsuario

# Criando o Blueprint para Usuários
usuario_bp = Blueprint('usuario_bp', __name__)

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


@usuario_bp.route('/usuarios', methods=['GET'])
@token_required
def getUsuario():
    # Instancia o service
    service = ServiceUsuario()

    # Chama o método que devolve o dicionário e o código HTTP
    response, status_code = service.listaUsuarios()

    # Retorna o JSON para o front-end
    return jsonify(response), status_code


@usuario_bp.route('/usuarios', methods=['POST'])
@token_required
def post_novoUsuario():
    # Captura o JSON enviado no corpo da requisição
    dados = request.get_json()

    service = ServiceUsuario()
    response, status_code = service.inclusaoUsuario(dados)

    return jsonify(response), status_code


# Usei <int:id_usuario> assumindo que seu cod_usuario no banco seja um número inteiro (serial).
# Se for UUID/Varchar, mude para <string:id_usuario> como estava no cliente.
@usuario_bp.route('/usuarios/<int:id_usuario>', methods=['PUT'])
@token_required
def put_editarUsuario(id_usuario):
    # O id_usuario vem da URL e os dados do corpo (JSON)
    dados = request.get_json()

    service = ServiceUsuario()
    response, status_code = service.editarUsuario(id_usuario, dados)

    return jsonify(response), status_code