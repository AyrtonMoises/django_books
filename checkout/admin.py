from django.contrib import admin

from .models import Carrinho, Pedido, PedidoItem


admin.site.register([Carrinho, Pedido, PedidoItem])