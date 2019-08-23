import importlib

from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings as chatterbot_settings
from chatterbot.trainers import ChatterBotCorpusTrainer

from django.conf import settings as django_settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    A Django management command for calling a
    chat bot's training method.
    """

    help = 'Trains the database used by the chat bot'
    can_import_settings = True

    def handle(self, *args, **options):        

        chatterbot = ChatBot(**chatterbot_settings.CHATTERBOT)

        trainer_settings = getattr(django_settings, 'CHATTERBOT_TRAINING', {})

        if trainer_settings:
            trainer_string = trainer_settings['trainer']
            module_name, class_name = trainer_string.rsplit('.', 1)
            trainer_class = getattr(importlib.import_module(module_name), class_name)
            trainer = trainer_class(chatterbot)
            trainer.train(trainer_settings['training_data'])

        # Django 1.8 does not define SUCCESS
        if hasattr(self.style, 'SUCCESS'):
            style = self.style.SUCCESS
        else:
            style = self.style.NOTICE

        self.stdout.write(style('Starting training...'))
        training_class = trainer.__class__.__name__
        self.stdout.write(style('ChatterBot trained using "%s"' % training_class))
