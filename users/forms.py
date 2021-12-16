from django import forms
from allauth.account.forms import SignupForm, LoginForm
from users.models import UserProfile


class CustomSignupForm(SignupForm):
    """Overridden Signup Form from django-allauth: new placeholders implemented"""

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter username here...'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email here...'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter first name here...'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter last name here...'}))
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Enter birthday here...'}))

    def __init__(self, *args, **kwargs):
        """Customizing password fields: placeholders and labels modified"""

        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password here...'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password...'
        self.fields['password2'].label = 'Confirm Password'

    def save(self, request):
        """Saves User model fields and birthday one-to-one-field"""

        user = super(CustomSignupForm, self).save(request)
        user_profile = UserProfile()
        user_profile.user = user
        user_profile.birthday = self.cleaned_data['birthday']
        user.save()
        user_profile.save()
        return user


class CustomLoginForm(LoginForm):
    """Overridden Login Form from django-allauth: new placeholders implemented"""

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs['placeholder'] = 'Enter username here...'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter password here...'
