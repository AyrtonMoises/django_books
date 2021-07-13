from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth import get_user_model


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
                return redirect('home')
            else:
                messages.error(request, "Email ou Senha está incorreto")
                return render(request, 'usuarios/login.html')
        else:
            messages.error(request, "Email ou Senha está incorreto")
            return render(request, 'usuarios/login.html')
    return render(request, 'usuarios/login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha1 = request.POST['senha1']
        senha2 = request.POST['senha2']
        if nome == '' or senha1 == '':
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
