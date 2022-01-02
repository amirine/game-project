from django.core.management.base import BaseCommand

from game.igdb_wrapper import IGDBRequestsHandler
from game.models import Genre, GameNew, Platform, Screenshot


class Command(BaseCommand):
    help = 'Updates games database with the list of genres and platforms'

    def genres_update(self):
        igdb = IGDBRequestsHandler()
        genres_from_igdb = igdb.get_genres()

        genres_to_update = []
        genres_to_insert = []

        if genres_from_igdb:
            for genre in genres_from_igdb:
                if Genre.objects.filter(**genre).exists():
                    genres_to_update.append(Genre(**genre))
                else:
                    genres_to_insert.append(Genre(**genre))
        else:
            genres_to_insert = [Genre(**genre) for genre in genres_from_igdb]

        Genre.objects.bulk_create(genres_to_insert)
        Genre.objects.bulk_update(genres_to_update, fields=['name'])

    def game_model_update_(self):
        igdb = IGDBRequestsHandler()
        entries_from_igdb = igdb.get_games()
        self.stdout.write(f"{entries_from_igdb}")

        entries_to_update = []
        entries_to_create = []

        for entry in entries_from_igdb:

            entry_object = GameNew(
                id=entry.get('id'),
                name=entry.get('name'),
                # cover_id = entry.get('name'),
                total_rating=entry.get('total_rating'),
                summary=entry.get('summary'),
                first_release_date=entry.get('first_release_date'),
                # screenshots =
                platform_id=1,
                rating=entry.get('rating'),
                rating_count=entry.get('rating_count'),
                aggregated_rating=entry.get('aggregated_rating'),
                aggregated_rating_count=entry.get('aggregated_rating_count'),
            )

            for platform in entry.get('platforms', []):
                entry_object.platforms.add(Platform.objects.get_or_create(**platform)[0])

            for genre in entry.get('genres', []):
                entry_object.genres.add(Genre.objects.get_or_create(**genre)[0])

                if GameNew.objects.filter(id=entry['id']).exists():
                    entries_to_update.append(entry_object)
                else:
                    entries_to_create.append(entry_object)

        fields = [field.name for field in GameNew._meta.fields if field.name != 'id']
        GameNew.objects.bulk_create(entries_to_create)
        GameNew.objects.bulk_update(entries_to_update, fields=fields)

    def game_model_update(self):
        igdb = IGDBRequestsHandler()
        entries_from_igdb = igdb.get_games()

        for entry in entries_from_igdb:

            if GameNew.objects.filter(id=entry['id']).exists():

                keys_to_update = ['name', 'total_rating', 'summary', 'first_release_date', 'rating', 'rating_count',
                                  'aggregated_rating', 'aggregated_rating_count']
                dict_to_update = {key: value for (key, value) in entry.items() if key in keys_to_update}
                GameNew.objects.filter(id=entry['id']).update(**dict_to_update)
                entry_obj = GameNew.objects.get(id=entry['id'])

                if entry.get('cover'):
                    entry_obj.cover_id = entry['cover']['image_id']
                entry_obj.save()
                # entry_obj.name = entry.get('name')
                # entry_obj.total_rating = entry.get('total_rating')
                # entry_obj.summary = entry.get('summary')
                # entry_obj.first_release_date = entry.get('first_release_date')
                # entry_obj.rating = entry.get('rating')
                # entry_obj.rating_count = entry.get('rating_count')
                # entry_obj.aggregated_rating = entry.get('aggregated_rating')
                # entry_obj.aggregated_rating_count = entry.get('aggregated_rating_count')
                # entry_obj.save()

                for genre in entry.get('genres', []):
                    if Genre.objects.filter(id=genre['id']).exists():
                        Genre.objects.filter(id=genre['id']).update(name=genre['name'])
                    else:
                        Genre.objects.create(**genre)
                entry_obj.genres.set(list(map(lambda genre1: genre1['id'], entry.get('genres', []))))

                for platform in entry.get('platforms', []):
                    if Platform.objects.filter(id=platform['id']).exists():
                        Platform.objects.filter(id=platform['id']).update(abbreviation=platform['abbreviation'])
                    else:
                        Platform.objects.create(**platform)
                entry_obj.platforms.set(list(map(lambda genre1: genre1['id'], entry.get('platforms', []))))

                for screenshot in entry.get('screenshots', []):
                    if Screenshot.objects.filter(id=screenshot['id']).exists():
                        Screenshot.objects.filter(id=screenshot['id']).update(image_id=screenshot['image_id'],
                                                                              game_id=entry['id'])
                    else:
                        Screenshot.objects.create(
                            id=screenshot['id'],
                            image_id=screenshot['image_id'],
                            game_id=entry['id']
                        )

            else:

                entry_obj = GameNew.objects.create(
                    id=entry.get('id'),
                    name=entry.get('name'),
                    # cover_id = entry.get('name'),
                    total_rating=entry.get('total_rating'),
                    summary=entry.get('summary'),
                    first_release_date=entry.get('first_release_date'),
                    rating=entry.get('rating'),
                    rating_count=entry.get('rating_count'),
                    aggregated_rating=entry.get('aggregated_rating'),
                    aggregated_rating_count=entry.get('aggregated_rating_count'),
                )

                if entry.get('cover'):
                    entry_obj.cover_id = entry['cover']['image_id']
                entry_obj.save()

                for genre in entry.get('genres', []):
                    if Genre.objects.filter(id=genre['id']).exists():
                        Genre.objects.filter(id=genre['id']).update(name=genre['name'])
                    else:
                        Genre.objects.create(**genre)
                entry_obj.genres.set(list(map(lambda genre1: genre1['id'], entry.get('genres', []))))

                for platform in entry.get('platforms', []):
                    if Platform.objects.filter(id=platform['id']).exists():
                        Platform.objects.filter(id=platform['id']).update(abbreviation=platform['abbreviation'])
                    else:
                        Platform.objects.create(**platform)
                entry_obj.platforms.set(list(map(lambda genre1: genre1['id'], entry.get('platforms', []))))


                for screenshot in entry.get('screenshots', []):
                    if Screenshot.objects.filter(id=screenshot['id']).exists():
                        Screenshot.objects.filter(id=screenshot['id']).update(image_id=screenshot['image_id'],
                                                                              game_id=entry['id'])
                    else:
                        Screenshot.objects.create(
                            id=screenshot['id'],
                            image_id=screenshot['image_id'],
                            game_id=entry['id']
                        )


    def game_genres_update(self, genres_from_igdb):
        genres_to_update = []
        genres_to_create = []
        db_genres = Genre.objects.all()
        for genre in genres_from_igdb:
            if db_genres.filter(id=genre['id']).first():
                genres_to_update.append(Genre(**genre))
            else:
                genres_to_create.append(Genre(**genre))

        fields = [field.name for field in Genre._meta.fields if field.name != 'id']
        Genre.objects.bulk_create(genres_to_create)
        Genre.objects.bulk_update(genres_to_update, fields=fields)

    def game_model_update_new(self):
        igdb = IGDBRequestsHandler()
        entries_from_igdb = igdb.get_games()

        for entry in entries_from_igdb:
            game, created = GameNew.objects.get_or_create(id=entry['id'])
            keys_to_update = ['name', 'total_rating', 'summary', 'first_release_date', 'rating', 'rating_count',
                              'aggregated_rating', 'aggregated_rating_count']
            dict_to_update = {key: value for (key, value) in entry.items() if key in keys_to_update}
            GameNew.objects.filter(id=entry['id']).update(**dict_to_update)

            game = GameNew.objects.get(id=entry['id'])

            if entry.get('cover'):
                game.cover_id = entry['cover']['image_id']
            game.save()

            self.game_genres_update(entry.get('genres', []))

            # for genre in entry.get('genres', []):
            #     if Genre.objects.filter(id=genre['id']).exists():
            #         Genre.objects.filter(id=genre['id']).update(name=genre['name'])
            #     else:
            #         Genre.objects.create(**genre)
            game.genres.set(list(map(lambda genre1: genre1['id'], entry.get('genres', []))))

            for platform in entry.get('platforms', []):
                if Platform.objects.filter(id=platform['id']).exists():
                    Platform.objects.filter(id=platform['id']).update(abbreviation=platform['abbreviation'])
                else:
                    Platform.objects.create(**platform)
            game.platforms.set(list(map(lambda genre1: genre1['id'], entry.get('platforms', []))))

            for screenshot in entry.get('screenshots', []):
                if Screenshot.objects.filter(id=screenshot['id']).exists():
                    Screenshot.objects.filter(id=screenshot['id']).update(image_id=screenshot['image_id'],
                                                                          game_id=entry['id'])
                else:
                    Screenshot.objects.create(
                        id=screenshot['id'],
                        image_id=screenshot['image_id'],
                        game_id=entry['id']
                    )

    def handle(self, *args, **options):

        self.game_model_update_new()
        self.stdout.write(self.style.SUCCESS('Done'))
