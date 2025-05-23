from flask import Flask
from faker import Faker
from instancias import conexionBD
from modelos import Usuario, TipoUsuario
from bcrypt import gensalt, hashpw
from pytest_mock import MockerFixture

faker = Faker()


def test_crear_usuario_correo_incorrecto(client: Flask):
    """
    Verifica que al pasar un correo invalido no permita la insercion
    """

    body = {
        'nombre': faker.name(),
        'correo': 'correo.com',
        'password': faker.password(
            length=9,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True),
        'tipoUsuario': 'ADMIN'
    }

    res = client.post('/registro', json=body)
    data = res.get_json()

    assert res.status_code == 400
    assert data['message'] == 'Error al registrar el usuario'
    # cuando tenemos un error de los serializadores estos retorna una lista y en la primera posicion tendremos el error del correo
    # {'content': [{'correo': ['Not a valid email address.']}] }
    assert data['content'][0]['correo'][0] == 'Correo invalido.'


# Hacer un test en el cual se valide cuando la contraseña no cumple los estandares
def test_crear_usuario_password_incorrecto(client: Flask):
    """
    Verifica que al pasar una password invalida no permita la insercion
    """

    body = {
        'nombre': faker.name(),
        'correo': faker.email(),
        'password': faker.password(
            length=5,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True),
        'tipoUsuario': 'ADMIN'
    }

    res = client.post('/registro', json=body)
    data = res.get_json()

    assert res.status_code == 400
    assert data['message'] == 'Error al registrar el usuario'
    assert data['content'][0]['password'][0] == 'El password debe tener al menos una mayus, una minus, un numero y un caracter especial y no menor a 8 caracteres'


# Hacer un test en el cual se valide cuando la informacion es correcta
def test_crear_usuario(client: Flask, mocker: MockerFixture):
    """
    Verifica que al pasar una password invalida no permita la insercion
    """
    mockerEnviarCorreo = mocker.patch('usuarios.usuarios_controller.enviar_correo')

    body = {
        'nombre': faker.name(),
        'correo': faker.email(),
        'password': faker.password(
            length=10,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True),
        'tipoUsuario': 'ADMIN'
    }

    res = client.post('/registro', json=body)
    data = res.get_json()

    assert res.status_code == 201
    assert data['message'] == 'Usuario registrado exitosamente'

    mockerEnviarCorreo.assert_called_once()

def test_login_usuario_incorrecto(client: Flask):
    body = {
        'correo': faker.email(),
        'password': faker.password()
    }

    res = client.post('/login', json=body)
    data = res.get_json()

    assert res.status_code == 404
    assert data['message'] == 'El usuario no existe'

def test_login_usuario_password_incorrecto(client:Flask):
    dataUsuarioFalso = {
        'nombre': faker.name(),
        'correo': faker.email(),
        'password': hashpw(bytes(faker.password(), 'utf-8'), gensalt()).decode('utf-8'),
        'tipoUsuario': TipoUsuario.ADMIN
    }

    usuarioFalso = Usuario(**dataUsuarioFalso)
    conexionBD.session.add(usuarioFalso)
    conexionBD.session.commit()

    body = {
        'correo': dataUsuarioFalso.get('correo'),
        'password': faker.password()
    }
    res = client.post('/login', json=body)
    data = res.get_json()
    assert res.status_code == 403
    assert data['message'] == 'Credenciales incorrectas'

def test_login_sin_correo(client:Flask):
    body = {
        'correo': '',
        'password': faker.password()
    }

    res = client.post('/login', json=body)
    data = res.get_json()

    assert res.status_code == 400
    assert data['content'][0]['correo'] == ['Correo invalido.']

def test_login_exitoso(client:Flask ,mocker: MockerFixture):
    mockerGenerarJWT = mocker.patch('usuarios.usuarios_controller.create_access_token')
    mockerGenerarJWT.return_value='TU_TOKEN'
    body = {
        'correo': faker.email(),
        'password': faker.password()
    }
    password = hashpw(bytes(body.get('password'),'utf-8'),
                      gensalt()).decode('utf-8')
  
    nuevoUsuario = Usuario(correo=body.get('correo'),
                           password=password, nombre= faker.name())
    conexionBD.session.add(nuevoUsuario)
    conexionBD.session.commit()

    res = client.post('/login', json=body)
    data = res.get_json()

    assert res.status_code == 200
    assert data['token'] == 'TU_TOKEN'
    mockerGenerarJWT.assert_called_with(identity=nuevoUsuario.id)