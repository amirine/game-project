from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from users.models import UserProfile


# class CustomSignupForm(SignupForm):
#     birthday_date = forms.DateField(label='Birthday')
#     first_name = forms.CharField(max_length=40, label='First Name')
#     last_name = forms.CharField(max_length=40, label='Last Name')
#
#     def save(self, request):
#         user = super(CustomSignupForm, self).save(request)
#         user_profile = UserProfile()
#         user_profile.user = user
#         user_profile.birthday_date = self.cleaned_data['birthday_date']
#         user.save()
#         user_profile.save()
#         return user

class RegisterUserForm(UserCreationForm):
    """Form for User registration"""

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-horizontal form-group','placeholder': 'Enter username here...'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-horizontal form-group', 'placeholder': 'Enter email here...'}),
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-horizontal', 'placeholder': 'Enter first name here...'}),
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-horizontal', 'placeholder': 'Enter last name here...'}),
    )
    birthday_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter birthday here...'}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password here...'}),
        label='Password',
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password...'}),
        label='Confirm password',
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user_profile = UserProfile()
    #     user_profile.user = user
    #     user_profile.birthday_date = self.cleaned_data['birthday_date']
    #     if commit:
    #         user.save()
    #         user_profile.save()
    #     return user


class LoginUserForm(AuthenticationForm):
    """Form for User login"""

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username here...'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password here...'})
    )
