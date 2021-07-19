from django.shortcuts import render
from django.db.models import Q

from livros.models import Livro, Autor, Editora


def busca(request):
    """Página de busca retornando autores, livros ou editoras"""
    livros = Livro.objects.filter(ativo=True)
    autores = Autor.objects.filter(ativo=True)
    if 'palavra_buscada' in request.GET:
        if request.GET['palavra_buscada'] != '':
            palavra_buscada = request.GET['palavra_buscada']
            livros = livros.filter(
                        (
                            Q(descricao__icontains=palavra_buscada) | 
                            Q(editora__descricao__icontains=palavra_buscada) |
                            Q(autor__nome__icontains=palavra_buscada) 
                        )
                    )
    dados = { 
        'livros': livros
    }
    return render(request, 'livros/busca/index.html', dados)