from django.urls import path
from .views import MainPageView, DetailPageView, MainPageViewSearch

urlpatterns = [
    path('main_page/', MainPageView.as_view(), name='main_page'),
    path('main_page_search/', MainPageViewSearch.as_view(), name='main_page_search'),
    path('detail_page/<int:game_id>/', DetailPageView.as_view(), name='detail_page'),
]
