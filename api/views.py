from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from game.models import Game, Genre, Platform, UserFavouriteGame, Screenshot, Cover
from api.serializers import GameSerializer, GenreSerializer, PlatformSerializer, ScreenshotSerializer, CoverSerializer, \
    UserFavouriteGameSerializer, MainPageGamesSetPagination, UserSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


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


class GameView(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    pagination_class = MainPageGamesSetPagination


class FUGView(viewsets.ModelViewSet):
    queryset = UserFavouriteGame.objects.all()
    serializer_class = UserFavouriteGameSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class FavouriteViewSet(viewsets.ModelViewSet):
#     serializer_class = GameSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return Game.objects.filter(favourite_games__is_deleted=False, favourite_games__user=self.request.user)


class FavouriteViewSet(viewsets.ModelViewSet):
    serializer_class = UserFavouriteGameSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserFavouriteGame.objects.filter(user=self.request.user, is_deleted=False)

    def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # if UserFavouriteGame.objects.filter(game__id=request.data['id']).first():

        if int(request.data['game']) in list(UserFavouriteGame.objects.filter(
                user=request.user).values_list('game', flat=True)):
            serializer = UserFavouriteGameSerializer(
                UserFavouriteGame.objects.filter(user=request.user, game__id=request.data['game']).first(),
                data=request.data
            )
            print('exists')
        else:
            # serializer = UserFavouriteGameSerializer(data=request.data)
            serializer = self.get_serializer(data=request.data)
            print('not exists')

        if serializer.is_valid():
            # serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # def create(self, request, *args, **kwargs):
        #     serializer = self.get_serializer(data=request.data)
        #     serializer.is_valid(raise_exception=True)
        #     self.perform_create(serializer)
        #     headers = self.get_success_headers(serializer.data)
        #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # game = UserFavouriteGame.get_or_create(request.data['id'])
        # serializer = SnippetSerializer(snippet, data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    # def put(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     serializer = SnippetSerializer(snippet, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def create(self, request, *args, **kwargs):
    #     many = True if isinstance(request.data, list) else False
    #     serializer = BookSerializer(data=request.data, many=many)
    #     serializer.is_valid(raise_exception=True)
    #     author = request.user  # you can change here
    #     book_list = [Book(**data, author=author) for data in serializer.validated_data]
    #     Book.objects.bulk_create(book_list)
    #     return Response({}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_deleted=False)


@api_view(['POST'])
def favourites(request, *args, **kwargs):
    if request.method == 'POST':
        print(request.body)
        print(args)
        print(kwargs)

        favourite_games = UserFavouriteGame.objects.all()
        serializer = UserFavouriteGameSerializer(favourite_games, many=True)
        return Response(serializer.data)


class UserFavouriteGamesList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        games = UserFavouriteGame.objects.filter(user=self.request.user, is_deleted=False)
        serializer = UserFavouriteGameSerializer(games, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     # {"action": "add", "games_ids": [123]}
    #     action = request.data['action']
    #     games_ids = request.data['games_ids']
    #
    #     if action == "add":
    #
    #     print(action)
    #     print(type(action))
    #     print(games_ids)
    #     print(type(games_ids))
    #     serializer = UserFavouriteGameSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

