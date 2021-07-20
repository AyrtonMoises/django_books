from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from livros.models import Livro
from .models import Carrinho, Pedido


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


def paypal(request, **kwargs):
    pedido_pk = kwargs.get('pk')
    pedido = get_object_or_404(
        Pedido.objects.filter(usuario=request.user), pk=pedido_pk
    )
    paypal_dict = pedido.paypal()
    paypal_dict['return_url'] = request.build_absolute_uri(
        reverse('pedidos')
    )
    paypal_dict['cancel_return'] = request.build_absolute_uri(
        reverse('pedidos')
    )
    paypal_dict['notify_url'] = request.build_absolute_uri(
        reverse('paypal-ipn')
    )
    form = PayPalPaymentsForm(initial=paypal_dict)
    dados = {
        'form': form
    }
    return render(request, 'checkout/paypal.html', dados) 

def paypal_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED and \
        ipn_obj.receiver_email == settings.PAYPAL_EMAIL:
        try:
            order = Order.objects.get(pk=ipn_obj.invoice)
            order.complete()
        except Order.DoesNotExist:
            pass

valid_ipn_received.connect(paypal_notification)
