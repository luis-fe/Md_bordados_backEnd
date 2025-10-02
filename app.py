from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from src.routes import routes_blueprint
app = Flask(__name__)
port = int(os.environ.get('PORT', 8080))

app.register_blueprint(routes_blueprint)
#Aqui registo todas as rotas , url's DO PROJETO, para acessar bastar ir na pasta "routes",
#duvidas o contato (62)99351-42-49 ou acessar a documentacao do projeto em:

CORS(app)

# Decorator para verificar o token fixo



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)