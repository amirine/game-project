import users.models
from django.db import models

# Create your models here.
from game.igdb_wrapper import IGDBRequestsHandler


class FavouriteGames(models.Model):
    user = models.ForeignKey(users.models.User, on_delete=models.CASCADE)
    game_id = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    def get_game_info(self):
        igdb = IGDBRequestsHandler()
        return igdb.get_musts_page_info(self.game_id)

    def __str__(self):
        return f'{self.game_id} {self.is_deleted}'
