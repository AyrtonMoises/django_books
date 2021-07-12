import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from django_resized import ResizedImageField

from .constantes import TIPOS_ENCARDENACAO, PAISES, IDIOMAS


def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)  

class Editora(models.Model):
    descricao = models.CharField(max_length=150, verbose_name='Descrição')
    ativa = models.BooleanField()
    imagem = ResizedImageField(size=[500, 300], quality=70, upload_to='editoras/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Editoras"
        verbose_name = "Editora"

    def __str__(self):
        return self.descricao


class Categoria(models.Model):
    descricao = models.CharField(max_length=150, verbose_name='Descrição')

    class Meta:
        verbose_name_plural = "Categorias"
        verbose_name = "Categoria"

    def __str__(self):
        return self.descricao

class Autor(models.Model):
    nome = models.CharField(max_length=150)
    ativo = models.BooleanField()
    imagem = ResizedImageField(size=[500, 300], quality=70, upload_to='autores/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Autores"
        verbose_name = "Autor"

    def __str__(self):
        return self.nome

class Livro(models.Model):
    descricao = models.CharField(max_length=150, verbose_name='Descrição')
    isbn = models.CharField(max_length=13)
    ano = models.PositiveSmallIntegerField(validators=[max_value_current_year,])
    edicao = models.PositiveSmallIntegerField(default=1, null=True)
    encadernacao = models.PositiveSmallIntegerField(choices=TIPOS_ENCARDENACAO, verbose_name='Encadernação')
    idioma = models.PositiveSmallIntegerField(default=1, choices=IDIOMAS, null=True)
    pais = models.CharField(default='BRA', max_length=3, choices=PAISES, blank=True, null=True)
    ean = models.CharField(max_length=13)
    ativo = models.BooleanField()
    imagem = ResizedImageField(size=[500, 300], quality=70, upload_to='livros/', blank=True, null=True)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    editora = models.ForeignKey(Editora, on_delete=models.CASCADE)
    categorias = models.ManyToManyField(Categoria)
    data_criacao = models.DateField(default=timezone.now, verbose_name='Data de criação')

    def __str__(self):
        return self.descricao