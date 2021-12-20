from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from game.igdb_wrapper import IGDBRequestsHandler
from game.models import UsersFavouriteGames, Game
from game.twitter_wrapper import TwitterWrapper
from django.core.paginator import Paginator


class MainPageView(View):
    """
    View for main page: displays main page without any filters.
    Called by initial page entering and by navbar logo click.
    """

    GAMES_LIMIT = 18
    GAMES_PER_PAGE = 6

    @staticmethod
    def get(request):
        """Gets games from database not filtered"""

        igdb = IGDBRequestsHandler()
        games = igdb.get_game_main_page_info(MainPageView.GAMES_LIMIT)
        context = {
            'page_obj': pagination_generate(request, games, MainPageView.GAMES_PER_PAGE),
            'genres': igdb.get_genres(),
            'platforms': igdb.get_platforms(),
        }
        return render(request, 'game/main_page.html', context)


class MainPageViewFilter(View):
    """
    View for main page with applied filters: handles requests after 'Apply' button click,
    displayed in filters sidebar area. Get method handles pagination.
    """

    GAMES_LIMIT = 18
    GAMES_PER_PAGE = 6

    def get(self, request):
        """Processes GET request to main page: displays games from database filtered by pages"""

        igdb = IGDBRequestsHandler()
        filters = request.session.get('filters')
        context = self.generate_context(request, igdb, filters)
        return render(request, 'game/main_page.html', context)

    def post(self, request):
        """Processes POST request to main page: displays games filtered after filters apply"""

        igdb = IGDBRequestsHandler()
        filters = {
            'lower_rating_bound': request.POST.get('rating-begin'),
            'upper_rating_bound': request.POST.get('rating-end'),
            'genres': request.POST.getlist('genres'),
            'platforms': request.POST.getlist('platforms'),
        }

        request.session['filters'] = filters
        context = self.generate_context(request, igdb, filters)
        return render(request, 'game/main_page.html', context)

    @staticmethod
    def generate_context(request, igdb: IGDBRequestsHandler, filters: dict) -> dict:
        """Generates context for pages"""

        games = igdb.get_game_main_page_info(MainPageViewFilter.GAMES_LIMIT, filters)
        return {
            'page_obj': pagination_generate(request, games, MainPageViewFilter.GAMES_PER_PAGE),
            'genres': igdb.get_genres(),
            'platforms': igdb.get_platforms(),
            'chosen_genres': list(map(int, filters.get('genres'))),
            'chosen_platforms': list(map(int, filters.get('platforms'))),
            'chosen_lower_rating_bound': filters.get('lower_rating_bound'),
            'chosen_upper_rating_bound': filters.get('upper_rating_bound'),
        }


class MainPageViewSearch(View):
    """
    View for search input processing. Search starts after input and Enter click.
    Performed by the name of the game.
    """

    GAMES_LIMIT = 18
    GAMES_PER_PAGE = 6

    @staticmethod
    def get(request):
        """Gets IGDB data using search input"""

        igdb = IGDBRequestsHandler()
        request.session['search_game'] = request.GET.get('search-data') or request.session.get('search_game')
        games = igdb.get_game_search_info(request.session.get('search_game'), MainPageViewSearch.GAMES_LIMIT)

        context = {
            'page_obj': pagination_generate(request, games, MainPageViewSearch.GAMES_PER_PAGE),
            'genres': igdb.get_genres(),
            'platforms': igdb.get_platforms(),
        }

        return render(request, 'game/main_page.html', context)


class DetailPageView(View):
    """
    View for detail page: displays wider info about the games.
    Games are followed by the tweets, containing hashtags with their names.
    Games can be added to musts on must button click.
    """

    TWEETS_LIMIT = 5

    @staticmethod
    def get(request, game_id):
        """Gets game info by id and returns template"""

        igdb = IGDBRequestsHandler()
        tweets = TwitterWrapper()
        game = igdb.get_game_detail_page_info(game_id)

        context = {
            'game': game,
            'tweets': tweets.request_return_handle(game['name'], DetailPageView.TWEETS_LIMIT),
            'is_added': game_id in list(request.user.favourites.values_list('game__game_id', flat=True)),
        }

        return render(request, 'game/game_detail_page.html', context)

    def post(self, request, game_id):
        """
        Adds game to favourites on must button click,
        deletes game from favourites on unmust button click
        """

        if game_id not in list(request.user.favourites.values_list('game__game_id', flat=True)):
            current_game, created = Game.objects.get_or_create(game_id=game_id)
            request.user.favourites.create(game=current_game, user=request.user)
        else:
            request.user.favourites.get(game__game_id=game_id).delete()

        return HttpResponse(200)


class MustsPageView(View):
    """
    View for musts page: displays favourite user games with the opportunity to soft delete items.
    Soft delete and add performed by button unmust/must click.
    """

    GAMES_LIMIT = 18
    GAMES_PER_PAGE = 12

    @staticmethod
    def get(request):
        """Gets favourite user games (soft deleted items are deleted completely) """

        request.user.favourites.filter(is_deleted=True).delete()
        favourite_games = request.user.favourites.all()
        context = {
            'page_obj': pagination_generate(request, favourite_games, MustsPageView.GAMES_PER_PAGE),
        }

        return render(request, 'game/musts_page.html', context)

    def post(self, request):
        """
        Soft deletes or adds to favourites again on button click: soft deleted items displayed.
        (After page reloading - get method - soft deleted items are deleted completely and no more displayed)
        """

        game_id = int(request.POST['game_id'])

        current_user_game = request.user.favourites.get(game__game_id=game_id)
        current_user_game.is_deleted = not current_user_game.is_deleted
        current_user_game.save()

        return HttpResponse(200)


def pagination_generate(request, games: list, games_per_page: int) -> Paginator:
    """Generates page object for the games pagination"""

    paginator = Paginator(games, games_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj
