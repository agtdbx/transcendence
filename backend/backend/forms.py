from django import forms
from db_test.models import User

class UserForm(forms.ModelForm):
 
    class Meta:
        model = User
        fields = ['profilPicture']
