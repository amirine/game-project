from django.contrib.auth.models import User
from django.db import models


class Platform(models.Model):
    """Model for game platforms"""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    abbreviation = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']


class Genre(models.Model):
    """Model for game genres"""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']


class Game(models.Model):
    """Model for games"""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40, blank=True)
    genres = models.ManyToManyField(Genre)
    platforms = models.ManyToManyField(Platform)
    total_rating = models.FloatField(null=True, blank=True)
    summary = models.TextField(blank=True)
    first_release_date = models.DateField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    rating_count = models.IntegerField(null=True, blank=True)
    aggregated_rating = models.FloatField(null=True, blank=True)
    aggregated_rating_count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.id} {self.name}'

    class Meta:
        ordering = ['-first_release_date']


class Screenshot(models.Model):
    """Model for game screenshots"""

    id = models.IntegerField(primary_key=True)
    image_id = models.URLField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return f'Screen {self.id}'


class UserFavouriteGame(models.Model):
    """Model for user - favourite game pairs (soft deleted or not)"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'favourite_games'

    def __str__(self):
        return f'{self.user.username} {self.game.name} {self.is_deleted}'


class Cover(models.Model):
    """Model for game cover"""

    id = models.IntegerField(primary_key=True)
    image_id = models.URLField()
    game = models.OneToOneField(Game, on_delete=models.CASCADE)

    def __str__(self):
        return f'Cover {self.id}'
