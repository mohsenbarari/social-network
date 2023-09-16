from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User



class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"your username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"your email"}))
    password1 = forms.CharField(label="password",widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"your password"}))
    password2 = forms.CharField(label="confirm password",widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"confirm password"}))


    def clean(self):
        cd = super().clean()
        p1 = cd["password1"]
        p2 = cd["password2"]
        if p1 and p2 and p1 != p2:
            raise ValidationError("your password does not match")
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("Your email is already registered")
        return email
    
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("Your username is already registered")
        return username





