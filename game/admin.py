from django.contrib import admin

from game.models import Game
from game.models import UsersFavouriteGames

admin.site.register(Game)
admin.site.register(UsersFavouriteGames)
