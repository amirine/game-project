from django.contrib import admin

from game.models import Game, Genre, Platform, Screenshot, UserFavouriteGame, Cover

admin.site.register(Game)
admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(Screenshot)
admin.site.register(Cover)
admin.site.register(UserFavouriteGame)
