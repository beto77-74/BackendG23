from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow.validate import Email, Regexp
from marshmallow import Schema, fields
from modelos import Usuario

class UsuarioSerializer(SQLAlchemyAutoSchema):
    password = auto_field(load_only=True, validate=[Regexp('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@!#$%&*])[A-Za-z0-9@!#$%&*]{8,}$', error='El password no cumple con las condiciones [A-Z][a-z][0-1][caracter especial]')])
    nombre = auto_field()
    correo = auto_field(validate=[Email(error='El correo no cumple con el formato correcto')])
    class Meta:
        model = Usuario


class LoginSerializer(Schema):
    correo = fields.Email(required=True)
    password = fields.String(required=True)
