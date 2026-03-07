# Usa uma imagem oficial leve do Python baseada em Debian
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala o gerenciador de pacotes
RUN pip install pipenv

# [BOA PRÁTICA] Copia APENAS os arquivos de dependência primeiro.
# Isso garante que o Docker use o cache e não reinstale tudo a cada mudança no código.
COPY Pipfile Pipfile.lock* ./

# Instala as dependências diretamente no sistema do container (--system)
RUN if [ -f "Pipfile" ]; then pipenv install --system --skip-lock; fi

# [BOA PRÁTICA] Copia o restante do código apenas no final
COPY . /app/