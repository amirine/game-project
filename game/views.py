from django.shortcuts import render
from django.views import View
from django.views.generic.base import ContextMixin
from game.igdb_wrapper import IGDBRequestsHandler
from game.twitter_wrapper import TwitterWrapper
from django.core.paginator import Paginator


class MainPageView(ContextMixin, View):
    games_per_page = 6
    max_games_number = 18

    def get(self, request):
        """Processes GET request to main page: displays games from database"""

        igdb = IGDBRequestsHandler()
        filters = request.session.get('filters', None)
        print('session get ', filters)
        games = igdb.get_game_main_page_info(MainPageView.max_games_number, filters)

        context = {
            'page_obj': pagination_generate(request, games, MainPageView.games_per_page),
            'genres': igdb.get_genres(),
            'platforms': igdb.get_platforms(),
            'chosen_genres': list(map(int, filters.get('genres'))) if filters else None,
            'chosen_platforms': list(map(int, filters.get('platforms'))) if filters else None,
            'chosen_lower_rating_bound': filters.get('lower_rating_bound') if filters else None,
            'chosen_upper_rating_bound': filters.get('upper_rating_bound') if filters else None,
        }

        return render(request, 'game/main_page.html', context)

    def post(self, request):
        """Processes POST request to main page: displays games filtered"""

        igdb = IGDBRequestsHandler()

        filters = {
            'lower_rating_bound': request.POST.get('rating-begin'),
            'upper_rating_bound': request.POST.get('rating-end'),
            'genres': request.POST.getlist('genres', list(map(lambda genre: str(genre['id']), igdb.get_genres()))),
            'platforms': request.POST.getlist('platforms',
                                              list(map(lambda genre: str(genre['id']), igdb.get_platforms()))),
        }

        request.session['filters'] = filters
        print('session post', request.session['filters'])
        print(filters)

        games = igdb.get_game_main_page_info(MainPageView.max_games_number, filters)

        context = {
            'page_obj': pagination_generate(request, games, MainPageView.games_per_page),
            'genres': igdb.get_genres(),
            'platforms': igdb.get_platforms(),
            'chosen_genres': list(map(int, filters['genres'])),
            'chosen_platforms': list(map(int, filters['platforms'])),
            'chosen_lower_rating_bound': filters['lower_rating_bound'],
            'chosen_upper_rating_bound': filters['upper_rating_bound'],
        }

        return render(request, 'game/main_page.html', context)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['test'] = 'hello'
    #     return context

    def generate_context(self, request, games, igdb, filters):
        """Generates context for main page"""

        return {
            'page_obj': pagination_generate(request, games, MainPageView.games_per_page),
            'genres': igdb.get_genres(),
            'platforms': igdb.get_platforms(),
            'chosen_genres': list(map(int, filters.get('genres'))) if filters else None,
            'chosen_platforms': list(map(int, filters.get('platforms'))) if filters else None,
            'chosen_lower_rating_bound': filters.get('lower_rating_bound') if filters else None,
            'chosen_upper_rating_bound': filters.get('upper_rating_bound') if filters else None,
        }


class MainPageViewSearch(View):

    def get(self, request):
        igdb = IGDBRequestsHandler()
        request.session['search_game_name'] = request.GET.get('search-data') or request.session.get('search_game_name')
        games = igdb.get_game_search_info(request.session.get('search_game_name'), MainPageView.max_games_number)

        context = {
            'page_obj': pagination_generate(request, games, MainPageView.games_per_page),
            'genres': igdb.get_genres(),
            'platforms': igdb.get_platforms(),
        }

        return render(request, 'game/main_page.html', context)


class DetailPageView(View):

    def get(self, request, game_id):
        igdb = IGDBRequestsHandler()
        tweets = TwitterWrapper()
        game = igdb.get_game_detail_page_info(game_id)

        context = {
            'game': game,
            'tweets': tweets.request_return_handle(game['name'], 5),
        }

        return render(request, 'game/game_detail_page.html', context)


def pagination_generate(request, games: list, games_per_page: int) -> Paginator:
    """Generates page object for the games display"""

    paginator = Paginator(games, games_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj
