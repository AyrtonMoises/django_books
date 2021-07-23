from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page

from livros.models import Livro, Autor, Categoria, Editora


@cache_page(60 * 5)
def home(request):
    """Home do site com principais destaques"""
    livros = Livro.objects.filter(ativo=True).order_by('-id')[:6]
    autores = Autor.objects.filter(ativo=True).order_by('-id')[:6]
    categorias = Categoria.objects.all()
    dados = { 
        'livros': livros,
        'autores': autores,
        'categorias': categorias
    }
    return render(request, 'livros/home/index.html', dados)

@cache_page(60 * 60)
def autores(request):
    """Lista de autores cadastrados"""
    autores = Autor.objects.filter(ativo=True)
    dados = { 
        'autores': autores
    }
    return render(request, 'livros/autores.html', dados)

@cache_page(60 * 60 * 24)
def categorias(request):
    """Lista de categorias cadastrados"""
    categorias = Categoria.objects.all()
    dados = { 
        'categorias': categorias
    }
    return render(request, 'livros/categorias.html', dados)

@cache_page(60 * 60)
def livros_por_autor(request, autor_id):
    """Lista de livros por autor"""
    livros = Livro.objects.filter(
        ativo=True, autor__pk=autor_id
        ).order_by('-ano','-ativo')
    dados = {
        'livros': livros
    }
    return render(request, 'livros/livros_lista.html', dados)

@cache_page(60 * 60)
def livros_por_editora(request, editora_id):
    """Lista de livros pela editora"""
    livros = Livro.objects.filter(
        ativo=True, editora__pk=editora_id
        ).order_by('-ano','-ativo')
    dados = {
        'livros': livros
    }
    return render(request, 'livros/livros_lista.html', dados)

@cache_page(60 * 60)
def livros_por_categoria(request, categoria_id):
    """Lista de livros por categoria"""
    livros = Livro.objects.filter(
            ativo=True, categorias__pk=categoria_id
            ).order_by('-ativo')
    dados = {
        'livros': livros
    }
    return render(request, 'livros/livros_lista.html', dados)

@cache_page(60 * 60)
def livro_detalhes(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id, ativo=True)
    dados = {
        'livro': livro
    }
    return render(request, 'livros/livro_detalhes.html', dados)