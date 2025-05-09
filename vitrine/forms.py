from django import forms
from .models import MessageContact
from .models import RencontreQuotidienne

class RencontreForm(forms.ModelForm):
    class Meta:
        model = RencontreQuotidienne
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RencontreForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Entrez {field.label.lower()}'
            })
            field.label_suffix = ' :'

class ContactForm(forms.ModelForm):
    class Meta:
        model = MessageContact
        fields = ['nom', 'email', 'sujet', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
