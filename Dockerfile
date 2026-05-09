# Usa uma imagem oficial do Python, versão "slim" para ser mais leve
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala as dependências do sistema operacional necessárias para o psycopg2
# (Apesar de usarmos o psycopg2-binary, ter a libpq é uma boa prática)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas o arquivo de requirements primeiro (para aproveitar o cache do Docker)
COPY requirements.txt .

# Instala as bibliotecas do Python (sem guardar cache do pip para economizar espaço)
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do código do projeto para o diretório de trabalho
COPY . .

# Expõe a porta 5000, que é a padrão do Flask
EXPOSE 5000

# Define variáveis de ambiente padrão do Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Comando para rodar a aplicação quando o container iniciar
CMD ["flask", "run"]