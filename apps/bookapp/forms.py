from django import forms
from django.forms import ModelForm
from .models import User

class RegisterForm(forms.Form):
    username = forms.CharField(
        label= '用户名',
        max_length = 32,
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入您的用户名'
            }
        )
    )

    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入您的邮箱'
            }
        )
    )

    password1 = forms.CharField(
        label='密码',
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入您的密码'
            }
        )
    )

    password2 = forms.CharField(
        label='确认密码',
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请确认您的密码'
            }
        )
    )

