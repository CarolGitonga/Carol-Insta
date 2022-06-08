from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', 'image_name', 'caption')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['profile','post']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')