import os

DEBUG = False  # En producción, debe ser False

# Secretos y claves de seguridad
SECRET_KEY = os.environ.get("SECRET_KEY", "my_secret_key")  # Valor por defecto en caso de no estar en el entorno
WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY", "csrf_secret_key")

# Configuración del servidor
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 5000)) 
# Configuración de la base de datos
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = int(os.environ.get("DB_PORT", 3306))
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "example")
DB_NAME = os.environ.get("DB_NAME", "reviews_db")
