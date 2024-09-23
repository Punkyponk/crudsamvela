import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://samvela:2SeoGMqxUjLbo2eZT3xpF7nqJQwrdiDT@dpg-crjk96dumphs73d1nt3g-a/samvela'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de la base de datos
class Estudiante(db.Model):
    __tablename__ = 'alumnos'
    __table_args__ = {'schema': 'public'}
    no_control = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String)
    ap_paterno = db.Column(db.String)
    ap_materno = db.Column(db.String)
    semestre = db.Column(db.Integer)

    def to_dict(self):
        return {
            'no_control': self.no_control,
            'nombre': self.nombre,
            'ap_paterno': self.ap_paterno,
            'ap_materno': self.ap_materno,
            'semestre': self.semestre
        }

# Obtener todos los estudiantes
@app.route('/api/alumnos', methods=['GET'])
def get_alumnos():
    alumnos = Estudiante.query.all()
    return jsonify([alumno.to_dict() for alumno in alumnos])

# Obtener un estudiante por no_control
@app.route('/api/alumnos/<string:no_control>', methods=['GET'])
def get_estudiante(no_control):
    estudiante = Estudiante.query.get(no_control)
    if estudiante:
        return jsonify(estudiante.to_dict())
    return jsonify({'message': 'Estudiante no encontrado'}), 404

# Crear un nuevo estudiante
@app.route('/api/alumnos', methods=['POST'])
def create_estudiante():
    data = request.get_json()
    nuevo_estudiante = Estudiante(
        no_control=data['no_control'],
        nombre=data['nombre'],
        ap_paterno=data['ap_paterno'],
        ap_materno=data['ap_materno'],
        semestre=data['semestre']
    )
    db.session.add(nuevo_estudiante)
    db.session.commit()
    return jsonify(nuevo_estudiante.to_dict()), 201

# Actualizar un estudiante
@app.route('/api/alumnos/<string:no_control>', methods=['PUT'])
def update_estudiante(no_control):
    data = request.get_json()
    estudiante = Estudiante.query.get(no_control)
    if estudiante:
        estudiante.nombre = data['nombre']
        estudiante.ap_paterno = data['ap_paterno']
        estudiante.ap_materno = data['ap_materno']
        estudiante.semestre = data['semestre']
        db.session.commit()
        return jsonify(estudiante.to_dict())
    return jsonify({'message': 'Estudiante no encontrado'}), 404

# Eliminar un estudiante
@app.route('/api/alumnos/<string:no_control>', methods=['DELETE'])
def delete_estudiante(no_control):
    estudiante = Estudiante.query.get(no_control)
    if estudiante:
        db.session.delete(estudiante)
        db.session.commit()
        return jsonify({'message': 'Estudiante eliminado'}), 200
    return jsonify({'message': 'Estudiante no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
