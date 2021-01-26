from django import forms 
from .models import Address, Job, UserPicture

class AddressForm(forms.ModelForm):
    
    class Meta:
        model = Address
        fields = ('__all__')


class JobForm(forms.ModelForm):
    
    class Meta:
        model = Job
        # fields = ("",)
        fields = ('__all__')


class UserPictureForm(forms.ModelForm):
    
    class Meta:
        model = UserPicture
        # fields = ("",)
        fields = ('__all__')



