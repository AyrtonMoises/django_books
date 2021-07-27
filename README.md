# Django Books
Loja virtual de livros simples usando o framework Django 

### Exemplo no Heroku
https://django-books-ecommerce.herokuapp.com/

### Instalação
#### Clonar repositório
```
git clone https://github.com/AyrtonMoises/django_books.git
```

#### Ambiente virtual
```
python -m venv myenv
myenv/scripts/activate
```

#### Instalação pacotes
```
pip install -r requirements.txt
crie suas variáveis de ambiente dentro de um arquivo .env na pasta setup
Exemplo:
DEBUG=on
SECRET_KEY=SUA_KEY
DATABASE_URL=postgres://postgres:sua_senha@127.0.0.1:5432/sua_database
PAGSEGURO_TOKEN=SEU_PAGSEGURO_TOKEN
PAGSEGURO_EMAIL=SEU_EMAIL_PAGSEGURO
PAGSEGURO_SANDBOX=True
```

#### Testes

```
python manage.py test apps
python manage.py test apps/nome_do_app
```

#### Execução

```
python manage.py runserver
```


