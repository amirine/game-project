from django.urls import path
from .views import MainPageView, DetailPageView, MainPageViewSearch, MainPageViewFilter, MustsPageView

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('main_page/search/', MainPageViewSearch.as_view(), name='main_page_search'),
    path('main_page/filter/', MainPageViewFilter.as_view(), name='main_page_filter'),
    path('detail_page/<int:game_id>/', DetailPageView.as_view(), name='detail_page'),
    path('musts_page/', MustsPageView.as_view(), name='musts_page'),
]
