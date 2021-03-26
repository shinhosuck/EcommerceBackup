from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from users.models import Profile
from django import forms



class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User 
        fields = [
            "username", 
            "first_name", 
            "last_name", 
            "email", 
            "password1", 
            "password2"
        ]


class UpdateUserInfoForm(forms.ModelForm):

    class Meta:
        model=User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email"
        ]


class UpdateProfileInfoForm(forms.ModelForm):

    class Meta:
        model=Profile 
        fields = ["image"]