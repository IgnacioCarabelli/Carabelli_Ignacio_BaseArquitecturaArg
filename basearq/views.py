
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from django.urls import reverse_lazy

from django.http import HttpResponse

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from django.db.models import Q

from .models import *
from .forms import *



#-------------- PAGINA EN CONSTRUCCION--------------------#

def pagina_en_construccion(request):
    return render(request, "basearq/pagina_en_construccion.html")

#---------------- REDES SOCIALES-----------------------#

def twitter(request):
    return render(request, "basearq/pagina_en_construccion.html")

def facebook(request):
    return render(request, "basearq/pagina_en_construccion.html")

#--------------------ARQUITECTO--------------------#

def agregar_arquitecto(request):
    return render(request, "basearq/agregar_arquitecto.html")

#--------------------NAVBAR--------------------#

def home(request):
    return render(request, "basearq/home.html")


def buscar(request):
    query = request.GET.get('q', '')
    if query:
        obras = Obra.objects.filter(
            Q(nombre__icontains=query) |
            Q(ciudad__nombre__icontains=query) |
            Q(arquitectos__nombre__icontains=query)
        ).distinct()
    else:
        obras = Obra.objects.all()

    return render(request, "basearq/buscar.html", {'obras': obras,'query': query,})


def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')

        print(f'Contacto de: {nombre} - {email} - Asunto: {asunto} - Mensaje: {mensaje}')

        return render(request, 'basearq/recepcion_contacto.html')

    return render(request, 'basearq/contacto.html') 

def recepcionContacto(request):
    return render(request, "basearq/recepcion_contacto.html")


def sobre_mi(request):
    return render(request, "basearq/sobre_mi.html")

#----------------CBV---CRUD DE ADMINISTRADOR---------------#

class listado_usuarios_admin(LoginRequiredMixin, ListView):
    model = User
    template_name = 'basearq/listado_usuarios_admin.html'  
    context_object_name = 'usuarios'

class crear_usuario_admin(LoginRequiredMixin, CreateView):
    model = User
    fields = ["first_name", "last_name", "email", "username" ]
    template_name = 'basearq/agregar_usuario_admin.html' 
    success_url = reverse_lazy("listado_usuarios_admin")

