from django import forms
from .models import Route


class RouterForm(forms.ModelForm):
    original_url = forms.URLField(
        widget=forms.URLInput(attrs={'placeholder': 'Enter the URL you want to shorten'})
    )
    class Meta:
        model = Route
        fields = ['original_url',]

