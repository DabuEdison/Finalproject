from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_passwords_match(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('confirm_password'):
            self.add_error('confirm_password', "Passwords do not match.")

    def is_valid(self):
        valid = super().is_valid()
        if valid:
            self.validate_passwords_match()
        return super().is_valid()
