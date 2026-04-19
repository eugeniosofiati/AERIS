FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

# Instala apenas as bibliotecas de desenvolvimento necessárias
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia os binários oficiais do seu Host (srvlinux) para o Container
# Isso garante que a versão do dump seja IGUAL à do seu servidor
COPY ./bin_host/mysqldump /usr/bin/mysqldump
COPY ./bin_host/mysql /usr/bin/mysql

# Copia as bibliotecas que o mysql/mysqldump do Ubuntu Jammy exige
# (Mapeamento focado apenas no necessário para o binário rodar)

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["tail", "-f", "/dev/null"]
