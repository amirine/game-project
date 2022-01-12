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
        user = User.objects.filter(id=request.user.id)
        serializer = UserSerializer(user, many=True)
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

    #
    # def post(self, request, format=None):
    #     serializer = UserFavouriteGameSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
# class OrganisationApiView(APIView):
#
#     serializers_class = serializers.OrganisationSerializer
#     parser_classes = [JSONParser]
#
#     def get(self, request, formate=None):
#         return Response({"message": "You are Cool!!"})
#
#     def post(self, request, formate=None):
#         serializer = self.serializers_class(data=request.data)
#         print(serializer)
#
#         if serializer.is_valid():
#             organisation_name = serializer.validated_data.get('organisation_name')
#             message = f"Reached POST {organisation_name}"
#             return Response({'message': message, status: 'HTTP_200_OK'})
#         else:
#             return Response(
#                 serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
