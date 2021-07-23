from django.shortcuts import render
from django.db.models import Q

from livros.models import Livro, Autor, Editora


def busca(request):
    """Página de busca retornando autores, livros ou editoras"""
    livros = Livro.objects.filter(ativo=True)
    autores = Autor.objects.filter(ativo=True)
    q =  request.GET.get('q','')
    if q:
        livros = livros.filter(
            (
                Q(descricao__icontains=q) | 
                Q(editora__descricao__icontains=q) |
                Q(autor__nome__icontains=q) 
            )
        )
    dados = { 
        'livros': livros
    }
    return render(request, 'livros/busca.html', dados)