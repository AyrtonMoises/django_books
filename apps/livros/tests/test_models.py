from django.test import TestCase
from django.urls import reverse

from model_bakery import baker

from livros.models import Livro


class LivroTestTestCase(TestCase):

    def setUp(self):
        self.livro = baker.make(Livro)

    def test_create_livro(self):
        """ Criar um livro """
        livro = baker.make(Livro)
        self.assertEqual(Livro.objects.count(), 2)

    def test_update_livro(self): 
        """ Atualizar um livro """  
        self.livro.descricao = 'Nova descrição'
        self.livro.valor = 1.50
        self.livro.save()
        self.assertEqual(self.livro.descricao, 'Nova descrição')
        self.assertEqual(self.livro.valor, 1.50)
        
    def test_delete_livro(self):
        """ Deletar um livro """
        self.livro.delete()
        self.assertEqual(Livro.objects.count(), 0)

    def test_get_absolute_url(self):
        """ Buscando absolute_url """
        self.assertEquals(
            self.livro.get_absolute_url(),
            reverse('livro_detalhes', kwargs={'livro_id': self.livro.pk })
        )