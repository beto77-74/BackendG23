from flask import Flask
from os import environ
from dotenv import load_dotenv
from instancias import bd
from flask_migrate import Migrate
from usuarios import usuarios_blueprint
from notas import nota_blueprint
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5, seconds=3)
JWTManager(app)

CORS(app, origins=['http://127.0.0.1:5500'], allow_headers='*',methods=['GET','POST','DELETE'])

jwt = JWTManager(app)
app.register_blueprint(usuarios_blueprint)
app.register_blueprint(nota_blueprint)

bd.init_app(app)

Migrate(app,bd)

@jwt.expired_token_loader
def token_experida(header, payload):
    return {
        'message': 'Token ha expirado, vuelve a iniciar sesion'
    }, 401

@jwt.unauthorized_loader
def token_faltante(argumento):
    print(argumento)
    return {
        'message':'Se necesita un token para realizar este requets'
    }

@app.route('/')
def inicio():
    return {
        'message':'aplicacion esta funcionando correctamente'
    }

if __name__ == '__main__':
    app.run(debug=True)