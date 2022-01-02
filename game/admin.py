from django.contrib import admin

from game.models import Game, Genre, Platform, GameNew, Screenshot, UserFavouriteGameNew
from game.models import UserFavouriteGame

admin.site.register(Game)
admin.site.register(UserFavouriteGame)
admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(GameNew)
admin.site.register(Screenshot)
admin.site.register(UserFavouriteGameNew)
