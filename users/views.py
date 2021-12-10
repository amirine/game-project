from django.views.generic import TemplateView
from django.contrib.auth.models import User


class ProfileView(TemplateView):
    """View for user profile"""

    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(id=kwargs["user_id"])
