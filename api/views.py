from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from game.models import Game, Genre, Platform, UserFavouriteGame, Screenshot, Cover
from api.serializers import GameSerializer, GenreSerializer, PlatformSerializer, ScreenshotSerializer, CoverSerializer, \
    MainPageGamesSetPagination, MustsPageGamesSetPagination, FavouritesPostSerializer


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


class FavouritesAPIView(APIView, MustsPageGamesSetPagination):
    """
    APIView for user's favourite games display. GET and POST methods available only for authorized users:
    user can view their musts (GET method), add and delete games from musts (POST method).
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Gets authorized user's favourite games. Returns entries from Game Model.
        """

        games = self.paginate_queryset(
            Game.objects.filter(favourite_games__user=self.request.user, favourite_games__is_deleted=False), request
        )
        serializer = GameSerializer(games, many=True)
        return self.get_paginated_response(serializer.data)

    @staticmethod
    def post(request, *args, **kwargs):
        """
        Performs action with games listed in POST request body: adds games to or deletes games from authorized
        user's musts (executes soft delete in case of "delete" action). Validates incoming game ids.

        POST request body format:
        {
            "action": <action to perform in string format> (available actions: "add", "delete")
            "game_ids": <list of game ids>
        }
        """

        serializer = FavouritesPostSerializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        instances = []

        for game_id in request.data['game_ids']:
            user_game, created = UserFavouriteGame.objects.get_or_create(game_id=game_id, user=request.user)
            if not created:
                user_game.is_deleted = not user_game.is_deleted
                user_game.save()
            instances.append(Game.objects.get(id=game_id))
        serializer = GameSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
