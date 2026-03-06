# Usa uma imagem oficial leve do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala o pipenv
RUN pip install pipenv

# Copia os arquivos do seu backend para o container
COPY . /app/

# Instala as dependências DIRETAMENTE no sistema do container (--system)
RUN if [ -f "Pipfile" ]; then pipenv install --system; fi