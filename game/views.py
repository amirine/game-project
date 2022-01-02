from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from game.igdb_wrapper import IGDBRequestsHandler
from game.models import Game, GameNew, Genre, Platform, UserFavouriteGameNew
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

        games = GameNew.objects.all()
        context = {
            'page_obj': pagination_generate(request, games, MainPageView.GAMES_PER_PAGE),
            'genres': Genre.objects.all(),
            'platforms': Platform.objects.all(),
        }

        if request.user.is_authenticated:
            context.update({
                'user_favourite_games': list(UserFavouriteGameNew.objects.filter(
                    user=request.user, is_deleted=False).values_list('game', flat=True))
            })
        # print(UserFavouriteGameNew.objects.filter(user=request.user, is_deleted=False).values_list('game', flat=True))
        # print(GameNew.objects.get(id=85031))
        # print(85031 in UserFavouriteGameNew.objects.filter(user=request.user, is_deleted=False).values_list('game'))
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

        filters = request.session.get('filters')
        context = self.generate_context(request, filters)
        return render(request, 'game/main_page.html', context)

    def post(self, request):
        """Processes POST request to main page: displays games filtered after filters apply"""

        filters = {
            'lower_rating_bound': request.POST.get('rating-begin'),
            'upper_rating_bound': request.POST.get('rating-end'),
            'genres': request.POST.getlist('genres'),
            'platforms': request.POST.getlist('platforms'),
        }

        request.session['filters'] = filters
        context = self.generate_context(request, filters)
        return render(request, 'game/main_page.html', context)

    @staticmethod
    def generate_context(request, filters: dict) -> dict:
        """Generates context for pages"""

        games = GameNew.objects.filter(
            total_rating__lte=filters['upper_rating_bound'],
            total_rating__gte=filters['lower_rating_bound'],
            genres__id__in=list(map(int, filters.get('genres'))),
            platforms__id__in=list(map(int, filters.get('platforms'))),
        )
        return {
            'page_obj': pagination_generate(request, games, MainPageViewFilter.GAMES_PER_PAGE),
            'genres': Genre.objects.all(),
            'platforms': Platform.objects.all(),
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

        # igdb = IGDBRequestsHandler()
        tweets = TwitterWrapper()
        game = GameNew.objects.get(id=game_id)

        context = {
            'game': game,
            'tweets': tweets.request_return_handle(game.name, DetailPageView.TWEETS_LIMIT),
        }

        if request.user.is_authenticated:
            context.update({
                # 'is_added': game_id in list(request.user.favourites.filter(is_deleted=False).
                #                             values_list('game__game_id', flat=True))
                'is_added': UserFavouriteGameNew.objects.filter(
                    user=request.user, is_deleted=False, game__id=game_id).exists()
            })

        return render(request, 'game/game_detail_page.html', context)

    def post(self, request, game_id):
        """
        Adds game to favourites on must button click, deletes game from favourites on unmust button click.
        Works on both main and musts pages must buttons.
        """

        if UserFavouriteGameNew.objects.filter(user=request.user, game__id=game_id).exists():
            current_game = request.user.favourite_games.get(game__id=game_id)
            current_game.is_deleted = not current_game.is_deleted
            current_game.save()
        else:
            current_game = GameNew.objects.get(id=game_id)
            request.user.favourite_games.create(game=current_game, user=request.user)

        return HttpResponse(status=200)


class MustsPageView(View):
    """
    View for musts page: displays favourite user games with the opportunity to soft delete items.
    Soft delete and add performed by button unmust/must click.
    """

    GAMES_LIMIT = 18
    GAMES_PER_PAGE = 12

    @staticmethod
    def get(request):
        """Gets favourite user games (soft deleted items are not displayed)"""

        # favourite_games = request.user.favourites.filter(is_deleted=False)
        # context = {
        #     'page_obj': pagination_generate(request, favourite_games, MustsPageView.GAMES_PER_PAGE),
        # }

        favourite_games = request.user.favourite_games.filter(is_deleted=False)
        context = {
            'page_obj': pagination_generate(request, favourite_games, MustsPageView.GAMES_PER_PAGE),
        }

        return render(request, 'game/musts_page.html', context)

    def post(self, request):
        """
        Soft deletes or adds to favourites again on button click: soft deleted items displayed.
        After page reloading - get method - soft deleted items no more displayed.
        """

        game_id = int(request.POST['game_id'])

        current_user_game = request.user.favourite_games.get(game__id=game_id)
        current_user_game.is_deleted = not current_user_game.is_deleted
        current_user_game.save()

        return HttpResponse(status=200)


def pagination_generate(request, games: list, games_per_page: int) -> Paginator:
    """Generates page object for the games pagination"""

    paginator = Paginator(games, games_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj
