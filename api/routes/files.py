import os
from flask import Blueprint, jsonify, request

# Definir el Blueprint para archivos
files_blueprint = Blueprint('files', __name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Endpoint para subir un archivo
@files_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "Archivo no proporcionado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return jsonify({"message": f"Archivo {file.filename} subido con éxito"}), 201

# Endpoint para visualizar el contenido de un archivo
@files_blueprint.route('/view/<filename>', methods=['GET'])
def view_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": f"Archivo {filename} no encontrado"}), 404

    with open(filepath, 'r') as file:
        content = file.read()
    return jsonify({"filename": filename, "content": content}), 200
