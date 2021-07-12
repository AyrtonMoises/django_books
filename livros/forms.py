from django.forms import ModelForm
from django.forms.widgets import TextInput

from .models import Categoria


class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'cor': TextInput(attrs={'type': 'color'}),
        }