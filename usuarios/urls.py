from django.urls import path

from usuarios.views import *


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('cadastro/', cadastro, name='cadastro'),
    path('perfil/', perfil, name='perfil'),
    path('alterar_senha/', alterar_senha, name='alterar_senha'),
    path('pedidos/', pedidos, name='pedidos'),
] 