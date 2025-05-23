from flask_restful import Resource, Api
from flask import request, Blueprint
from modelos import Nota
from instancias import bd
from marshmallow.exceptions import ValidationError
from .notas_serializer import NotaSerializer
from flask_jwt_extended import jwt_required, get_jwt_identity

nota_blueprint = Blueprint('nota_bp', __name__)
api = Api(nota_blueprint)

class Notas(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            dataSerializada = NotaSerializer().load(data)
            identificador = get_jwt_identity()
            print(identificador)

            nuevaNota = Nota(usuarioId=identificador, **dataSerializada)
            bd.session.add(nuevaNota)
            bd.session.commit()
            resultado = NotaSerializer().dump(nuevaNota)

            return{
                'message': 'Nota creada exitosamente',
                'content' : resultado
            }, 201
        except ValidationError as error:
            return{
                'message': 'Error al crear la Nota',
                'content' : error.args
            }, 400
        
    @jwt_required()
    def get(self):
        identificador = get_jwt_identity()
        notas = bd.session.query(Nota).filter(Nota.usuarioId == identificador).all()

        resultado = NotaSerializer().dump(notas, many=True) 
        return {
            'content': resultado
        }       
    
class NotaController(Resource):
    @jwt_required()
    def delete(self, id):
        usuarioId = get_jwt_identity()
        notaEncontrada = bd.session.query(Nota).filter(Nota.id == id, Nota.usuarioId == usuarioId ).first()
       
        if not notaEncontrada:
            return {
                'message': 'La nota que intentas elimininar no existe'
            }, 404
        
        bd.session.query(Nota).filter(Nota.id == notaEncontrada.id).delete()
        bd.session.commit()
        
        return {
                'message': 'Nota eliminada exitosamente'
        }

        
api.add_resource(Notas,'/notas')
api.add_resource(NotaController,'/notas/<int:id>')