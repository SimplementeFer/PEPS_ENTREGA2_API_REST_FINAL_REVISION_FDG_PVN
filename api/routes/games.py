from flask import Blueprint, jsonify, request
from models.db import get_db_connection
from funciones_auxiliares import sanitize_input, validar_session_normal  # Importamos la función de validación

games_blueprint = Blueprint('games', __name__)

# Endpoint para obtener todos los juegos
@games_blueprint.route('/', methods=['GET'])
def get_games():
    if not validar_session_normal():
        return jsonify({"error": "Acceso no autorizado"}), 401  # Verificación de sesión

    connection = get_db_connection()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM juegos")
            games = cursor.fetchall()
        connection.close()
        return jsonify(games), 200
    return jsonify({"error": "Error al conectar con la base de datos"}), 500

# Endpoint para obtener un juego específico por su ID
@games_blueprint.route('/<int:game_id>', methods=['GET'])
def get_game(game_id):
    if not validar_session_normal():
        return jsonify({"error": "Acceso no autorizado"}), 401  # Verificación de sesión

    connection = get_db_connection()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM juegos WHERE id = %s", (game_id,))
            game = cursor.fetchone()
        connection.close()

        if game:
            return jsonify(game), 200
        else:
            return jsonify({"error": "Juego no encontrado"}), 404
    return jsonify({"error": "Error al conectar con la base de datos"}), 500

# Endpoint para agregar un nuevo juego
@games_blueprint.route('/', methods=['POST'])
def add_game():
    if not validar_session_normal():
        return jsonify({"error": "Acceso no autorizado"}), 401  # Verificación de sesión

    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    price = data.get('price')

    if not name or not price:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    # Sanitizar la entrada
    name = sanitize_input(name)
    description = sanitize_input(description)
    price = sanitize_input(price)

    connection = get_db_connection()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO juegos (name, description, price) VALUES (%s, %s, %s)",
                (name, description, price)
            )
            connection.commit()
        connection.close()
        return jsonify({"message": "Juego agregado exitosamente"}), 201
    return jsonify({"error": "Error al conectar con la base de datos"}), 500

# Endpoint para actualizar un juego por ID
@games_blueprint.route('/<int:game_id>', methods=['PUT'])
def update_game(game_id):
    if not validar_session_normal():
        return jsonify({"error": "Acceso no autorizado"}), 401  # Verificación de sesión

    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    price = data.get('price')

    if not name or not price:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    # Sanitizar la entrada
    name = sanitize_input(name)
    description = sanitize_input(description)
    price = sanitize_input(price)

    connection = get_db_connection()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE juegos SET name = %s, description = %s, price = %s WHERE id = %s",
                (name, description, price, game_id)
            )
            connection.commit()
        connection.close()
        return jsonify({"message": "Juego actualizado exitosamente"}), 200
    return jsonify({"error": "Error al conectar con la base de datos"}), 500

# Endpoint para eliminar un juego por ID
@games_blueprint.route('/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    if not validar_session_normal():
        return jsonify({"error": "Acceso no autorizado"}), 401  # Verificación de sesión

    connection = get_db_connection()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM juegos WHERE id = %s", (game_id,))
            connection.commit()
        connection.close()
        return jsonify({"message": "Juego eliminado exitosamente"}), 200
    return jsonify({"error": "Error al conectar con la base de datos"}), 500
