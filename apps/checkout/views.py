import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings

from pagseguro import PagSeguro

from livros.models import Livro
from .models import Carrinho, Pedido

logger = logging.getLogger('checkout.views')


def carrinho(request):
    """ Carrinho de compras """
    CarrinhoItemFormSet = modelformset_factory(Carrinho, 
        fields=('quantidade',), can_delete=True, extra=0
    )
    if request.session.session_key:
        formset = CarrinhoItemFormSet(
        queryset=Carrinho.objects.filter(
            carrinho_key=request.session.session_key
        ), data=request.POST or None
    )
    else:
        formset = CarrinhoItemFormSet(queryset=Carrinho.objects.none())

    if request.method == 'POST':
        if formset.is_valid():
            messages.success(request, 'Carrinho atualizado com sucesso')
            formset.save()
            formset = CarrinhoItemFormSet(
                queryset = Carrinho.objects.filter(
                    carrinho_key=request.session.session_key
                )
            )

    carrinho = Carrinho.objects.filter(
        carrinho_key=request.session.session_key
    )
    dados = {
        'carrinho': carrinho,
        'formset': formset
    }
    return render(request, 'checkout/carrinho.html', dados)

def adiciona_carrinho(request, livro_id):
    """ Adiciona livro ao carrinho """
    livro = get_object_or_404(Livro, pk=livro_id)
    logger.debug('Livro %s adicionado ao carrinho' % livro)
    if request.session.session_key is None:
        request.session.save()
    carrinho_item, created = Carrinho.objects.adiciona_item(
        request.session.session_key, livro
    )

    if created:
        messages.success(request, 'Livro adicionado com sucesso')
    else:
        messages.success(request, 'Livro atualizado com sucesso')

    return redirect('carrinho')

@login_required
def finaliza_compra(request):
    """Finaliza compra criando o pedido"""
    session_key = request.session.session_key
    if session_key and Carrinho.objects.filter(
        carrinho_key=session_key).exists():
        carrinho_itens = Carrinho.objects.filter(carrinho_key=session_key)
        pedido = Pedido.objects.criar_pedido(
            usuario=request.user, carrinho_itens=carrinho_itens
        )
        messages.success(request, 'Seu pedido foi finalizado com sucesso!')
        carrinho_itens.delete()
    else:
        messages.info(request, 'Não há itens no carrinho de compras')
        return redirect('carrinho')
    dados = {
        'pedido': pedido
    }
    return render(request, 'checkout/finaliza_compra.html', dados)


def pagseguro(request, **kwargs):
    pedido_pk = kwargs.get('pk')
    pedido = get_object_or_404(
        Pedido.objects.filter(usuario=request.user), pk=pedido_pk
    )
    pg = pedido.pagseguro()
    pg.redirect_url = request.build_absolute_uri(
        reverse('pedidos')
    )
    pg.notification_url = request.build_absolute_uri(
        reverse('pagseguro_notification')
    )
    response = pg.checkout()
    return redirect(response.payment_url)

@csrf_exempt
def pagseguro_notification(request):
    notification_code = request.POST.get('notificationCode', None)
    if notification_code:
        pg = PagSeguro(
            email=settings.PAGSEGURO_EMAIL, token=settings.PAGSEGURO_TOKEN,
            config={'sandbox': settings.PAGSEGURO_SANDBOX}
        )
        notification_data = pg.check_notification(notification_code)
        status = notification_data.status
        reference = notification_data.reference
        try:
            pedido = Pedido.objects.get(pk=reference)
        except Pedido.DoesNotExist:
            pass
        else:
            pedido.pagseguro_update_status(status)
    return HttpResponse('OK')