from django.contrib.auth.models import User
from django.db import models
from game.igdb_wrapper import IGDBRequestsHandler


class NotSoftDeletedGameManager(models.Manager):
    """Manager for filtered objects display: gets games not soft deleted"""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Game(models.Model):
    """Game model"""

    game_id = models.IntegerField()

    def get_game_info_musts(self):
        """Gets game info for must page by game_id"""

        igdb = IGDBRequestsHandler()
        return igdb.get_musts_page_info(self.game_id)

    def get_active_users_number(self):
        return self.favourites.filter(is_deleted=False).count()

    def __str__(self):
        return f'{self.game_id}'


class UserFavouriteGame(models.Model):
    """Model for user - favourite game pairs (soft deleted or not) """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()
    not_deleted_objects = NotSoftDeletedGameManager()

    class Meta:
        default_related_name = 'favourites'

    def __str__(self):
        return f'{self.user.username} {self.game.game_id} {self.is_deleted}'
