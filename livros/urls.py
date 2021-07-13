from django.urls import path

from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('autores/', autores, name='autores'),
    path('categorias/', categorias, name='categorias'),
    path('livros_por_autor/<int:autor_id>', livros_por_autor, name='livros_por_autor'),
    path('livros_por_categoria/<int:categoria_id>', livros_por_categoria, name='livros_por_categoria'),
    path('busca/', busca, name='busca'),
]
