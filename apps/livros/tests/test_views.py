from django.test import TestCase, Client
from django.urls import reverse

from model_bakery import baker

from livros.models import Livro


class HomeViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('home')
        self.livros = baker.make(Livro, _quantity=10)

    def tearDown(self):
        Livro.objects.all().delete()

    def test_view_ok(self):
        """ Testa exibição da view """
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'livros/home/index.html')

    def test_context(self):
        """ Testa quantidade de livros na home """
        response = self.client.get(self.url)
        self.assertTrue('livros' in response.context)
        livros_lista = response.context['livros']
        self.assertEquals(livros_lista.count(), 6)


class BuscaViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('busca')
        self.livros = baker.make(Livro, descricao='Exemplo', _quantity=5)
        self.livros += baker.make(Livro, descricao='Teste', _quantity=3)

    def test_view_ok(self):
        """ Testa exibição da view """
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'livros/busca.html')

    def test_context(self):
        """ Testa quantidade de livros no resultado """
        response = self.client.get(self.url, {'q': 'Exemplo'} )
        self.assertTrue('livros' in response.context)
        livros_lista = response.context['livros']
        self.assertEquals(livros_lista.count(), 5)
        response = self.client.get(self.url, {'q': 'Teste'} )
        self.assertTrue('livros' in response.context)
        livros_lista = response.context['livros']
        self.assertEquals(livros_lista.count(), 3)