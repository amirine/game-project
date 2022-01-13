from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from game.models import Game, Genre, Platform, Screenshot, Cover, UserFavouriteGame
from django.conf import settings


class MainPageGamesSetPagination(PageNumberPagination):
    page_size = settings.GAMES_PER_PAGE_MAIN


class MustsPageGamesSetPagination(PageNumberPagination):
    page_size = settings.GAMES_PER_PAGE_MUSTS


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        result = super(GameSerializer, self).to_representation(instance)
        return {key: result[key] for key in result if result[key]}

    # def __init__(self, instance=None, data=None, **kwargs):
    #     if instance:
    #         setattr(self.Meta, 'depth', 1)
    #     else:
    #         setattr(self.Meta, 'depth', 0)
    #     super(GameSerializer, self).__init__(instance, data, **kwargs)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'

    def to_representation(self, instance):
        result = super(PlatformSerializer, self).to_representation(instance)
        return {key: result[key] for key in result if result[key]}


class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        fields = '__all__'


class CoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cover
        fields = '__all__'


class UserFavouriteGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavouriteGame
        fields = ['game']
        # depth = 1


class UserSerializer(serializers.ModelSerializer):
    favourite_games1 = serializers.SerializerMethodField('get_cars')

    def get_cars(self, user):
        game_queryset = User.objects.filter(favourite_games__is_deleted=False).values('id')
        serializer = GameSerializer(instance=game_queryset, many=True, context=self.context)

        return serializer.data

    #
    # favourite_games_deleted = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=UserFavouriteGame.objects.filter(is_deleted=True)
    # )

    class Meta:
        model = User
        fields = ['id', 'username', 'favourite_games1']
