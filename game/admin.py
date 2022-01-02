from django.contrib import admin

from game.models import Game
from game.models import UserFavouriteGame

admin.site.register(Game)
admin.site.register(UserFavouriteGame)
