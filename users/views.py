from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, render, redirect
# from allauth.account.views import SignupView, LoginView, PasswordResetView, LogoutView


# def profile(request, user_id):
#     context = {
#         'user': get_object_or_404(User, id=user_id),
#     }
#
#     return render(request, 'users/profile_info_page.html', context)
#
# class MySignup(SignupView):
#     template_name = 'users/signup_page.html'
#
#
# class MyLoginView(LoginView):
#     template_name = 'users/login_page.html'
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import RegisterUserForm, LoginUserForm
from users.models import UserProfile


class RegisterUser(CreateView):
    """View for User registration"""

    form_class = RegisterUserForm
    template_name = 'users/signup_page.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """Redirection to Home page in case of successful registration"""

        user = form.save()
        user_profile = UserProfile()
        user_profile.user = user
        user_profile.birthday_date = form.cleaned_data['birthday_date']
        user_profile.save()
        login(self.request, user)
        return redirect('main_page')


class LoginUser(LoginView):
    """View for User login"""

    form_class = LoginUserForm
    template_name = 'users/login_page.html'

    def get_success_url(self):
        return reverse_lazy('main_page')


def logout_user(request):
    """View for User logout"""

    logout(request)
    return redirect('login')



