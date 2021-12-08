from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday_date = models.DateField('Birthday')

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return self.user.username

    USERNAME_FIELD = 'user.username'
