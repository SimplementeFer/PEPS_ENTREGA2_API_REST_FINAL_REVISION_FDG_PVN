# Imagen base
FROM python:3.9-slim

# Instalar dependencias necesarias para compilar mysqlclient
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*  

# Establecer el directorio de trabajo
WORKDIR /proyecto_python

# Copiar el archivo de requerimientos
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código fuente del proyecto
COPY . .

# Exponer el puerto 5000
EXPOSE 5000

# Ejecutar el archivo app.py directamente
CMD ["python", "app.py"]
