from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del Pokémon',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción del Pokémon'
            })
        }
        labels = {
            'title': 'Nombre',
            'description': 'Descripción'
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or title.strip() == '':
            raise forms.ValidationError("El nombre es requerido.")
        return title.strip().title()