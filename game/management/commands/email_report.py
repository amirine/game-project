from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Updates games database with the list of genres and platforms'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Done'))
