import nltk
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        for item in ['punkt', 'wordnet']:
            nltk.download(item, download_dir=settings.NLTK_DATA)
