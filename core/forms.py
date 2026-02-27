from.import models
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['username', 'email', 'password']
