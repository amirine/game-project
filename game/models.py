from django.contrib.auth.models import User
from django.db import models

from game.igdb_wrapper import IGDBRequestsHandler
from game.twitter_wrapper import TwitterWrapper


class Game(models.Model):
    game_id = models.IntegerField()

    def get_game_info_musts(self):
        igdb = IGDBRequestsHandler()
        return igdb.get_musts_page_info(self.game_id)

    def get_game_info_detail(self):
        igdb = IGDBRequestsHandler()
        return igdb.get_game_detail_page_info(self.game_id)

    def get_game_info_tweets(self, tweets_limit):
        igdb = IGDBRequestsHandler()
        game = igdb.get_musts_page_info(self.game_id)
        tweets = TwitterWrapper()
        return tweets.request_return_handle(game['name'], tweets_limit)

    def get_active_users_number(self):
        # current_game = Game.objects.get(game_id=self.game_id)
        return self.usersfavouritegames_set.filter(is_deleted=False).count()




    def __str__(self):
        return f'{self.game_id}'


class UsersFavouriteGames(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} {self.game.game_id} {self.is_deleted}'
