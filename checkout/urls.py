from django.urls import path

from .views import *


urlpatterns = [
    path('carrinho/', carrinho, name='carrinho'),
    path('carrinho/adiciona/<int:livro_id>/', adiciona_carrinho, name='adiciona_carrinho'),
    path('finaliza_compra/', finaliza_compra, name='finaliza_compra'),
    path('finaliza_compra/pagseguro/<int:pk>/', pagseguro, name='pagseguro'),
    path('notificacoes/pagseguro/', pagseguro_notification, name='pagseguro'),
]
