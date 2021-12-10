from django.urls import path
from users.views import ProfileView

urlpatterns = [
    path('<int:user_id>/', ProfileView.as_view(), name='profile_info'),
]
