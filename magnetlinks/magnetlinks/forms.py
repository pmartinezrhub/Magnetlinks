from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError  
from django.contrib.auth import password_validation
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
    MAGNET_REGEX = r"^magnet:\?xt=urn:btih:[A-Fa-f0-9]{40}(&.*)?$"
    HASH_REGEX = r"^[A-Fa-f0-9]{40}$"
    
    class Meta:
        model = MagnetLink
        fields = ['category',  'magnetlink', 'description', 'imagelink']
        CATEGORY_CHOICES = [
            ('movies', 'Movies'),
            ('music', 'Music'),
            ('ames', 'Games'),
            ('software', 'Software'),
        ]

        widgets = {
            #'title': forms.TextInput(attrs={'size': 60}),
            'magnetlink': forms.TextInput(attrs={'placeholder': 'magnet link or BTIH', 'size': 60}),
            'description': forms.Textarea(attrs={'class': 'long-input', 'rows': 8}),
            'imagelink': forms.URLInput(attrs={'placeholder': 'Enter image URL', 'size': 60}),
            'category': forms.Select(attrs={'class': 'dropdown', 'default': 'Files'}),
        }

    
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

class AccountForm(forms.ModelForm):
    oldpassword = forms.CharField(required=False, max_length=65, widget=forms.PasswordInput, label="Old password")
    newpassword = forms.CharField(required=False, max_length=65, widget=forms.PasswordInput, label="New password")
    repeatpassword = forms.CharField(required=False, max_length=65, widget=forms.PasswordInput, label="Repeat password")
    delete_account = forms.BooleanField(required=False, label="Delete my account")
    confirm_delete = forms.CharField(required=False, label="Type DELETE to confirm", max_length=10)
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        deleting = cleaned_data.get('delete_account')
        oldpassword = cleaned_data.get('oldpassword')
        newpassword = cleaned_data.get('newpassword')

        # Caso: Eliminar cuenta
        if deleting:
            if self.user.username == "admin":
                raise forms.ValidationError("The admin account cannot be deleted.")
            confirm_text = cleaned_data.get('confirm_delete', '').strip()
            if confirm_text != 'DELETE':
                raise forms.ValidationError("To delete your account, type DELETE in the confirmation field.")
        
        # Caso: Cambiar contraseña
        else:
            if not oldpassword:
                raise forms.ValidationError("Old password is required.")
            if not newpassword:
                raise forms.ValidationError("New password is required.")
            if not self.user.check_password(oldpassword):
                raise forms.ValidationError("Old password is incorrect.")

        return cleaned_data

    def save(self, commit=True):
        if self.cleaned_data.get('delete_account'):
            self.user.delete()
            return None
        else:
            self.user.set_password(self.cleaned_data['newpassword'])
            if commit:
                self.user.save()
            return self.user
