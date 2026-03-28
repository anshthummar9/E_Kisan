from django import forms
from .models import SoilReport

SOIL_CHOICES = [
    ('Black', 'Black'),
    ('Red', 'Red'),
    ('Medium Brown', 'Medium Brown'),
    ('Dark Brown', 'Dark Brown'),
    ('Light Brown', 'Light Brown'),
    ('Reddish Brown', 'Reddish Brown'),
]

class SoilAnalysisForm(forms.ModelForm):
    city = forms.CharField(max_length=100, help_text="Enter your city to fetch weather data automatically.")
    
    class Meta:
        model = SoilReport
        fields = ['soil_color', 'nitrogen', 'phosphorus', 'potassium', 'ph', 'city']
        widgets = {
            'soil_color': forms.Select(choices=SOIL_CHOICES, attrs={'class': 'form-select'}),
            'nitrogen': forms.NumberInput(attrs={'class': 'form-control'}),
            'phosphorus': forms.NumberInput(attrs={'class': 'form-control'}),
            'potassium': forms.NumberInput(attrs={'class': 'form-control'}),
            'ph': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }
