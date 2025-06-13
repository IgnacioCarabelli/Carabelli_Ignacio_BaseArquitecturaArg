
from django.urls import path

from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

urlpatterns = [


    path('home/', views.home, name="home"),
    path('contacto/', views.contacto, name='contacto'),
    path('buscar/', views.buscar, name='buscar'),


    path('recepcion_contacto/', views.recepcionContacto, name='recepcion_contacto'),

    path('twitter/', views.twitter, name='twitter'),
    path('facebook/', views.facebook, name='facebook'),

    
    path('pagina_en_construccion', views.facebook, name='pagina_en_construccion'),
    
    path('carga_usuarios/', views.registrate, name='carga_usuarios'),

    path('ingreso/', views.ingreso, name='ingreso'),
    path('editar_mi_perfil/', views.editarPerfil, name='editar_mi_perfil'),
    path('agregar_avatar/', views.agregarAvatar, name='agregar_avatar'),

    path('sobre_mi/', views.sobre_mi, name='sobre_mi'),
    
    path('salir/', LogoutView.as_view(template_name="basearq/salir.html"), name='salir'),

    path('agregar_usuario_admin/', views.crear_usuario_admin.as_view(), name='agregar_usuario_admin'),
    path('editar_usuario_admin/<int:pk>/', views.editar_usuario_admin.as_view(), name='editar_usuario_admin'),
    path('borrar_usuario_admin/<int:pk>/', views.borrar_usuario_admin.as_view(), name='borrar_usuario_admin'),
    path('ingreso/listado_usuarios_admin/', views.listado_usuarios_admin.as_view(template_name="basearq/listado_usuarios_admin.html"), name='listado_usuarios_admin'),

    path('listado_obras/', views.listado_obras, name='listado_obras'),
    path('listado_obras/agregar_obras/', views.cargar_obra, name='agregar_obras'),
    path('agregar_obras/', views.cargar_obra, name='agregar_obra_desde_home'),

    path('agregar_ciudad/', views.agregar_ciudad, name='agregar_ciudad'),
    path('agregar_arquitecto/', views.agregar_arquitecto, name='agregar_arquitecto'),
    
    path('listado_arquitectos/', views.listado_arquitectos, name='listado_arquitectos'),
    path('listado_ciudades/', views.listado_ciudades, name='listado_ciudades'),
    path('listado_nombre_obras/', views.listado_nombre_obras, name='listado_nombre_obras'),


    path('detalle_obras/<int:obra_id>/', views.detalle_obra, name='detalle_obra'),


    path('cambiar_contraseña/',auth_views.PasswordChangeView.as_view(template_name='basearq/cambiar_contraseña.html',success_url=reverse_lazy('editar_mi_perfil')),name='cambiar_contraseña'),



]




