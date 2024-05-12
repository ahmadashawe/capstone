from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext, gettext_lazy as _
from django import forms
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import Employee
from django.contrib.auth.models import User

class EmployeeSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    birthdate = forms.DateField(required=True)
    joining_date = forms.DateField(required=True)
    phone = forms.CharField(max_length=155, required=True)
    pic = forms.ImageField(required=False)
    country = CountryField().formfield(
        widget=CountrySelectWidget(attrs={'class': 'form-control', 'class' : 'form-select'})
    )
    department = forms.CharField(max_length=100, required=True)
    role = forms.CharField(max_length=100, required=True)
    years_of_exp = forms.IntegerField(min_value=0, required=True)
    overtime_hours = forms.IntegerField(min_value=0, required=False)
    teach_course = forms.CharField(max_length=100, required=False)
    hours_worked_per_week = forms.IntegerField(min_value=0, required=False)
    
    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'email', 'birthdate', 'joining_date', 'phone', 'country', 'department', 'role', 'years_of_exp','overtime_hours')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@upm.edu.sa'):
            raise ValidationError("Email must end with '@upm.edu.sa'.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if user.role == 'Teaching':
            user.teach_course = self.cleaned_data.get('teach_course')
            user.hours_worked_per_week = self.cleaned_data.get('hours_worked_per_week')
        if commit:
            user.save()
        return user





class LoginForm(AuthenticationForm):
    email = forms.EmailField(
        max_length=255,
        validators=[
            EmailValidator(
                message='Wrong Email',
                code='invalid_email'
            ),
        ],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']  

    class Meta:
        model = Employee
        fields = ['email', 'password']


