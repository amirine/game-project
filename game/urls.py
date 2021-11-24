from django.contrib import admin
from django.urls import path

from .views import MainPageView, DetailPageView

urlpatterns = [
    path('main_page/', MainPageView.as_view(), name='main_page'),
    path('detail_page/', DetailPageView.as_view(), name='detail_page'),
]
