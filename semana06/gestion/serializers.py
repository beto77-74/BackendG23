from rest_framework.serializers import ModelSerializer
from .models import Plato, Ingrediente, Usuario

class IngredienteSerializer(ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = '__all__'

class PlatoSerializer(ModelSerializer):
    ingredientes = IngredienteSerializer(many=True, read_only=True)
    class Meta:
        model = Plato
        fields = '__all__'



class RegistroUsuarioSerializer(ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'