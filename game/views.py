from django.shortcuts import render, redirect
from django.views import View
from game.igdb_wrapper import IGDBRequestsHandler
from game.models import UsersFavouriteGames, Game
from game.twitter_wrapper import TwitterWrapper
from django.core.paginator import Paginator
from django.db.models import F


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
            'is_added': False,
        }

        # current_game = Game.objects.get_or_create(game_id=game_id)
        if game_id in list(request.user.usersfavouritegames_set.values_list('game__game_id', flat=True)):
            context.update({'is_soft_deleted': request.user.usersfavouritegames_set.get(game__game_id=game_id).is_deleted,
                            'is_added': True})
        # if game_id in [el.game_id for el in request.user.favouritegames_set.all()]:
        #     context.update({'is_soft_deleted': request.user.favouritegames_set.get(game_id=game_id).is_deleted,
        #                     'is_added': True})

        return render(request, 'game/game_detail_page.html', context)

    def post(self, request, game_id):
        """Gets game info by id and returns template"""

        print("i'm in")

        # current_game = FavouriteGames(game_id=game_id)
        # current_game, created = Game.objects.get_or_create(game_id=game_id)
        # print(type(current_game))
        print(list(request.user.usersfavouritegames_set.values_list('game__game_id', flat=True)))
        if game_id not in list(request.user.usersfavouritegames_set.values_list('game__game_id', flat=True)):
            current_game, created = Game.objects.get_or_create(game_id=game_id)
            user_game = UsersFavouriteGames.objects.create(game=current_game, user=request.user)
            request.user.usersfavouritegames_set.add(user_game)
            # current_game.usersfavouritegames_set.add(user_game)
            print(UsersFavouriteGames.objects.filter(game__game_id=game_id))
            print(current_game.usersfavouritegames_set.all())
            print('1')
        else:
            # current_game = Game.objects.create(game_id=game_id)
            current_user_game = request.user.usersfavouritegames_set.get(game__game_id=game_id)
            current_user_game.is_deleted = not current_user_game.is_deleted
            current_user_game.save()
            current_game = Game.objects.get(game_id=game_id)
            print(current_game)
            print(current_game.usersfavouritegames_set.all())
            print('2')

        return redirect('detail_page', game_id)


def pagination_generate(request, games: list, games_per_page: int) -> Paginator:
    """Generates page object for the games pagination"""

    paginator = Paginator(games, games_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


class MustsPageView(View):
    """
    View for main page: displays main page without any filters.
    Called by initial page entering and by navbar logo click.
    """

    GAMES_LIMIT = 18
    GAMES_PER_PAGE = 12

    @staticmethod
    def get(request):
        """Gets games from database not filtered"""

        favourite_games = request.user.usersfavouritegames_set.filter(is_deleted=False)
        context = {
            'page_obj': pagination_generate(request, favourite_games, MustsPageView.GAMES_PER_PAGE),
        }

        return render(request, 'game/musts_page.html', context)

    def post(self, request):

        print("i'm in")
        game_id = int(request.POST['game_id'])
        print(game_id)

        if game_id not in list(request.user.usersfavouritegames_set.values_list('game__game_id', flat=True)):
            current_game, created = Game.objects.get_or_create(game_id=game_id)
            request.user.usersfavouritegames_set.create(game=current_game, user=request.user)
            print(UsersFavouriteGames.objects.filter(game__game_id=game_id))
            print(current_game.usersfavouritegames_set.all())
            print('1')
        else:
            # current_game = Game.objects.create(game_id=game_id)
            current_user_game = request.user.usersfavouritegames_set.get(game__game_id=game_id)
            current_user_game.is_deleted = not current_user_game.is_deleted
            current_user_game.save()
            print(UsersFavouriteGames.objects.filter(game__game_id=game_id))
            current_game = Game.objects.get(game_id=game_id)
            print(current_game.usersfavouritegames_set.all())
            print('2')

        favourite_games = request.user.usersfavouritegames_set.all()
        context = {
            'page_obj': pagination_generate(request, favourite_games, MustsPageView.GAMES_PER_PAGE),
        }

        return render(request, 'game/musts_page.html', context)
