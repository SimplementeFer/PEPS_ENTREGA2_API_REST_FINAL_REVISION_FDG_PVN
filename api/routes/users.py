from flask import Blueprint, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import get_db_connection
from funciones_auxiliares import sanitize_input, create_session, delete_session  # Importamos la función de sanitización

# Creación del Blueprint para las rutas de usuario
users_blueprint = Blueprint('users', __name__)

# Endpoint para registrar usuarios
@users_blueprint.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validar si los datos necesarios están presentes
    if not username or not password:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    # Sanitizar la entrada
    username = sanitize_input(username)
    password = sanitize_input(password)

    # Conexión a la base de datos
    connection = get_db_connection()
    if connection:
        try:
            # Intentamos insertar el usuario en la base de datos
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO usuarios (username, password) VALUES (%s, %s)",
                    (username, generate_password_hash(password))
                )
                connection.commit()
            connection.close()
            return jsonify({"message": f"Usuario {username} registrado exitosamente"}), 201
        except Exception as e:
            # Si ocurre un error, cerramos la conexión y devolvemos un mensaje de error
            connection.close()
            return jsonify({"error": f"Error al registrar usuario: {e}"}), 500
    return jsonify({"error": "Error al conectar con la base de datos"}), 500


# Endpoint para el login de usuarios
@users_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validar si los datos necesarios están presentes
    if not username or not password:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    # Sanitizar la entrada
    username = sanitize_input(username)
    password = sanitize_input(password)

    # Conexión a la base de datos
    connection = get_db_connection()
    if connection:
        try:
            # Intentamos buscar al usuario en la base de datos
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username))
                user = cursor.fetchone()
            connection.close()

            # Si el usuario existe y las contraseñas coinciden, la autenticación es exitosa
            if user and check_password_hash(user['password'], password):
                app.logger.info("Acceso usuario %s correcto",username)
                create_session(username, user['perfil'])
                return jsonify({"message": "Inicio de sesión exitoso"}), 200

            # Si las credenciales no son válidas, devolvemos un error 401
            return jsonify({"error": "Credenciales inválidas"}), 401
            app.logger.info("Acceso usuario %s incorrecto",username)
        except Exception as e:
            connection.close()
            return jsonify({"error": f"Error al autenticar usuario: {e}"}), 500
    return jsonify({"error": "Error al conectar con la base de datos"}), 500


# Endpoint para cerrar sesión
@users_blueprint.route("/logout", methods=['GET'])
def logout_user():
    try:
        delete_session()  # Elimina todos los datos de la sesión
        ret = {"status": "OK"}
        code = 200
    except Exception as e:
        ret = {"status": "ERROR", "error": str(e)}
        code = 500

    response = make_response(json.dumps(ret), code)
    return response
    