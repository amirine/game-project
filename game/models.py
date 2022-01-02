from django.contrib.auth.models import User
from django.db import models
from game.igdb_wrapper import IGDBRequestsHandler


class Game(models.Model):
    """Game model"""

    game_id = models.IntegerField()

    def get_game_info_by_id(self):
        """Gets game info for must page by game_id"""

        igdb = IGDBRequestsHandler()
        return igdb.get_musts_page_info(self.game_id)

    def __str__(self):
        return f'{self.game_id}'


class UserFavouriteGame(models.Model):
    """Model for user - favourite game pairs (soft deleted or not)"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'favourites'

    def __str__(self):
        return f'{self.user.username} {self.game.game_id} {self.is_deleted}'


class Platform(models.Model):
    """Model for game platforms"""

    id = models.IntegerField(primary_key=True)
    abbreviation = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.abbreviation}'


class Genre(models.Model):
    """Model for game genres"""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.name}'


class GameNew(models.Model):
    """Model for games"""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40, null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    platforms = models.ManyToManyField(Platform)
    cover_id = models.URLField(null=True, blank=True)
    total_rating = models.FloatField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    first_release_date = models.DateField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    rating_count = models.IntegerField(null=True, blank=True)
    aggregated_rating = models.FloatField(null=True, blank=True)
    aggregated_rating_count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Screenshot(models.Model):
    """Model for game screenshots"""

    id = models.IntegerField(primary_key=True)
    image_id = models.URLField()
    game = models.ForeignKey(GameNew, on_delete=models.CASCADE)

    def __str__(self):
        return f'Screen {self.id} for game {self.game_id}'

class UserFavouriteGameNew(models.Model):
    """Model for user - favourite game pairs (soft deleted or not)"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(GameNew, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'favourite_games'

    def __str__(self):
        return f'{self.user.username} {self.game.name} {self.is_deleted}'
