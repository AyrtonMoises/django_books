from django.urls import path

from usuarios.views import login, logout, cadastro, perfil, alterar_senha


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('cadastro/', cadastro, name='cadastro'),
    path('perfil/', perfil, name='perfil'),
    path('alterar_senha/', alterar_senha, name='alterar_senha'),
] 