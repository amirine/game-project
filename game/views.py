from django.shortcuts import render
from django.views import View
from game.igdb_wrapper import BasicIGDBRequestsHandler
from game.twitter_wrapper import TwitterWrapper
from django.core.paginator import Paginator


class MainPageView(View):

    games_per_page = 6
    max_games_number = 18

    def get(self, request):
        """Processes GET request to main page: displays games from database"""

        igdb = BasicIGDBRequestsHandler()
        games = igdb.get_game_main_page_info(MainPageView.max_games_number)
        print(games)
        paginator = Paginator(games, MainPageView.games_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'genres': igdb.get_genres(),
            'platforms': igdb.get_platforms(),
        }

        return render(request, 'game/main_page.html', context)

    def post(self, request):
        """Processes POST request to main page: displays games filtered by checkbox"""

        igdb = BasicIGDBRequestsHandler()

        filters = {
            'lower_rating_bound': request.POST['rating-begin'],
            'upper_rating_bound': request.POST['rating-end'],
            'genres': request.POST.getlist('genres'),
            'platforms': request.POST.getlist('platforms'),
        }

        games = igdb.get_game_main_page_info(MainPageView.max_games_number, filters)
        paginator = Paginator(games, MainPageView.games_per_page)
        page_number = request.POST.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'genres': igdb.get_genres(),
            'platforms': igdb.get_platforms(),
            'chosen_genres': list(map(int, filters['genres'])),
            'chosen_platforms': list(map(int, filters['platforms'])),
            'chosen_lower_rating_bound': filters['lower_rating_bound'],
            'chosen_upper_rating_bound': filters['upper_rating_bound'],
        }

        return render(request, 'game/main_page.html', context)

    @staticmethod
    def pagination_generate(request, games: list, games_per_page: int):
        """Generates page object for the games display"""

        paginator = Paginator(games, games_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return page_obj


class DetailPageView(View):

    def get(self, request, game_id):
        igdb = BasicIGDBRequestsHandler()
        tweets = TwitterWrapper()
        game = igdb.get_game_detail_page_info(game_id)

        context = {
            'game': game,
            'tweets': tweets.request_return_handle(game['name'], 5),
        }

        return render(request, 'game/game_detail_page.html', context)
