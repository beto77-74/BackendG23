from flask_restful import Resource, Api
from flask import Blueprint
from instancias import bd
from modelos import Usuario
from flask import request
from .usuarios_serializer import UsuarioSerializer,LoginSerializer
from marshmallow.exceptions import ValidationError
from bcrypt import gensalt, hashpw, checkpw
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token

usuarios_blueprint = Blueprint('usuarios_bp',__name__)
api = Api(usuarios_blueprint)

class Registro(Resource):
    def post(self):
        data = request.get_json()
        try:
            dataSerializada = UsuarioSerializer().load(data)
            
            salt = gensalt()
            password = bytes(dataSerializada.get('password'),'utf-8')
            hashedPassword = hashpw(password,salt)
            print(hashedPassword)
            nuevaPassword = hashedPassword.decode('utf-8')
            dataSerializada['password']=nuevaPassword
            
            nuevoUsuario = Usuario(**dataSerializada)
            bd.session.add(nuevoUsuario)
            bd.session.commit()

            return {
                'message':'Usuario creado correctamente'
            }, 201

        except ValidationError as error:
            return {
                'message':'Error al crear el usuario',
                'content':error.args
            }, 400
        except IntegrityError as error:
             return {
                'message':'Error al crear el usuario',
                'message':'Usuario con el correo ya existe'
             }, 400

        
class Login(Resource):
    def post(self):
        data = request.get_json()
        try:
            dataValidada =  LoginSerializer().load(data)
            usuarioEncontrado = bd.session.query(Usuario).with_entities(Usuario.password,Usuario.id).filter(
                Usuario.correo == dataValidada.get('correo')).first()
            
            if not usuarioEncontrado:
                return {
                    'message':'Usuario no existe',
                }, 404
            
            print(usuarioEncontrado)
            passwordEncontrada = bytes(usuarioEncontrado[0],'utf-8')
            passwordEntrante = bytes(dataValidada.get('password'),'utf-8')

            validacionPassword = checkpw(passwordEntrante,passwordEncontrada)
            if validacionPassword == True:
                usuarioId = str(usuarioEncontrado[1])
                token = create_access_token(identity=usuarioId, additional_claims={
                    'tipoUsuario':'SUPERUSUARIO'
                })
                return {
                    'message':'Bienvenido',
                    'content': token
                }
            else:
                return {
                    'message':'Credenciales incorrectas',
                }, 403
            
        except ValidationError as error:
            return {
                'message':'Error al hacer el login',
                'content': error.args
         }
    
api.add_resource(Registro,'/registro')
api.add_resource(Login,'/login')