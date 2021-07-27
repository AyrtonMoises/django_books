from django import forms

from django.contrib.auth import get_user_model


class PerfilForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=254, 
        required=True, 
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    username = forms.CharField(
        label="Nome",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']