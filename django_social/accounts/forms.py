from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

class UserCreationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(),label="Confirm password")
    class Meta: 
        model = User
        fields = ("phone_number","email","password","password2")

    def clean_password2(self):
        p1 = self.cleaned_data.get("password")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2 :
            raise ValidationError("Passwords must match !!!")
        return p2
    

    def save(self, commit = True):
        user =  super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ("phone_number","email","password","is_active","is_admin")