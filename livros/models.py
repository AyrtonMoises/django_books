import datetime

from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

from django_resized import ResizedImageField

from .constantes import TIPOS_ENCARDENACAO, PAISES, IDIOMAS


def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)  

class Editora(models.Model):
    descricao = models.CharField(max_length=150, verbose_name='Descrição')
    ativa = models.BooleanField()

    class Meta:
        verbose_name_plural = "Editoras"
        verbose_name = "Editora"

    def __str__(self):
        return self.descricao


class Categoria(models.Model):
    descricao = models.CharField(max_length=150, verbose_name='Descrição')
    cor = models.CharField(max_length=7)

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
    
    @property
    def categorias_autor(self):
        """Lista categorias de livros do autor"""
        categorias = []
        for livro in self.autor_livro.all():
            for categoria in livro.categorias.all():
                categorias.append(categoria)
        return set(categorias)


class Livro(models.Model):
    descricao = models.CharField(max_length=150, verbose_name='Descrição')
    detalhes = models.TextField(blank=True, null=True)
    isbn = models.CharField(max_length=13, validators=[MinLengthValidator(13),], verbose_name='ISBN')
    ano = models.PositiveSmallIntegerField(validators=[max_value_current_year,])
    edicao = models.PositiveSmallIntegerField(default=1, null=True, verbose_name='Edição')
    encadernacao = models.PositiveSmallIntegerField(choices=TIPOS_ENCARDENACAO, verbose_name='Encadernação')
    idioma = models.PositiveSmallIntegerField(default=1, choices=IDIOMAS, null=True)
    pais = models.CharField(default='BRA', max_length=3, choices=PAISES, blank=True, null=True)
    ean = models.CharField(max_length=13, verbose_name='EAN')
    ativo = models.BooleanField()
    imagem = ResizedImageField(size=[500, 300], quality=70, upload_to='livros/', blank=True, null=True)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='autor_livro')
    editora = models.ForeignKey(Editora, on_delete=models.CASCADE, related_name='editora_livro')
    categorias = models.ManyToManyField(Categoria)
    data_criacao = models.DateField(default=timezone.now, verbose_name='Data de criação')
    estoque = models.PositiveSmallIntegerField()
    desconto = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(99)])

    def __str__(self):
        return self.descricao


@receiver(post_save, sender=Editora)
def editora_altera_status(sender, instance, created, **kwargs):
    """Ativa/Inativa livro quando editora atualizar status"""
    if not created:
        for livro in instance.editora_livro.all():
            livro.ativo = instance.ativa
            livro.save()
        
@receiver(post_save, sender=Autor)
def autor_altera_status(sender, instance, created, **kwargs):
    """Ativa/Inativa livro quando autor atualizar status"""
    if not created:
        for livro in instance.autor_livro.all():
            livro.ativo = instance.ativo
            livro.save()