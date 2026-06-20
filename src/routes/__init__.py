# routes/__init__.py


# Importa os blueprints de cada arquivo de rotas
from .cliente_routes import cliente_bp
from .usuario_routes import usuario_bp
from .tamanho_routes import tamanho_bp
from .fase_routes import fase_bp
from .roteiro_routes import roteiro_bp
from .roteiro_fase_routes import roteiro_fase_bp
from .op_routes import op_bp
def init_routes(app):
    """
    Função responsável por registrar todos os Blueprints na aplicação Flask.
    Dessa forma, o app.py principal fica muito mais limpo.
    """
    # O url_prefix='/api' faz com que todas as rotas de cliente comecem com /api/clientes
    app.register_blueprint(cliente_bp, url_prefix='/api')
    
    # Futuros registros:
    app.register_blueprint(usuario_bp, url_prefix='/api')
    app.register_blueprint(tamanho_bp, url_prefix='/api')
    app.register_blueprint(roteiro_bp, url_prefix='/api')
    app.register_blueprint(fase_bp, url_prefix='/api')
    app.register_blueprint(roteiro_fase_bp, url_prefix='/api')
    app.register_blueprint(op_bp, url_prefix='/api')

    # app.register_blueprint(fase_bp, url_prefix='/api')
    # app.register_blueprint(roteiro_bp, url_prefix='/api')