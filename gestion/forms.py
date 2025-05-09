from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Membre, User, Classe


class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'prenom', 'age', 'telephone']

    def __init__(self, *args, **kwargs):
        super(MembreForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Entrez {field.label.lower()}'
            })
            field.label_suffix = ' :'


User = get_user_model()

class CreateMoniteurForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mot de passe'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Email"}),
        }


class AssignMoniteurForm(forms.Form):
    moniteur = forms.ModelChoiceField(
        queryset=User.objects.filter(role='moniteur'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    classe = forms.ModelChoiceField(
        queryset=Classe.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
