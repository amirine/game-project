from django.shortcuts import render
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = 'game/main_page.html'


class DetailPageView(TemplateView):
    template_name = 'game/game_detail_page.html'
