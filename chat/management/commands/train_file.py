from django.core.management.base import BaseCommand

from ...training import train_file


class Command(BaseCommand):

    help = 'Trains the chat bot using a line seperated file'
    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('file', help='The file to train with')

    def handle(self, *args, **options):
        with open(options['file']) as f:
            train_file(options['file'], f)
