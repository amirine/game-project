from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from game.models import Game, Genre, Platform, Screenshot, Cover, UserFavouriteGame
from django.conf import settings


class MainPageGamesSetPagination(PageNumberPagination):
    """Sets games limit per page displayed on Main Page"""

    page_size = settings.GAMES_PER_PAGE_MAIN


class MustsPageGamesSetPagination(PageNumberPagination):
    """Sets games limit per page displayed on Musts Page"""

    page_size = settings.GAMES_PER_PAGE_MUSTS


class GameSerializer(serializers.ModelSerializer):
    """Serializer for Game Model"""

    class Meta:
        model = Game
        fields = '__all__'
        # depth = 1

    def to_representation(self, instance):
        """Ensures only not null keys are displayed"""

        result = super(GameSerializer, self).to_representation(instance)
        return {key: result[key] for key in result if result[key]}


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre Model"""

    class Meta:
        model = Genre
        fields = '__all__'


class PlatformSerializer(serializers.ModelSerializer):
    """Serializer for Platform Model"""

    class Meta:
        model = Platform
        fields = '__all__'

    def to_representation(self, instance):
        """Ensures only not null keys are displayed"""

        result = super(PlatformSerializer, self).to_representation(instance)
        return {key: result[key] for key in result if result[key]}


class ScreenshotSerializer(serializers.ModelSerializer):
    """Serializer for Screenshot Model"""

    class Meta:
        model = Screenshot
        fields = '__all__'


class CoverSerializer(serializers.ModelSerializer):
    """Serializer for Cover Model"""

    class Meta:
        model = Cover
        fields = '__all__'

# class CustomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Media
#         read_only_fields = ('id', 'karma', 'createdByUser', 'creationDate')
