# Usa uma imagem oficial e leve do Node.js (versão 20 LTS)
FROM node:20-alpine

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependências primeiro (otimiza o cache do Docker)
COPY package.json package-lock.json* ./

# Instala as dependências do projeto
RUN npm install

# Copia o restante do código do frontend
COPY . .

# Expõe a porta padrão do Vite
EXPOSE 5173

# Inicia o Vite e força ele a expor a rede para fora do container (--host)
CMD ["npm", "run", "dev", "--", "--host"]