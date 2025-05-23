from django.shortcuts import render
from django.http import HttpResponse
from .models import Plato, Ingrediente, Usuario
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ViewSet
from .serializers import PlatoSerializer, IngredienteSerializer, RegistroUsuarioSerializer
from rest_framework import status
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.models import AnonymousUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def vistaPrueba(request):
    print(request)

    return HttpResponse(content='Hola')


def mostrarRecetario(request):
    # SELECT * FROM platos;
    platos = Plato.objects.all()
    
    # el contexto siempre debe de ser un dict
    return render(request=request, template_name='mostrar_recetario.html', context={"platos": platos})

def editarRecetario(request, id):
    plato = Plato.objects.filter(id = id).first()
    
    return render(request=request, template_name='editar_recetario.html', context={"plato": plato})

class PlatosController(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(
            responses={
                200:openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='Los platos son'),
                    'content': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT, properties= {
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='1'),
                        'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Ceviche'),
                        'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Delicioso plato'),
                        'usuarioId': openapi.Schema(type=openapi.TYPE_INTEGER, description='1'),
                        'esPublico': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Estado'),
                    }, example = {
                        'id': 1,
                        'nombre': 'Ceviche',
                        'descripcion': 'Delicioso ceviche',
                        'usuarioId': 3,
                        'esPublico': False
                    }))
                    }),
                401: openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication credentials were not provided."')
                })})

    def get(self, request:Request):
        print(request.query_params)
        queryParams = request.query_params
        totaLQueryParams = len(queryParams.keys())
        filtros = {}
        print(request.user.id)
        
        if (queryParams):
            if(queryParams.get('nombre')):
                filtros['nombre__icontains'] = queryParams.get('nombre')
            if (queryParams.get('id')):
                filtros['id'] = queryParams.get('id')

            totalFiltrosABuscar = len(filtros.keys())
            if (totaLQueryParams != totalFiltrosABuscar):
                return Response(data={
                    'message': 'Prametros incorrecros'
                })
        filtros['usuarioId'] = request.user.id
        platos = Plato.objects.filter(**filtros).all()
        serializer = PlatoSerializer(instance = platos, many =True)
        return Response(data={
            'message': 'Los platos son',
            'content': serializer.data
        })
    
    @swagger_auto_schema(
            request_body=PlatoSerializer
    )
    def post(self, request: Request):
        data = request.data
        data['usuarioId']=request.user.id
        serializer = PlatoSerializer(data=data)
        dataValida = serializer.is_valid()
        if dataValida:
            serializer.save()
            return Response(data={
                'message': 'Plato creado exitosamente',
                'content': serializer.data
            },status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'message': 'Error al crear el plato',
                'content': serializer.errors           
            }, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(http_method_names=['GET'])
def verificarStatusServidor(request):
    horaSistema = datetime.now()
    return Response(data={
        'message': 'El servidor esta funcionando correctamente',
            'content': horaSistema.strftime('%d-%m-%Y %H:%M:%S')    
    })

# class CrearIngrediente (CreateAPIView):
#     serializer_class=IngredienteSerializer
#     queryset = Ingrediente.objects.all()
#     permission_classes =[IsAuthenticated]

class CrearIngredienteController(CreateAPIView):
    serializer_class = IngredienteSerializer
    queryset = Ingrediente.objects.all()
    permission_classes =[IsAuthenticated]

    def post(self,request):
        usuarioId = request.user.id
        print(usuarioId)

        platoEncontrado = Plato.objects.filter(id = request.data.get('platoId')).first()
        if not platoEncontrado:
            return Response(data={
                'message': 'Plato a ingresar no existe'
            }, status=status.HTTP_404_NOT_FOUND)
        
        usuarioPertenece = platoEncontrado.usuarioId.id

        if usuarioPertenece != usuarioId:
             return Response(data={
                'message': 'El usuario no tiene acceso a este plato'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializador= self.serializer_class(data=request.data)

        if serializador.is_valid():
            ingredienteCreado = serializador.save()
            resultado = self.serializer_class(instance=ingredienteCreado)
            dataResultado = resultado.data
            return Response(data=dataResultado, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializador.errors)

class DevolverListarEliminarIngredienteController(RetrieveUpdateDestroyAPIView):
    serializer_class=IngredienteSerializer
    queryset = Ingrediente.objects.all()

class DevolverListarEliminarIngredienteController(RetrieveUpdateDestroyAPIView):
    serializer_class = IngredienteSerializer
    queryset = Ingrediente.objects.all()

@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['correo','password','nombre'],
        properties={
            'nombre':openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del cheff'),
            'correo':openapi.Schema(type=openapi.TYPE_STRING, description='Correo del cheff'),
            'password':openapi.Schema(type=openapi.TYPE_STRING, description='Passwor con no menor a 6 caracteres'),
        },example = {
            'nombre': 'Jhon Doe',
            'correo':'jhon@email.com',
            'password':'Welcome123!'
        }
    ),
    methods=['POST'],
    responses={201:'Usuario creado exitosamente',400:'Error al crear el usuario'}
)

@api_view(http_method_names=['POST'])
def registrarUsuario(request):
    serializador = RegistroUsuarioSerializer(data = request.data)
    if serializador.is_valid():
        nombre = serializador.validated_data.get('nombre')
        correo = serializador.validated_data.get('correo')
        password = serializador.validated_data.get('password')
        nuevoUsuario = Usuario(nombre=nombre,
                               correo=correo)
        nuevoUsuario.set_password(password)
        nuevoUsuario.save()
        return Response(data={
        'message': 'Usuario creado exitosamente'
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(data={
        'message': 'Usuario con error',
        'content':serializador.error
        }, status=status.HTTP_404_NOT_FOUND)
    
@api_view(http_method_names=['POST'])
def loginManual(request):
    data = request.data
    usuarioEncontrado = Usuario.objects.filter(correo=data.get('correo')).first()

    if not usuarioEncontrado:
        return Response(data={
            'message': 'Usuario no existe'
        }, status = status.HTTP_404_NOT_FOUND)
    passwordCorrecto = usuarioEncontrado.check_password(data.get('password'))

    if not passwordCorrecto:
         return Response(data={
            'message': 'Credenciales incorrectas'
        }, status = status.HTTP_404_NOT_FOUND)
    
    token = RefreshToken.for_user(usuarioEncontrado)
    return Response(data={
        'token': token.access_token.__str__()
    })

class PlatoViewset(ViewSet):
    def list(self, request):
        pass

    def retrieve(self, request, pk):
        platoEncontrado = Plato.objects.filter(id=pk).first()
        if not platoEncontrado:
            return Response(data={
                'message':'Plato no existe'
            },status=status.HTTP_404_NOT_FOUND)
        
        if not platoEncontrado.esPublico:
            if type(request.user.id) == AnonymousUser:
                return Response(data={
                    'message':'Se necesita una token para esta peticion'
                },status=status.HTTP_400_BAD_REQUEST)
            else:
                if platoEncontrado.usuarioId.id != request.user.id:
                    return Response(data={
                        'message':'Credenciales incorrectas'
                    },status=status.HTTP_403_FORBIDDEN)

        serializer = PlatoSerializer(instance=platoEncontrado)
        #print(platoEncontrado.ingredientes.all())
        return Response(data={
            'content': serializer.data
        })

    def create(self, request):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request,pk=None):
        pass

    def destroy(self, request,pk=None):
        pass