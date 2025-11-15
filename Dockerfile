FROM python:3.13.5-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copia requirements primeiro
COPY requirements.txt /app/

# Dependências mínimas (remover se não precisar compilar nada)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia código
COPY . /app/

# Diretórios necessários
RUN mkdir -p /app/uploads /app/data

# Expor portas usadas pelos serviços Gradio
EXPOSE 7860 7861

ENV GRADIO_SERVER_NAME="0.0.0.0"

# Comando padrão (docker-compose sobrescreve quando necessário)
CMD ["python", "chat_gradio.py"]