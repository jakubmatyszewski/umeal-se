from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    re_password = forms.CharField(
        label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_re_password(self):
        cd = self.cleaned_data
        if cd["password"] != cd["re_password"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["re_password"]