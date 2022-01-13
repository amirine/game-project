from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import GameViewSet, GenreViewSet, PlatformViewSet, ScreenshotViewSet, CoverViewSet, FavouriteViewSet

router = DefaultRouter()
router.register(r'api-games', GameViewSet)
router.register(r'api-genres', GenreViewSet)
router.register(r'api-platforms', PlatformViewSet)
router.register(r'api-screenshots', ScreenshotViewSet)
router.register(r'api-covers', CoverViewSet)
router.register(r'api-test', FavouriteViewSet, 'favourites')

urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
]
