import os
from flask import Flask, jsonify, request
from routes.games import games_blueprint
from routes.users import users_blueprint
from routes.files import files_blueprint
from funciones_auxiliares import prepare_response_extra_headers 
import settings  # Importamos el archivo settings.py
from logging.config import dictConfig

# Asegurarse de que el directorio de logs exista
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configuración de la cabecera
extra_headers = prepare_response_extra_headers(True)

# Configuración inicial del proyecto
app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Configuración de la sesión con cookies http
app.config.update(
    PERMANENT_SESSION_LIFETIME=600,  # Tiempo de vida de la sesión en segundos
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',  # Lax puede ser sustituido por 'Strict' si necesitas más seguridad
)

# Registro de rutas
def register_routes(app):
    app.register_blueprint(games_blueprint, url_prefix="/api/games")
    app.register_blueprint(users_blueprint, url_prefix="/api/users")
    app.register_blueprint(files_blueprint, url_prefix="/files")

# Registro de rutas en la instancia principal
register_routes(app)

print("Rutas registradas:", app.url_map)

# Configuración de los logs
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "logs/flask.log",
                "formatter": "default",
            },
            "time-rotate": {
               "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": "logs/flask.log",
                "when": "D",
                "interval": 10,
                "backupCount": 5,
                "formatter": "default",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console", "time-rotate"]},
    }
)

@app.after_request
def afterRequest(response):
    response.headers['Server'] = 'API'
    app.logger.info(
        "path: %s | method: %s | status: %s | size: %s >>> %s",
        request.path,
        request.method,
        response.status,
        response.content_length if response.content_length else 'N/A',
        request.remote_addr,
    )
    response.headers.extend(extra_headers)
    return response

# Punto de entrada de la aplicación
if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT, debug=False)
