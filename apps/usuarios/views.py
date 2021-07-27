from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from checkout.models import Pedido
from .forms import PerfilForm


User = get_user_model()

def login(request):
    """Realiza login do usuario"""
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if email == "" or senha == "":
            messages.error(request, "Campos email e senha não podem ficar em branco!")
            return redirect('login')
        if User.objects.filter(email=email).exists():
            username = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=username, password=senha)
            if user is not None:
                auth.login(request, user)
                proxima_pagina = request.POST.get('next')
                if proxima_pagina:
                    return redirect(proxima_pagina)
                return redirect('home')
            else:
                messages.error(request, "Email/Senha estão incorretos")
                return render(request, 'usuarios/login.html')
        else:
            messages.error(request, "Email/Senha estão incorretos")
            return render(request, 'usuarios/login.html')
    return render(request, 'usuarios/login.html')

def logout(request):
    """Realiza logout do usuário"""
    auth.logout(request)
    return redirect('home')

def cadastro(request):
    """Cadastra usuário"""
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha1 = request.POST['senha1']
        senha2 = request.POST['senha2']
        if nome == '' or senha1 == '' or email == '':
            return redirect('cadastro')
        if senha1 != senha2:
            messages.error(request, 'As senhas não são iguais')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário com esse email já existe')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Usuário com esse nome já existe')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha1)
        messages.success(request, 'Usuário cadastrado com sucesso')
        return redirect('login')
    return render(request, 'usuarios/cadastro.html')

@login_required
def perfil(request):
    """Atualiza dados de perfil do usuário"""
    usuario = get_object_or_404(User, pk=request.user.pk)
    form = PerfilForm(request.POST or None, instance=usuario)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso')
            return redirect('perfil')
    return render(request, 'usuarios/perfil/atualizar-perfil.html', { 'form' : form })

@login_required
def alterar_senha(request):
    """Alteração de senha do usuário"""
    if request.POST:
        senha_atual = request.POST['senha_atual']
        senha_nova = request.POST['senha1']
        senha_confirmacao = request.POST['senha2']
        if senha_nova != senha_confirmacao:
            messages.error(request, 'Senhas não são iguais')
            return redirect('alterar_senha')
        if not senha_atual or not senha_nova:
            messages.error(request, 'Campos Senha atual e Nova senha são obrigatórios')
            return redirect('alterar_senha')
        usuario = User.objects.get(pk=request.user.pk)
        if not usuario.check_password(senha_atual):
            messages.error(request, 'Senha atual está incorreta')
            return redirect('alterar_senha')         
        usuario.set_password(senha_nova)
        usuario.save()
        messages.success(request, 'Senha atualizada com sucesso')
        return redirect('login')
    return render(request, 'usuarios/perfil/alterar-senha.html')

@login_required
def pedidos(request):
    """Pedidos do usuário"""
    pedidos = Pedido.objects.filter(usuario=request.user)
    paginator = Paginator(pedidos, 5)
    page = request.GET.get('page')
    pedidos_por_pagina = paginator.get_page(page)

    dados = {
        'pedidos': pedidos_por_pagina
    }
    return render(request, 'usuarios/perfil/pedidos.html', dados)