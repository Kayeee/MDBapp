from django import forms
import models

class SignupForm(forms.ModelForm):
    class Meta:
        model = models.MDBUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'date_of_birth']
