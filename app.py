# app.py

from flask import Flask
from routes import init_routes  # Importa a função do __init__.py da pasta routes

app = Flask(__name__)

# Chama a função que registra todas as rotas de uma vez só
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)