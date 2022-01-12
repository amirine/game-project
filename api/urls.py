from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import GameViewSet, GenreViewSet, PlatformViewSet, ScreenshotViewSet, CoverViewSet, \
    favourites, UserFavouriteGamesList, FUGView, UserViewSet

router = DefaultRouter()
router.register(r'api-games', GameViewSet)
router.register(r'api-genres', GenreViewSet)
router.register(r'api-platforms', PlatformViewSet)
router.register(r'api-screenshots', ScreenshotViewSet)
router.register(r'api-covers', CoverViewSet)
router.register(r'api-fuv', FUGView)
router.register(r'api-user', UserViewSet)
# router.register(r'api-test', UserFavouriteGamesList)

# router.register(r'api-favourites1', UserFavouriteGamesList)

urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    path('favourites/', favourites),
    path('test/', UserFavouriteGamesList.as_view()),
]
