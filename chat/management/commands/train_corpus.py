from django.core.management.base import BaseCommand

from ...training import train_corpus


class Command(BaseCommand):

    help = 'Trains the chat bot using a corpus'
    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('corpus', help='The corpus to train with, e.g. "chatterbot.corpus.english.greetings"')

    def handle(self, *args, **options):
        train_corpus(options['corpus'])
