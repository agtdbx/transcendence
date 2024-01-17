from django import forms
from db_test.models import User

class UserForm(forms.ModelForm):
 
    class Meta:
        model = User
        fields = ['profilPicture']
        
class PasswordForm(forms.Form):
    currentPassword = forms.CharField()
    newPassword = forms.CharField()
    confirmNewPassword = forms.CharField()
