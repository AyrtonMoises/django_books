from django.urls import path

from usuarios.views import login, logout, cadastro


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('cadastro/', cadastro, name='cadastro'),
] 