class editar_usuario_admin(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name", "email", "username", ]
    template_name = 'basearq/agregar_usuario_admin.html' 
    success_url = reverse_lazy("listado_usuarios_admin")

class borrar_usuario_admin(LoginRequiredMixin, DeleteView):
    model = User
    fields = ["first_name", "last_name", "email", "username" ]
    template_name = 'basearq/borrar_usuario_admin.html' 
    success_url = reverse_lazy("listado_usuarios_admin")


#----------------EDITAR PERFIL USUARIO---------------#

@login_required
def editarPerfil(request):
    usuario = request.user

    if request.method == "POST":
        miform = UsuarioEditForm(request.POST, instance=usuario)
        avatar_form = AvatarForm(request.POST, request.FILES)

        if miform.is_valid() and avatar_form.is_valid():
            
            miform.save()

            
            imagen = avatar_form.cleaned_data.get("imagen")
            if imagen:
                
                Avatar.objects.filter(user=usuario).delete()
                nuevo_avatar = Avatar(user=usuario, imagen=imagen)
                nuevo_avatar.save()

                
                request.session["avatar"] = nuevo_avatar.imagen.url

            return redirect(reverse_lazy('home'))
    else:
        miform = UsuarioEditForm(instance=usuario)
        avatar_form = AvatarForm()

    return render(request, 'basearq/editar_mi_perfil.html', {'form': miform, 'avatar_form': avatar_form})


#----------------Registrate / Ingresa----------------------------#

def registrate(request):
    if request.method == "POST":
        miformulario = RegistroForm(request.POST)
        if miformulario.is_valid():
            user = miformulario.save(commit=False)
            
            admin_code = miformulario.cleaned_data.get('admin_code')
            if admin_code == 'SOYADMIN2025':  
                user.is_staff = True
                user.is_superuser = True
                
            user.save()
            return redirect(reverse_lazy('home'))
    else:
        miformulario = RegistroForm()

    return render(request, 'basearq/carga_usuarios.html', {"form": miformulario})


def ingreso(request):
    if request.method == "POST":
        usuario = request.POST["username"]
        clave = request.POST["password"]
        user = authenticate(request, username=usuario, password=clave)

        if user is not None:
            login(request, user)

            
            if user.is_superuser:
                return redirect('listado_usuarios_admin')  
            else:
                return redirect('home') 

        else:
            return redirect(reverse_lazy('ingreso'))
    else:
        miform = AuthenticationForm()

    return render(request, "basearq/ingreso.html", {"form": miform})


#----------------AVATAR----------------------------#

@login_required
def agregarAvatar(request):
    if request.method == "POST":
        miform = AvatarForm(request.POST, request.FILES)
        if miform.is_valid():
            usuario = request.user
            imagen = miform.cleaned_data["imagen"]
            
            avatarviejo = Avatar.objects.filter(user=usuario)
            avatarviejo.delete()  
            
            avatar = Avatar(user=usuario, imagen=imagen)
            avatar.save()

            request.session["avatar"] = avatar.imagen.url

            return redirect(reverse_lazy("home"))
    else:
        miform = AvatarForm()
    
    return render(request, "basearq/editar_mi_perfil.html", {"form": miform})


#----------------NUEVAS OBRAS--------------------------#

@login_required
def cargar_obra(request):
    if request.method == 'POST':
        obra_form = ObraForm(request.POST)
        imagen_form = ImagenObraForm(request.POST, request.FILES)

        if obra_form.is_valid() and imagen_form.is_valid():
            obra = obra_form.save()
            imagen = imagen_form.cleaned_data['imagen']
            ImagenObra.objects.create(obra=obra, imagen=imagen)
            return redirect('listado_obras')  
    else:
        obra_form = ObraForm()
        imagen_form = ImagenObraForm()

    return render(request, 'basearq/agregar_obras.html', {'obra_form': obra_form,'imagen_form': imagen_form})


@login_required
def agregar_ciudad(request):
    if request.method == 'POST':
        form = CiudadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agregar_obras')  
    else:
        form = CiudadForm()
    return render(request, 'basearq/agregar_ciudad.html', {'form': form})


@login_required
def agregar_arquitecto(request):
    if request.method == 'POST':
        form = ArquitectoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agregar_obras')  
    else:
        form = ArquitectoForm()
    return render(request, 'basearq/agregar_arquitecto.html', {'form': form})


#----------------LISTADO DE OBRAS CON BUSCADOR--------------------------#

@login_required
def listado_obras(request):
    query = request.GET.get('q', '')
    
    if query:
        obras = Obra.objects.filter(Q(nombre__icontains=query) | Q(ciudad__nombre__icontains=query) | Q(arquitectos__nombre__icontains=query)).distinct()
    else:
        obras = Obra.objects.all()
    
    return render(request, 'basearq/listado_obras.html', {'obras': obras,'query': query})


#----------------BUSCAR DE ARQUITECTOS / OBRAS / CIUDADES--------------------------#


def listado_arquitectos(request):
    arquitectos = Arquitecto.objects.all()
    return render(request, 'basearq/listado_arquitectos.html', {'arquitectos': arquitectos}) 

def listado_ciudades(request):
    ciudades = Ciudad.objects.all()
    return render(request, 'basearq/listado_ciudades.html', {'ciudades': ciudades}) 

def listado_nombre_obras(request):
    obras = Obra.objects.all()
    return render(request, 'basearq/listado_nombre_obras.html', {'obras': obras})

#----------------DETALLE DE LAS OBRAS--------------------------#

def detalle_obra(request, obra_id):
    obra = get_object_or_404(Obra, pk=obra_id)
    return render(request, 'basearq/detalle_obra.html', {'obra': obra})

