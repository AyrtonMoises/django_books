from django.test import Client, TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model

from model_bakery import baker

from checkout.models import Carrinho

User = get_user_model()

class CreateCarrinhoTestCase(TestCase):

    def setUp(self):
        self.livro = baker.make('livros.Livro')
        self.client = Client()
        self.url = reverse(
            'adiciona_carrinho', kwargs={ 'livro_id': self.livro.pk }
        )

    def test_adicionando_item_carrinho(self):
        """ Teste adicionando 1 item ao carrinho """
        response = self.client.get(self.url)
        redirect_url = reverse('carrinho')
        self.assertRedirects(response, redirect_url)
        self.assertEqual(Carrinho.objects.count(), 1)

    def test_adicionando_2_itens_carrinho(self):
        """ Teste adicionando mais um produto ao carrinho """
        response = self.client.get(self.url)
        response = self.client.get(self.url)
        carrinho = Carrinho.objects.get()
        self.assertEqual(carrinho.quantidade, 2)


class CheckoutViewTestCase(TestCase):

    def setUp(self):
        self.usuario = baker.prepare(User)
        self.usuario.set_password('123')
        self.usuario.save()

        self.carrinho = baker.make(Carrinho)
        self.client = Client()
        self.checkout_url = reverse('finaliza_compra')

    def test_checkout_view(self):
        """ Testa checkout do carrinho """
        response = self.client.get(self.checkout_url)
        redirect_url = '{}?next={}'.format(
            reverse(settings.LOGIN_URL), self.checkout_url
        )
        self.assertRedirects(response, redirect_url)
        self.client.login(username=self.usuario.username, password='123')
        self.carrinho.carrinho_key = self.client.session.session_key
        self.carrinho.save()
        response = self.client.get(self.checkout_url)
        self.assertTemplateUsed(response, 'checkout/finaliza_compra.html')