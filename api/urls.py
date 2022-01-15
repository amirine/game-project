from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import GameViewSet, GenreViewSet, PlatformViewSet, ScreenshotViewSet, CoverViewSet, FavouritesAPIView

router = DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'platforms', PlatformViewSet)
router.register(r'screenshots', ScreenshotViewSet)
router.register(r'covers', CoverViewSet)

urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    path('favourites/', FavouritesAPIView.as_view(), name='favourites')
]
