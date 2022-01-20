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
        fields = ['id', 'name', 'genres', 'platforms', 'total_rating', 'summary', 'first_release_date', 'rating',
                  'rating_count', 'aggregated_rating', 'aggregated_rating_count']

    def to_representation(self, instance):
        """Ensures only not null keys are displayed"""

        result = super().to_representation(instance)
        return {key: result[key] for key in result if result[key]}


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre Model"""

    class Meta:
        model = Genre
        fields = ['id', 'name']


class PlatformSerializer(serializers.ModelSerializer):
    """Serializer for Platform Model"""

    class Meta:
        model = Platform
        fields = ['id', 'name', 'abbreviation']

    def to_representation(self, instance):
        """Ensures only not null keys are displayed"""

        result = super().to_representation(instance)
        return {key: result[key] for key in result if result[key]}


class ScreenshotSerializer(serializers.ModelSerializer):
    """Serializer for Screenshot Model"""

    class Meta:
        model = Screenshot
        fields = ['id', 'image_id', 'game']


class CoverSerializer(serializers.ModelSerializer):
    """Serializer for Cover Model"""

    class Meta:
        model = Cover
        fields = ['id', 'image_id', 'game']


class FavouritesPostSerializer(serializers.Serializer):
    """
    Serializer created to validate POST method body for FavouritesAPIView. Takes {action} and {game_ids} values from
    POST request and checks their correctness.
    """

    action = serializers.ChoiceField(choices=["add", "delete"])
    game_ids = serializers.ListField()

    def validate(self, data):
        """
        Validates incoming games according to the action: prohibits adding games that already exist in user's musts or
        don't exist in Games database, prohibits deleting games not added to user's musts.
        """

        def exists_in_database(game_id: int) -> bool:
            """Checks game existence in database by id"""

            return Game.objects.filter(id=game_id).exists()

        def exists_in_user_musts(game_id: int, user=self.context['user']) -> bool:
            """Checks game existence in {user}'s musts by id"""

            return UserFavouriteGame.objects.filter(game__id=game_id, user=user, is_deleted=False).exists()

        for game_id in data["game_ids"]:

            if data["action"] == "add" and not exists_in_database(game_id):
                raise serializers.ValidationError(detail=f"Game {game_id} doesn't exist in database.")

            if data["action"] == "add" and exists_in_user_musts(game_id):
                raise serializers.ValidationError(detail=f"Game {game_id} already exists in user's musts.")

            if data["action"] == "delete" and not exists_in_user_musts(game_id):
                raise serializers.ValidationError(detail=f"Game {game_id} isn't added to user's musts.")

        return data
