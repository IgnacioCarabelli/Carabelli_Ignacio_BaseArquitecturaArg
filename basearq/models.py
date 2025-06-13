from django.db import models
from django.contrib.auth.models import User


#------------------CARGA DE OBRAS -----------------#


class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Arquitecto(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Obra(models.Model):
    nombre = models.CharField(max_length=200)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    arquitectos = models.ManyToManyField(Arquitecto)
    fecha_publicacion = models.DateField(auto_now_add=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class ImagenObra(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='obras/')  

    def __str__(self):
        return f"Imagen de {self.obra.nombre}"


#------------------CARGA DE AVATAR -----------------#

class Avatar(models.Model):
    imagen = models.ImageField(upload_to="avatares")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.imagen}"