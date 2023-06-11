from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your Username',
        'class': "w-full py-4 px-6 rounded-xl"
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your Name',
        'class': "w-full py-4 px-6 rounded-xl"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your Surname',
        'class': "w-full py-4 px-6 rounded-xl"
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your Email Address',
        'class': "w-full py-4 px-6 rounded-xl"
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your Password',
        'class': "w-full py-4 px-6 rounded-xl"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your Password Again',
        'class': "w-full py-4 px-6 rounded-xl"
    }))


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your Username',
        'class': "w-full py-4 px-6 rounded-xl"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your Password',
        'class': "w-full py-4 px-6 rounded-xl"
    }))
