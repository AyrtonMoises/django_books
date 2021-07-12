from django.contrib import admin

from .models import Editora, Autor, Categoria, Livro

from .forms import CategoriaForm

class LivroAdmin(admin.ModelAdmin):
    readonly_fields = ["data_criacao"]
    list_display = ('id','descricao','editora','autor','valor','ativo',)
    list_display_links = ('id', 'descricao',)
    search_fields = ('descricao',)
    list_filter = ('categorias',)
    list_editable = ('ativo',)
    list_per_page = 10


class CategoriaAdmin(admin.ModelAdmin):
    form = CategoriaForm
    fieldsets = (
        (None, {
            'fields': ('descricao', 'cor')
            }),
        )

admin.site.register(Editora)
admin.site.register(Autor)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Livro, LivroAdmin)
