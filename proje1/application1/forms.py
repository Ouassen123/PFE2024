from django import forms
from .models import Livre, Auteur

class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = '__all__'

class AuteurForm(forms.ModelForm):
    date_naissance = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']
    )
    class Meta:
        model = Auteur
        fields = '__all__'