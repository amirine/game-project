from django.urls import path
from users.views import LoginUser, RegisterUser, logout_user
# from allauth.account.views import logout

# urlpatterns = [
#     path('<int:user_id>/', profile, name='profile_info'),
#     path('signup/', MySignup.as_view(), name='account_signup'),
#     path('login/', MyLoginView.as_view(), name='account_login'),
#     path("logout/", logout, name="account_logout"),
# ]

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
]
