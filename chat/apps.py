from django.apps import AppConfig
from django.utils.translation import gettext as _


class Config(AppConfig):
    name = 'chat'
    label = 'chat'
    verbose_name = _('Chat')
