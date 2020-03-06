from django.core.files import File
from django.core.management.base import BaseCommand

from ...models import Conversation


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file', help='The file to train with')

    def handle(self, *args, **options):
        with open(options['file']) as f:
            Conversation(file=File(f)).save()
