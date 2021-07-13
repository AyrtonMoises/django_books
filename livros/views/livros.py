from django.shortcuts import render

from livros.models import Livro, Autor, Categoria, Editora


def home(request):
    """Home do site com principais destaques"""
    livros = Livro.objects.filter(ativo=True).order_by('-id')[:4]
    autores = Autor.objects.filter(ativo=True).order_by('-id')[:8]
    categorias = Categoria.objects.all()
    dados = { 
        'livros': livros,
        'autores': autores,
        'categorias': categorias
    }
    return render(request, 'livros/home/index.html', dados)


def autores(request):
    """Lista de autores cadastrados"""
    autores = Autor.objects.filter(ativo=True)
    dados = { 
        'autores': autores
    }
    return render(request, 'livros/autores/index.html', dados)

def categorias(request):
    """Lista de categorias cadastrados"""
    categorias = Categoria.objects.all()
    dados = { 
        'categorias': categorias
    }
    return render(request, 'livros/categorias/index.html', dados)

def livros_por_autor(request, autor_id):
    """Lista de livros por autor"""
    livros = Livro.objects.filter(ativo=True, autor__pk=autor_id)
    dados = {
        'livros': livros
    }
    return render(request, 'livros/livros/index.html', dados)

def livros_por_categoria(request, categoria_id):
    """Lista de livros por categoria"""
    livros = Livro.objects.filter(ativo=True, categorias__pk=categoria_id)
    dados = {
        'livros': livros
    }
    return render(request, 'livros/livros/index.html', dados)
