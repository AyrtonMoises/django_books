from django.db import models
from django.db.models import Sum, F
from django.conf import settings

from livros.models import Livro


class CarrinhoManager(models.Manager):
    def adiciona_item(self, carrinho_key, livro):
        """Adiciona item ao carrinho"""
        if self.filter(carrinho_key=carrinho_key, livro=livro).exists():
            created = False
            carrinho_item = self.get(carrinho_key=carrinho_key, livro=livro)
            carrinho_item.quantidade = carrinho_item.quantidade + 1
            carrinho_item.save()
        else:
            created = True
            valor_livro = livro.valor
            if livro.desconto:
                valor_desconto = (livro.valor / 100) * livro.desconto
                valor_livro = livro.valor - round(valor_desconto, 2)                
            carrinho_item = Carrinho.objects.create(
                carrinho_key=carrinho_key, livro=livro, valor=valor_livro
            )
        return carrinho_item, created


class Carrinho(models.Model):
    carrinho_key = models.CharField(
        'Chave do Carrinho', max_length=40, db_index=True
    )
    livro = models.ForeignKey(
        'livros.Livro', verbose_name='Livro', on_delete=models.CASCADE
    )
    quantidade = models.PositiveSmallIntegerField('Quantidade', default=1)
    valor = models.DecimalField('Valor', max_digits=8, decimal_places=2)

    objects = CarrinhoManager()

    class Meta:
        verbose_name = 'Item do carrinho'
        verbose_name_plural = 'Itens dos carrinhos'
        unique_together = (( 'carrinho_key', 'livro' ),)

    def __str__(self):
        return '{} [{}]'.format(self.livro, self.quantidade)


class PedidoManager(models.Manager):

    def criar_pedido(self, usuario, carrinho_itens):
        pedido = self.create(usuario=usuario)
        itens = []
        for item in carrinho_itens:
            itens.append(
                PedidoItem(
                    pedido=pedido, quantidade=item.quantidade, livro=item.livro, 
                    valor=item.valor
                )
            )
        PedidoItem.objects.bulk_create(itens)
        return pedido

class Pedido(models.Model):

    STATUS_CHOICES = (
        (0,'Aguardando pagamento'),
        (1,'Concluída'),
        (2,'Cancelada'),
    )

    FORMAS_PAGAMENTO_CHOICES = (
        ('deposit', 'Depósito'),
        ('pagseguro', 'PagSeguro'),
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name='Usuário', 
        on_delete=models.CASCADE
    )
    status = models.IntegerField(
        'Situação', choices=STATUS_CHOICES, default=0, blank=True
    )
    forma_pagamento = models.CharField(
        'Opção de Pagamento', choices=FORMAS_PAGAMENTO_CHOICES, 
        default='deposit', max_length=50
    )
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    objects = PedidoManager()

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-id']

    def __str__(self):
        return 'Pedido #{}'.format(self.pk)

    def total(self):
        total = self.pedido_itens.aggregate(
            total=Sum(F('valor') * F('quantidade')) 
        ).get('total')
        return total


class PedidoItem(models.Model):
    pedido = models.ForeignKey(
        Pedido, verbose_name='Pedido', related_name='pedido_itens', on_delete=models.CASCADE
    )
    livro = models.ForeignKey(
        'livros.Livro', verbose_name='Livro', on_delete=models.CASCADE
    )
    quantidade = models.PositiveSmallIntegerField('Quantidade', default=1)
    valor = models.DecimalField('Valor', max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'
        ordering = ['-id']

    def __str__(self):
        return '[{}] {}'.format(self.pedido, self.livro)

def post_save_carrinho(instance, **kwargs):
    if instance.quantidade < 1:
        instance.delete()

models.signals.post_save.connect(
    post_save_carrinho, sender=Carrinho, dispatch_uid='post_save_carrinho'
)