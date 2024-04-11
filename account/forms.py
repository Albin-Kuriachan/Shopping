from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from account.models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField \
        (widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Email'}))
    password = forms.CharField \
        (widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Password'}))





# class RegisterForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['email', 'password','first_name', 'last_name']
#         widgets = {
#             'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'autocomplete': 'off'}),
#             'password': forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder':'Password'}),
#             # 'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
#             'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
#         }



class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control fakePassword', 'autocomplete': 'off', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'autocomplete': 'off'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }


class PasswordResetForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control fakePassword', 'autocomplete': 'off', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email', 'autocomplete': 'off', 'disabled': True}),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']