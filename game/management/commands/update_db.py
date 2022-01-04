from django.core.management.base import BaseCommand
from django.db.models import ForeignKey

from game.igdb_wrapper import IGDBRequestsHandler
from game.models import Genre, Platform, Screenshot, Game


class Command(BaseCommand):
    help = 'Updates games database with the list of genres and platforms'

    def related_field_update(self, entries_from_igdb, model):
        """
        Updates model entries connected with the main Game Model table by ManyToManyField or ForeignKey:
        Platform Model, Genre Model, Screenshot Model entries
        :param entries_from_igdb: dict - data from IGDB (not django project's postgres database)
        :param model: Queryset - model for entries update (Platform, Genre, Screenshot)
        :return: list - list of Queriset objects created or updated
        """
        entries_to_update = []
        entries_to_create = []
        db_entries = model.objects.all()
        fk_fields = [field.name for field in model._meta.fields if isinstance(field, ForeignKey)]

        for entry in entries_from_igdb:
            """Transforms ForeignKey fields names to {fieldname_id} form to set ForeignKey values (e.g. game -> game_id)"""
            corrected_entry = {(f"{key}_id" if key in fk_fields else key): value for key, value in entry.items()}
            if db_entries.filter(id=entry['id']).first():
                entries_to_update.append(model(**corrected_entry))
            else:
                entries_to_create.append(model(**corrected_entry))

        fields = [field.name for field in model._meta.fields if field.name != 'id']
        model.objects.bulk_create(entries_to_create)
        model.objects.bulk_update(entries_to_update, fields=fields)

        return [*entries_to_update, *entries_to_create]

    def game_model_update_new_(self):
        igdb = IGDBRequestsHandler()
        entries_from_igdb = igdb.get_games()

        for entry in entries_from_igdb:
            game, created = Game.objects.get_or_create(id=entry['id'])
            # keys_to_update = [field.name for field in Game._meta.fields
            #                   if not isinstance(field, (ForeignKey, ManyToManyField, OneToOneField)) and field.name != 'id']
            keys_to_update = ['name', 'total_rating', 'summary', 'first_release_date', 'rating', 'rating_count',
                              'aggregated_rating', 'aggregated_rating_count']
            dict_to_update = {key: value for (key, value) in entry.items() if key in keys_to_update}

            Game.objects.filter(id=entry['id']).update(**dict_to_update)
            game = Game.objects.get(id=entry['id'])
            if entry.get('cover'):
                game.cover_id = entry['cover']['image_id']
            game.save()
            # game.cover_id.set(self.related_field_update(entry.get('cover', []), Cover))
            game.genres.set(self.related_field_update(entry.get('genres', []), Genre))
            game.platforms.set(self.related_field_update(entry.get('platforms', []), Platform))
            game.screenshot_set.set(self.related_field_update(entry.get('screenshots', []), Screenshot))

    def handle(self, *args, **options):

        self.game_model_update_new_()
        self.stdout.write(self.style.SUCCESS('Database updated successfully'))
