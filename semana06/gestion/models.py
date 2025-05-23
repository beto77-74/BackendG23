from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class ManejadorUsuario(BaseUserManager):
    def create_superuser(self,nombre,correo,password):
        if not correo:
            return ValueError('El correo es obligatorio')
        
        nuevoCorreo =self.normalize_email(correo)
        nuevoUsuario = self.model(correo=nuevoCorreo, nombre = nombre)

        nuevoUsuario.set_password(password)
        nuevoUsuario.is_superuser=True
        nuevoUsuario.is_staff=True

        nuevoUsuario.save()

class Usuario(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    nombre = models.TextField(null=False)
    correo= models.EmailField(unique=True,null=False)
    password= models.TextField(null=False)
    
    is_staff = models.BooleanField(default=False)
    is_active =models.BooleanField(default=True)
    USERNAME_FIELD = 'correo'

    REQUIRED_FIELDS = ['nombre']

    objects = ManejadorUsuario()

    class Meta:
        db_table = 'usuarios'

# Create your models here.
class Plato(models.Model):
    id=models.AutoField(primary_key=True)
    nombre= models.TextField(null=False)
    descripcion = models.TextField()
    usuarioId = models.ForeignKey(to=Usuario,on_delete=models.PROTECT, db_column='usuario_id', null=False)
    esPublico = models.BooleanField(default=True, null=False, db_column='es_publico')

    class Meta:
        db_table = 'platos'
        ordering = ['nombre']

class Ingrediente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.TextField(null=False)
    cantidad = models.TextField(null=False)
    # Cuando queremos agregar una relacion entre dos tablas podemos indicar cual sera su comportamiento a nivel de base de datos con la eliminacion
    # CASCADE > Si se elimina un plato se eliminara sus ingredientes
    # PROTECT > evita la eliminacion del plato si es que este tiene ingredientes y emite un error de tipo ProectedError
    # RESTRICT > hace lo mismo que el protect pero emite un error de tipo RestrictedError
    # SET_NULL > permite la eliminacion del plato y a sus ingredientes les cambia el valor a null, PERO esta columna tiene que tener la opcion de admitir valores nulos
    # SET_DEFAULT > permite la eliminacion y cambiara el valor del plato_id a un valor definir por defecto
    # DO_NOTHING > permite la eliminacion del plato y no cambia el valor de la llave foranea dejando asi un error a nivel de base de datos porque no se podra vincular correctamente la informacion
    platoId = models.ForeignKey(
        to=Plato, 
        db_column='plato_id', 
        on_delete=models.PROTECT, 
        related_name='ingredientes',
        null=False)

    class Meta:
        db_table = 'ingredientes'

class Preparacion(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.TextField(null=False)
    orden = models.IntegerField(null=False)
    platoId = models.ForeignKey(to=Plato,
                                db_column='plato_id',
                                on_delete=models.PROTECT,
                                related_name='preparaciones',
                                null=False)
    class Meta:
        db_table = 'preparaciones'
        unique_together = [['orden','platoId']]

