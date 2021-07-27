from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from model_bakery import baker

from checkout.models import Carrinho, Pedido

User = get_user_model()

class CarrinhoTestTestCase(TestCase):

    def setUp(self):
        self.livro = baker.make(Carrinho, _quantity=3)

    def test_post_carrinho(self):
        """ Teste de remoção de item quando quantidade for atualizada a zero """
        carrinho = Carrinho.objects.all()[0]
        carrinho.quantidade = 0
        carrinho.save()
        self.assertEqual(Carrinho.objects.count(), 2)


class PedidoTestCase(TestCase):

    def setUp(self):
        self.carrinho = baker.make(Carrinho)
        self.usuario = baker.make(User)

    def test_create_pedido(self):
        """ Teste criando pedido com itens do carrinho """
        Pedido.objects.criar_pedido(self.usuario, [self.carrinho])
        self.assertEqual(Pedido.objects.count(), 1)
        pedido = Pedido.objects.get()
        self.assertEqual(pedido.usuario, self.usuario)
        pedido_itens = pedido.pedido_itens.get()
        self.assertEqual(pedido_itens.livro, self.carrinho.livro)