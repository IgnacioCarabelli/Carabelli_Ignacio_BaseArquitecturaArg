from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import *


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput )
    password2 = forms.CharField(label="Confirma tu Contraseña", widget=forms.PasswordInput )
    admin_code = forms.CharField(label="Código de administrador (opcional)", required=False, max_length=50)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UsuarioEditForm(UserChangeForm):  
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="Nombre", max_length=20, required=True)
    last_name = forms.CharField(label="Apellido", max_length=20, required=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            self.fields.pop('password')



#------------------AVATAR -----------------#

class AvatarForm(forms.Form):
    imagen = forms.ImageField(required=True)


#------------------CARGA DE OBRAS -----------------#

class ObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['nombre', 'ciudad', 'arquitectos', 'descripcion']

class ImagenObraForm(forms.ModelForm):
    class Meta:
        model = ImagenObra
        fields = ['imagen']

class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        fields = ['nombre']

class ArquitectoForm(forms.ModelForm):
    class Meta:
        model = Arquitecto
        fields = ['nombre']