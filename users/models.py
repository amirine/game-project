from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class UserProfile(models.Model):
    """Model for user: class User extended by birthday field"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField('Birthday')

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return self.user.username

    def get_current_age(self):
        """Gets current age of the user by birhday date"""

        today = datetime.now()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
