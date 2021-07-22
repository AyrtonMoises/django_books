from django.forms import ModelForm
from django.forms.widgets import TextInput, CheckboxSelectMultiple

from .models import Categoria, Livro


class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'cor': TextInput(attrs={'type': 'color'}),
        }


class LivroForm(ModelForm):
    class Meta:
        model = Livro
        fields = '__all__'
        widgets = {
            'categorias': CheckboxSelectMultiple,
        }