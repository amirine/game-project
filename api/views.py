from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from game.models import Game, Genre, Platform, UserFavouriteGame, Screenshot, Cover
from api.serializers import GameSerializer, GenreSerializer, PlatformSerializer, ScreenshotSerializer, CoverSerializer, \
    UserFavouriteGameSerializer, MainPageGamesSetPagination, MustsPageGamesSetPagination


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    pagination_class = MainPageGamesSetPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


class ScreenshotViewSet(viewsets.ModelViewSet):
    queryset = Screenshot.objects.all()
    serializer_class = ScreenshotSerializer


class CoverViewSet(viewsets.ModelViewSet):
    queryset = Cover.objects.all()
    serializer_class = CoverSerializer


class FavouriteViewSet(viewsets.ModelViewSet):
    serializer_class = UserFavouriteGameSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MustsPageGamesSetPagination

    def get_queryset(self):
        return UserFavouriteGame.objects.filter(user=self.request.user, is_deleted=False)

    def get_object_(self, obj_id, user):
        return UserFavouriteGame.objects.get_or_create(game_id=obj_id, user=user)[0]

    def validate_ids(self, game_ids, user, action):
        #     {"action": "add","ids": [47,563]}
        if action == "add":
            for id in game_ids:
                if not Game.objects.filter(id=id).first():
                    return [False, {"detail": f"Game {id} doesn't exist in database."}]
                elif UserFavouriteGame.objects.filter(game__id=id, user=user, is_deleted=False).first():
                    return [False, {"detail": f"Game {id} is already in user musts."}]
            return [True, None]

        elif action == "delete":
            for id in game_ids:
                if not UserFavouriteGame.objects.filter(game__id=id, user=user, is_deleted=False).first():
                    return [False, {"detail": f"Game {id} isn't added to current user musts."}]
            return [True, None]

    def create(self, request, *args, **kwargs):
        print(request.data)
        id_list = request.data['ids']
        action = request.data['action']
        instances = []

        is_valid, errors = self.validate_ids(id_list, request.user, action)
        if is_valid:
            for id in id_list:
                obj = self.get_object_(obj_id=id, user=request.user)
                obj.is_deleted = not obj.is_deleted
                obj.save()
                instances.append(obj)
            serializer = UserFavouriteGameSerializer(instances, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)
