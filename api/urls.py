from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import GameViewSet, GenreViewSet, PlatformViewSet, ScreenshotViewSet, CoverViewSet, \
    FavouriteAPIView

router = DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'platforms', PlatformViewSet)
router.register(r'screenshots', ScreenshotViewSet)
router.register(r'covers', CoverViewSet)
# router.register(r'favourites', FavouriteViewSet, 'favourites')
# router.register(r'test1', FavouriteAPIView, 'test1')


urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    path('test/', FavouriteAPIView.as_view())
]
