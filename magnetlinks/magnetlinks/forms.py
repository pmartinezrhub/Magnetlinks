from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError  
from .models import MagnetLink
from captcha.fields import CaptchaField
import re

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    captcha = CaptchaField()
    

class RegisterForm(UserCreationForm):
    captcha = CaptchaField()
    class Meta:
        model=User
        fields = ['username','password1','password2'] 


class MagnetLinkForm(forms.ModelForm):
    
    captcha = CaptchaField()

    class Meta:
        model = MagnetLink
        fields = ['title', 'magnetlink', 'description', 'imagelink']
        widgets = {
            'title': forms.TextInput(attrs={'size': 60}),
            'magnetlink': forms.TextInput(attrs={'placeholder': 'magnet link or hash', 'size': 60}),
            'description': forms.Textarea(attrs={'class': 'long-input', 'rows': 8}),
            'imagelink': forms.URLInput(attrs={'placeholder': 'Enter image URL', 'size': 60}),
        }

    MAGNET_REGEX = r"^magnet:\?xt=urn:btih:[A-Fa-f0-9]{40}(&.*)?$"
    HASH_REGEX = r"^[A-Fa-f0-9]{40}$"

    def clean(self):
        cleaned_data = super().clean()
        magnetlink = cleaned_data.get("magnetlink")

        
        if not magnetlink:
            raise ValidationError("You must provide either a valid magnet link or a 40-character hexadecimal hash.")
        
        if re.match(self.MAGNET_REGEX, magnetlink):
            return cleaned_data  

        if re.match(self.HASH_REGEX, magnetlink):
            return cleaned_data  

        print(magnetlink)
        raise ValidationError("The 'magnetlink' must be a valid magnet link or a 40-character hexadecimal hash.")
