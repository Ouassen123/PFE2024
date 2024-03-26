# forms.py

from django import forms
from .models import JobOffer

class JobOfferForm(forms.ModelForm):
    class Meta:
        model = JobOffer
        fields = ['title', 'description', 'required_experience']
