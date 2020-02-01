from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Conversation, Statement


def train(modeladmin, request, queryset):
    for instance in queryset:
        instance.train()


train.short_description = _('Train selected Conversation again')


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created', 'modified')
    actions = [train]


@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = ('request', 'response', 'conversation',  'is_root')
