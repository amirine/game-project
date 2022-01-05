from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import ForeignKey, OneToOneField, ManyToManyField
from django.conf import settings

from game.igdb_wrapper import IGDBRequestsHandler
from game.models import Genre, Platform, Screenshot, Game, Cover


class Command(BaseCommand):
    """Management command for games database update"""

    help = 'Updates games database with the list of genres and platforms'

    @staticmethod
    def model_entries_update(entries_from_igdb: list, model) -> list:
        """
        Updates {model} entries from received {entries_from_igdb} list of entries obtained from IGDB API and returns ids
        of updated items. Models to update - models related to Game Model: Genre, Platform, Screenshot, Cover.

        Sets ForeignKey and OneToOneField relations using integer id of the related model: {corrected_entry}
        dictionary transforms ForeignKey/OneToOne fields names to {fieldname}_id form so that ForeignKey/OneToOneField
        values can be set via integers (e.g. {'game': 1} -> {'game_id': 1})
        """

        entries_to_update = []
        entries_to_create = []
        db_entries = model.objects.all()
        related_fields = [field.name for field in model._meta.fields if isinstance(field, (ForeignKey, OneToOneField))]

        for entry in entries_from_igdb:
            corrected_entry = {(f"{key}_id" if key in related_fields else key): value for key, value in entry.items()}
            if db_entries.filter(id=entry['id']).first():
                entries_to_update.append(model(**corrected_entry))
            else:
                entries_to_create.append(model(**corrected_entry))

        fields = [field.name for field in model._meta.fields if field.name != 'id']
        model.objects.bulk_create(entries_to_create)
        model.objects.bulk_update(entries_to_update, fields=fields)

        return list(map(lambda item: item['id'], entries_from_igdb))

    def game_model_entries_update(self):
        """
        Updates/creates Game Model entries:
            1. gets or creates game object by id
            2. updates non-relation fields (name, summary, rating, etc.)
            3. updates relationship fields (platforms, genres): updates/creates new objects of corresponding models
                via {model_entries_update} function
            4. updates related fields - fields in models with Game Model object as ForeignKey or OneToOne field
                (screenshot, cover) using {model_entries_update} function
        """

        igdb = IGDBRequestsHandler()
        entries_from_igdb = igdb.get_games(limit=settings.DB_UPDATE_GAMES_LIMIT)

        for entry in entries_from_igdb:

            game, created = Game.objects.get_or_create(id=entry['id'])
            non_relation_fields = [field.name for field in Game._meta.fields if field.name != 'id' and
                                   not isinstance(field, (ForeignKey, ManyToManyField, OneToOneField))]
            non_relation_fields_dict = {key: value for (key, value) in entry.items() if key in non_relation_fields}
            Game.objects.filter(id=entry['id']).update(**non_relation_fields_dict)

            game.genres.set(self.model_entries_update(entry.get('genres', []), Genre))
            game.platforms.set(self.model_entries_update(entry.get('platforms', []), Platform))
            self.model_entries_update(entry.get('screenshots', []), Screenshot)
            if entry.get('cover'):
                self.model_entries_update([entry.get('cover')], Cover)

    @transaction.atomic
    def handle(self, *args, **options):

        self.game_model_entries_update()
        self.stdout.write(self.style.SUCCESS('Database updated successfully.'))
