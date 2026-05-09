# app.py

from flask import Flask
from src.routes import init_routes  # <-- Sem o ponto inicial!

app = Flask(__name__)

# Chama a função que registra todas as rotas de uma vez só
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') # O host='0.0.0.0' é importante para o Docker!