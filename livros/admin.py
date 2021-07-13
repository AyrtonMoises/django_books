from django.contrib import admin

from .models import Editora, Autor, Categoria, Livro

from .forms import CategoriaForm, LivroForm


class EditoraAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'ativa',)
    list_display_links = ('id', 'descricao',)
    search_fields = ('descricao', 'id',)
    list_editable = ('ativa',)
    list_per_page = 15


class AutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'ativo',)
    list_display_links = ('id', 'nome',)
    list_editable = ('ativo',)
    list_filter = ('ativo',)

    list_per_page = 15


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao',)
    list_editable = ('descricao',)
    form = CategoriaForm
    ordering = ['id', ]


class LivroAdmin(admin.ModelAdmin):
    readonly_fields = ["data_criacao"]
    list_display = ('id', 'descricao', 'editora', 'autor', 'valor', 'ativo',)
    list_display_links = ('id', 'descricao',)
    list_filter = ('categorias',)
    list_editable = ('ativo',)
    list_per_page = 15
    form = LivroForm
    fieldsets = (
        ('Principais informações', {
            'fields': ('imagem', 'descricao', 'detalhes', 'ean', 'autor',
                       'editora', 'categorias', ('ano', 'edicao'),
                       'encadernacao', ('idioma', 'pais'),)
        }),
        ('Disponibilidade e valor', {
            'fields': ('valor', 'ativo',)
        })
    )

admin.site.register(Editora, EditoraAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Livro, LivroAdmin)
