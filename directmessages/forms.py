from django import forms 

from .models import DirectMessage

class DirectMessageForm(forms.ModelForm):
    
    class Meta:
        model = DirectMessage
        fields = ("receiver","subject", "body")
        widgets = {
            'body': forms.Textarea(attrs={'cols':50, 'rows': 10}),
        }
