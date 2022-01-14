from django.contrib.auth.models import User
from rest_framework import viewsets, status, views
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, GenericViewSet

from game.models import Game, Genre, Platform, UserFavouriteGame, Screenshot, Cover
from api.serializers import GameSerializer, GenreSerializer, PlatformSerializer, ScreenshotSerializer, CoverSerializer, \
    MainPageGamesSetPagination, MustsPageGamesSetPagination


class GameViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Games display. GET method is available for all users: authorized and unauthorized.
    POST, DELETE and PUT can be performed only by admin user.
    """

    queryset = Game.objects.all()
    serializer_class = GameSerializer
    pagination_class = MainPageGamesSetPagination
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class GenreViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Genres display. GET method is available for all users: authorized and unauthorized.
    POST, DELETE and PUT can be performed only by admin user.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class PlatformViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Platforms display. GET method is available for all users: authorized and unauthorized.
    POST, DELETE and PUT can be performed only by admin user.
    """

    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class ScreenshotViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Screenshots display. GET method is available for all users: authorized and unauthorized.
    POST, DELETE and PUT can be performed only by admin user.
    """

    queryset = Screenshot.objects.all()
    serializer_class = ScreenshotSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class CoverViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Covers display. GET method is available for all users: authorized and unauthorized.
    POST, DELETE and PUT can be performed only by admin user.
    """

    queryset = Cover.objects.all()
    serializer_class = CoverSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


# class FavouriteAPIView(APIView):
class FavouriteAPIView(APIView, MustsPageGamesSetPagination):
    """
    APIView for authorized user's favourite games display. GET and POST methods available:
    user can view their musts (GET method), add and delete games from musts (POST method).
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Gets authorized user's favourite games. Returns entries from Game Model.
        """

        games = self.paginate_queryset(Game.objects.filter(favourite_games__user=self.request.user,
                                                           favourite_games__is_deleted=False), request)
        serializer = GameSerializer(games, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Performs action with games listed in POST request body: adds games to or deletes games from authorized
        user's musts (executes soft delete in case of "delete" action). Validates incoming game ids.

        POST request body format:
        {
            "action": <action to perform in string format> (available actions: "add", "delete")
            "game_ids": <list of game ids>
        }
        """

        self.validate_request()
        game_ids = request.data.get('game_ids', None)
        action = request.data.get('action', None)
        instances = []

        for game_id in game_ids:
            self.validate_game_id(game_id, request.user, action)
            user_game, created = UserFavouriteGame.objects.get_or_create(game_id=game_id, user=request.user)
            if not created:
                user_game.is_deleted = not user_game.is_deleted
                user_game.save()
            instances.append(Game.objects.get(id=game_id))
        serializer = GameSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def validate_game_id(game_id: int, user: User, action: str) -> None:
        """
        Validates incoming game by its {game_id} according to {action}: prohibits adding games that already exist in
        {user}'s musts or doesn't exist in Games database, prohibits deleting games not added to {user}'s musts.
        """

        def exists_in_database(game_id: int) -> bool:
            """Checks game existence in database by id"""

            return Game.objects.filter(id=game_id).first()

        def exists_in_user_musts(game_id: int, user: User) -> bool:
            """Checks game existence in {user}'s musts by id"""

            return UserFavouriteGame.objects.filter(game__id=id, user=user, is_deleted=False).first()

        if action == "add" and not exists_in_database(game_id):
            raise ValidationError(detail=f"Game {id} doesn't exist in database.")

        if action == "add" and exists_in_user_musts(game_id, user):
            raise ValidationError(detail=f"Game {id} is already in user musts.")

        if action == "delete" and not exists_in_user_musts(game_id, user):
            raise ValidationError(detail=f"Game {id} isn't added to current user musts.")

    def validate_request(self):
        action = self.request.data.get('action', None)
        game_ids = self.request.data.get('game_ids', None)

        if len(self.request.data) != 2:
            raise ValidationError(detail=f"Input dict size is not correct.")

        if action is None or game_ids is None:
            raise ValidationError(detail=f"Null fields values.")

        if action not in ['add', 'delete'] or not isinstance(action, str):
            raise ValidationError(detail=f"Error action value.")

        if not isinstance(game_ids, list):
            raise ValidationError(detail=f"Not list value in game_ids field.")

