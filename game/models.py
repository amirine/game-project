from django.contrib.auth.models import User
from django.db import models
from game.igdb_wrapper import IGDBRequestsHandler


class Game(models.Model):
    game_id = models.IntegerField()

    def get_game_info_musts(self):
        igdb = IGDBRequestsHandler()
        return igdb.get_musts_page_info(self.game_id)

    def get_active_users_number(self):
        return self.favourites.filter(is_deleted=False).count()

    def __str__(self):
        return f'{self.game_id}'


class UsersFavouriteGames(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'favourites'

    def __str__(self):
        return f'{self.user.username} {self.game.game_id} {self.is_deleted}'
