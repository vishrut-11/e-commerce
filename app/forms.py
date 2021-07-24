from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer

class CustomerRegistrationform(UserCreationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"placeholder": "Enter Your Unique username", "class":"form-control"}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={"placeholder": "Enter Your Email","class":"form-control"}))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={"placeholder": "Enter Your Password", "class":"form-control"}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={"placeholder": "Confrim Your Password", "class":"form-control"}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1' ,'password2']
        labels = {'email': 'Email'}
        

class Loginform(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"placeholder": "Enter Your username", 'autofocus': True, "class":"form-control"}))
    password = forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={"placeholder": "Enter Your Password", "autocomplete":"current-password", "class":"form-control"}))

class Mypasswordchangeform(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True, "class":"form-control"}),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your New Pasword", "autocomplete":"new-password", "class":"form-control"}),  
        help_text=password_validation.password_validators_help_text_html(),    
    )

    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Your Password", "autocomplete":"new-password", "class":"form-control"}),
    )

class MypasswordResetform(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"placeholder": "Enter your Email", 'autocomplete': 'email', "class":"form-control"}),
    )


class Mysetpasswordform(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', "class":"form-control"}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', "class":"form-control"}),
    )

class CustomerProfileform(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "locality", "city", "state", "zipcode"]
        widgets = {"name":forms.TextInput(attrs={"placeholder": "Enter Your Name", "class":"form-control"}),
                    "locality":forms.TextInput(attrs={"placeholder": "Enter Your locality", "class":"form-control"}),
                    "city":forms.TextInput(attrs={"placeholder": "Enter Your city", "class":"form-control"}),
                    "state":forms.Select(attrs={"placeholder": "Choose Your state", "class":"form-control"}),
                    "zipcode":forms.NumberInput(attrs={"placeholder": "Enter Your zipcode", "class":"form-control"})}
