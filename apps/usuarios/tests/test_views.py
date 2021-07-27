from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings

from model_bakery import baker

from django.contrib.auth import get_user_model


class LoginViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = baker.prepare(
            settings.AUTH_USER_MODEL, email='teste@teste.com'
        )
        self.user.set_password('123')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_login_ok(self):
        """ Teste de login com credenciais corretas """
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/login.html')
        data = {'email': self.user.email, 'senha': '123'}
        response = self.client.post(self.login_url, data)
        redirect_url = reverse(settings.LOGIN_REDIRECT_URL)
        self.assertRedirects(response, redirect_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_error(self):
        """ Teste de login com credenciais incorretas """
        data = {'email': self.user.email, 'senha': '1234'}
        response = self.client.post(self.login_url, data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/login.html')


class CadastroViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('cadastro')
        self.model_user = get_user_model()

    def test_cadastro_ok(self):
        """ Teste de cadastro de usuário """
        data = {'nome': 'teste', 'email': 'teste', 'senha1': 'teste123', 'senha2': 'teste123'}
        response = self.client.post(self.register_url, data)
        index_url = reverse('login')
        self.assertRedirects(response, index_url)
        self.assertEquals(self.model_user.objects.count(), 1)

    def test_cadastro_senhas_diferentes(self):
        """ Teste de cadastro de usuário com senhas diferentes """
        data = {'nome': 'teste', 'email': 'teste', 'senha1': 'teste123', 'senha2': 'teste1234'}
        response = self.client.post(self.register_url, data)
        index_url = reverse('cadastro')
        self.assertRedirects(response, index_url)
        self.assertEquals(self.model_user.objects.count(), 0)

    def test_cadastro_sem_email(self):
        """ Teste de cadastro de usuário com senhas diferentes """
        data = {'nome': 'teste', 'email': '', 'senha1': 'teste123', 'senha2': 'teste123'}
        response = self.client.post(self.register_url, data)
        index_url = reverse('cadastro')
        self.assertRedirects(response, index_url)
        self.assertEquals(self.model_user.objects.count(), 0)


class CadastroUpdateTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('perfil')
        self.user = baker.prepare(
            settings.AUTH_USER_MODEL, email='teste@teste.com'
        )
        self.user.set_password('123')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_update_user_ok(self):
        """ Teste atualizando dados de perfil do usuário """
        data = {'username': 'teste_atualizado', 'email': 'teste_atualizado@teste.com'}
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.client.login(username=self.user.username, password='123')
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.url)
        self.user.refresh_from_db()
        self.assertEquals(self.user.email, 'teste_atualizado@teste.com')
        self.assertEquals(self.user.username, 'teste_atualizado')

    def test_update_user_error(self):
        """ Teste atualizando dados de perfil do usuário com campos vazios """
        data = {'username': '', 'email': ''}
        self.client.login(username=self.user.username, password='123')
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'username', 'Este campo é obrigatório.')

